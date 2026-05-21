"""
Tum sonuclari tek bir kapsamli README.md'ye yaz.
Icerik:
  1. Proje ozeti + mimari
  2. tsfresh-ensemble-stationary 9-detector sonuclari (her realdata icin)
  3. ens-final 19-vektor (9 eski + 10 yeni) + meta + karar (her realdata icin)
  4. Kisa-seri (n<=100) basarim analizi (iki pipeline icin de)
  5. Ground truth karsilastirma ozeti
  6. Hizli komutlar
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "runner" / "results"

OLD_CLASSES = [
    "collective_anomaly", "contextual_anomaly", "deterministic_trend",
    "mean_shift", "point_anomaly", "stochastic_trend",
    "trend_shift", "variance_shift", "volatility",
]
OLD_ABBR = ["col", "ctx", "det", "ms", "pt", "st", "ts", "vs", "vol"]

NEW_ALL_MODELS = [
    "stationary", "deterministic_trend", "stochastic_trend", "volatility",
    "collective_anomaly", "contextual_anomaly", "mean_shift",
    "point_anomaly", "trend_shift", "variance_shift",
]
NEW_ABBR = ["sta", "det", "stoch", "vol", "col", "ctx", "ms", "pt", "ts", "vs"]

BASE_LABELS = ["stationary", "deterministic_trend", "stochastic_trend", "volatility"]
ANOM_LABELS = ["collective_anomaly", "contextual_anomaly", "mean_shift",
               "point_anomaly", "trend_shift", "variance_shift"]


def load_ensfinal_all():
    """ens-final tahminlerini iki kosudan birlestir."""
    items = []
    for fname in ["ensfinal_realdata.json", "ensfinal_short.json"]:
        p = RESULTS / fname
        if p.exists():
            items.extend(json.load(open(p, encoding="utf-8")))
    return sorted(items, key=lambda r: r["n"])


def load_tsfresh_only():
    """tsfresh-ensemble-stationary tek-pipeline (predictions.csv) realdata satirlari."""
    df = pd.read_csv(RESULTS / "predictions.csv")
    df = df[df["source"] == "realdata"].sort_values("n")
    return df


def fmt_prob(p):
    """0.0000 -> '.00', 0.5718 -> '.57', 0.9999 -> '1.0'"""
    if p is None or pd.isna(p):
        return "  -"
    if p >= 0.995:
        return "1.0"
    if p < 0.005:
        return ".00"
    return f"{p:.2f}".lstrip("0")


def build_readme():
    ens = load_ensfinal_all()
    tsf = load_tsfresh_only()
    gt = pd.read_csv(RESULTS / "label_comparison.csv") if (RESULTS / "label_comparison.csv").exists() else None

    out = []
    out.append("# ts-proje — Time Series Anomali Siniflandirma Pipeline")
    out.append("")
    out.append("Bu repo, **39 davranissal kategoride** zaman serisi siniflandirmasi yapan iki ensemble pipeline'in")
    out.append("kurulumunu, sifirdan egitimini (sadece 390 betise sentetik seri ile) ve gercek-dunya")
    out.append("verilerinin bu pipeline'larda nasil siniflandirildigini iceriyor.")
    out.append("")
    out.append("**GitHub:** https://github.com/KereMath/ts-proje")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Icindekiler")
    out.append("")
    out.append("1. [Proje yapisi](#proje-yapisi)")
    out.append("2. [Iki pipeline mimarisi](#iki-pipeline-mimarisi)")
    out.append("3. [Egitim + 39 grup eval ozeti](#egitim--39-grup-eval-ozeti)")
    out.append("4. [Pipeline-1: tsfresh-ensemble-stationary realdata sonuclari (9 detector)](#pipeline-1-tsfresh-ensemble-stationary-realdata-sonuclari-9-detector)")
    out.append("5. [Pipeline-2: ens-final realdata sonuclari (19-vektor + meta + karar)](#pipeline-2-ens-final-realdata-sonuclari-19-vektor--meta--karar)")
    out.append("6. [Kisa-seri (n<=100) basarim analizi](#kisa-seri-n100-basarim-analizi)")
    out.append("7. [Ground truth karsilastirmasi (Datasets.pdf)](#ground-truth-karsilastirmasi-datasetspdf)")
    out.append("8. [Hizli komutlar](#hizli-komutlar)")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Proje yapisi ----
    out.append("## Proje yapisi")
    out.append("")
    out.append("```")
    out.append("ceylanhoca/")
    out.append("|-- betise/                       # sentetik veri ureticisi")
    out.append("|-- realdata/                     # 41 ham gercek seri")
    out.append("|-- Auto_Feature_ML/              # referans (Auto Feature ML No Window 12K)")
    out.append("|-- tsfresh-ensemble-stationary/  # ESKI ensemble: 9 binary detector (pre-trained)")
    out.append("|-- ensemble-alldata/             # YENI ensemble: 10 binary (BIZIM egittik)")
    out.append("|-- stationary-detection-ml/      # Stationary detector: 21 feature GradientBoosting")
    out.append("|-- ens-final/                    # Meta-stacking orkestratoru (BIZIM egittik)")
    out.append("|-- runner/                       # bizim yazdigimiz tum scriptler")
    out.append("|   |-- data/")
    out.append("|   |   |-- synthetic/            # 50 betise serisi (stochastic-trend, n=45 ve n=100)")
    out.append("|   |   |-- realdata/             # 41 dosya tek-kolon CSV")
    out.append("|   |   `-- generated/            # 390 betise serisi (39 grup × 10)")
    out.append("|   `-- results/                  # raporlar ve JSON ciktilari")
    out.append("|-- NIHAI_RAPOR.md")
    out.append("|-- Datasets.pdf / Datasets.docx  # realdata kaynaklari + ground truth")
    out.append("`-- plan.md")
    out.append("```")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Mimari ----
    out.append("## Iki pipeline mimarisi")
    out.append("")
    out.append("### Pipeline-1: `tsfresh-ensemble-stationary` (tek-katmanli eski ensemble)")
    out.append("- Ham seri -> tsfresh `EfficientFCParameters` -> **777 feature**")
    out.append("- **9 binary detector** (one-vs-rest, her sinif icin XGBoost/LightGBM/MLP'den en iyisi)")
    out.append("- Karar: argmax(P)")
    out.append("- Egitim: orijinal repoda **12K seri/sinif** (uzunluk 300-500)")
    out.append("")
    out.append("### Pipeline-2: `ens-final` (7-asamali hiyerarsik stacking)")
    out.append("Ham seri -> tsfresh 777 feature -> ardarda:")
    out.append("1. **Stationarity gate** — 21 ozel feature, GradientBoosting -> P(stationary)")
    out.append("2. **Eski ensemble** — 9 binary -> 9 olasilik (yukaridaki pipeline-1)")
    out.append("3. **Yeni ensemble** — 10 binary (4 base + 6 anomali) -> 10 olasilik (BIZIM egittik, 390 seri)")
    out.append("4. **14 turetilmis meta-feature** + 777 standardized tsfresh = **810 boyutlu meta-vektor**")
    out.append("5. **Router** — XGB+LGB ensemble -> P(combo vs single)")
    out.append("6. **Base type meta-learner** — 4-class XGB+LGB -> base argmax")
    out.append("7. **6 anomali meta-learner** + per-anomali (alpha, threshold) blend")
    out.append("")
    out.append("Karar mantigi: stationarity gate (>=0.92) -> stationary; router (<0.30) -> single base only;")
    out.append("yoksa combo dali (base + blended anomali listesi).")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Egitim ozeti ----
    out.append("## Egitim + 39 grup eval ozeti")
    out.append("")
    out.append("- **Sentetik veri uretildi:** betise ile 39 grup × 10 seri = **390 seri** (uzunluk [80, 150])")
    out.append("- **ensemble-alldata egitildi** (N=60): 10 binary model, ortalama Test F1 = 0.852")
    out.append("- **ens-final meta-learner'lar egitildi** (META_N_PER_GROUP=8, 312 ornek)")
    out.append("- **39 grup degerlendirme** (egitim seti uzerinde, samples_per_leaf=10):")
    out.append("")
    out.append("| Metric | Sayi | Yuzde |")
    out.append("|---|---|---|")
    out.append("| **FULL match** | **344 / 390** | **%88.21** |")
    out.append("| PARTIAL | 41 | %10.51 |")
    out.append("| NONE | 5 | %1.28 |")
    out.append("")
    out.append("Orijinal raporda raporlanan tavan **%89.07** (19500 egitim + 4400 eval ile). Bizim 390 seri ile farka **<%1**.")
    out.append("")
    out.append("Detay: [ens-final/results/evaluation_report.md](ens-final/results/evaluation_report.md)")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Pipeline-1: tsfresh-ensemble-stationary realdata 9-detector ----
    out.append("## Pipeline-1: tsfresh-ensemble-stationary realdata sonuclari (9 detector)")
    out.append("")
    out.append("Her satir bir realdata dosyasi. 9 binary detector'un `P(class=1)` olasiligi.")
    out.append("Kisaltma: col=collective, ctx=contextual, det=deterministic_trend, ms=mean_shift, pt=point,")
    out.append("st=stochastic_trend, ts=trend_shift, vs=variance_shift, vol=volatility.")
    out.append("**ARG** sutunu = argmax karar (modelin sectigi sinif).")
    out.append("")
    header = "| dosya | n | " + " | ".join(OLD_ABBR) + " | **ARG** |"
    sep = "|---|---|" + "|".join(["---"] * 9) + "|---|"
    out.append(header)
    out.append(sep)
    for _, row in tsf.iterrows():
        cells = " | ".join(fmt_prob(row[f"P_{c}"]) for c in OLD_CLASSES)
        out.append(f"| {row['name']} | {row['n']} | {cells} | **{row['pred'][:8]}** |")
    out.append("")
    out.append("**Gozlem:** 39 dosyadan 37'si `contextual_anomaly` olarak siniflandirildi. Eski modelin OOD bias'i bariz.")
    out.append("")
    out.append("Detayli: [runner/results/predictions.csv](runner/results/predictions.csv) (90 seri × 9 olasilik)")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Pipeline-2: ens-final full 19+ vector ----
    out.append("## Pipeline-2: ens-final realdata sonuclari (19-vektor + meta + karar)")
    out.append("")
    out.append("Her satir bir realdata dosyasi. Kolonlar:")
    out.append("- **9 eski ensemble** (Pipeline-1'in ayni 9 detector probability'si)")
    out.append("- **10 yeni ensemble** (bizim egittigimiz 4 base + 6 anomali)")
    out.append("- **4 base meta-learner softmax** (stationary/det_trend/stoch_trend/volatility)")
    out.append("- **6 anomali meta-learner P** (collective/contextual/mean/point/trend_shift/variance)")
    out.append("- **P(stat)** = stationarity gate, **P(comb)** = router combo prob")
    out.append("- **Karar** = (base, anomali listesi)")
    out.append("")
    out.append("### 19 ham probability (9 eski + 10 yeni)")
    out.append("")
    header = ("| dosya | n | " +
              " | ".join("o_" + a for a in OLD_ABBR) + " | " +
              " | ".join("n_" + a for a in NEW_ABBR) + " |")
    sep = "|---|---|" + "|".join(["---"] * 19) + "|"
    out.append(header)
    out.append(sep)
    for r in ens:
        old_cells = " | ".join(fmt_prob(r["old_probs"][c]) for c in OLD_CLASSES)
        new_cells = " | ".join(fmt_prob(r["new_probs"][c]) for c in NEW_ALL_MODELS)
        out.append(f"| {r['name']} | {r['n']} | {old_cells} | {new_cells} |")
    out.append("")
    out.append("### Meta-learner + karar")
    out.append("")
    out.append("Kisaltma: base_st=P(stationary), base_dt=P(det_trend), base_str=P(stoch_trend), base_vol=P(volatility).")
    out.append("a_*: 6 anomali meta P. **path** = stat_gate/single/combo. **anom**: tetiklenen anomaliler.")
    out.append("")
    base_abbr = ["b_st", "b_dt", "b_str", "b_vol"]
    anom_abbr = ["a_col", "a_ctx", "a_ms", "a_pt", "a_ts", "a_vs"]
    header = ("| dosya | n | " + " | ".join(base_abbr) + " | " +
              " | ".join(anom_abbr) + " | P(stat) | P(comb) | path | base | anom |")
    sep = "|---|---|" + "|".join(["---"] * 12) + "|---|---|---|---|---|"
    out.append(header)
    out.append(sep)
    for r in ens:
        base_cells = " | ".join(fmt_prob(r["base_probs"][b]) for b in BASE_LABELS)
        anom_cells = " | ".join(fmt_prob(r["anom_probs"][a]) for a in ANOM_LABELS)
        triggered = ", ".join(a[:3] for a in r["pred_anoms"]) if r["pred_anoms"] else "-"
        out.append(
            f"| {r['name']} | {r['n']} | {base_cells} | {anom_cells} | "
            f"{fmt_prob(r['stat_prob'])} | {fmt_prob(r['router_combo_prob'])} | "
            f"{r['decision_path']} | **{r['pred_base'][:8]}** | {triggered} |"
        )
    out.append("")
    out.append("**Gozlem:**")
    out.append("- 37/37 dosya `combo` yoluna gitti. Stationarity gate hicbirinde acilmadi (>=0.92 esigi cok yuksek).")
    out.append("- Yeni ensemble (n_sta, n_str vs.) eski'nin contextual bias'ini cok daha iyi yonetiyor.")
    out.append("- Stationary olmasi gereken bircok dosyada base meta 'stationary' diyor ama anomali kolu over-fire.")
    out.append("")
    out.append("Detayli JSON (her dosya icin 31 probability):")
    out.append("- [runner/results/ensfinal_realdata.json](runner/results/ensfinal_realdata.json) (n>=50, 32 dosya)")
    out.append("- [runner/results/ensfinal_short.json](runner/results/ensfinal_short.json) (20<=n<50, 5 dosya — W1 dahil)")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Short-series analysis ----
    out.append("## Kisa-seri (n<=100) basarim analizi")
    out.append("")
    out.append("Plan.md'deki ana soru: 'algoritmanin kisa seriler ozelinde basarimi nasil, hem ts-ensemble hem ens-final icin?'")
    out.append("")
    out.append("### Pipeline-1 (tsfresh-ensemble-stationary)")
    out.append("")
    out.append("**Sentetik kisa stochastic-trend serileri** (5 tip × 2 uzunluk × 5 seri):")
    out.append("")
    out.append("| Sentetik tipi | n | accuracy | ort P(stoch_trend) | Tahmin (hep) |")
    out.append("|---|---|---|---|---|")
    out.append("| rw | 45 | %0 | 0.001 | contextual_anomaly |")
    out.append("| rw | 100 | %0 | 0.010 | contextual_anomaly |")
    out.append("| rwd | 45 | %0 | 0.001 | contextual_anomaly |")
    out.append("| rwd | 100 | %0 | 0.003 | contextual_anomaly |")
    out.append("| ari | 45 | %0 | 0.004 | contextual_anomaly |")
    out.append("| ari | 100 | %0 | 0.007 | contextual_anomaly |")
    out.append("| ima | 45 | %0 | 0.016 | contextual_anomaly |")
    out.append("| ima | 100 | %0 | 0.024 | contextual_anomaly |")
    out.append("| arima | 45 | %0 | 0.006 | contextual_anomaly |")
    out.append("| arima | 100 | %0 | 0.002 | contextual_anomaly |")
    out.append("")
    out.append("**Sonuc:** n=45'te de n=100'de de %0 dogru. Sorun **kisa uzunluk DEGIL**, modelin OOD bias'i.")
    out.append("Saf white noise N(0,1) bile P(contextual)=0.9995 veriyor.")
    out.append("")
    out.append("**realdata kisa seriler** (n<=100): 23 dosya, 21'i contextual_anomaly, 2'si deterministic_trend.")
    out.append("")
    out.append("### Pipeline-2 (ens-final)")
    out.append("")
    out.append("Ens-final MIN_SERIES_LENGTH=50 (default). Dolayisiyla:")
    out.append("- n>=50 olan 32 realdata dosyasi normal pipeline'a girdi")
    out.append("- 20<=n<50 olan 5 dosya (W1, uspop, strikes, W15-1, W15-2) ozel scriptle (`runner/21_ensfinal_short_realdata.py`) pipeline'a sokuldu")
    out.append("- n<20 olan 4 dosya (W9, W10, W16, rec_dataframe) tsfresh stabilite riski sebebiyle atlandi")
    out.append("")
    out.append("**Kisa realdata (n<=100) ens-final tahminleri:**")
    out.append("")
    out.append("| dosya | n | base | anomaliler | path | P(stat) | P(combo) |")
    out.append("|---|---|---|---|---|---|---|")
    short_ens = sorted([r for r in ens if r["n"] <= 100], key=lambda x: x["n"])
    for r in short_ens:
        anoms = ", ".join(r["pred_anoms"]) if r["pred_anoms"] else "-"
        out.append(
            f"| {r['name']} | {r['n']} | {r['pred_base']} | {anoms} | "
            f"{r['decision_path']} | {fmt_prob(r['stat_prob'])} | {fmt_prob(r['router_combo_prob'])} |"
        )
    out.append("")
    out.append("**Sonuc:**")
    out.append("- Pipeline-1'in aksine pipeline-2 farkli base tipleri ayirt edebiliyor (deterministic_trend, stochastic_trend, stationary, volatility).")
    out.append("- W15-1 ve W15-2'de P(stat) yuksek (0.82-0.84) ama 0.92 esigi gecmedi -> combo'ya yonlendirildi.")
    out.append("- Sentetik egitim seti uzunluk [80, 150] araliginda; n=21 (uspop), n=30 (strikes), n=45-46 gibi kisa seriler aslinda egitim distribution disinda -> bu da OOD.")
    out.append("- ens-final 39-grup egitim setinde stationary grup 1 (uzunluk 80-150) icin %70 FULL, ama gercek kisa stationary seriler (W1, strikes) icin anomali over-fire mevcut.")
    out.append("")
    out.append("**Iki pipeline karsilastirmasi (W1 ornegi, n=45):**")
    out.append("")
    out.append("| Pipeline | W1 tahmini | Yorum |")
    out.append("|---|---|---|")
    out.append("| Pipeline-1 (sadece eski 9 detector) | `contextual_anomaly` (P=0.57) | bias |")
    out.append("| Pipeline-2 (ens-final tam stack) | `stochastic_trend` + `collective`, `variance_shift` | meta override etti, base degisti |")
    out.append("| **PDF Ground Truth** | **`stationary`** + point_anomaly | Wei: AO/IO at t=4,7,9,36 |")
    out.append("")
    out.append("Yani Pipeline-2 Pipeline-1'in contextual bias'ini override etti, **ama PDF'teki dogru cevaba** (stationary) ulasamadi.")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Ground truth comparison ----
    out.append("## Ground truth karsilastirmasi (Datasets.pdf)")
    out.append("")
    out.append("`Datasets.pdf` (Wei, Brockwell, Lutkepohl, Shumway & Stoffer, Bai-Perron kaynaklarindan) **21 realdata dosyasi** icin")
    out.append("acik etiketler veriyor.")
    out.append("")
    if gt is not None:
        counts = gt["match"].value_counts().to_dict()
        out.append("**Ozet:**")
        out.append("")
        out.append("| Match | Sayi |")
        out.append("|---|---|")
        for mt in ["FULL", "PARTIAL", "NONE", "MISSING"]:
            out.append(f"| {mt} | {counts.get(mt, 0)} |")
        out.append("")
        base_correct = sum(1 for _, r in gt.iterrows() if r["base_ok"])
        not_missing = len(gt[gt["match"] != "MISSING"])
        out.append(f"**Base type dogru: {base_correct} / {not_missing}** (MISSING haric)")
        out.append("")
        # Stationary highlight
        stat_files = gt[gt["gt_base"] == "stationary"]
        out.append("**Kesin stationary oldugu PDF'te belirtilen dosyalar:**")
        out.append("")
        out.append("| dosya | n | kaynak | model base | base✓ |")
        out.append("|---|---|---|---|---|")
        for _, r in stat_files.iterrows():
            mark = "✓" if r["base_ok"] else "✗"
            out.append(f"| {r['file']} | {r['n']} | {r['source']} | {r['pred_base']} | {mark} |")
        out.append("")
    out.append("Tam karsilastirma: [runner/results/LABEL_KARSILASTIRMA.md](runner/results/LABEL_KARSILASTIRMA.md)")
    out.append("")
    out.append("**Ana bulgular:**")
    out.append("- **0 FULL match** — anomali tarafi tamamen over-fire ediyor")
    out.append("- Base type **8 / 19** (~%42) dogru — DAX returns, US_investment gibi finansal/ekonomik stationary dosyalari dogru tanindi")
    out.append("- Sezonsallik kategorisi eksikligi: airpass, INDPRO, UNRATE, deaths (hepsi seasonal+stoch) -> deterministic_trend deniyor")
    out.append("- W1 (stationary+point) yanlis: hem base hem anomali tutmuyor")
    out.append("")
    out.append("---")
    out.append("")

    # ---- Reproducibility ----
    out.append("## Hizli komutlar")
    out.append("")
    out.append("```powershell")
    out.append("# Bagimliliklar")
    out.append("pip install numpy pandas tsfresh scikit-learn lightgbm xgboost statsmodels arch scipy joblib")
    out.append("")
    out.append("# 1. Sentetik veri (390 seri, 39 grup × 10)")
    out.append("python runner/10_generate_39groups.py")
    out.append("")
    out.append("# 2. Yeni ensemble (10 binary model) egitimi")
    out.append("cd ensemble-alldata; python main.py; cd ..")
    out.append("")
    out.append("# 3. ens-final meta-learner + 39 grup eval")
    out.append("cd ens-final; python main.py --force; cd ..")
    out.append("")
    out.append("# 4. realdata ens-final pipeline")
    out.append("python runner/20_ensfinal_realdata.py        # n>=50")
    out.append("python runner/21_ensfinal_short_realdata.py  # 20<=n<50 (W1 dahil)")
    out.append("")
    out.append("# 5. Pipeline-1 (tsfresh-ensemble-stationary tek basina)")
    out.append("python runner/01_generate_synthetic.py")
    out.append("python runner/02_convert_realdata.py")
    out.append("python runner/03_run_pipeline.py")
    out.append("python runner/04_build_report.py")
    out.append("")
    out.append("# 6. Ground truth karsilastirma")
    out.append("python runner/30_compare_labels.py")
    out.append("")
    out.append("# 7. Bu README'yi yeniden uret")
    out.append("python runner/40_build_readme.py")
    out.append("```")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Daha fazla detay")
    out.append("")
    out.append("- [NIHAI_RAPOR.md](NIHAI_RAPOR.md) — Tum yapilanlarin kronolojik raporu")
    out.append("- [plan.md](plan.md) — Hocadan gelen orijinal plan")
    out.append("- [Datasets.pdf](Datasets.pdf) — realdata kaynaklari + ground truth")
    out.append("- [runner/results/RAPOR.md](runner/results/RAPOR.md) — Pipeline-1 detayli rapor")
    out.append("- [runner/results/ENSFINAL_REALDATA_RAPOR.md](runner/results/ENSFINAL_REALDATA_RAPOR.md) — Pipeline-2 detayli rapor")
    out.append("- [runner/results/ENSFINAL_SHORT_RAPOR.md](runner/results/ENSFINAL_SHORT_RAPOR.md) — W1 + kisa seriler ens-final raporu")
    out.append("- [runner/results/LABEL_KARSILASTIRMA.md](runner/results/LABEL_KARSILASTIRMA.md) — Ground truth karsilastirma")
    out.append("- [ens-final/results/evaluation_report.md](ens-final/results/evaluation_report.md) — 39 grup eval")
    out.append("")

    text = "\n".join(out) + "\n"
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"README.md yazildi: {ROOT / 'README.md'}")
    print(f"Boyut: {len(text):,} karakter, {text.count(chr(10)):,} satir")


if __name__ == "__main__":
    build_readme()
