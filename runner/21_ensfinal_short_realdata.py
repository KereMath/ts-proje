"""
ens-final pipeline'ini KISA realdata (n<50) dosyalari icin de calistir.
MIN_SERIES_LENGTH kontrolunu bypass eder (W1, uspop, strikes, vs.).

Cikti: runner/results/ensfinal_short.json + md
"""
import json
import sys
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ens-final"))

from config import (
    ANOM_LABELS, BASE_LABELS, META_MODELS_DIR,
    NEW_ALL_MODELS, OLD_CLASSES, PROCESSED_DIR,
)
from processor import (
    _compute_derived_features, get_new_probs, get_old_probs,
    load_new_ensemble, load_old_ensemble, read_series,
)
from stat_detector import load_stationary_detector, predict_stationary_batch

from tsfresh import extract_features as tsfresh_extract
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute

RUNNER = Path(__file__).resolve().parent
REAL_DIR = RUNNER / "data" / "realdata"
OUT = RUNNER / "results"
OUT.mkdir(exist_ok=True)

# tsfresh stabilite icin pratikte n>=20 gerekli; ondan kucuk olanlari atla
PRACTICAL_MIN = 20


def extract_batch(series_list, n_jobs=2):
    dfs = []
    for i, s in enumerate(series_list):
        dfs.append(pd.DataFrame({"id": i, "time": np.arange(len(s)), "value": s.astype(float)}))
    combined = pd.concat(dfs, ignore_index=True)
    X_df = tsfresh_extract(
        combined, column_id="id", column_sort="time", column_value="value",
        default_fc_parameters=EfficientFCParameters(),
        disable_progressbar=True, n_jobs=n_jobs,
    )
    impute(X_df)
    return X_df.values


def main():
    # --- 1. Kisa dosyalari topla ---
    print(f"[1] CSV dosyalari taraniyor (kisa olanlar n<50)...")
    items, series_list = [], []
    for c in sorted(REAL_DIR.glob("*.csv")):
        s = read_series(c)
        n = len(s)
        if n < 50 and n >= PRACTICAL_MIN:
            items.append({"name": c.name, "n": int(n)})
            series_list.append(s)
            print(f"   {c.name:<24} n={n}")
        elif n < PRACTICAL_MIN:
            print(f"   {c.name:<24} n={n} (cok kisa, tsfresh stabilite riskli — ATLANDI)")

    if not series_list:
        print("Hic kisa dosya yok.")
        return

    print(f"\n[2] tsfresh extraction ({len(series_list)} kisa seri)...")
    X = extract_batch(series_list, n_jobs=2)
    X_clean = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

    # --- 3. Modelleri yukle ---
    print("\n[3] Modeller yukleniyor...")
    old_models = load_old_ensemble()
    new_models = load_new_ensemble()
    base_meta = joblib.load(META_MODELS_DIR / "base_meta.pkl")
    anom_metas = {a: joblib.load(META_MODELS_DIR / f"anom_{a}.pkl")
                  for a in ANOM_LABELS
                  if (META_MODELS_DIR / f"anom_{a}.pkl").exists()}
    router = joblib.load(META_MODELS_DIR / "router.pkl")
    blend_params = joblib.load(META_MODELS_DIR / "blend_weights.pkl")
    tsfresh_scaler = joblib.load(PROCESSED_DIR / "tsfresh_scaler.pkl")
    stat_model, stat_scaler, stat_selector = load_stationary_detector()

    # --- 4. Ensemble inference ---
    print(f"\n[4] Ensemble inference ({len(series_list)} seri)...")
    n = len(series_list)
    raw_old = np.zeros((n, 9))
    raw_new = np.zeros((n, 10))
    for i in range(n):
        raw_old[i] = get_old_probs(old_models, X[i])
        raw_new[i] = get_new_probs(new_models, X[i])

    derived = _compute_derived_features(raw_old, raw_new)
    X_scaled = tsfresh_scaler.transform(X_clean)
    meta_X = np.hstack([raw_old, raw_new, derived, X_scaled])

    stat_probs = predict_stationary_batch(stat_model, stat_scaler, stat_selector, series_list)

    xgb_bp = base_meta["xgb"].predict_proba(meta_X)
    lgb_bp = base_meta["lgb"].predict_proba(meta_X)
    base_pred = np.argmax(0.5 * xgb_bp + 0.5 * lgb_bp, axis=1)

    xgb_r = router["xgb"].predict_proba(meta_X)[:, 1]
    lgb_r = router["lgb"].predict_proba(meta_X)[:, 1]
    router_p = 0.5 * xgb_r + 0.5 * lgb_r

    anom_probs_d = {}
    for a, m in anom_metas.items():
        xp = m["xgb"].predict_proba(meta_X)[:, 1]
        lp = m["lgb"].predict_proba(meta_X)[:, 1]
        anom_probs_d[a] = 0.5 * xp + 0.5 * lp

    # --- 5. Karar ---
    raw_new_anom = raw_new[:, 4:]
    results = []
    for i, it in enumerate(items):
        base_type = BASE_LABELS[base_pred[i]]
        if stat_probs[i] >= 0.92:
            pred_base, pred_anoms = "stationary", []
            decision_path = "stat_gate"
        elif router_p[i] < 0.30:
            pred_base, pred_anoms = base_type, []
            decision_path = "single"
        else:
            anomalies = []
            for j, anom_name in enumerate(ANOM_LABELS):
                params = blend_params.get(anom_name, {"alpha": 1.0, "threshold": 0.5})
                meta_p = anom_probs_d[anom_name][i]
                new_p = float(raw_new_anom[i, j])
                blended = params["alpha"] * meta_p + (1 - params["alpha"]) * new_p
                eff_t = min(params["threshold"], 0.0) if base_type == "stationary" else params["threshold"]
                if blended >= eff_t:
                    anomalies.append(anom_name)
            pred_base, pred_anoms = base_type, anomalies
            decision_path = "combo"

        rec = {
            "name": it["name"], "n": it["n"],
            "pred_base": pred_base, "pred_anoms": pred_anoms,
            "decision_path": decision_path,
            "stat_prob": round(float(stat_probs[i]), 4),
            "router_combo_prob": round(float(router_p[i]), 4),
            "base_probs": {BASE_LABELS[k]: round(float((0.5*xgb_bp[i] + 0.5*lgb_bp[i])[k]), 4)
                            for k in range(4)},
            "anom_probs": {a: round(float(anom_probs_d[a][i]), 4) for a in ANOM_LABELS},
            "old_probs": {OLD_CLASSES[k]: round(float(raw_old[i,k]), 4) for k in range(9)},
            "new_probs": {NEW_ALL_MODELS[k]: round(float(raw_new[i,k]), 4) for k in range(10)},
        }
        results.append(rec)

    # --- 6. Save ---
    with open(OUT / "ensfinal_short.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[5] JSON: {OUT / 'ensfinal_short.json'}")

    # --- 7. Markdown (W1 detayli) ---
    md = []
    md.append("# ens-final Pipeline: KISA realdata (n<50) Sonuclari\n")
    md.append(f"Toplam {len(results)} kisa dosya. (n<{PRACTICAL_MIN} olanlar tsfresh stabilite icin atlandi.)\n")
    md.append("\n## Ozet Tablo\n")
    md.append("| dosya | n | yol | base | anomaliler | P(stat) | P(combo) |")
    md.append("|---|---|---|---|---|---|---|")
    for r in sorted(results, key=lambda x: x["n"]):
        md.append(
            f"| {r['name']} | {r['n']} | {r['decision_path']} | {r['pred_base']} | "
            f"{', '.join(r['pred_anoms']) if r['pred_anoms'] else '-'} | "
            f"{r['stat_prob']:.3f} | {r['router_combo_prob']:.3f} |"
        )

    # W1 detayli
    md.append("\n\n## W1 Detayli (plan.md'de ozellikle istenmis)\n")
    w1 = next((r for r in results if r["name"] == "W1.csv"), None)
    if w1:
        md.append(f"**n = {w1['n']}**")
        md.append(f"**Tahmin:** {w1['pred_base']} + {w1['pred_anoms'] if w1['pred_anoms'] else '(anomali yok)'}")
        md.append(f"**Path:** {w1['decision_path']}, P(stat)={w1['stat_prob']}, P(combo)={w1['router_combo_prob']}\n")
        md.append("### Eski ensemble 9 detector P(class=1):")
        md.append("```")
        for k, v in w1["old_probs"].items():
            md.append(f"  {k:24s} {v}")
        md.append("```\n")
        md.append("### Yeni ensemble 10 model P(class=1):")
        md.append("```")
        for k, v in w1["new_probs"].items():
            md.append(f"  {k:24s} {v}")
        md.append("```\n")
        md.append("### Base type meta-learner (4-class softmax):")
        md.append("```")
        for k, v in w1["base_probs"].items():
            md.append(f"  {k:24s} {v}")
        md.append("```\n")
        md.append("### Anomali meta-learner (6 binary):")
        md.append("```")
        for k, v in w1["anom_probs"].items():
            md.append(f"  {k:24s} {v}")
        md.append("```\n")
    else:
        md.append("W1 sonuclar listesinde bulunamadi.\n")

    out_md = OUT / "ENSFINAL_SHORT_RAPOR.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"   MD: {out_md}")


if __name__ == "__main__":
    main()
