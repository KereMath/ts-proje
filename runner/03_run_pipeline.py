"""
tsfresh-ensemble-stationary pipeline'ini calistir.

Input: tum sentetik (runner/data/synthetic/*.csv) + realdata (runner/data/realdata/*.csv) seriler
Adimlar:
  1. Her seri icin tsfresh EfficientFCParameters ile 777 feature cikar
  2. Her bir 9 detector'e ozel scaler ile transform et
  3. predict_proba(...)[:, 1] al
  4. Argmax ensemble decision
  5. Sonuclari runner/results/predictions.json + summary.md olarak yaz
"""
import json
import sys
import time
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT / "tsfresh-ensemble-stationary"
sys.path.insert(0, str(REPO))

from tsfresh import extract_features as tsfresh_extract
from tsfresh.feature_extraction import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import impute

# Class list (order matches config.py in repo)
CLASSES = [
    "collective_anomaly", "contextual_anomaly", "deterministic_trend",
    "mean_shift", "point_anomaly", "stochastic_trend",
    "trend_shift", "variance_shift", "volatility",
]

MODELS_DIR = REPO / "trained_models"
DATA_DIRS = {
    "synthetic": Path(__file__).resolve().parent / "data" / "synthetic",
    "realdata":  Path(__file__).resolve().parent / "data" / "realdata",
}
RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_detectors():
    print("[1] Loading 9 detectors...")
    loaded = {}
    for cname in CLASSES:
        d = MODELS_DIR / cname
        with open(d / "best_model_info.json") as f:
            info = json.load(f)
        best = info["best_model"]
        model = joblib.load(d / f"{best}.joblib")
        scalers = joblib.load(d / "scalers.pkl")
        scaler = scalers["scaler"] if isinstance(scalers, dict) and "scaler" in scalers else scalers
        loaded[cname] = {"model": model, "scaler": scaler, "best": best}
        print(f"   {cname:<24} -> {best}")
    return loaded


def read_series(csv_path):
    df = pd.read_csv(csv_path)
    # ilk numerik kolonu al
    for col in df.columns:
        try:
            arr = pd.to_numeric(df[col], errors="coerce").dropna().values
            if len(arr) > 0:
                return arr.astype(float)
        except Exception:
            continue
    raise ValueError(f"No numeric column found in {csv_path}")


def collect_inputs():
    items = []
    # sentetik
    syn_manifest = json.loads((DATA_DIRS["synthetic"] / "manifest.json").read_text())
    syn_meta = {m["file"]: m for m in syn_manifest}
    for csv in sorted(DATA_DIRS["synthetic"].glob("*.csv")):
        meta = syn_meta.get(csv.name, {})
        items.append({
            "source": "synthetic",
            "name": csv.name,
            "path": str(csv),
            "kind": meta.get("kind"),
            "length_target": meta.get("length"),
            "expected_class": "stochastic_trend",
        })
    # realdata
    for csv in sorted(DATA_DIRS["realdata"].glob("*.csv")):
        items.append({
            "source": "realdata",
            "name": csv.name,
            "path": str(csv),
            "expected_class": None,
        })
    return items


def extract_one_batch(series_list, ids):
    """Bir batch icin tsfresh'i tek seferde calistir, sira korunur."""
    dfs = []
    for sid, s in zip(ids, series_list):
        dfs.append(pd.DataFrame({"id": sid, "time": np.arange(len(s)), "value": s.astype(float)}))
    big = pd.concat(dfs, ignore_index=True)
    X_df = tsfresh_extract(
        big, column_id="id", column_sort="time", column_value="value",
        default_fc_parameters=EfficientFCParameters(),
        disable_progressbar=True, n_jobs=0,
    )
    impute(X_df)
    # ids siralamasi
    X_df = X_df.reindex(ids)
    return X_df


def run_predict_per_detector(detectors, X_row):
    """Bir tek satir (numpy array, 777 boyut) icin her detector'un P(class=1) degeri."""
    out = {}
    for cname, det in detectors.items():
        try:
            x_scaled = det["scaler"].transform(X_row.reshape(1, -1))
            p = float(det["model"].predict_proba(x_scaled)[0, 1])
            out[cname] = p
        except Exception as e:
            out[cname] = None
    return out


def main():
    t0 = time.time()
    detectors = load_detectors()
    items = collect_inputs()
    print(f"\n[2] Reading {len(items)} series...")

    series_list = []
    keep = []
    for it in items:
        try:
            s = read_series(it["path"])
            if len(s) < 5:
                it["status"] = f"SKIP_TOO_SHORT (n={len(s)})"
                continue
            series_list.append(s)
            it["n"] = int(len(s))
            keep.append(it)
        except Exception as e:
            it["status"] = f"SKIP_READ_ERROR ({e})"
    print(f"   {len(keep)} usable series")

    # tsfresh extraction (batch)
    print(f"\n[3] tsfresh feature extraction ({len(keep)} series)...")
    ids = [f"s{i}" for i in range(len(keep))]
    X_df = extract_one_batch(series_list, ids)
    X = X_df.values
    print(f"   feature matrix: {X.shape}")

    # Predict
    print(f"\n[4] Running 9 detectors per series...")
    results = []
    for i, it in enumerate(keep):
        per = run_predict_per_detector(detectors, X[i])
        # Argmax (None'lari atla)
        valid = {k: v for k, v in per.items() if v is not None}
        if valid:
            best = max(valid, key=valid.get)
            best_p = valid[best]
        else:
            best = None
            best_p = None
        rec = {
            **it,
            "probs": per,
            "ensemble_pred": best,
            "ensemble_pred_prob": best_p,
            "match_expected": (best == it.get("expected_class")) if it.get("expected_class") else None,
        }
        results.append(rec)

    elapsed = time.time() - t0
    print(f"\n[5] Done in {elapsed:.1f}s")

    # Save full predictions
    out_json = RESULTS_DIR / "predictions.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"   Wrote {out_json}")

    # Save also a flat CSV for easy viewing
    rows = []
    for r in results:
        row = {
            "source": r["source"], "name": r["name"], "n": r.get("n"),
            "kind": r.get("kind"), "expected": r.get("expected_class"),
            "pred": r["ensemble_pred"], "pred_prob": r["ensemble_pred_prob"],
            "match": r.get("match_expected"),
        }
        for cname in CLASSES:
            row[f"P_{cname}"] = r["probs"].get(cname)
        rows.append(row)
    df_out = pd.DataFrame(rows)
    df_out.to_csv(RESULTS_DIR / "predictions.csv", index=False)
    print(f"   Wrote {RESULTS_DIR / 'predictions.csv'}")


if __name__ == "__main__":
    main()
