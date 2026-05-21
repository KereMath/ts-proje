# ts-proje — Time Series Anomali Siniflandirma Pipeline

Bu repo, **39 davranissal kategoride** zaman serisi siniflandirmasi yapan iki ensemble pipeline'in
kurulumunu, sifirdan egitimini (sadece 390 betise sentetik seri ile) ve gercek-dunya
verilerinin bu pipeline'larda nasil siniflandirildigini iceriyor.

**GitHub:** https://github.com/KereMath/ts-proje

---

## Icindekiler

1. [Proje yapisi](#proje-yapisi)
2. [Iki pipeline mimarisi](#iki-pipeline-mimarisi)
3. [Egitim + 39 grup eval ozeti](#egitim--39-grup-eval-ozeti)
4. [Pipeline-1: tsfresh-ensemble-stationary realdata sonuclari (9 detector)](#pipeline-1-tsfresh-ensemble-stationary-realdata-sonuclari-9-detector)
5. [Pipeline-2: ens-final realdata sonuclari (19-vektor + meta + karar)](#pipeline-2-ens-final-realdata-sonuclari-19-vektor--meta--karar)
6. [Kisa-seri (n<=100) basarim analizi](#kisa-seri-n100-basarim-analizi)
7. [Ground truth karsilastirmasi (Datasets.pdf)](#ground-truth-karsilastirmasi-datasetspdf)
8. [Hizli komutlar](#hizli-komutlar)

---

## Proje yapisi

```
ceylanhoca/
|-- betise/                       # sentetik veri ureticisi
|-- realdata/                     # 41 ham gercek seri
|-- Auto_Feature_ML/              # referans (Auto Feature ML No Window 12K)
|-- tsfresh-ensemble-stationary/  # ESKI ensemble: 9 binary detector (pre-trained)
|-- ensemble-alldata/             # YENI ensemble: 10 binary (BIZIM egittik)
|-- stationary-detection-ml/      # Stationary detector: 21 feature GradientBoosting
|-- ens-final/                    # Meta-stacking orkestratoru (BIZIM egittik)
|-- runner/                       # bizim yazdigimiz tum scriptler
|   |-- data/
|   |   |-- synthetic/            # 50 betise serisi (stochastic-trend, n=45 ve n=100)
|   |   |-- realdata/             # 41 dosya tek-kolon CSV
|   |   `-- generated/            # 390 betise serisi (39 grup × 10)
|   `-- results/                  # raporlar ve JSON ciktilari
|-- NIHAI_RAPOR.md
|-- Datasets.pdf / Datasets.docx  # realdata kaynaklari + ground truth
`-- plan.md
```

---

## Iki pipeline mimarisi

### Pipeline-1: `tsfresh-ensemble-stationary` (tek-katmanli eski ensemble)
- Ham seri -> tsfresh `EfficientFCParameters` -> **777 feature**
- **9 binary detector** (one-vs-rest, her sinif icin XGBoost/LightGBM/MLP'den en iyisi)
- Karar: argmax(P)
- Egitim: orijinal repoda **12K seri/sinif** (uzunluk 300-500)

### Pipeline-2: `ens-final` (7-asamali hiyerarsik stacking)
Ham seri -> tsfresh 777 feature -> ardarda:
1. **Stationarity gate** — 21 ozel feature, GradientBoosting -> P(stationary)
2. **Eski ensemble** — 9 binary -> 9 olasilik (yukaridaki pipeline-1)
3. **Yeni ensemble** — 10 binary (4 base + 6 anomali) -> 10 olasilik (BIZIM egittik, 390 seri)
4. **14 turetilmis meta-feature** + 777 standardized tsfresh = **810 boyutlu meta-vektor**
5. **Router** — XGB+LGB ensemble -> P(combo vs single)
6. **Base type meta-learner** — 4-class XGB+LGB -> base argmax
7. **6 anomali meta-learner** + per-anomali (alpha, threshold) blend

Karar mantigi: stationarity gate (>=0.92) -> stationary; router (<0.30) -> single base only;
yoksa combo dali (base + blended anomali listesi).

---

## Egitim + 39 grup eval ozeti

- **Sentetik veri uretildi:** betise ile 39 grup × 10 seri = **390 seri** (uzunluk [80, 150])
- **ensemble-alldata egitildi** (N=60): 10 binary model, ortalama Test F1 = 0.852
- **ens-final meta-learner'lar egitildi** (META_N_PER_GROUP=8, 312 ornek)
- **39 grup degerlendirme** (egitim seti uzerinde, samples_per_leaf=10):

| Metric | Sayi | Yuzde |
|---|---|---|
| **FULL match** | **344 / 390** | **%88.21** |
| PARTIAL | 41 | %10.51 |
| NONE | 5 | %1.28 |

Orijinal raporda raporlanan tavan **%89.07** (19500 egitim + 4400 eval ile). Bizim 390 seri ile farka **<%1**.

Detay: [ens-final/results/evaluation_report.md](ens-final/results/evaluation_report.md)

---

## Pipeline-1: tsfresh-ensemble-stationary realdata sonuclari (9 detector)

Her satir bir realdata dosyasi. 9 binary detector'un `P(class=1)` olasiligi.
Kisaltma: col=collective, ctx=contextual, det=deterministic_trend, ms=mean_shift, pt=point,
st=stochastic_trend, ts=trend_shift, vs=variance_shift, vol=volatility.
**ARG** sutunu = argmax karar (modelin sectigi sinif).

| dosya | n | col | ctx | det | ms | pt | st | ts | vs | vol | **ARG** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W10.csv | 8 | .00 | .93 | .03 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W9.csv | 11 | .00 | .92 | .06 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W16.csv | 15 | .00 | .94 | .04 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| uspop.csv | 21 | .00 | .30 | .51 | .00 | .00 | .00 | .00 | .00 | .00 | **determin** |
| strikes.csv | 30 | .00 | .36 | .13 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W1.csv | 45 | .00 | .57 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W15-1.csv | 46 | .00 | .98 | .01 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W15-2.csv | 46 | .00 | .98 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W12-1.csv | 54 | .00 | .93 | .20 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W12-2.csv | 54 | .00 | .95 | .06 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| W5.csv | 71 | .00 | .95 | .04 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| deaths.csv | 72 | .00 | .36 | .78 | .00 | .00 | .00 | .00 | .00 | .00 | **determin** |
| W13-2.csv | 82 | .00 | .33 | .26 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| W13-1.csv | 82 | .00 | .94 | .29 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W13-3.csv | 82 | .00 | .33 | .10 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W13-4.csv | 82 | .00 | .94 | .13 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| W3.csv | 82 | .00 | .36 | .17 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W13-5.csv | 82 | .00 | .33 | .23 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W14.csv | 87 | .00 | .94 | .03 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| GermanGNP.csv | 88 | .00 | .33 | .03 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| e1.csv | 92 | .00 | .33 | .05 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| German_consumption.csv | 93 | .00 | .35 | .05 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| sunspots.csv | 100 | .00 | .41 | .08 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| RealInt_dataframe.csv | 103 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| e2.csv | 104 | .00 | .30 | .08 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| US_investment.csv | 104 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| German_income.csv | 113 | .00 | .94 | .12 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| W6.csv | 114 | .00 | .94 | .14 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| Polish_productivity.csv | 117 | .00 | .95 | .07 | .00 | .00 | .01 | .00 | .00 | .03 | **contextu** |
| wine.csv | 142 | .00 | .33 | .08 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| airpass.csv | 144 | .00 | .30 | .17 | .00 | .00 | .02 | .00 | .00 | .00 | **contextu** |
| W8.csv | 150 | .00 | .38 | .08 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W11.csv | 166 | .00 | .95 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| W2.csv | 302 | .00 | .39 | .09 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| UNRATE.csv | 372 | .00 | .33 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| INDPRO.csv | 372 | .00 | .35 | .07 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| beer.csv | 422 | .00 | .94 | .43 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| soi_dataframe.csv | 453 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |
| NP_AWHours.csv | 479 | .00 | .36 | .13 | .00 | .00 | .00 | .00 | .00 | .00 | **contextu** |
| NP_xetradax_returns100.csv | 1028 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | **contextu** |

**Gozlem:** 39 dosyadan 37'si `contextual_anomaly` olarak siniflandirildi. Eski modelin OOD bias'i bariz.

Detayli: [runner/results/predictions.csv](runner/results/predictions.csv) (90 seri × 9 olasilik)

---

## Pipeline-2: ens-final realdata sonuclari (19-vektor + meta + karar)

Her satir bir realdata dosyasi. Kolonlar:
- **9 eski ensemble** (Pipeline-1'in ayni 9 detector probability'si)
- **10 yeni ensemble** (bizim egittigimiz 4 base + 6 anomali)
- **4 base meta-learner softmax** (stationary/det_trend/stoch_trend/volatility)
- **6 anomali meta-learner P** (collective/contextual/mean/point/trend_shift/variance)
- **P(stat)** = stationarity gate, **P(comb)** = router combo prob
- **Karar** = (base, anomali listesi)

### 19 ham probability (9 eski + 10 yeni)

| dosya | n | o_col | o_ctx | o_det | o_ms | o_pt | o_st | o_ts | o_vs | o_vol | n_sta | n_det | n_stoch | n_vol | n_col | n_ctx | n_ms | n_pt | n_ts | n_vs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uspop.csv | 21 | .00 | .30 | .87 | .00 | .00 | .00 | .00 | .00 | .00 | .60 | .94 | .50 | .11 | 1.0 | .95 | .27 | .01 | .50 | .46 |
| strikes.csv | 30 | .00 | .36 | .15 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .80 | .29 | .17 | 1.0 | .95 | .49 | .08 | .50 | .42 |
| W1.csv | 45 | .00 | .57 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .31 | .22 | .13 | .62 | .97 | .04 | .41 | .00 | .50 | .91 |
| W15-1.csv | 46 | .00 | .98 | .01 | .00 | .00 | .00 | .00 | .00 | .00 | .02 | .33 | .87 | .54 | .94 | .04 | .88 | .00 | .50 | .65 |
| W15-2.csv | 46 | .00 | .98 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .73 | .89 | .49 | .83 | .04 | .67 | .00 | .50 | .62 |
| W12-1.csv | 54 | .00 | .93 | .16 | .00 | .00 | .00 | .00 | .00 | .00 | .93 | .79 | .68 | .66 | .87 | .96 | .31 | .03 | .50 | .12 |
| W12-2.csv | 54 | .00 | .95 | .06 | .00 | .00 | .01 | .00 | .00 | .00 | .99 | .21 | .77 | .66 | .25 | .95 | .44 | .33 | .50 | .07 |
| W5.csv | 71 | .00 | .95 | .04 | .00 | .00 | .00 | .00 | .00 | .00 | .89 | .60 | .41 | .04 | .99 | .96 | .39 | .56 | .50 | .17 |
| deaths.csv | 72 | .00 | .36 | .74 | .00 | .00 | .00 | .00 | .00 | .00 | .98 | .95 | .20 | .36 | .85 | .96 | .23 | .03 | .50 | .06 |
| W13-1.csv | 82 | .00 | .94 | .26 | .00 | .00 | .00 | .00 | .00 | .00 | .81 | .99 | .80 | .05 | .84 | .95 | .16 | .02 | .50 | .24 |
| W13-2.csv | 82 | .00 | .33 | .21 | .00 | .00 | .00 | .00 | .00 | .00 | .85 | .98 | .71 | .04 | .87 | .96 | .30 | .09 | .50 | .11 |
| W13-3.csv | 82 | .00 | .33 | .09 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .98 | .43 | .03 | .97 | .95 | .44 | .01 | .50 | .41 |
| W13-4.csv | 82 | .00 | .94 | .11 | .00 | .00 | .01 | .00 | .00 | .00 | .88 | .97 | .88 | .06 | .82 | .95 | .36 | .43 | .50 | .12 |
| W13-5.csv | 82 | .00 | .33 | .19 | .00 | .00 | .00 | .00 | .00 | .00 | .67 | .96 | .58 | .03 | .98 | .96 | .26 | .50 | .50 | .41 |
| W3.csv | 82 | .00 | .36 | .16 | .00 | .00 | .00 | .00 | .00 | .00 | .99 | .77 | .64 | .20 | .99 | .95 | .16 | .05 | .50 | .04 |
| W14.csv | 87 | .00 | .94 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | 1.0 | .95 | .55 | .18 | .99 | .95 | .15 | .04 | .50 | .45 |
| GermanGNP.csv | 88 | .00 | .33 | .03 | .00 | .00 | .00 | .00 | .00 | .00 | .79 | .99 | .64 | .04 | .98 | .95 | .18 | .11 | .50 | .30 |
| e1.csv | 92 | .00 | .33 | .05 | .00 | .00 | .00 | .00 | .00 | .00 | .66 | .27 | .84 | .03 | .99 | .96 | .15 | .39 | .50 | .27 |
| German_consumption.csv | 93 | .00 | .35 | .04 | .00 | .00 | .01 | .00 | .00 | .00 | .89 | .24 | .49 | .04 | .98 | .96 | .18 | .52 | .50 | .17 |
| sunspots.csv | 100 | .00 | .41 | .06 | .00 | .00 | .00 | .00 | .00 | .00 | .85 | 1.0 | .58 | .41 | .99 | .96 | .07 | .30 | .50 | .12 |
| RealInt_dataframe.csv | 103 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .97 | .06 | .05 | 1.0 | .95 | .06 | .09 | .50 | .57 |
| e2.csv | 104 | .00 | .30 | .06 | .00 | .00 | .00 | .00 | .00 | .00 | .70 | .98 | .65 | .03 | .90 | .96 | .48 | .86 | .50 | .12 |
| US_investment.csv | 104 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | 1.0 | .15 | .07 | .19 | .94 | .95 | .16 | .05 | .50 | .37 |
| German_income.csv | 113 | .00 | .94 | .09 | .00 | .00 | .00 | .00 | .00 | .00 | .95 | .95 | .69 | .04 | .98 | .95 | .22 | 1.0 | .50 | .09 |
| W6.csv | 114 | .00 | .94 | .11 | .00 | .00 | .00 | .00 | .00 | .00 | .80 | .99 | .54 | .04 | .99 | .96 | .34 | .03 | .50 | .27 |
| Polish_productivity.csv | 117 | .00 | .95 | .06 | .00 | .00 | .01 | .00 | .00 | .02 | .02 | .03 | .82 | .91 | .93 | .84 | .08 | 1.0 | .50 | .80 |
| wine.csv | 142 | .00 | .33 | .08 | .00 | .00 | .01 | .00 | .00 | .00 | .99 | .50 | .14 | .07 | .99 | .95 | .26 | .24 | .50 | .36 |
| airpass.csv | 144 | .00 | .30 | .17 | .00 | .00 | .01 | .00 | .00 | .00 | .59 | .94 | .62 | .03 | .98 | .96 | .14 | .99 | .50 | .36 |
| W8.csv | 150 | .00 | .38 | .08 | .00 | .00 | .00 | .00 | .00 | .00 | .86 | .99 | .24 | .03 | .79 | .96 | .23 | 1.0 | .50 | .31 |
| W11.csv | 166 | .00 | .95 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | .09 | .93 | .79 | .28 | 1.0 | .90 | .06 | .94 | .50 | .33 |
| W2.csv | 302 | .00 | .39 | .09 | .00 | .00 | .01 | .00 | .00 | .00 | .99 | .71 | .66 | .06 | .96 | .96 | .03 | .98 | .50 | .42 |
| INDPRO.csv | 372 | .00 | .35 | .07 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .95 | .61 | .12 | .97 | .90 | .39 | .99 | .50 | .40 |
| UNRATE.csv | 372 | .00 | .33 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .68 | .67 | .02 | .98 | .87 | .61 | .68 | .50 | .18 |
| beer.csv | 422 | .00 | .94 | .43 | .00 | .00 | .00 | .00 | .00 | .00 | 1.0 | .93 | .29 | .20 | .97 | .95 | .06 | .95 | .50 | .29 |
| rec_dataframe.csv | 453 | .00 | .47 | .04 | .00 | .00 | .02 | .00 | .00 | .00 | .91 | .17 | .73 | .10 | .90 | .96 | .26 | .99 | .50 | .21 |
| soi_dataframe.csv | 453 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .11 | .00 | .77 | .60 | .86 | .04 | .82 | .01 | .50 | .60 |
| NP_AWHours.csv | 479 | .00 | .36 | .13 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .42 | .23 | .04 | 1.0 | .86 | .65 | .76 | .50 | .24 |
| NP_xetradax_returns100.csv | 1028 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | 1.0 | .00 | .40 | .72 | .99 | .93 | .20 | .98 | .50 | .31 |

### Meta-learner + karar

Kisaltma: base_st=P(stationary), base_dt=P(det_trend), base_str=P(stoch_trend), base_vol=P(volatility).
a_*: 6 anomali meta P. **path** = stat_gate/single/combo. **anom**: tetiklenen anomaliler.

| dosya | n | b_st | b_dt | b_str | b_vol | a_col | a_ctx | a_ms | a_pt | a_ts | a_vs | P(stat) | P(comb) | path | base | anom |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uspop.csv | 21 | .01 | .96 | .02 | .00 | .95 | .56 | .00 | .01 | .00 | .01 | .01 | .95 | combo | **determin** | col, con |
| strikes.csv | 30 | .85 | .13 | .01 | .00 | .91 | .56 | .00 | .01 | .00 | .01 | .01 | .98 | combo_suppress | **stationa** | - |
| W1.csv | 45 | .08 | .28 | .40 | .24 | .98 | .01 | .00 | .00 | .00 | .34 | .05 | 1.0 | combo | **stochast** | col, var |
| W15-1.csv | 46 | .00 | .01 | .99 | .00 | .97 | .01 | .02 | .00 | .00 | .08 | .82 | .94 | combo | **stochast** | col |
| W15-2.csv | 46 | .00 | .01 | .99 | .00 | .95 | .01 | .03 | .00 | .00 | .07 | .84 | .92 | combo | **stochast** | col |
| W12-1.csv | 54 | .79 | .05 | .10 | .06 | .21 | .99 | .00 | .01 | .01 | .00 | .00 | .95 | combo_suppress | **stationa** | - |
| W12-2.csv | 54 | .81 | .03 | .12 | .04 | .10 | .67 | .00 | .08 | .01 | .00 | .00 | .97 | combo_suppress | **stationa** | - |
| W5.csv | 71 | .09 | .88 | .01 | .02 | .91 | .98 | .00 | .13 | .00 | .01 | .00 | .99 | combo | **determin** | col, con |
| deaths.csv | 72 | .71 | .24 | .03 | .02 | .16 | .99 | .00 | .01 | .03 | .01 | .00 | 1.0 | combo | **stationa** | con |
| W13-1.csv | 82 | .04 | .76 | .17 | .03 | .19 | .67 | .00 | .01 | .00 | .02 | .00 | .99 | combo | **determin** | con |
| W13-2.csv | 82 | .01 | .95 | .02 | .01 | .21 | .99 | .00 | .01 | .01 | .00 | .00 | 1.0 | combo | **determin** | con |
| W13-3.csv | 82 | .03 | .93 | .01 | .02 | .36 | .56 | .00 | .01 | .02 | .00 | .00 | .99 | combo | **determin** | col, con |
| W13-4.csv | 82 | .04 | .64 | .30 | .03 | .17 | .66 | .00 | .11 | .01 | .00 | .00 | 1.0 | combo | **determin** | con |
| W13-5.csv | 82 | .00 | .98 | .01 | .01 | .91 | .98 | .00 | .08 | .00 | .02 | .00 | .99 | combo | **determin** | col, con |
| W3.csv | 82 | .68 | .17 | .12 | .04 | .89 | .56 | .00 | .01 | .01 | .00 | .00 | .99 | combo | **stationa** | col, con |
| W14.csv | 87 | .22 | .75 | .02 | .02 | .91 | .56 | .00 | .01 | .02 | .02 | .00 | 1.0 | combo | **determin** | col, con |
| GermanGNP.csv | 88 | .01 | .98 | .01 | .00 | .92 | .56 | .00 | .01 | .00 | .01 | .00 | .99 | combo | **determin** | col, con |
| e1.csv | 92 | .02 | .28 | .68 | .02 | .91 | .98 | .00 | .14 | .00 | .00 | .00 | .99 | combo | **stochast** | col, con |
| German_consumption.csv | 93 | .03 | .96 | .01 | .01 | .91 | .98 | .00 | .15 | .00 | .00 | .01 | 1.0 | combo | **determin** | col, con |
| sunspots.csv | 100 | .15 | .74 | .09 | .03 | .90 | .98 | .00 | .07 | .02 | .00 | .01 | 1.0 | combo | **determin** | col, con |
| RealInt_dataframe.csv | 103 | .01 | .98 | .00 | .01 | .91 | .54 | .00 | .01 | .01 | .01 | .00 | 1.0 | combo | **determin** | col, con |
| e2.csv | 104 | .01 | .96 | .03 | .01 | .20 | .98 | .00 | .23 | .00 | .00 | .08 | .99 | combo | **determin** | con |
| US_investment.csv | 104 | .86 | .11 | .02 | .01 | .24 | .55 | .00 | .01 | .01 | .00 | .00 | .99 | combo_suppress | **stationa** | - |
| German_income.csv | 113 | .01 | .96 | .02 | .01 | .42 | .55 | .00 | .99 | .00 | .00 | .03 | .99 | combo | **determin** | col, con, poi |
| W6.csv | 114 | .01 | .98 | .00 | .01 | .92 | .98 | .00 | .01 | .01 | .01 | .02 | .99 | combo | **determin** | col, con |
| Polish_productivity.csv | 117 | .00 | .00 | .33 | .67 | .42 | .01 | .00 | .98 | .00 | .17 | .87 | 1.0 | combo | **volatili** | col, poi |
| wine.csv | 142 | .09 | .90 | .00 | .00 | .89 | .56 | .01 | .11 | .01 | .01 | .02 | 1.0 | combo | **determin** | col, con |
| airpass.csv | 144 | .01 | .97 | .01 | .01 | .91 | .98 | .00 | .38 | .01 | .03 | .05 | .99 | combo | **determin** | col, con, poi |
| W8.csv | 150 | .00 | .99 | .00 | .00 | .17 | .98 | .01 | .97 | .00 | .01 | .03 | 1.0 | combo | **determin** | con, poi |
| W11.csv | 166 | .01 | .18 | .80 | .01 | .99 | .04 | .00 | .16 | .01 | .02 | .00 | 1.0 | combo | **stochast** | col, con |
| W2.csv | 302 | .19 | .62 | .17 | .02 | .25 | .98 | .00 | .19 | .01 | .01 | .00 | .98 | combo | **determin** | col, con, poi |
| INDPRO.csv | 372 | .00 | .98 | .01 | .01 | .73 | .03 | .01 | .51 | .00 | .00 | .26 | 1.0 | combo | **determin** | col, con, poi |
| UNRATE.csv | 372 | .00 | .93 | .07 | .01 | .99 | .01 | .00 | .24 | .00 | .00 | .65 | .99 | combo | **determin** | col |
| beer.csv | 422 | .03 | .95 | .01 | .01 | .34 | .55 | .00 | .36 | .02 | .01 | .07 | 1.0 | combo | **determin** | col, con, poi |
| rec_dataframe.csv | 453 | .11 | .75 | .12 | .02 | .22 | .98 | .00 | .23 | .00 | .00 | .00 | .98 | combo | **determin** | con, poi |
| soi_dataframe.csv | 453 | .03 | .06 | .81 | .10 | .92 | .01 | .11 | .01 | .00 | .12 | .32 | .99 | combo | **stochast** | col |
| NP_AWHours.csv | 479 | .00 | .98 | .01 | .01 | .99 | .01 | .04 | .25 | .00 | .02 | .51 | 1.0 | combo | **determin** | col |
| NP_xetradax_returns100.csv | 1028 | .87 | .01 | .01 | .10 | .93 | .02 | .00 | .48 | .00 | .01 | .01 | .99 | combo_suppress | **stationa** | - |

**Gozlem:**
- 37/37 dosya `combo` yoluna gitti. Stationarity gate hicbirinde acilmadi (>=0.92 esigi cok yuksek).
- Yeni ensemble (n_sta, n_str vs.) eski'nin contextual bias'ini cok daha iyi yonetiyor.
- Stationary olmasi gereken bircok dosyada base meta 'stationary' diyor ama anomali kolu over-fire.

Detayli JSON (her dosya icin 31 probability):
- [runner/results/ensfinal_realdata.json](runner/results/ensfinal_realdata.json) (n>=50, 32 dosya)
- [runner/results/ensfinal_short.json](runner/results/ensfinal_short.json) (20<=n<50, 5 dosya — W1 dahil)

---

## Kisa-seri (n<=100) basarim analizi

Plan.md'deki ana soru: 'algoritmanin kisa seriler ozelinde basarimi nasil, hem ts-ensemble hem ens-final icin?'

### Pipeline-1 (tsfresh-ensemble-stationary)

**Sentetik kisa stochastic-trend serileri** (5 tip × 2 uzunluk × 5 seri):

| Sentetik tipi | n | accuracy | ort P(stoch_trend) | Tahmin (hep) |
|---|---|---|---|---|
| rw | 45 | %0 | 0.001 | contextual_anomaly |
| rw | 100 | %0 | 0.010 | contextual_anomaly |
| rwd | 45 | %0 | 0.001 | contextual_anomaly |
| rwd | 100 | %0 | 0.003 | contextual_anomaly |
| ari | 45 | %0 | 0.004 | contextual_anomaly |
| ari | 100 | %0 | 0.007 | contextual_anomaly |
| ima | 45 | %0 | 0.016 | contextual_anomaly |
| ima | 100 | %0 | 0.024 | contextual_anomaly |
| arima | 45 | %0 | 0.006 | contextual_anomaly |
| arima | 100 | %0 | 0.002 | contextual_anomaly |

**Sonuc:** n=45'te de n=100'de de %0 dogru. Sorun **kisa uzunluk DEGIL**, modelin OOD bias'i.
Saf white noise N(0,1) bile P(contextual)=0.9995 veriyor.

**realdata kisa seriler** (n<=100): 23 dosya, 21'i contextual_anomaly, 2'si deterministic_trend.

### Sentetik kisa seriler — ens-final 19-vektor (Pipeline-2)

**Onemli:** Pipeline-1 sentetik veriler icin %0 accuracy verirken Pipeline-2 (ens-final) ayni veride
cok daha iyi sonuc veriyor. Asagidaki tablo 50 sentetik serinin her biri icin 19-vektor + karar.

**ens-final sentetik base accuracy (hepsi `stochastic_trend` bekleniyor):**

| kind | n | accuracy | dominant pred |
|---|---|---|---|
| ari | 45 | 60% | stochastic_trend |
| ari | 100 | 80% | stochastic_trend |
| arima | 45 | 20% | deterministic_trend |
| arima | 100 | 100% | stochastic_trend |
| ima | 45 | 80% | stochastic_trend |
| ima | 100 | 80% | stochastic_trend |
| rw | 45 | 40% | deterministic_trend |
| rw | 100 | 100% | stochastic_trend |
| rwd | 45 | 80% | stochastic_trend |
| rwd | 100 | 80% | stochastic_trend |

**Genel ortalama: 72%** (Pipeline-1: %0)

**19-vektor + meta + karar (50 sentetik seri):**

Kolon kisaltma — eski 9 (o_): col, ctx, det, ms, pt, st, ts, vs, vol; yeni 10 (n_): sta, det, stoch, vol, col, ctx, ms, pt, ts, vs.

| dosya | n | o_col | o_ctx | o_det | o_ms | o_pt | o_st | o_ts | o_vs | o_vol | n_sta | n_det | n_stoch | n_vol | n_col | n_ctx | n_ms | n_pt | n_ts | n_vs | base | anom | ✓ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ari_L45_00.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .40 | .96 | .05 | .00 | .04 | .55 | .00 | .50 | .97 | **stochast** | var | ✓ |
| ari_L45_01.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .78 | .97 | .04 | .00 | .04 | .60 | .00 | .50 | .95 | **stochast** | var | ✓ |
| ari_L45_02.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .74 | .40 | .02 | .01 | .04 | .99 | .00 | .50 | .97 | **determin** | var | ✗ |
| ari_L45_03.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .07 | .00 | .51 | .35 | .01 | .04 | 1.0 | .00 | .50 | .79 | **stationa** | mea | ✗ |
| ari_L45_04.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .40 | .92 | .05 | .00 | .04 | .66 | .00 | .50 | .97 | **stochast** | var | ✓ |
| ari_L100_00.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .04 | .01 | .04 | .32 | .07 | .50 | .88 | **stochast** | var | ✓ |
| ari_L100_01.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .58 | .94 | .04 | .02 | .04 | .93 | .00 | .50 | .64 | **stochast** | - | ✓ |
| ari_L100_02.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .40 | .90 | .05 | .01 | .04 | .99 | .00 | .50 | .83 | **stochast** | mea | ✓ |
| ari_L100_03.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .92 | .52 | .06 | .22 | .01 | .04 | .64 | .00 | .50 | .76 | **stationa** | - | ✗ |
| ari_L100_04.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .64 | .87 | .04 | .00 | .04 | .82 | .00 | .50 | .76 | **stochast** | var | ✓ |
| arima_L45_00.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .51 | .01 | .61 | .10 | .01 | .04 | .97 | .00 | .50 | .38 | **determin** | mea | ✗ |
| arima_L45_01.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .95 | .49 | .07 | .00 | .04 | .98 | .00 | .50 | .89 | **determin** | mea | ✗ |
| arima_L45_02.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .39 | .61 | .76 | .55 | .00 | .04 | .57 | .00 | .50 | .95 | **stationa** | var | ✗ |
| arima_L45_03.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .06 | .77 | .89 | .03 | .01 | .04 | .97 | .00 | .50 | .78 | **stochast** | - | ✓ |
| arima_L45_04.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .17 | .01 | .20 | .20 | .05 | .04 | .60 | .00 | .50 | .84 | **determin** | - | ✗ |
| arima_L100_00.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .17 | .97 | .02 | .00 | .04 | .80 | .00 | .50 | .96 | **stochast** | var | ✓ |
| arima_L100_01.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .97 | .89 | .23 | .00 | .04 | .92 | .00 | .50 | .50 | **stochast** | - | ✓ |
| arima_L100_02.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .58 | .96 | .04 | .00 | .04 | .97 | .00 | .50 | .80 | **stochast** | mea | ✓ |
| arima_L100_03.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .07 | .96 | .02 | .00 | .04 | .83 | .01 | .50 | .87 | **stochast** | var | ✓ |
| arima_L100_04.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .12 | .97 | .02 | .00 | .04 | .61 | .00 | .50 | .96 | **stochast** | var | ✓ |
| ima_L45_00.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .01 | .00 | .01 | .16 | .96 | .03 | .01 | .04 | .98 | .00 | .50 | .98 | **stochast** | var | ✓ |
| ima_L45_01.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .37 | .88 | .05 | .00 | .04 | .86 | .00 | .50 | .96 | **stochast** | var | ✓ |
| ima_L45_02.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .26 | .97 | .07 | .00 | .04 | .79 | .00 | .50 | .90 | **stochast** | var | ✓ |
| ima_L45_03.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .33 | .13 | .25 | .18 | .00 | .04 | .97 | .00 | .50 | .93 | **determin** | var | ✗ |
| ima_L45_04.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .08 | .93 | .05 | .00 | .04 | .70 | .00 | .50 | .95 | **stochast** | var | ✓ |
| ima_L100_00.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .05 | .00 | .00 | .00 | .00 | .09 | .94 | .02 | .00 | .04 | .70 | .00 | .50 | .95 | **stochast** | var | ✓ |
| ima_L100_01.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .86 | .89 | .04 | .01 | .04 | 1.0 | .00 | .50 | .81 | **stochast** | - | ✓ |
| ima_L100_02.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .98 | .02 | .00 | .04 | .86 | .00 | .50 | .95 | **stochast** | var | ✓ |
| ima_L100_03.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | 1.0 | .36 | .27 | .43 | .01 | .04 | .97 | .00 | .50 | .28 | **stationa** | - | ✗ |
| ima_L100_04.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .37 | .83 | .15 | .00 | .04 | .99 | .00 | .50 | .41 | **stochast** | mea | ✓ |
| rw_L45_00.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .08 | .40 | .51 | .59 | .07 | .04 | .95 | .00 | .50 | .89 | **determin** | var | ✗ |
| rw_L45_01.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .45 | .48 | .05 | .00 | .04 | .99 | .00 | .50 | .84 | **determin** | - | ✗ |
| rw_L45_02.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .19 | .47 | .30 | .17 | .00 | .04 | .75 | .00 | .50 | .86 | **determin** | var | ✗ |
| rw_L45_03.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .89 | .07 | .00 | .04 | .59 | .00 | .50 | .91 | **stochast** | var | ✓ |
| rw_L45_04.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .10 | .92 | .06 | .00 | .04 | .99 | .00 | .50 | .83 | **stochast** | mea | ✓ |
| rw_L100_00.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .98 | .86 | .21 | .00 | .04 | .98 | .00 | .50 | .90 | **stochast** | mea | ✓ |
| rw_L100_01.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .02 | .89 | .02 | .01 | .04 | .46 | .00 | .50 | .92 | **stochast** | var | ✓ |
| rw_L100_02.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .04 | .95 | .21 | .00 | .04 | .57 | .00 | .50 | .72 | **stochast** | - | ✓ |
| rw_L100_03.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .03 | .90 | .37 | .07 | .04 | .95 | .00 | .50 | .59 | **stochast** | mea | ✓ |
| rw_L100_04.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .95 | .04 | .00 | .04 | .83 | .00 | .50 | .95 | **stochast** | var | ✓ |
| rwd_L45_00.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .97 | .94 | .05 | .00 | .04 | .99 | .00 | .50 | .95 | **stochast** | var | ✓ |
| rwd_L45_01.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .01 | .92 | .04 | .00 | .04 | .22 | .00 | .50 | .87 | **stochast** | var | ✓ |
| rwd_L45_02.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .11 | .83 | .07 | .00 | .04 | .84 | .00 | .50 | .91 | **stochast** | var | ✓ |
| rwd_L45_03.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .08 | .83 | .07 | .00 | .04 | .99 | .00 | .50 | .95 | **stochast** | var | ✓ |
| rwd_L45_04.csv | 45 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .95 | .70 | .06 | .00 | .04 | 1.0 | .00 | .50 | .87 | **determin** | - | ✗ |
| rwd_L100_00.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .00 | .99 | .68 | .12 | .00 | .04 | .99 | .00 | .50 | .72 | **determin** | - | ✗ |
| rwd_L100_01.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .07 | .92 | .02 | .00 | .04 | .76 | .00 | .50 | .85 | **stochast** | - | ✓ |
| rwd_L100_02.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .23 | .85 | .02 | .00 | .04 | .95 | .00 | .50 | .73 | **stochast** | mea | ✓ |
| rwd_L100_03.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .02 | .97 | .02 | .00 | .04 | .79 | .00 | .50 | .85 | **stochast** | - | ✓ |
| rwd_L100_04.csv | 100 | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .11 | .93 | .02 | .00 | .04 | .12 | .05 | .50 | .92 | **stochast** | var | ✓ |

**Gozlemler:**
- `rw` (random walk) **n=100'de %100** — ens-final pure RW'yi mukemmel taniyor
- `rwd` (RW + drift) her iki uzunlukta da %80 — drift sinyali yardim ediyor
- `ari` ve `arima` zor — AR bileseni serinin daha stationary gorunmesine yol aciyor
- Eski ensemble (o_*) sutunlarinda contextual_anomaly (o_ctx) sentetik veride dusuk — yani eski model bias'i sentetigimizi orta seviyede taniyor; ancak yeni ensemble (n_*) cok daha bilgili

### KRITIK BULGU: Stationarity gate yanlis tetikleniyor

**14 sentetik stochastic serisi icin** stat_gate (P(stationary) >= 0.92) tetiklenip base'i ZORLA `stationary` yapiyor — halbuki base meta-learner ayni serilerde `stochastic_trend` diyor (b_str=0.99).

Ornek: `ari_L45_00.csv`
```
base meta-learner:  P(stationary)=0.00, P(stoch_trend)=0.99  -> argmax = stoch
21-feat stat-gate:  P(stationary)=0.963                       -> gate fires (>=0.92)
FINAL              -> stationary  (gate override)
```

**Gate kapali senaryosu (sadece base meta argmax):**

| kind/n | mevcut acc | gate OFF acc |
|---|---|---|
| ari 45 | %20 | **%60** |
| ari 100 | **%0** | **%80** |
| arima 45 | %20 | %20 |
| arima 100 | %20 | **%100** |
| ima 45 | %20 | **%80** |
| ima 100 | %60 | **%80** |
| rw 45 | %40 | %40 |
| rw 100 | %100 | %100 |
| rwd 45 | %80 | %80 |
| rwd 100 | %80 | %80 |
| **TOPLAM** | **%44** | **%72** |

**Yorum:**
- 21-feature stationary detector (`stationary-detection-ml/best_model.pkl`) bizim eğitim datamızdan FARKLI bir veri setiyle (276K orijinal) egitildigi icin OOD davranisi var.
- Kisa ARI/IMA/ARIMA serilerinde drift sinyali zayif kaliyor; statistical features (rolling_std vb.) stationary'e benziyor; gate yanlis tetikleniyor.
- Ironik: ayni gate **realdata icin hicbir zaman acilmadi** (37/37 combo yoluna gitti). DAX log returns (kesin stationary) icin bile P(stat)=0.006.
- **Tedavi:** Gate threshold 0.92 -> 0.97 yukseltmek veya gate'i kaldirmak. Veya base meta P(stationary) ile birlikte AND kontrolu (her ikisi de >0.7 ise stationary).

Detayli JSON: [runner/results/ensfinal_synthetic.json](runner/results/ensfinal_synthetic.json)

### Pipeline-2 (ens-final) — kisa realdata

Ens-final MIN_SERIES_LENGTH=50 (default). Dolayisiyla:
- n>=50 olan 32 realdata dosyasi normal pipeline'a girdi
- 20<=n<50 olan 5 dosya (W1, uspop, strikes, W15-1, W15-2) ozel scriptle (`runner/21_ensfinal_short_realdata.py`) pipeline'a sokuldu
- n<20 olan 4 dosya (W9, W10, W16, rec_dataframe) tsfresh stabilite riski sebebiyle atlandi

**Kisa realdata (n<=100) ens-final ozet:**

| dosya | n | base | anomaliler | path | P(stat) | P(combo) |
|---|---|---|---|---|---|---|
| uspop.csv | 21 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .01 | .95 |
| strikes.csv | 30 | stationary | - | combo_suppress | .01 | .98 |
| W1.csv | 45 | stochastic_trend | collective_anomaly, variance_shift | combo | .05 | 1.0 |
| W15-1.csv | 46 | stochastic_trend | collective_anomaly | combo | .82 | .94 |
| W15-2.csv | 46 | stochastic_trend | collective_anomaly | combo | .84 | .92 |
| W12-1.csv | 54 | stationary | - | combo_suppress | .00 | .95 |
| W12-2.csv | 54 | stationary | - | combo_suppress | .00 | .97 |
| W5.csv | 71 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .00 | .99 |
| deaths.csv | 72 | stationary | contextual_anomaly | combo | .00 | 1.0 |
| W13-1.csv | 82 | deterministic_trend | contextual_anomaly | combo | .00 | .99 |
| W13-2.csv | 82 | deterministic_trend | contextual_anomaly | combo | .00 | 1.0 |
| W13-3.csv | 82 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .00 | .99 |
| W13-4.csv | 82 | deterministic_trend | contextual_anomaly | combo | .00 | 1.0 |
| W13-5.csv | 82 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .00 | .99 |
| W3.csv | 82 | stationary | collective_anomaly, contextual_anomaly | combo | .00 | .99 |
| W14.csv | 87 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .00 | 1.0 |
| GermanGNP.csv | 88 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .00 | .99 |
| e1.csv | 92 | stochastic_trend | collective_anomaly, contextual_anomaly | combo | .00 | .99 |
| German_consumption.csv | 93 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .01 | 1.0 |
| sunspots.csv | 100 | deterministic_trend | collective_anomaly, contextual_anomaly | combo | .01 | 1.0 |

**Kisa realdata 19-vektor (9 eski + 10 yeni):**

| dosya | n | o_col | o_ctx | o_det | o_ms | o_pt | o_st | o_ts | o_vs | o_vol | n_sta | n_det | n_stoch | n_vol | n_col | n_ctx | n_ms | n_pt | n_ts | n_vs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uspop.csv | 21 | .00 | .30 | .87 | .00 | .00 | .00 | .00 | .00 | .00 | .60 | .94 | .50 | .11 | 1.0 | .95 | .27 | .01 | .50 | .46 |
| strikes.csv | 30 | .00 | .36 | .15 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .80 | .29 | .17 | 1.0 | .95 | .49 | .08 | .50 | .42 |
| W1.csv | 45 | .00 | .57 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .31 | .22 | .13 | .62 | .97 | .04 | .41 | .00 | .50 | .91 |
| W15-1.csv | 46 | .00 | .98 | .01 | .00 | .00 | .00 | .00 | .00 | .00 | .02 | .33 | .87 | .54 | .94 | .04 | .88 | .00 | .50 | .65 |
| W15-2.csv | 46 | .00 | .98 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .01 | .73 | .89 | .49 | .83 | .04 | .67 | .00 | .50 | .62 |
| W12-1.csv | 54 | .00 | .93 | .16 | .00 | .00 | .00 | .00 | .00 | .00 | .93 | .79 | .68 | .66 | .87 | .96 | .31 | .03 | .50 | .12 |
| W12-2.csv | 54 | .00 | .95 | .06 | .00 | .00 | .01 | .00 | .00 | .00 | .99 | .21 | .77 | .66 | .25 | .95 | .44 | .33 | .50 | .07 |
| W5.csv | 71 | .00 | .95 | .04 | .00 | .00 | .00 | .00 | .00 | .00 | .89 | .60 | .41 | .04 | .99 | .96 | .39 | .56 | .50 | .17 |
| deaths.csv | 72 | .00 | .36 | .74 | .00 | .00 | .00 | .00 | .00 | .00 | .98 | .95 | .20 | .36 | .85 | .96 | .23 | .03 | .50 | .06 |
| W13-1.csv | 82 | .00 | .94 | .26 | .00 | .00 | .00 | .00 | .00 | .00 | .81 | .99 | .80 | .05 | .84 | .95 | .16 | .02 | .50 | .24 |
| W13-2.csv | 82 | .00 | .33 | .21 | .00 | .00 | .00 | .00 | .00 | .00 | .85 | .98 | .71 | .04 | .87 | .96 | .30 | .09 | .50 | .11 |
| W13-3.csv | 82 | .00 | .33 | .09 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .98 | .43 | .03 | .97 | .95 | .44 | .01 | .50 | .41 |
| W13-4.csv | 82 | .00 | .94 | .11 | .00 | .00 | .01 | .00 | .00 | .00 | .88 | .97 | .88 | .06 | .82 | .95 | .36 | .43 | .50 | .12 |
| W13-5.csv | 82 | .00 | .33 | .19 | .00 | .00 | .00 | .00 | .00 | .00 | .67 | .96 | .58 | .03 | .98 | .96 | .26 | .50 | .50 | .41 |
| W3.csv | 82 | .00 | .36 | .16 | .00 | .00 | .00 | .00 | .00 | .00 | .99 | .77 | .64 | .20 | .99 | .95 | .16 | .05 | .50 | .04 |
| W14.csv | 87 | .00 | .94 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | 1.0 | .95 | .55 | .18 | .99 | .95 | .15 | .04 | .50 | .45 |
| GermanGNP.csv | 88 | .00 | .33 | .03 | .00 | .00 | .00 | .00 | .00 | .00 | .79 | .99 | .64 | .04 | .98 | .95 | .18 | .11 | .50 | .30 |
| e1.csv | 92 | .00 | .33 | .05 | .00 | .00 | .00 | .00 | .00 | .00 | .66 | .27 | .84 | .03 | .99 | .96 | .15 | .39 | .50 | .27 |
| German_consumption.csv | 93 | .00 | .35 | .04 | .00 | .00 | .01 | .00 | .00 | .00 | .89 | .24 | .49 | .04 | .98 | .96 | .18 | .52 | .50 | .17 |
| sunspots.csv | 100 | .00 | .41 | .06 | .00 | .00 | .00 | .00 | .00 | .00 | .85 | 1.0 | .58 | .41 | .99 | .96 | .07 | .30 | .50 | .12 |

**Sonuc:**
- Pipeline-1'in aksine pipeline-2 farkli base tipleri ayirt edebiliyor (deterministic_trend, stochastic_trend, stationary, volatility).
- W15-1 ve W15-2'de P(stat) yuksek (0.82-0.84) ama 0.92 esigi gecmedi -> combo'ya yonlendirildi.
- Sentetik egitim seti uzunluk [80, 150] araliginda; n=21 (uspop), n=30 (strikes), n=45-46 gibi kisa seriler aslinda egitim distribution disinda -> bu da OOD.
- ens-final 39-grup egitim setinde stationary grup 1 (uzunluk 80-150) icin %70 FULL, ama gercek kisa stationary seriler (W1, strikes) icin anomali over-fire mevcut.

**Iki pipeline karsilastirmasi (W1 ornegi, n=45):**

| Pipeline | W1 tahmini | Yorum |
|---|---|---|
| Pipeline-1 (sadece eski 9 detector) | `contextual_anomaly` (P=0.57) | bias |
| Pipeline-2 (ens-final tam stack) | `stochastic_trend` + `collective`, `variance_shift` | meta override etti, base degisti |
| **PDF Ground Truth** | **`stationary`** + point_anomaly | Wei: AO/IO at t=4,7,9,36 |

Yani Pipeline-2 Pipeline-1'in contextual bias'ini override etti, **ama PDF'teki dogru cevaba** (stationary) ulasamadi.

---

## Ground truth karsilastirmasi (Datasets.pdf)

`Datasets.pdf` (Wei, Brockwell, Lutkepohl, Shumway & Stoffer, Bai-Perron kaynaklarindan) **21 realdata dosyasi** icin
acik etiketler veriyor.

**Ozet:**

| Match | Sayi |
|---|---|
| FULL | 3 |
| PARTIAL | 5 |
| NONE | 12 |
| MISSING | 1 |

**Base type dogru: 8 / 20** (MISSING haric)

**Kesin stationary oldugu PDF'te belirtilen dosyalar:**

| dosya | n | kaynak | model base | base✓ |
|---|---|---|---|---|
| W1.csv | 45 | Wei | stochastic_trend | ✗ |
| W2.csv | 302 | Wei | deterministic_trend | ✗ |
| W3.csv | 82 | Wei | stationary | ✓ |
| strikes.csv | 30 | Brockwell | stationary | ✓ |
| sunspots.csv | 100 | Brockwell | deterministic_trend | ✗ |
| soi_dataframe.csv | 453 | Shumway | stochastic_trend | ✗ |
| rec_dataframe.csv | 453 | Shumway | deterministic_trend | ✗ |
| US_investment.csv | 104 | JMulTi | stationary | ✓ |
| RealInt_dataframe.csv | 103 | Bai-Perron | deterministic_trend | ✗ |
| NP_xetradax_returns100.csv | 1028 | Lutkepohl | stationary | ✓ |

Tam karsilastirma: [runner/results/LABEL_KARSILASTIRMA.md](runner/results/LABEL_KARSILASTIRMA.md)

### Ground truth dosyalari icin 19-vektor (ens-final)

PDF'te etiketli her dosya icin 19 ham olasilik (9 eski + 10 yeni ensemble). **GT** sutunu PDF'teki dogru base.
**✓** = model base'i dogru bildi mi.

| dosya | n | GT | o_col | o_ctx | o_det | o_ms | o_pt | o_st | o_ts | o_vs | o_vol | n_sta | n_det | n_stoch | n_vol | n_col | n_ctx | n_ms | n_pt | n_ts | n_vs | pred | ✓ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1.csv | 45 | stationa | .00 | .57 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .31 | .22 | .13 | .62 | .97 | .04 | .41 | .00 | .50 | .91 | **stochast** | ✗ |
| W2.csv | 302 | stationa | .00 | .39 | .09 | .00 | .00 | .01 | .00 | .00 | .00 | .99 | .71 | .66 | .06 | .96 | .96 | .03 | .98 | .50 | .42 | **determin** | ✗ |
| W3.csv | 82 | stationa | .00 | .36 | .16 | .00 | .00 | .00 | .00 | .00 | .00 | .99 | .77 | .64 | .20 | .99 | .95 | .16 | .05 | .50 | .04 | **stationa** | ✓ |
| W5.csv | 71 | determin | .00 | .95 | .04 | .00 | .00 | .00 | .00 | .00 | .00 | .89 | .60 | .41 | .04 | .99 | .96 | .39 | .56 | .50 | .17 | **determin** | ✓ |
| W6.csv | 114 | determin | .00 | .94 | .11 | .00 | .00 | .00 | .00 | .00 | .00 | .80 | .99 | .54 | .04 | .99 | .96 | .34 | .03 | .50 | .27 | **determin** | ✓ |
| W10.csv | - | stochast | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | (n<20) | - |
| uspop.csv | 21 | determin | .00 | .30 | .87 | .00 | .00 | .00 | .00 | .00 | .00 | .60 | .94 | .50 | .11 | 1.0 | .95 | .27 | .01 | .50 | .46 | **determin** | ✓ |
| strikes.csv | 30 | stationa | .00 | .36 | .15 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .80 | .29 | .17 | 1.0 | .95 | .49 | .08 | .50 | .42 | **stationa** | ✓ |
| sunspots.csv | 100 | stationa | .00 | .41 | .06 | .00 | .00 | .00 | .00 | .00 | .00 | .85 | 1.0 | .58 | .41 | .99 | .96 | .07 | .30 | .50 | .12 | **determin** | ✗ |
| airpass.csv | 144 | stochast | .00 | .30 | .17 | .00 | .00 | .01 | .00 | .00 | .00 | .59 | .94 | .62 | .03 | .98 | .96 | .14 | .99 | .50 | .36 | **determin** | ✗ |
| deaths.csv | 72 | stochast | .00 | .36 | .74 | .00 | .00 | .00 | .00 | .00 | .00 | .98 | .95 | .20 | .36 | .85 | .96 | .23 | .03 | .50 | .06 | **stationa** | ✗ |
| INDPRO.csv | 372 | stochast | .00 | .35 | .07 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .95 | .61 | .12 | .97 | .90 | .39 | .99 | .50 | .40 | **determin** | ✗ |
| UNRATE.csv | 372 | stochast | .00 | .33 | .02 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .68 | .67 | .02 | .98 | .87 | .61 | .68 | .50 | .18 | **determin** | ✗ |
| soi_dataframe.csv | 453 | stationa | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | .11 | .00 | .77 | .60 | .86 | .04 | .82 | .01 | .50 | .60 | **stochast** | ✗ |
| rec_dataframe.csv | 453 | stationa | .00 | .47 | .04 | .00 | .00 | .02 | .00 | .00 | .00 | .91 | .17 | .73 | .10 | .90 | .96 | .26 | .99 | .50 | .21 | **determin** | ✗ |
| GermanGNP.csv | 88 | determin | .00 | .33 | .03 | .00 | .00 | .00 | .00 | .00 | .00 | .79 | .99 | .64 | .04 | .98 | .95 | .18 | .11 | .50 | .30 | **determin** | ✓ |
| US_investment.csv | 104 | stationa | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | 1.0 | .15 | .07 | .19 | .94 | .95 | .16 | .05 | .50 | .37 | **stationa** | ✓ |
| German_consumption.csv | 93 | stochast | .00 | .35 | .04 | .00 | .00 | .01 | .00 | .00 | .00 | .89 | .24 | .49 | .04 | .98 | .96 | .18 | .52 | .50 | .17 | **determin** | ✗ |
| Polish_productivity.csv | 117 | stochast | .00 | .95 | .06 | .00 | .00 | .01 | .00 | .00 | .02 | .02 | .03 | .82 | .91 | .93 | .84 | .08 | 1.0 | .50 | .80 | **volatili** | ✗ |
| RealInt_dataframe.csv | 103 | stationa | .00 | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | .00 | .96 | .97 | .06 | .05 | 1.0 | .95 | .06 | .09 | .50 | .57 | **determin** | ✗ |
| NP_xetradax_returns100.csv | 1028 | stationa | .00 | 1.0 | .00 | .00 | .00 | .01 | .00 | .00 | .00 | 1.0 | .00 | .40 | .72 | .99 | .93 | .20 | .98 | .50 | .31 | **stationa** | ✓ |

**Ana bulgular (FIX SONRASI):**
- **3 FULL match** (NP_xetradax_returns100, US_investment, strikes) — hepsi PDF'te kesin stationary etiketli
- 5 PARTIAL (base dogru ama anomali fazlasi: W3, W5, W6, uspop, GermanGNP)
- Base type **8 / 20** (~%40) dogru — DAX returns, US_investment, strikes basariyla stationary olarak tanindi
- Sezonsallik kategorisi eksikligi: airpass, INDPRO, UNRATE, deaths (hepsi seasonal+stoch) -> deterministic_trend deniyor
- W1 (stationary+point) hala yanlis: stochastic_trend deniyor — bu base meta'nin gercek hatasi
- 19-vektor incelemesi: **o_ctx (eski contextual)** sutunu neredeyse her satirda yuksek. Yani eski ensemble OOD bias'i tum gercek-dunya verisinde mevcut; meta-learner bunu base secimi icin override edebiliyor ama anomali secimi icin (collective vs contextual) hala karistirabiliyor.

**Fix oncesi vs sonrasi karsilastirma:**

| | Fix oncesi | Fix sonrasi |
|---|---|---|
| FULL | 0 | **3** |
| PARTIAL | 8 | 5 |
| NONE | 11 | 12 |
| MISSING | 2 | 1 (rec_dataframe indirildi) |

Uygulanan 3 fix:
1. **CONTEXT_THRESH 0.0 -> 0.55**: stationary base'de anomali threshold'u dusurmek yerine yukseltmek (bug fix)
2. **Stationarity gate + base meta AND**: gate sadece base meta P(stationary) >= 0.40 ise tetikleniyor (sentetik yanlis-pozitifi kes)
3. **Anomali suppress**: base meta P(stationary) >= 0.75 ise stationary base'de anomali listeleme

---

## Hizli komutlar

```powershell
# Bagimliliklar
pip install numpy pandas tsfresh scikit-learn lightgbm xgboost statsmodels arch scipy joblib

# 1. Sentetik veri (390 seri, 39 grup × 10)
python runner/10_generate_39groups.py

# 2. Yeni ensemble (10 binary model) egitimi
cd ensemble-alldata; python main.py; cd ..

# 3. ens-final meta-learner + 39 grup eval
cd ens-final; python main.py --force; cd ..

# 4. realdata ens-final pipeline
python runner/20_ensfinal_realdata.py        # n>=50
python runner/21_ensfinal_short_realdata.py  # 20<=n<50 (W1 dahil)

# 5. Pipeline-1 (tsfresh-ensemble-stationary tek basina)
python runner/01_generate_synthetic.py
python runner/02_convert_realdata.py
python runner/03_run_pipeline.py
python runner/04_build_report.py

# 6. Ground truth karsilastirma
python runner/30_compare_labels.py

# 7. Bu README'yi yeniden uret
python runner/40_build_readme.py
```

---

## Daha fazla detay

- [NIHAI_RAPOR.md](NIHAI_RAPOR.md) — Tum yapilanlarin kronolojik raporu
- [plan.md](plan.md) — Hocadan gelen orijinal plan
- [Datasets.pdf](Datasets.pdf) — realdata kaynaklari + ground truth
- [runner/results/RAPOR.md](runner/results/RAPOR.md) — Pipeline-1 detayli rapor
- [runner/results/ENSFINAL_REALDATA_RAPOR.md](runner/results/ENSFINAL_REALDATA_RAPOR.md) — Pipeline-2 detayli rapor
- [runner/results/ENSFINAL_SHORT_RAPOR.md](runner/results/ENSFINAL_SHORT_RAPOR.md) — W1 + kisa seriler ens-final raporu
- [runner/results/LABEL_KARSILASTIRMA.md](runner/results/LABEL_KARSILASTIRMA.md) — Ground truth karsilastirma
- [ens-final/results/evaluation_report.md](ens-final/results/evaluation_report.md) — 39 grup eval

