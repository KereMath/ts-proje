"""
ens-final pipeline'ini realdata uzerinde calistir.
Egitilmis modelleri (eski ensemble + yeni ensemble + stationary detector + meta-learners)
yukler ve runner/data/realdata/*.csv tum dosyalari ic.

Cikti: runner/results/ensfinal_realdata.json (+ csv + md)
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
    ANOM_LABELS, BASE_LABELS, META_MODELS_DIR, MIN_SERIES_LENGTH,
    NEW_ALL_MODELS, OLD_CLASSES, PROCESSED_DIR, RESULTS_DIR,
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


def extract_batch(series_list, n_jobs=4):
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
    # --- 1. Veri ---
    csvs = sorted(REAL_DIR.glob("*.csv"))
    print(f"[1] {len(csvs)} CSV dosyasi bulundu.")
    items, series_list = [], []
    for c in csvs:
        s = read_series(c)
        items.append({"name": c.name, "n": int(len(s))})
        if len(s) >= MIN_SERIES_LENGTH:
            items[-1]["used"] = True
            series_list.append(s)
        else:
            items[-1]["used"] = False
    keep = [it for it in items if it["used"]]
    print(f"   {len(keep)} dosya pipeline'a uygun (n>=50)")

    # --- 2. tsfresh ---
    print(f"\n[2] tsfresh extraction ({len(series_list)} seri)...")
    X = extract_batch(series_list, n_jobs=4)

    # --- 3. Load all models ---
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
    print("   Tum modeller yuklendi.")

    # --- 4. Old + New ensemble probabilities ---
    print(f"\n[4] Ensemble inference ({len(series_list)} seri)...")
    n = len(series_list)
    raw_old = np.zeros((n, 9))
    raw_new = np.zeros((n, 10))
    for i in range(n):
        raw_old[i] = get_old_probs(old_models, X[i])
        raw_new[i] = get_new_probs(new_models, X[i])

    derived = _compute_derived_features(raw_old, raw_new)
    X_clean = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    X_scaled = tsfresh_scaler.transform(X_clean)
    meta_X = np.hstack([raw_old, raw_new, derived, X_scaled])

    # --- 5. Stationary detector ---
    stat_probs = predict_stationary_batch(stat_model, stat_scaler, stat_selector, series_list)

    # --- 6. Meta-learner inference ---
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

    # --- 7. Decision logic ---
    raw_new_anom = raw_new[:, 4:]
    results = []
    for i, it in enumerate(keep):
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

    # --- 8. Save ---
    with open(OUT / "ensfinal_realdata.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[5] Yazildi: {OUT / 'ensfinal_realdata.json'}")

    # Compact CSV
    rows = []
    for r in results:
        rows.append({
            "name": r["name"], "n": r["n"],
            "pred_base": r["pred_base"],
            "pred_anoms": ", ".join(r["pred_anoms"]) if r["pred_anoms"] else "",
            "path": r["decision_path"],
            "stat_prob": r["stat_prob"],
            "router_p": r["router_combo_prob"],
            **{f"base_{k}": v for k, v in r["base_probs"].items()},
            **{f"anom_{k}": v for k, v in r["anom_probs"].items()},
        })
    pd.DataFrame(rows).to_csv(OUT / "ensfinal_realdata.csv", index=False)
    print(f"   CSV: {OUT / 'ensfinal_realdata.csv'}")

    # --- 9. Markdown report ---
    md = []
    md.append("# ens-final Pipeline: realdata Sonuclari\n")
    md.append(f"Toplam {len(results)} realdata dosyasi pipeline'dan gecti.\n")
    md.append("\n## Tahmin Tablosu\n")
    md.append("| dosya | n | yol | base | anomaliler | P(stat) | P(combo) |")
    md.append("|---|---|---|---|---|---|---|")
    for r in sorted(results, key=lambda x: x["n"]):
        md.append(
            f"| {r['name']} | {r['n']} | {r['decision_path']} | {r['pred_base']} | "
            f"{', '.join(r['pred_anoms']) if r['pred_anoms'] else '-'} | "
            f"{r['stat_prob']:.3f} | {r['router_combo_prob']:.3f} |"
        )
    md.append("\n\n## Base Type Dagilimi\n")
    base_dist = pd.Series([r["pred_base"] for r in results]).value_counts()
    md.append("```")
    md.append(base_dist.to_string())
    md.append("```\n")
    md.append("\n## Decision Path Dagilimi\n")
    pd_dist = pd.Series([r["decision_path"] for r in results]).value_counts()
    md.append("```")
    md.append(pd_dist.to_string())
    md.append("```\n")
    md.append("\n## Anomaly Frekansi\n")
    from collections import Counter
    cnt = Counter()
    for r in results:
        for a in r["pred_anoms"]:
            cnt[a] += 1
    md.append("```")
    for a in ANOM_LABELS:
        md.append(f"{a:24s} {cnt.get(a, 0)}")
    md.append("```\n")
    md.append("\n## Kisa Seriler (n<=100) Detayi\n")
    md.append("| dosya | n | base | anomaliler | path |")
    md.append("|---|---|---|---|---|")
    for r in sorted([r for r in results if r["n"] <= 100], key=lambda x: x["n"]):
        md.append(
            f"| {r['name']} | {r['n']} | {r['pred_base']} | "
            f"{', '.join(r['pred_anoms']) if r['pred_anoms'] else '-'} | {r['decision_path']} |"
        )
    out_md = OUT / "ENSFINAL_REALDATA_RAPOR.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"   MD: {out_md}")


if __name__ == "__main__":
    main()
