"""
Sweep'te bulunan optimal blend'i realdata ve sentetik test setlerinde uygula.
Baseline (trainer-learned) vs Optimized karsilastirma.
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

REAL_DIR = Path(r"c:\Users\Pc\Desktop\ceylanhoca\runner\data\realdata")
SYN_DIR = Path(r"c:\Users\Pc\Desktop\ceylanhoca\contextual-off\data_10x\synthetic")
OUT = Path(__file__).resolve().parent / "results"

STAT_BASE_AND = 0.40
STAT_CONFIDENT = 0.75
CTX_THRESH = 0.55
ROUTER_THETA = 0.40

REAL_GT = {
    "W1.csv": "stationary", "W2.csv": "stationary", "W3.csv": "stationary",
    "W5.csv": "deterministic_trend", "W6.csv": "deterministic_trend",
    "W10.csv": "stochastic_trend",
    "uspop.csv": "deterministic_trend", "strikes.csv": "stationary",
    "sunspots.csv": "stationary", "airpass.csv": "stochastic_trend",
    "deaths.csv": "stochastic_trend",
    "INDPRO.csv": "stochastic_trend", "UNRATE.csv": "stochastic_trend",
    "soi_dataframe.csv": "stationary", "rec_dataframe.csv": "stationary",
    "GermanGNP.csv": "deterministic_trend",
    "US_investment.csv": "stationary",
    "German_consumption.csv": "stochastic_trend",
    "Polish_productivity.csv": "stochastic_trend",
    "RealInt_dataframe.csv": "stationary",
    "NP_xetradax_returns100.csv": "stationary",
}


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


def predict(meta_X, ens_base_p, base_pred, router_p, stat_probs,
            anom_probs_d, raw_new_anom, blend, stat_gate):
    preds = []
    for i in range(meta_X.shape[0]):
        base_type = BASE_LABELS[base_pred[i]]
        if stat_probs[i] >= stat_gate and ens_base_p[i, 0] >= STAT_BASE_AND:
            preds.append(("stationary", []))
            continue
        if router_p[i] < ROUTER_THETA:
            preds.append((base_type, []))
            continue
        anomalies = []
        suppress = (base_type == "stationary" and ens_base_p[i, 0] >= STAT_CONFIDENT)
        if not suppress:
            for j, anom_name in enumerate(ANOM_LABELS):
                params = blend[anom_name]
                blended = params["alpha"] * anom_probs_d[anom_name][i] + (1 - params["alpha"]) * float(raw_new_anom[i, j])
                eff_t = max(params["threshold"], CTX_THRESH) if base_type == "stationary" else params["threshold"]
                if blended >= eff_t:
                    anomalies.append(anom_name)
        preds.append((base_type, anomalies))
    return preds


def evaluate_realdata(preds, items):
    base_ok = 0
    full = 0
    for it, (pb, pa) in zip(items, preds):
        if it["expected_base"] is None:
            continue
        if pb == it["expected_base"]:
            base_ok += 1
        if pb == it["expected_base"] and not pa:  # GT'de hep anomali yok (saf)
            full += 1
    return base_ok, full


def main():
    print("[1] Veri toplaniyor...")
    real_items, real_series = [], []
    for c in sorted(REAL_DIR.glob("*.csv")):
        s = read_series(c)
        if len(s) >= 20:
            real_items.append({"name": c.name, "n": int(len(s)),
                                "expected_base": REAL_GT.get(c.name)})
            real_series.append(s)
    syn_items, syn_series = [], []
    manifest = json.load(open(SYN_DIR / "manifest.json"))
    for m in manifest:
        path = SYN_DIR / m["file"]
        if not path.exists():
            continue
        s = pd.read_csv(path)["value"].values.astype(float)
        syn_items.append({"name": m["file"], "kind": m["kind"], "n": int(m["length"]),
                           "expected_base": "stochastic_trend"})
        syn_series.append(s)
    all_items = real_items + syn_items
    all_series = real_series + syn_series
    print(f"   realdata: {len(real_items)} | sentetik: {len(syn_items)} | toplam: {len(all_items)}")

    print(f"\n[2] tsfresh extraction ({len(all_series)} seri)...")
    X = extract_batch(all_series)
    X_clean = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

    print("\n[3] Modeller yukleniyor...")
    old_models = load_old_ensemble()
    new_models = load_new_ensemble()
    base_meta = joblib.load(META_MODELS_DIR / "base_meta.pkl")
    anom_metas = {a: joblib.load(META_MODELS_DIR / f"anom_{a}.pkl")
                  for a in ANOM_LABELS
                  if (META_MODELS_DIR / f"anom_{a}.pkl").exists()}
    router = joblib.load(META_MODELS_DIR / "router.pkl")
    blend_baseline = joblib.load(META_MODELS_DIR / "blend_weights.pkl")
    tsfresh_scaler = joblib.load(PROCESSED_DIR / "tsfresh_scaler.pkl")
    stat_model, stat_scaler, stat_selector = load_stationary_detector()
    # Optim
    sweep_json = json.load(open(OUT / "alpha_thresh_sweep.json"))
    blend_optim = sweep_json["best_blend"]
    best_stat_gate = sweep_json["best_stat_gate"]
    print(f"   Optim STAT_GATE={best_stat_gate}, blend:")
    for a in ANOM_LABELS:
        print(f"     {a:<22} alpha={blend_optim[a]['alpha']:.2f} t={blend_optim[a]['threshold']:.2f}")

    print(f"\n[4] Ensemble inference...")
    n = len(all_series)
    raw_old = np.zeros((n, 8))
    raw_new = np.zeros((n, 9))
    for i in range(n):
        raw_old[i] = get_old_probs(old_models, X[i])
        raw_new[i] = get_new_probs(new_models, X[i])
    derived = _compute_derived_features(raw_old, raw_new)
    X_scaled = tsfresh_scaler.transform(X_clean)
    meta_X = np.hstack([raw_old, raw_new, derived, X_scaled])
    stat_probs = predict_stationary_batch(stat_model, stat_scaler, stat_selector, all_series)
    xgb_bp = base_meta["xgb"].predict_proba(meta_X)
    lgb_bp = base_meta["lgb"].predict_proba(meta_X)
    ens_base_p = 0.5 * xgb_bp + 0.5 * lgb_bp
    base_pred = np.argmax(ens_base_p, axis=1)
    xgb_r = router["xgb"].predict_proba(meta_X)[:, 1]
    lgb_r = router["lgb"].predict_proba(meta_X)[:, 1]
    router_p = 0.5 * xgb_r + 0.5 * lgb_r
    anom_probs_d = {}
    for a, m in anom_metas.items():
        xp = m["xgb"].predict_proba(meta_X)[:, 1]
        lp = m["lgb"].predict_proba(meta_X)[:, 1]
        anom_probs_d[a] = 0.5 * xp + 0.5 * lp
    raw_new_anom = raw_new[:, 4:]

    print(f"\n[5] Baseline (STAT_GATE=0.95) vs Optimized (STAT_GATE={best_stat_gate})...")
    base_preds = predict(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                          anom_probs_d, raw_new_anom, blend_baseline, 0.95)
    opt_preds = predict(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                         anom_probs_d, raw_new_anom, blend_optim, best_stat_gate)

    # Sentetik base accuracy
    def syn_acc(preds, items):
        c = 0; t = 0
        for it, (pb, _) in zip(items, preds):
            if it.get("expected_base") == "stochastic_trend":
                t += 1
                if pb == "stochastic_trend":
                    c += 1
        return c, t

    real_base_preds = base_preds[:len(real_items)]
    syn_base_preds = base_preds[len(real_items):]
    real_opt_preds = opt_preds[:len(real_items)]
    syn_opt_preds = opt_preds[len(real_items):]

    rb_base, rf_base = evaluate_realdata(real_base_preds, real_items)
    rb_opt, rf_opt = evaluate_realdata(real_opt_preds, real_items)
    sc_base, st = syn_acc(syn_base_preds, syn_items)
    sc_opt, _ = syn_acc(syn_opt_preds, syn_items)

    rd_with_gt = sum(1 for it in real_items if it["expected_base"])
    print(f"\nRealdata base accuracy (GT'li {rd_with_gt}/{len(real_items)} dosya):")
    print(f"   Baseline:  {rb_base}/{rd_with_gt}")
    print(f"   Optimized: {rb_opt}/{rd_with_gt} ({rb_opt - rb_base:+d})")
    print(f"\nRealdata FULL (GT=stationary, anom=[] dosyalar icin):")
    # Stationary GT'li dosyalar
    stat_files = [it for it in real_items if it["expected_base"] == "stationary"]
    print(f"   Stationary GT count: {len(stat_files)}")
    print(f"   Baseline FULL:  {rf_base}/{len(stat_files)}")
    print(f"   Optimized FULL: {rf_opt}/{len(stat_files)} ({rf_opt - rf_base:+d})")

    print(f"\nSentetik base accuracy ({st} stochastic_trend dosya):")
    print(f"   Baseline:  {sc_base}/{st} ({100*sc_base/st:.1f}%)")
    print(f"   Optimized: {sc_opt}/{st} ({100*sc_opt/st:.1f}%) ({sc_opt - sc_base:+d})")

    # MD rapor
    md = []
    md.append("# Optimized Blend Evaluation\n")
    md.append("Baseline (trainer-learned blend, STAT_GATE=0.95) vs Optimized (sweep'ten).\n")
    md.append(f"## Optimized config\n")
    md.append(f"- STAT_GATE = **{best_stat_gate}**")
    md.append("- Blend:")
    for a in ANOM_LABELS:
        md.append(f"  - {a}: alpha={blend_optim[a]['alpha']:.2f}, t={blend_optim[a]['threshold']:.2f}")
    md.append("\n## Sonuclar\n")
    md.append("| Metrik | Baseline | Optimized | Δ |")
    md.append("|---|---|---|---|")
    md.append(f"| Realdata base accuracy ({rd_with_gt} dosya) | {rb_base}/{rd_with_gt} | {rb_opt}/{rd_with_gt} | {rb_opt-rb_base:+d} |")
    md.append(f"| Realdata FULL (stat GT, {len(stat_files)} dosya) | {rf_base}/{len(stat_files)} | {rf_opt}/{len(stat_files)} | {rf_opt-rf_base:+d} |")
    md.append(f"| Sentetik base accuracy ({st} dosya) | {sc_base}/{st} ({100*sc_base/st:.1f}%) | {sc_opt}/{st} ({100*sc_opt/st:.1f}%) | {sc_opt-sc_base:+d} |")
    md.append("\n## Realdata detayli (stationary GT)\n")
    md.append("| dosya | n | GT | baseline pred | optim pred | optim anom |")
    md.append("|---|---|---|---|---|---|")
    for idx, it in enumerate(real_items):
        if it["expected_base"] != "stationary":
            continue
        bp = base_preds[idx][0]
        op = opt_preds[idx][0]
        oa = ", ".join(opt_preds[idx][1]) if opt_preds[idx][1] else "-"
        md.append(f"| {it['name']} | {it['n']} | stationary | {bp} | {op} | {oa} |")

    (OUT / "OPTIMIZED_EVAL.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nWrote: {OUT / 'OPTIMIZED_EVAL.md'}")


if __name__ == "__main__":
    main()
