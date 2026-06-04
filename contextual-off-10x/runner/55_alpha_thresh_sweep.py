"""
Per-anomaly (alpha, threshold) grid sweep.
contextual cikinca optimal degerler degismis mi gor.

Yaklasim: siralı per-anomaly grid (collective -> mean -> point -> trend -> variance).
Her anomali icin alpha x threshold grid'de gez, diger anomaliler en iyi bilinen
(alpha, threshold) ile sabit. Skor: 38-grup training set FULL count.

Sabit: STAT_GATE=1.00 (sweep onceden optimal gosterdi), STAT_BASE_AND=0.40,
STAT_CONFIDENT=0.75, CTX_THRESH=0.55, ROUTER_THETA=0.40.

Cikti: runner/results/ALPHA_THRESH_SWEEP.md + .json
"""
import json
import sys
import warnings
from itertools import product
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ens-final"))

from config import (
    ANOM_LABELS, BASE_LABELS, GROUP_EXPECTED, GROUP_PATHS, META_MODELS_DIR,
    NEW_ALL_MODELS, OLD_CLASSES, PROCESSED_DIR, SOURCE_GROUPS,
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

# Sabit (sweep'te degismeyen)
STAT_BASE_AND = 0.40
STAT_CONFIDENT = 0.75
CTX_THRESH = 0.55
ROUTER_THETA = 0.40

# Sweep grid'leri (v2: threshold genisletildi 0.30-0.90, alpha ince granular)
STAT_GATE_GRID = [0.90, 0.95, 1.00]                              # 3 deger (etki minimal)
ALPHA_GRID = [0.20, 0.35, 0.50, 0.65, 0.80, 0.95]                # 6 deger
THRESH_GRID = [round(0.30 + 0.05 * k, 2) for k in range(13)]      # 0.30 - 0.90, 13 deger

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


def collect_training_eval(n_per_group=20):
    import random
    random.seed(42)
    items, series = [], []
    for gid, gname, roots in SOURCE_GROUPS:
        all_csvs = []
        for root in roots:
            if root.exists():
                all_csvs.extend([f for f in root.rglob("*.csv") if f.name != "metadata.csv"])
        if not all_csvs:
            continue
        sampled = random.sample(all_csvs, min(n_per_group, len(all_csvs)))
        exp = GROUP_EXPECTED[gid]
        for c in sampled:
            s = read_series(c)
            if len(s) >= 50:
                items.append({"name": c.name, "n": int(len(s)), "gid": gid,
                              "expected_base": exp["base"], "expected_anoms": exp["anomalies"]})
                series.append(s)
    return items, series


def predict_one(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                anom_probs_d, raw_new_anom, blend_cfg, stat_gate):
    """blend_cfg = {anom_name: {'alpha': ..., 'threshold': ...}}"""
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
                params = blend_cfg[anom_name]
                alpha = params["alpha"]
                threshold = params["threshold"]
                meta_p = anom_probs_d[anom_name][i]
                new_p = float(raw_new_anom[i, j])
                blended = alpha * meta_p + (1 - alpha) * new_p
                eff_t = max(threshold, CTX_THRESH) if base_type == "stationary" else threshold
                if blended >= eff_t:
                    anomalies.append(anom_name)
        preds.append((base_type, anomalies))
    return preds


def match_type(pred_base, pred_anoms, expected_base, expected_anoms):
    base_ok = (pred_base == expected_base)
    pset = set(pred_anoms)
    eset = set(expected_anoms)
    if not eset:
        if base_ok and not pset:
            return "FULL"
        elif base_ok:
            return "PARTIAL"
        else:
            return "NONE"
    all_in = eset.issubset(pset)
    no_extra = (pset == eset)
    if base_ok and all_in and no_extra:
        return "FULL"
    elif base_ok or all_in:
        return "PARTIAL"
    return "NONE"


def evaluate(meta_X, ens_base_p, base_pred, router_p, stat_probs,
             anom_probs_d, raw_new_anom, blend_cfg, items, stat_gate):
    preds = predict_one(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                          anom_probs_d, raw_new_anom, blend_cfg, stat_gate)
    full = partial = none = 0
    for it, (pb, pa) in zip(items, preds):
        mt = match_type(pb, pa, it["expected_base"], it["expected_anoms"])
        if mt == "FULL": full += 1
        elif mt == "PARTIAL": partial += 1
        else: none += 1
    return preds, full, partial, none


def main():
    print("[1] Veri toplaniyor (training eval: 760 ornek)...")
    train_items, train_series = collect_training_eval(n_per_group=20)
    print(f"   Training eval: {len(train_items)}")

    print(f"\n[2] tsfresh extraction ({len(train_series)})...")
    X = extract_batch(train_series, n_jobs=4)
    X_clean = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

    print("\n[3] Modeller yukleniyor...")
    old_models = load_old_ensemble()
    new_models = load_new_ensemble()
    base_meta = joblib.load(META_MODELS_DIR / "base_meta.pkl")
    anom_metas = {a: joblib.load(META_MODELS_DIR / f"anom_{a}.pkl")
                  for a in ANOM_LABELS
                  if (META_MODELS_DIR / f"anom_{a}.pkl").exists()}
    router = joblib.load(META_MODELS_DIR / "router.pkl")
    blend_params_orig = joblib.load(META_MODELS_DIR / "blend_weights.pkl")
    tsfresh_scaler = joblib.load(PROCESSED_DIR / "tsfresh_scaler.pkl")
    stat_model, stat_scaler, stat_selector = load_stationary_detector()

    print(f"\n[4] Ensemble inference (cache)...")
    n = len(train_series)
    raw_old = np.zeros((n, 8))
    raw_new = np.zeros((n, 9))
    for i in range(n):
        raw_old[i] = get_old_probs(old_models, X[i])
        raw_new[i] = get_new_probs(new_models, X[i])
    derived = _compute_derived_features(raw_old, raw_new)
    X_scaled = tsfresh_scaler.transform(X_clean)
    meta_X = np.hstack([raw_old, raw_new, derived, X_scaled])
    stat_probs = predict_stationary_batch(stat_model, stat_scaler, stat_selector, train_series)
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

    print(f"\n[5] Baseline (trainer-learned, STAT_GATE=0.95) eval...")
    blend_baseline = {a: dict(blend_params_orig[a]) for a in ANOM_LABELS}
    _, bf, bp, bn = evaluate(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                              anom_probs_d, raw_new_anom, blend_baseline, train_items, 0.95)
    print(f"   Baseline: FULL={bf} PARTIAL={bp} NONE={bn} ({100*bf/n:.1f}%)")
    print(f"   Baseline params:")
    for a in ANOM_LABELS:
        bx = blend_baseline[a]
        print(f"      {a:<22} alpha={bx['alpha']:.2f} thresh={bx['threshold']:.2f}")

    print(f"\n[6] JOINT sweep: {len(STAT_GATE_GRID)} STAT_GATE x sıralı per-anomaly grid...")
    print(f"   STAT_GATE: {STAT_GATE_GRID}")
    print(f"   alpha grid: {ALPHA_GRID}")
    print(f"   threshold grid: {THRESH_GRID}")
    print(f"   Per anomali kombo: {len(ALPHA_GRID) * len(THRESH_GRID)} x {len(ANOM_LABELS)} anomali")

    # Per STAT_GATE: siralı per-anomaly optimize
    joint_results = []  # her STAT_GATE icin en iyi konfigurasyon
    per_anom_history_per_gate = {}

    for stat_gate in STAT_GATE_GRID:
        print(f"\n   === STAT_GATE = {stat_gate} ===")
        # Baseline blend ile baslayalim
        blend_curr = {a: dict(blend_baseline[a]) for a in ANOM_LABELS}
        history = {a: [] for a in ANOM_LABELS}
        for anom_name in ANOM_LABELS:
            best_full = -1
            best_cfg = None
            for alpha, thresh in product(ALPHA_GRID, THRESH_GRID):
                trial = {a: dict(blend_curr[a]) for a in ANOM_LABELS}
                trial[anom_name] = {"alpha": alpha, "threshold": thresh}
                _, f, p, no = evaluate(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                                         anom_probs_d, raw_new_anom, trial, train_items, stat_gate)
                history[anom_name].append({
                    "alpha": alpha, "threshold": thresh, "FULL": f, "PARTIAL": p, "NONE": no,
                })
                if f > best_full:
                    best_full = f
                    best_cfg = {"alpha": alpha, "threshold": thresh}
            blend_curr[anom_name] = best_cfg
        # Final FULL bu STAT_GATE ile
        _, ff, fp, fn = evaluate(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                                  anom_probs_d, raw_new_anom, blend_curr, train_items, stat_gate)
        print(f"   OPTIMIZED @ STAT_GATE={stat_gate}: FULL={ff} ({100*ff/n:.1f}%)")
        joint_results.append({
            "stat_gate": stat_gate,
            "blend": blend_curr,
            "FULL": ff, "PARTIAL": fp, "NONE": fn,
        })
        per_anom_history_per_gate[stat_gate] = history

    # En iyi joint konfigurasyon
    best_joint = max(joint_results, key=lambda r: r["FULL"])
    blend_optim = best_joint["blend"]
    best_stat_gate = best_joint["stat_gate"]
    ff = best_joint["FULL"]; fp = best_joint["PARTIAL"]; fn = best_joint["NONE"]
    print(f"\n[7] EN IYI JOINT: STAT_GATE={best_stat_gate} -> FULL={ff}/{n} ({100*ff/n:.1f}%)")
    print(f"   Baseline farki: {bf} -> {ff} ({ff-bf:+d} FULL)")

    # Optimal blend'i sakla
    optim_path = OUT / "blend_optim.pkl"
    joblib.dump({"stat_gate": best_stat_gate, "blend": blend_optim}, optim_path)

    # Markdown rapor
    md = []
    md.append("# Joint (STAT_GATE x Per-Anomaly Alpha+Threshold) Grid Sweep\n")
    md.append(f"**contextual-off-10x** — training eval (20/grup × 38 grup = {n} seri)\n")
    md.append(f"\n## Baseline (trainer-learned blend_weights.pkl + STAT_GATE=0.95)\n")
    md.append(f"- FULL: {bf}/{n} ({100*bf/n:.1f}%)")
    md.append(f"- PARTIAL: {bp}, NONE: {bn}\n")

    md.append("\n## STAT_GATE x Joint Optimization\n")
    md.append("Her STAT_GATE icin: 5 anomali sıralı (alpha, threshold) grid optimize edildi.")
    md.append("\n| STAT_GATE | FULL | PARTIAL | NONE | FULL% |")
    md.append("|---|---|---|---|---|")
    for r in joint_results:
        marker = " ← **EN IYI**" if r["stat_gate"] == best_stat_gate else ""
        md.append(f"| {r['stat_gate']:.2f} | {r['FULL']} | {r['PARTIAL']} | {r['NONE']} | {100*r['FULL']/n:.1f}%{marker} |")

    md.append(f"\n## EN IYI joint config\n")
    md.append(f"- **STAT_GATE = {best_stat_gate}**")
    md.append(f"- **FULL: {ff}/{n} ({100*ff/n:.1f}%)**, PARTIAL: {fp}, NONE: {fn}")
    md.append(f"- Baseline farki: **{ff-bf:+d} FULL** ({bf} -> {ff})\n")

    md.append("\n## Optimal blend dictionary\n```python")
    md.append(f"# STAT_GATE = {best_stat_gate}")
    md.append("blend_optim = {")
    for a in ANOM_LABELS:
        o = blend_optim[a]
        md.append(f"    '{a}': {{'alpha': {o['alpha']:.2f}, 'threshold': {o['threshold']:.2f}}},")
    md.append("}\n```")

    md.append("\n## Per-STAT_GATE secilen blend params\n")
    md.append("| STAT_GATE | " + " | ".join(ANOM_LABELS) + " | FULL |")
    md.append("|---|" + "|".join("---" for _ in ANOM_LABELS) + "|---|")
    for r in joint_results:
        cells = [f"{r['stat_gate']:.2f}"]
        for a in ANOM_LABELS:
            o = r["blend"][a]
            cells.append(f"α={o['alpha']:.2f}/t={o['threshold']:.2f}")
        cells.append(str(r["FULL"]))
        md.append("| " + " | ".join(cells) + " |")

    md.append("\n## En iyi STAT_GATE icin per-anomaly grid (FULL count)\n")
    best_history = per_anom_history_per_gate[best_stat_gate]
    for a in ANOM_LABELS:
        md.append(f"\n### {a} @ STAT_GATE={best_stat_gate}\n")
        md.append("| alpha\\thresh |" + "|".join(f" {t:.2f} " for t in THRESH_GRID) + "|")
        md.append("|---|" + "|".join("---" for _ in THRESH_GRID) + "|")
        for alpha in ALPHA_GRID:
            row = [f"**{alpha:.2f}**"]
            for t in THRESH_GRID:
                hit = next(h for h in best_history[a] if h["alpha"] == alpha and h["threshold"] == t)
                row.append(str(hit["FULL"]))
            md.append("| " + " | ".join(row) + " |")

    out_md = OUT / "ALPHA_THRESH_SWEEP.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nWrote: {out_md}")
    print(f"Optimal config: {optim_path}")

    # JSON
    with open(OUT / "alpha_thresh_sweep.json", "w", encoding="utf-8") as f:
        json.dump({
            "baseline_full": bf, "baseline_total": n,
            "best_stat_gate": best_stat_gate,
            "best_blend": blend_optim,
            "best_full": ff, "best_partial": fp, "best_none": fn,
            "joint_results": [
                {"stat_gate": r["stat_gate"], "blend": r["blend"],
                 "FULL": r["FULL"], "PARTIAL": r["PARTIAL"], "NONE": r["NONE"]}
                for r in joint_results
            ],
        }, f, indent=2)


if __name__ == "__main__":
    main()
