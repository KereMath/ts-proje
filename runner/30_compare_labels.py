"""
Datasets.pdf'teki ground truth label'lari ile bizim ens-final pipeline
tahminlerini karsilastir.

Cikti: runner/results/LABEL_KARSILASTIRMA.md + .csv
"""
import json
from pathlib import Path

import pandas as pd

RUNNER = Path(__file__).resolve().parent
OUT = RUNNER / "results"

# ----------------------------------------------------------------------
# Ground truth — Datasets.pdf'ten cikarildi
# ----------------------------------------------------------------------
# Format: file_name -> {base, anomalies, source, notes}
# Pipeline labelleri ile uyusmasi icin:
#   - "seasonal" -> stochastic_trend (bizim pipeline seasonal-only kategorisi yok)
#   - "seasonal unit root" -> stochastic_trend
#   - "regular and seasonal stochastic trend" -> stochastic_trend
#   - "non stat in mean with trend" -> deterministic_trend
#   - "exponentially increasing" -> deterministic_trend (eksponansiyel/cubic)
#   - "structural break" -> trend_shift veya mean_shift
GROUND_TRUTH = {
    # --- Wei (Time Series Analysis 4ed) ---
    "W1.csv": {
        "base": "stationary",
        "anomalies": ["point_anomaly"],  # outliers at t=4,7,9,36 (AO/IO)
        "source": "Wei",
        "notes": "stationary, AO/IO outliers at t=4,7,9,36",
    },
    "W2.csv": {
        "base": "stationary",
        "anomalies": ["variance_shift"],  # stationary in mean, may not in variance
        "source": "Wei",
        "notes": "stationary in mean, possibly variance shift",
    },
    "W3.csv": {
        "base": "stationary",
        "anomalies": ["variance_shift"],
        "source": "Wei",
        "notes": "stationary in mean, possibly variance shift",
    },
    "W5.csv": {
        "base": "deterministic_trend",
        "anomalies": ["mean_shift"],  # TC at t=81,82 — temp change
        "source": "Wei",
        "notes": "non-stat in mean, increasing trend, TC at t=81,82",
    },
    "W6.csv": {
        "base": "deterministic_trend",
        "anomalies": ["variance_shift"],
        "source": "Wei",
        "notes": "non-stat in mean AND variance",
    },
    "W10.csv": {
        "base": "stochastic_trend",
        "anomalies": ["point_anomaly"],  # AO at t=12, IO at t=27
        "source": "Wei",
        "notes": "seasonal unit root, outliers t=12,27 (cok kisa n=32)",
    },

    # --- Brockwell & Davis ---
    "uspop.csv": {
        "base": "deterministic_trend",
        "anomalies": [],
        "source": "Brockwell",
        "notes": "exponentially increasing (US population)",
    },
    "strikes.csv": {
        "base": "stationary",
        "anomalies": [],
        "source": "Brockwell",
        "notes": "erratic, slowly rising level — pratikte stationary",
    },
    "sunspots.csv": {
        "base": "stationary",
        "anomalies": [],
        "source": "Brockwell",
        "notes": "Wolfer sunspots, cyclic period ~11 years",
    },
    "airpass.csv": {
        "base": "stochastic_trend",
        "anomalies": [],
        "source": "Brockwell",
        "notes": "regular + seasonal stochastic trend",
    },
    "deaths.csv": {
        "base": "stochastic_trend",
        "anomalies": [],
        "source": "Brockwell",
        "notes": "regular + seasonal unit root (period 12)",
    },

    # --- Shumway & Stoffer + Federal Reserve ---
    "INDPRO.csv": {
        "base": "stochastic_trend",
        "anomalies": [],
        "source": "Shumway",
        "notes": "ARIMA(0,1,1)(0,1,1)_12 — seasonal stochastic trend",
    },
    "UNRATE.csv": {
        "base": "stochastic_trend",
        "anomalies": [],
        "source": "Shumway",
        "notes": "Monthly Fed Unemployment 1948-1978",
    },
    "soi_dataframe.csv": {
        "base": "stationary",
        "anomalies": [],
        "source": "Shumway",
        "notes": "Southern Oscillation Index, cyclic ~1/yr",
    },
    "rec_dataframe.csv": {
        "base": "stationary",
        "anomalies": [],
        "source": "Shumway",
        "notes": "Recruitment series — stationary (BIZDE n=0)",
    },

    # --- JMulTi (Lutkepohl) ---
    "GermanGNP.csv": {
        "base": "deterministic_trend",
        "anomalies": ["trend_shift"],
        "source": "JMulTi",
        "notes": "structural break at 1990Q3 (German unification)",
    },
    "US_investment.csv": {
        "base": "stationary",
        "anomalies": [],
        "source": "JMulTi",
        "notes": "better as I(0) than I(1)",
    },
    "German_consumption.csv": {
        "base": "stochastic_trend",
        "anomalies": [],
        "source": "JMulTi",
        "notes": "log consumption has unit root",
    },
    "Polish_productivity.csv": {
        "base": "stochastic_trend",
        "anomalies": ["trend_shift"],
        "source": "JMulTi",
        "notes": "structural shift 1990Q1",
    },

    # --- Bai-Perron ---
    "RealInt_dataframe.csv": {
        "base": "stationary",
        "anomalies": ["mean_shift"],
        "source": "Bai-Perron",
        "notes": "US real interest rate, breaks at 1966,1972,1980",
    },

    # --- Other (DAX returns) ---
    "NP_xetradax_returns100.csv": {
        "base": "stationary",
        "anomalies": [],
        "source": "Lutkepohl",
        "notes": "DAX log returns (finansal teori: stationary)",
    },
}


def load_predictions():
    """ens-final pipeline'in iki kosusunu birlestirip dict olarak don."""
    preds = {}
    for fname in ["ensfinal_realdata.json", "ensfinal_short.json"]:
        fpath = OUT / fname
        if not fpath.exists():
            continue
        data = json.load(open(fpath, encoding="utf-8"))
        for r in data:
            preds[r["name"]] = {
                "n": r["n"],
                "pred_base": r["pred_base"],
                "pred_anoms": r["pred_anoms"],
                "decision_path": r["decision_path"],
                "stat_prob": r["stat_prob"],
                "router_combo_prob": r["router_combo_prob"],
            }
    return preds


def compare_one(gt, pr):
    """Bir dosya icin (base_match, anomaly_match, match_type) don."""
    base_ok = gt["base"] == pr["pred_base"]
    gt_anom = set(gt["anomalies"])
    pr_anom = set(pr["pred_anoms"])
    if not gt_anom:
        # Ground truth bos -> tahmin de bos olmali
        anom_ok = (len(pr_anom) == 0)
    else:
        # Tum gt anomaliler tahminde olmali (extra olmasi PARTIAL'a yol acmaz, FULL'i bozar)
        anom_ok = gt_anom.issubset(pr_anom) and (pr_anom == gt_anom)
    # MATCH TYPE — eski raporlarla ayni tanim:
    #   FULL: base OK + tum gt_anom var + extra anom yok
    #   PARTIAL: base OK ya da gt_anom hepsi var (ama digeri degil)
    #   NONE: hicbiri
    if not gt_anom:
        if base_ok and not pr_anom:
            mt = "FULL"
        elif base_ok:
            mt = "PARTIAL"  # base dogru ama yanlis anomali ekledi
        else:
            mt = "NONE"
    else:
        all_gt_in_pr = gt_anom.issubset(pr_anom)
        no_extra = (pr_anom == gt_anom)
        if base_ok and all_gt_in_pr and no_extra:
            mt = "FULL"
        elif base_ok and all_gt_in_pr:
            mt = "PARTIAL"  # base + tum gt anom var, ama extra anom da var
        elif base_ok or all_gt_in_pr:
            mt = "PARTIAL"
        else:
            mt = "NONE"
    return base_ok, anom_ok, mt


def main():
    preds = load_predictions()
    print(f"Toplam {len(preds)} pipeline tahmini, {len(GROUND_TRUTH)} ground truth label")

    rows = []
    for fname, gt in GROUND_TRUTH.items():
        if fname not in preds:
            rows.append({
                "file": fname, "n": "-", "source": gt["source"],
                "gt_base": gt["base"], "gt_anoms": ", ".join(gt["anomalies"]) or "-",
                "pred_base": "(pipeline'a girmedi)",
                "pred_anoms": "-",
                "base_ok": False, "match": "MISSING",
                "notes": gt["notes"],
            })
            continue
        pr = preds[fname]
        base_ok, anom_ok, mt = compare_one(gt, pr)
        rows.append({
            "file": fname, "n": pr["n"], "source": gt["source"],
            "gt_base": gt["base"], "gt_anoms": ", ".join(gt["anomalies"]) or "-",
            "pred_base": pr["pred_base"],
            "pred_anoms": ", ".join(pr["pred_anoms"]) or "-",
            "base_ok": base_ok,
            "match": mt,
            "notes": gt["notes"],
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "label_comparison.csv", index=False)

    # --- Markdown ---
    md = []
    md.append("# realdata Ground Truth vs ens-final Tahminleri\n")
    md.append("Ground truth Datasets.pdf'ten cikarildi (Wei, Brockwell, Lutkepohl, Shumway & Stoffer, Bai-Perron).\n")
    md.append("\n**Etiket eslesimi notlari:**")
    md.append("- Pipeline sadece 4 base sinif tahmin eder: stationary / deterministic_trend / stochastic_trend / volatility")
    md.append("- 'Seasonal unit root' ve 'regular+seasonal stochastic trend' → `stochastic_trend` olarak esledim")
    md.append("- 'AO/IO outliers' (Wei) → `point_anomaly`")
    md.append("- 'TC (temporary change)' → `mean_shift` (ya da `trend_shift`)")
    md.append("- 'structural break' → `trend_shift` veya `mean_shift`\n")

    # Match types
    counts = df["match"].value_counts().to_dict()
    md.append("\n## Ozet\n")
    md.append("| Match | Sayi |")
    md.append("|---|---|")
    for mt in ["FULL", "PARTIAL", "NONE", "MISSING"]:
        md.append(f"| {mt} | {counts.get(mt, 0)} |")
    md.append(f"| **TOPLAM** | **{len(rows)}** |")

    base_correct = sum(1 for r in rows if r["base_ok"])
    md.append(f"\n**Base type dogru: {base_correct} / {len([r for r in rows if r['match']!='MISSING'])}** "
              f"(MISSING dosyalar haric)")

    # --- Full Comparison Table ---
    md.append("\n## Tum karsilastirma\n")
    md.append("| dosya | n | kaynak | GT base | GT anomali | model base | model anomali | base✓ | match |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for _, r in df.iterrows():
        base_mark = "✓" if r["base_ok"] else "✗"
        # Highlight match type
        mt_str = r["match"]
        if mt_str == "FULL":
            mt_str = f"**{mt_str}**"
        md.append(
            f"| {r['file']} | {r['n']} | {r['source']} | {r['gt_base']} | {r['gt_anoms']} | "
            f"{r['pred_base']} | {r['pred_anoms']} | {base_mark} | {mt_str} |"
        )

    # --- Notlar bolumu ---
    md.append("\n## Detayli notlar (PDF'ten)\n")
    md.append("| dosya | not |")
    md.append("|---|---|")
    for _, r in df.iterrows():
        md.append(f"| {r['file']} | {r['notes']} |")

    # Critical stationary cases
    md.append("\n## KESIN STATIONARY oldugu bilinen dosyalar\n")
    md.append("PDF'te acikca 'stationary' diye etiketlenmis dosyalar:\n")
    stat_files = [r for _, r in df.iterrows() if r["gt_base"] == "stationary"]
    md.append("| dosya | n | kaynak | model base | model anomali | base✓ | match |")
    md.append("|---|---|---|---|---|---|---|")
    for r in stat_files:
        base_mark = "✓" if r["base_ok"] else "✗"
        md.append(
            f"| {r['file']} | {r['n']} | {r['source']} | {r['pred_base']} | "
            f"{r['pred_anoms']} | {base_mark} | {r['match']} |"
        )

    out_md = OUT / "LABEL_KARSILASTIRMA.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Yazildi: {out_md}")
    print(f"CSV    : {OUT / 'label_comparison.csv'}")


if __name__ == "__main__":
    main()
