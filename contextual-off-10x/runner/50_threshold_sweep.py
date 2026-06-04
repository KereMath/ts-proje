"""
Stationarity threshold sweep:
- STAT_GATE: [0.85, 0.90, 0.92, 0.95, 0.97, 0.99]
- STAT_BASE_AND sabit 0.40
- STAT_CONFIDENT: [0.60, 0.70, 0.75, 0.85] (anomali suppress esigi)
- CTX_THRESH sabit 0.55

Once tek tsfresh ekstraksiyonu yap, sonra her threshold kombinasyonu icin
karar mantigini uygula. Sentetik (500 dosya), realdata (~38 dosya) ve 38-grup
egitim seti uzerinde sonuclari karsilastir.

Cikti: runner/results/threshold_sweep.json + threshold_sweep.md
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
OUT.mkdir(exist_ok=True)

# Sweep grid: STAT_GATE 0.00 -> 1.00, 0.05 adimli (21 deger)
STAT_GATES = [round(0.05 * k, 2) for k in range(21)]  # 0.00, 0.05, ..., 1.00
STAT_CONFIDENTS = [0.75]  # sabit, sweep odakli STAT_GATE
STAT_BASE_AND = 0.0   # 0.40 -> 0.0 (kapali, sweep saf STAT_GATE etkisi)
CTX_THRESH = 0.55
ROUTER_THETA = 0.40

# Realdata ground truth (Datasets.pdf'ten)
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


def collect_realdata():
    items, series = [], []
    for c in sorted(REAL_DIR.glob("*.csv")):
        s = read_series(c)
        if len(s) >= 20:
            gt = REAL_GT.get(c.name)
            items.append({"source": "realdata", "name": c.name, "n": int(len(s)),
                           "expected_base": gt, "expected_anoms": [] if gt else None, "gid": None})
            series.append(s)
    return items, series


def collect_synthetic():
    items, series = [], []
    manifest = json.load(open(SYN_DIR / "manifest.json"))
    for m in manifest:
        path = SYN_DIR / m["file"]
        if not path.exists():
            continue
        s = pd.read_csv(path)["value"].values.astype(float)
        items.append({"source": "synthetic", "name": m["file"], "kind": m["kind"],
                       "n": int(m["length"]),
                       "expected_base": "stochastic_trend", "expected_anoms": []})
        series.append(s)
    return items, series


def collect_training_eval(n_per_group=20):
    """Egitim grup'larindan her birinden n_per_group ornek topla (eval).
    Random sample ile."""
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
                items.append({"source": "training", "name": c.name, "n": int(len(s)),
                              "gid": gid, "group_name": gname,
                              "expected_base": exp["base"], "expected_anoms": exp["anomalies"]})
                series.append(s)
    return items, series


def predict_with_thresholds(meta_X, ens_base_p, base_pred, router_p, stat_probs,
                             anom_probs_d, raw_new_anom, blend_params,
                             stat_gate, stat_confident):
    """Tek bir threshold konfigurasyonu icin tahminler."""
    preds = []
    for i in range(meta_X.shape[0]):
        base_type = BASE_LABELS[base_pred[i]]
        if stat_probs[i] >= stat_gate and ens_base_p[i, 0] >= STAT_BASE_AND:
            pred_base, pred_anoms = "stationary", []
        elif router_p[i] < ROUTER_THETA:
            pred_base, pred_anoms = base_type, []
        else:
            anomalies = []
            suppress = (base_type == "stationary" and ens_base_p[i, 0] >= stat_confident)
            if not suppress:
                for j, anom_name in enumerate(ANOM_LABELS):
                    params = blend_params.get(anom_name, {"alpha": 1.0, "threshold": 0.5})
                    meta_p = anom_probs_d[anom_name][i]
                    new_p = float(raw_new_anom[i, j])
                    blended = params["alpha"] * meta_p + (1 - params["alpha"]) * new_p
                    eff_t = max(params["threshold"], CTX_THRESH) if base_type == "stationary" else params["threshold"]
                    if blended >= eff_t:
                        anomalies.append(anom_name)
            pred_base, pred_anoms = base_type, anomalies
        preds.append((pred_base, pred_anoms))
    return preds


def match_type(pred_base, pred_anoms, expected_base, expected_anoms):
    if expected_base is None:
        return "?"  # realdata, ground truth yok
    base_ok = (pred_base == expected_base)
    pred_set = set(pred_anoms)
    exp_set = set(expected_anoms)
    if not exp_set:
        if base_ok and not pred_set:
            return "FULL"
        elif base_ok:
            return "PARTIAL"
        else:
            return "NONE"
    else:
        all_in = exp_set.issubset(pred_set)
        no_extra = (pred_set == exp_set)
        if base_ok and all_in and no_extra:
            return "FULL"
        elif base_ok or all_in:
            return "PARTIAL"
        else:
            return "NONE"


def main():
    print("[1] Veri toplaniyor...")
    real_items, real_series = collect_realdata()
    syn_items, syn_series = collect_synthetic()
    train_items, train_series = collect_training_eval(n_per_group=20)  # 38 x 20 = 760
    all_items = real_items + syn_items + train_items
    all_series = real_series + syn_series + train_series
    print(f"   realdata: {len(real_items)} | sentetik: {len(syn_items)} | egitim eval: {len(train_items)}")
    print(f"   Toplam: {len(all_items)} seri")

    print(f"\n[2] tsfresh extraction (batch {len(all_series)})...")
    X = extract_batch(all_series, n_jobs=4)
    X_clean = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

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

    print(f"\n[4] Ensemble inference ({len(all_series)} seri)...")
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

    print(f"\n[5] Threshold sweep ({len(STAT_GATES)} x {len(STAT_CONFIDENTS)} = "
          f"{len(STAT_GATES)*len(STAT_CONFIDENTS)} kombo)...")
    sweep = []
    for stat_gate, stat_conf in product(STAT_GATES, STAT_CONFIDENTS):
        preds = predict_with_thresholds(
            meta_X, ens_base_p, base_pred, router_p, stat_probs,
            anom_probs_d, raw_new_anom, blend_params,
            stat_gate, stat_conf,
        )
        # Match'leri hesapla
        per_source = {"realdata": {"FULL":0,"PARTIAL":0,"NONE":0,"total":0,"base_ok":0},
                      "synthetic": {"FULL":0,"PARTIAL":0,"NONE":0,"total":0,"base_ok":0},
                      "training": {"FULL":0,"PARTIAL":0,"NONE":0,"total":0,"base_ok":0}}
        for it, (pb, pa) in zip(all_items, preds):
            src = it["source"]
            if it["expected_base"] is None:
                per_source[src]["total"] += 1
                continue
            mt = match_type(pb, pa, it["expected_base"], it["expected_anoms"])
            per_source[src][mt] += 1
            per_source[src]["total"] += 1
            if pb == it["expected_base"]:
                per_source[src]["base_ok"] += 1
        sweep.append({
            "stat_gate": stat_gate, "stat_confident": stat_conf,
            "per_source": per_source,
        })
        # Kompakt log
        rd = per_source["realdata"]
        syn = per_source["synthetic"]
        trn = per_source["training"]
        print(f"  gate={stat_gate:.2f} conf={stat_conf:.2f} "
              f"| Training: F={trn['FULL']}/{trn['total']} ({100*trn['FULL']/max(trn['total'],1):.1f}%)"
              f" | Synthetic base_ok={syn['base_ok']}/{syn['total']}"
              f" | Realdata base_ok={rd['base_ok']}/{rd['total']}")

    out = {"sweep": sweep, "n_total": n,
           "n_realdata": len(real_items), "n_synthetic": len(syn_items),
           "n_training": len(train_items)}
    with open(OUT / "threshold_sweep.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote: {OUT / 'threshold_sweep.json'}")

    # Markdown ozet (STAT_CONFIDENT=0.75'te tum STAT_GATE degerleri)
    md = []
    md.append("# Stationarity Threshold Sweep (contextual-off-10x)\n")
    md.append(f"Toplam {n} seri test edildi.")
    md.append(f"- realdata: {len(real_items)}")
    md.append(f"- sentetik (50/config = 500 stoch_trend): {len(syn_items)}")
    md.append(f"- egitim seti eval (20/grup × 38 grup): {len(train_items)}\n")
    md.append("STAT_CONFIDENT sabit 0.75. STAT_GATE 0.00 -> 1.00 (0.05 adimli).\n")

    for conf in STAT_CONFIDENTS:
        md.append(f"\n## STAT_CONFIDENT = {conf}\n")
        md.append("| STAT_GATE | Training FULL | Train PARTIAL | Train NONE | Train FULL% | Sentetik base✓ | Sent base% | Realdata base✓ |")
        md.append("|---|---|---|---|---|---|---|---|")
        for row in sweep:
            if row["stat_confident"] != conf:
                continue
            tr = row["per_source"]["training"]
            syn = row["per_source"]["synthetic"]
            rd = row["per_source"]["realdata"]
            tr_pct = 100 * tr["FULL"] / max(tr["total"], 1)
            syn_pct = 100 * syn["base_ok"] / max(syn["total"], 1)
            md.append(f"| {row['stat_gate']:.2f} | {tr['FULL']} | {tr['PARTIAL']} | {tr['NONE']} | "
                       f"{tr_pct:.1f}% | {syn['base_ok']}/{syn['total']} | {syn_pct:.1f}% | "
                       f"{rd['base_ok']}/{rd['total']} |")

    # En iyi konfigurasyon
    md.append("\n## En iyi konfigurasyonlar\n")
    # Egitim FULL'a gore
    best_tr = max(sweep, key=lambda r: r["per_source"]["training"]["FULL"])
    md.append(f"- **En yuksek Training FULL:** gate={best_tr['stat_gate']:.2f} "
              f"conf={best_tr['stat_confident']:.2f} -> {best_tr['per_source']['training']['FULL']}/{best_tr['per_source']['training']['total']}")
    best_syn = max(sweep, key=lambda r: r["per_source"]["synthetic"]["base_ok"])
    md.append(f"- **En yuksek Sentetik base_ok:** gate={best_syn['stat_gate']:.2f} "
              f"conf={best_syn['stat_confident']:.2f} -> {best_syn['per_source']['synthetic']['base_ok']}/{best_syn['per_source']['synthetic']['total']}")
    best_rd = max(sweep, key=lambda r: r["per_source"]["realdata"]["base_ok"])
    md.append(f"- **En yuksek Realdata base_ok:** gate={best_rd['stat_gate']:.2f} "
              f"conf={best_rd['stat_confident']:.2f} -> {best_rd['per_source']['realdata']['base_ok']}/{best_rd['per_source']['realdata']['total']}")

    out_md = OUT / "THRESHOLD_SWEEP.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote: {out_md}")


if __name__ == "__main__":
    main()
