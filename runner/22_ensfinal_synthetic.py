"""
50 sentetik stochastic-trend serisini (n=45 ve n=100) ens-final pipeline'a sok.
19-vektor (9 eski + 10 yeni) + meta + karar cikar.

Cikti: runner/results/ensfinal_synthetic.json
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
    load_new_ensemble, load_old_ensemble,
)
from stat_detector import load_stationary_detector, predict_stationary_batch

from tsfresh import extract_features as tsfresh_extract
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute

RUNNER = Path(__file__).resolve().parent
SYN_DIR = RUNNER / "data" / "synthetic"
OUT = RUNNER / "results"


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
    manifest = json.load(open(SYN_DIR / "manifest.json"))
    items, series_list = [], []
    for m in manifest:
        path = SYN_DIR / m["file"]
        if not path.exists():
            continue
        s = pd.read_csv(path)["value"].values.astype(float)
        items.append({"name": m["file"], "kind": m["kind"], "n": int(m["length"])})
        series_list.append(s)
    print(f"[1] {len(items)} sentetik seri yuklendi")

    print(f"[2] tsfresh extraction...")
    X = extract_batch(series_list)
    X_clean = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

    print(f"[3] Modeller yukleniyor...")
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
            **it,
            "expected_class": "stochastic_trend",
            "base_correct": pred_base == "stochastic_trend",
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

    with open(OUT / "ensfinal_synthetic.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[4] {len(results)} sentetik seri ens-final'dan gecti")
    print(f"   JSON: {OUT / 'ensfinal_synthetic.json'}")

    # Quick stats
    df = pd.DataFrame([{
        "kind": r["kind"], "n": r["n"],
        "base_correct": r["base_correct"],
        "pred_base": r["pred_base"],
    } for r in results])
    print("\nens-final sentetik accuracy (base = stochastic_trend bekleniyor):")
    print(df.groupby(["kind", "n"])["base_correct"].mean().to_string())
    print("\nens-final sentetik tahmin sinifi dagilimi:")
    print(df.groupby(["kind", "n"])["pred_base"].value_counts().to_string())


if __name__ == "__main__":
    main()
