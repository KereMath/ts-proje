"""
Ground truth karsilastirma (contextual-off).
contextual GT olan dosyalar zaten yok (PDF'te de yoktu).
"""
import json
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent / "results"

# Datasets.pdf ground truth (contextual etiketli dosya yok zaten)
GROUND_TRUTH = {
    "W1.csv": {"base": "stationary", "anomalies": ["point_anomaly"], "source": "Wei",
               "notes": "stationary + AO/IO outliers"},
    "W2.csv": {"base": "stationary", "anomalies": ["variance_shift"], "source": "Wei",
               "notes": "stationary in mean, var shift"},
    "W3.csv": {"base": "stationary", "anomalies": ["variance_shift"], "source": "Wei",
               "notes": "stationary in mean, var shift"},
    "W5.csv": {"base": "deterministic_trend", "anomalies": ["mean_shift"], "source": "Wei",
               "notes": "trend + TC"},
    "W6.csv": {"base": "deterministic_trend", "anomalies": ["variance_shift"], "source": "Wei",
               "notes": "trend + var"},
    "W10.csv": {"base": "stochastic_trend", "anomalies": ["point_anomaly"], "source": "Wei",
                "notes": "seasonal unit root"},
    "uspop.csv": {"base": "deterministic_trend", "anomalies": [], "source": "Brockwell",
                  "notes": "exp trend"},
    "strikes.csv": {"base": "stationary", "anomalies": [], "source": "Brockwell",
                    "notes": "stationary"},
    "sunspots.csv": {"base": "stationary", "anomalies": [], "source": "Brockwell",
                     "notes": "cyclic stationary"},
    "airpass.csv": {"base": "stochastic_trend", "anomalies": [], "source": "Brockwell",
                    "notes": "regular+seasonal stoch trend"},
    "deaths.csv": {"base": "stochastic_trend", "anomalies": [], "source": "Brockwell",
                   "notes": "seasonal stoch trend"},
    "INDPRO.csv": {"base": "stochastic_trend", "anomalies": [], "source": "Shumway",
                   "notes": "seasonal stoch trend"},
    "UNRATE.csv": {"base": "stochastic_trend", "anomalies": [], "source": "Shumway",
                   "notes": "seasonal stoch trend"},
    "soi_dataframe.csv": {"base": "stationary", "anomalies": [], "source": "Shumway",
                          "notes": "cyclic stationary"},
    "rec_dataframe.csv": {"base": "stationary", "anomalies": [], "source": "Shumway",
                          "notes": "stationary"},
    "GermanGNP.csv": {"base": "deterministic_trend", "anomalies": ["trend_shift"],
                      "source": "JMulTi", "notes": "break 1990Q3"},
    "US_investment.csv": {"base": "stationary", "anomalies": [], "source": "JMulTi",
                          "notes": "I(0)"},
    "German_consumption.csv": {"base": "stochastic_trend", "anomalies": [], "source": "JMulTi",
                                "notes": "unit root"},
    "Polish_productivity.csv": {"base": "stochastic_trend", "anomalies": ["trend_shift"],
                                 "source": "JMulTi", "notes": "shift 1990Q1"},
    "RealInt_dataframe.csv": {"base": "stationary", "anomalies": ["mean_shift"],
                               "source": "Bai-Perron", "notes": "breaks 1966,72,80"},
    "NP_xetradax_returns100.csv": {"base": "stationary", "anomalies": [], "source": "Lutkepohl",
                                    "notes": "DAX log returns"},
}


def main():
    preds = {}
    p = OUT / "realdata.json"
    if p.exists():
        for r in json.load(open(p, encoding="utf-8")):
            preds[r["name"]] = r

    rows = []
    for fname, gt in GROUND_TRUTH.items():
        if fname not in preds:
            rows.append({
                "file": fname, "n": "-", "source": gt["source"],
                "gt_base": gt["base"], "gt_anoms": ", ".join(gt["anomalies"]) or "-",
                "pred_base": "(pipeline'a girmedi)", "pred_anoms": "-",
                "base_ok": False, "match": "MISSING",
            })
            continue
        pr = preds[fname]
        base_ok = pr["pred_base"] == gt["base"]
        gt_anom = set(gt["anomalies"])
        pr_anom = set(pr["pred_anoms"])
        if not gt_anom:
            if base_ok and not pr_anom:
                mt = "FULL"
            elif base_ok:
                mt = "PARTIAL"
            else:
                mt = "NONE"
        else:
            all_in = gt_anom.issubset(pr_anom)
            no_extra = (pr_anom == gt_anom)
            if base_ok and all_in and no_extra:
                mt = "FULL"
            elif base_ok and all_in:
                mt = "PARTIAL"
            elif base_ok or all_in:
                mt = "PARTIAL"
            else:
                mt = "NONE"
        rows.append({
            "file": fname, "n": pr["n"], "source": gt["source"],
            "gt_base": gt["base"], "gt_anoms": ", ".join(gt["anomalies"]) or "-",
            "pred_base": pr["pred_base"],
            "pred_anoms": ", ".join(pr["pred_anoms"]) or "-",
            "base_ok": base_ok, "match": mt,
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "label_comparison.csv", index=False)

    print("Match counts:"); print(df["match"].value_counts())
    print()
    bc = df["base_ok"].sum()
    nm = len(df[df["match"] != "MISSING"])
    print(f"Base correct: {bc}/{nm}")
    print()
    print("Stationary dosyalar:")
    for _, r in df[df["gt_base"] == "stationary"].iterrows():
        mark = "✓" if r["base_ok"] else "✗"
        print(f"  [{r['match']:<7}] {r['file']:<32} pred={r['pred_base']:<22} anom={r['pred_anoms'][:50]}")


if __name__ == "__main__":
    main()
