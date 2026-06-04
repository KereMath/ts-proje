# contextual-off-10x: 10x Veri + Stationarity Threshold Sweep

contextual-off pipeline'inin 10x veri ile yeniden egitimi + stationarity
threshold sweep (0.00 -> 1.00, 0.05 adimli, 21 deger).

## 1. Veri olcekleme

| Bilesen | 1x | 10x | Δ |
|---|---|---|---|
| Egitim verisi | 380 | **38,000** | 100x |
| Sentetik test | 50 | **500** | 10x |
| realdata | 38 (sabit) | 38 (sabit) | - |
| ensemble-alldata N | 60 | **600** | 10x |
| ens-final META_N_PER_GROUP | 8 | **80** | 10x |

## 2. ensemble-alldata egitim — dramatic iyilesme

| Model | 1x F1 | **10x F1** | Δ |
|---|---|---|---|
| stationary | 0.89 | 0.89 | ≈ |
| deterministic_trend | 0.67 | **0.91** | +0.24 |
| stochastic_trend | 0.89 | 0.94 | +0.05 |
| volatility | 0.80 | 0.92 | +0.12 |
| collective_anomaly | 1.00 | 1.00 | ≈ |
| mean_shift | 0.83 | 0.92 | +0.09 |
| point_anomaly | 0.96 | 1.00 | +0.04 |
| trend_shift | **0.50** | **0.96** | **+0.46** |
| variance_shift | 0.92 | 0.95 | +0.03 |

`trend_shift` dramatic iyilesti. Kucuk veriyle sadece 30 pozitif vardi, 10x'te
600 pozitif → model dogru ogrendi.

## 3. ens-final 38-grup eval

| Setup | FULL | PARTIAL | NONE | FULL% |
|---|---|---|---|---|
| contextual-off (1x) | 357 | 21 | 2 | **93.95%** |
| contextual-off-10x | 320 | 54 | 6 | **84.21%** |

10x'te 380 ornek eval edildi (samples_per_leaf=10). FULL% dustu cunku
threshold'lar 1x'e gore kalibre edilmis — sweep ile optimize edilebilir.

## 4. Sentetik test (500 stochastic-trend serisi)

| kind | n=45 | n=100 |
|---|---|---|
| ari | %76 | %80 |
| arima | %72 | %66 |
| ima | %70 | %78 |
| rw | %82 | %96 |
| rwd | %72 | %98 |
| **TOPLAM** | | **%79** |

10x ile sentetik %72 → %79. Mütevazi iyilesme.

## 5. Stationarity Threshold Sweep (21 deger, 0.00 -> 1.00)

**Sabitler:** STAT_BASE_AND = 0.0 (gate'i bagimsiz birak), STAT_CONFIDENT = 0.75,
CTX_THRESH = 0.55, ROUTER_THETA = 0.40.

Test set: 760 training (20/grup × 38) + 500 sentetik + 38 realdata = 1298 seri.

| STAT_GATE | Training FULL% | Sentetik base% | Realdata base✓/20 |
|---|---|---|---|
| 0.00 | 2.6% | 0% | **10** |
| 0.05 | 40.5% | 1.8% | 7 |
| 0.10 | 49.6% | 4.2% | 6 |
| 0.15 | 53.6% | 6.4% | 6 |
| 0.20 | 56.3% | 9.4% | 6 |
| 0.25 | 58.0% | 11.4% | 6 |
| 0.30 | 60.0% | 14.4% | 6 |
| 0.35 | 61.8% | 17.2% | 5 |
| 0.40 | 62.5% | 20.0% | 5 |
| 0.45 | 63.0% | 22.4% | 5 |
| 0.50 | 64.1% | 23.8% | 5 |
| 0.55 | 65.7% | 25.4% | 5 |
| 0.60 | 66.4% | 28.2% | 5 |
| 0.65 | 67.5% | 31.2% | 5 |
| 0.70 | 69.1% | 34.8% | 5 |
| 0.75 | 70.7% | 37.2% | 5 |
| 0.80 | 71.8% | 41.2% | 5 |
| 0.85 | 72.6% | 46.0% | 5 |
| 0.90 | 73.7% | 51.0% | 6 |
| 0.95 | 74.2% | 60.6% | 6 |
| **1.00** | **75.3%** | **77.0%** | 6 |

### Net Trade-off

| Kriter | En iyi STAT_GATE | Sonuc |
|---|---|---|
| Training FULL | **1.00** (gate kapali) | 75.3% (572/760) |
| Sentetik base accuracy | **1.00** (gate kapali) | 77.0% (385/500) |
| Realdata base accuracy | **0.00** (gate her zaman fire) | 10/20 (50%) |

**Kritik bulgu:** Stationarity gate **EGITIM SETI ve SENTETIK** icin tamamen
kapalı **EN iyi**, **REALDATA icin** tamamen acik (gate=0.0) **EN iyi**.

Bu, gate'in iki rolü icin karşıt etkisi olduğunu gösteriyor:
- **Gate=0.00**: Her sey "stationary" gibi davraniyor → realdata'da stationary
  olan dosyalar (DAX returns, US_investment, sunspots vs.) dogru cikiyor (10/20)
- **Gate=1.00**: Gate hic aktif olmuyor → meta-learner argmax çalısıyor →
  egitim seti ve sentetik mukemmel ama realdata'da stationary'leri kacirilıyor

### Onerilen konfigurasyon

Realdata performansi onemli ise: **STAT_GATE = 0.95-1.00**, STAT_CONFIDENT = 0.75,
STAT_BASE_AND = 0.40. Bu noktada Training %74, Sentetik %60, Realdata 6/20
(orta yol).

Sadece realdata icin: **STAT_GATE = 0.00** (everything-stationary) 10/20 ama
egitim sıfırlaniyor — pratik degil.

## 6. Klasor yapisi

```
contextual-off-10x/
├── README.md
├── ensemble-alldata/         # N=600 ile yeniden egitildi
│   ├── config.py
│   ├── trained_models/       # 9 .pkl (10x sample size)
│   └── results/training_results.json
├── ens-final/                # META_N_PER_GROUP=80
│   ├── config.py
│   ├── meta_models/          # base + 5 anom + router + blend
│   └── results/evaluation*.json
└── runner/
    ├── 20_realdata.py
    ├── 22_synthetic.py       # 500 sentetik test
    ├── 30_compare.py
    ├── 50_threshold_sweep.py # 21 STAT_GATE
    └── results/
        ├── realdata.json
        ├── synthetic.json
        ├── threshold_sweep.json
        └── THRESHOLD_SWEEP.md
```

## 7. Reproducibility

```powershell
# 1. 38000 egitim serisi (38 grup × 1000)
python contextual-off/runner/10_generate_38groups_10x.py

# 2. 500 sentetik test serisi
python contextual-off/runner/02_generate_synthetic_10x.py

# 3. ensemble-alldata egit (N=600)
cd contextual-off-10x/ensemble-alldata; python main.py; cd ../..

# 4. ens-final egit (META_N_PER_GROUP=80)
cd contextual-off-10x/ens-final; python main.py --force; cd ../..

# 5. Inference + threshold sweep
python contextual-off-10x/runner/20_realdata.py
python contextual-off-10x/runner/22_synthetic.py
python contextual-off-10x/runner/50_threshold_sweep.py
```

NOT: `contextual-off/data_10x/` ve `processed_data/` klasorleri gitignore'da
(181MB) — reproducible script var.

## 6. Joint Alpha/Threshold Sweep (per-anomaly grid)

`runner/55_alpha_thresh_sweep.py`: 3 STAT_GATE × 5 anomali × 6 alpha × 13 threshold = 1170 evaluation, training set'i (20/grup × 38 = 760) optimize ediyor.

### Optimal blend (sweep'ten)
| anomali | baseline alpha/thresh | **optimal alpha/thresh** |
|---|---|---|
| collective_anomaly | 0.55/0.46 | **0.20/0.85** |
| mean_shift | 0.65/0.44 | **0.50/0.80** |
| point_anomaly | 0.55/0.46 | **0.20/0.75** |
| trend_shift | 0.75/0.38 | **0.20/0.90** |
| variance_shift | 0.60/0.54 | **0.35/0.90** |

**Kritik gozlem:** Trainer'in ogrendigi threshold'lar (0.38-0.54) **cok dusuk**. Optimal degerler **0.75-0.90 arasinda**. Bu, 10x modellerin yuksek probability'leri icin trainer'in F1-maximize stratejisinin pipeline FULL-maximize ile uyusmadigini gosteriyor.

### Sonuc: training-set overfitting
| Metrik | Baseline | Optimized | Delta |
|---|---|---|---|
| Training FULL (760) | 571 | **584** | **+13** (+1.7 puan) |
| Realdata base acc (20 GT) | 6 | 6 | +0 |
| Realdata FULL (10 saf stat) | 0 | 0 | +0 |
| Sentetik base acc (500) | 385 (77%) | 385 (77%) | +0 |

Optimization training set'i iyilestirdi (+13 FULL) ama **test setlerine yansimadi**. Egitim seti icinde grid search ile bulunan degerler, gercek-dunya verilerinde ayni kalibrasyon avantajini vermiyor.

### STAT_GATE etkisiz
Joint sweep'te 3 STAT_GATE degerinde (0.90, 0.95, 1.00) sonuc **aynen ayni** (584/760). Cunku STAT_BASE_AND=0.40 sabit ve training set'te neredeyse hicbir ornekte hem stat_prob>=gate hem base_meta_p_stat>=0.40 birlikte saglanmiyor (eski sweep gosterdi).

### Cikarim
- **Trainer threshold'lari overfit:** Eğitim seti optimum'u, test setine generalize etmiyor
- **10x veri binary F1'leri iyilestirdi** ama pipeline FULL match icin "more samples != better decisions"
- **Anomali threshold'larini yukseltmek** (0.70+) FULL_match'te kucuk iyilesme veriyor (+13/760 = +1.7 puan) ama test seti degismez
- **Realdata FULL=0** sebebi: 10x ile modeller daha tutarli ama saf stationary realdata icin base meta P(stationary)>0.75 esigi nadiren saglaniyor; suppress mekanizmasi tetiklenemiyor

Detay: [runner/results/ALPHA_THRESH_SWEEP.md](runner/results/ALPHA_THRESH_SWEEP.md), [runner/results/OPTIMIZED_EVAL.md](runner/results/OPTIMIZED_EVAL.md)
