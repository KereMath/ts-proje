"""
predictions.csv'den okuyup ozetli bir markdown raporu uretir:
1. Sentetik (stochastic-trend) icin tip ve uzunluk basina basarim
2. Tum realdata icin tahminler
3. Her bir model (9 detector) icin probability dagilimi
4. Kisa-seri (n<=100) ozel basarim analizi
"""
import json
import sys
from pathlib import Path

import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parent / "results"
CLASSES = [
    "collective_anomaly", "contextual_anomaly", "deterministic_trend",
    "mean_shift", "point_anomaly", "stochastic_trend",
    "trend_shift", "variance_shift", "volatility",
]
PROB_COLS = [f"P_{c}" for c in CLASSES]


def fmt_probs(row):
    parts = []
    for c in CLASSES:
        v = row[f"P_{c}"]
        try:
            parts.append(f"{c[:3].upper()}={v:.2f}")
        except Exception:
            parts.append(f"{c[:3].upper()}=NA")
    return " ".join(parts)


def main():
    df = pd.read_csv(RESULTS_DIR / "predictions.csv")
    out = []
    out.append("# tsfresh-ensemble-stationary Pipeline Raporu\n")
    out.append("Pipeline: 9 binary detector (one-vs-rest), her detector tsfresh 777-feature uzerinde calisir.")
    out.append("Karar: argmax(P_collective, P_contextual, P_det_trend, P_mean_shift, P_point, P_stoch_trend, P_trend_shift, P_var_shift, P_volatility).\n")
    out.append(f"Toplam {len(df)} seri (synthetic + realdata) test edildi.\n")

    # ---------------- 1. Synthetic accuracy per kind & length -----------
    out.append("---\n\n## 1. Sentetik (betise) Sonuclar - Stochastic Trend tiplere gore\n")
    syn = df[df.source == "synthetic"].copy()
    out.append("Beklenen sinif: `stochastic_trend` (hepsi icin)\n")
    grp = syn.groupby(["kind", "n"]).agg(
        n_series=("name", "count"),
        accuracy=("match", "mean"),
        mean_P_stoch=("P_stochastic_trend", "mean"),
        mean_P_pred=("pred_prob", "mean"),
    ).round(3)
    out.append("| kind | n | seri | accuracy | ort. P(stoch_trend) | ort. P(pred) |")
    out.append("|---|---|---|---|---|---|")
    for (kind, n), row in grp.iterrows():
        out.append(f"| {kind} | {n} | {int(row['n_series'])} | {row['accuracy']:.2%} | {row['mean_P_stoch']:.3f} | {row['mean_P_pred']:.3f} |")

    # Predicted class distribution
    out.append("\n### Tahmin sinifi dagilimi (sentetik):\n")
    pred_dist = syn.groupby(["kind", "n", "pred"]).size().unstack(fill_value=0)
    out.append("```")
    out.append(pred_dist.to_string())
    out.append("```\n")

    # ---------------- 2. Realdata predictions table --------------------
    out.append("---\n\n## 2. realdata Tahminleri\n")
    rd = df[df.source == "realdata"].copy().sort_values("n")
    out.append("Beklenen sinif yok (labeled degil); pipeline'in ne dedigini gosterir.\n")
    out.append("| dosya | n | pred | P(pred) | P(stoch) | P(context) | P(volat) | P(det_trend) |")
    out.append("|---|---|---|---|---|---|---|---|")
    for _, row in rd.iterrows():
        out.append(
            f"| {row['name']} | {int(row['n'])} | {row['pred']} | {row['pred_prob']:.3f} | "
            f"{row['P_stochastic_trend']:.3f} | {row['P_contextual_anomaly']:.3f} | "
            f"{row['P_volatility']:.3f} | {row['P_deterministic_trend']:.3f} |"
        )

    # ---------------- 3. Per-detector probability stats ----------------
    out.append("\n---\n\n## 3. Her Detector'un Ortalama Probability Dagilimi\n")
    out.append("Sentetik (hepsi stoch_trend), realdata ve gruplu ortalamalar.\n")
    out.append("| detector | sentetik ort. | realdata ort. | sentetik max | realdata max |")
    out.append("|---|---|---|---|---|")
    for c in CLASSES:
        pc = f"P_{c}"
        s_mean = syn[pc].mean()
        r_mean = rd[pc].mean()
        s_max = syn[pc].max()
        r_max = rd[pc].max()
        out.append(f"| {c} | {s_mean:.3f} | {r_mean:.3f} | {s_max:.3f} | {r_max:.3f} |")

    # ---------------- 4. Short-series (n <= 100) analysis -------------
    out.append("\n---\n\n## 4. Kisa-seri (n<=100) Performans Analizi\n")
    short = df[(df.n <= 100) & (df.n.notna())].copy()
    out.append(f"Kisa serilerin (n<=100) sayisi: {len(short)}\n")
    out.append("### Sentetik kisa-seri (n=45 vs n=100):\n")
    syn_short = syn[syn.n <= 100]
    a45 = syn_short[syn_short.n == 45]["match"].mean() if len(syn_short[syn_short.n==45]) else None
    a100 = syn_short[syn_short.n == 100]["match"].mean() if len(syn_short[syn_short.n==100]) else None
    out.append(f"- n=45: accuracy={a45:.2%}" if a45 is not None else "- n=45: yok")
    out.append(f"- n=100: accuracy={a100:.2%}" if a100 is not None else "- n=100: yok")

    out.append("\n### Sentetik n=45'te tahmin sinifi dagilimi:\n")
    out.append("```")
    out.append(syn_short[syn_short.n == 45]["pred"].value_counts().to_string())
    out.append("```\n")

    out.append("\n### Sentetik n=100'de tahmin sinifi dagilimi:\n")
    out.append("```")
    out.append(syn_short[syn_short.n == 100]["pred"].value_counts().to_string())
    out.append("```\n")

    # Realdata short
    rd_short = rd[rd.n <= 100]
    out.append(f"\n### realdata kisa (n<=100) tahmin sinifi dagilimi ({len(rd_short)} dosya):\n")
    out.append("```")
    out.append(rd_short["pred"].value_counts().to_string())
    out.append("```\n")

    # W1 specifically
    out.append("\n### W1 (n=45) detayli probability'leri:\n")
    w1 = df[df.name == "W1.csv"]
    if len(w1):
        row = w1.iloc[0]
        out.append("```")
        for c in CLASSES:
            out.append(f"  P_{c:24s} = {row[f'P_{c}']:.4f}")
        out.append(f"\n  ARGMAX -> {row['pred']}  (P={row['pred_prob']:.4f})")
        out.append("```\n")

    # ---------------- 5. Yorum / Observed behavior --------------------
    out.append("\n---\n\n## 5. Gozlemler\n")
    # All-classes prediction across entire dataset
    all_dist = df["pred"].value_counts()
    out.append("Tum verisetinde tahmin sinifi dagilimi:\n```")
    out.append(all_dist.to_string())
    out.append("```\n")

    # Note about model behavior
    out.append("\n### Onemli not\n")
    out.append("- Model neredeyse her seri icin yuksek `P(contextual_anomaly)` veriyor.")
    out.append("- Bu modelin egitim setinde (sentetik 12K seri/sinif, uzunluk 300-500) contextual_anomaly siniflarinin")
    out.append("  cok belirgin (ayrismis) sinyallere sahip oldugunu, gercek/farkli uzunlukta veride yanlis bir sekilde")
    out.append("  bu sinifin tetiklendigini gosteriyor (OOD davranisi).")
    out.append("- Bu nedenle kisa seriler ozelinde, kisa-seri ozellikle sorun degil — model her uzunlukta benzer hata yapiyor.")
    out.append("- `stochastic_trend` detector'u sentetik random-walk/ARIMA serilerinde bile P~0 verdi:")
    out.append("  modelin egitim datasiyla bizim uretti(gimiz daginim arasinda buyuk fark var.")

    # Write file
    out_path = RESULTS_DIR / "RAPOR.md"
    text = "\n".join(out) + "\n"
    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote: {out_path}")
    print(f"  bytes: {out_path.stat().st_size}")


if __name__ == "__main__":
    main()
