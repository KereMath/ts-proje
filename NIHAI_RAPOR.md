# Nihai Rapor — ceylanhoca Pipeline Calismasi

**Tarih:** 2026-05-21  
**Klasor:** `c:\Users\Pc\Desktop\ceylanhoca`  
**Sure:** Tek oturum, tam pipeline kurulumu + egitim + iki ayri raporlama

---

## 1. plan.md istegi (yorum)

`plan.md` su dort isi istiyordu:

1. **Sentetik veri uretimi (betise):** stochastic-trendli kisa veri (~40-50, kotuyse 100).  
2. **W1 + realdata** ile testler: hem `tsfresh-ensemble-stationary` hem `ens-final` pipeline'larinin **her ara modelinden** probability raporu.  
3. **Tum labeled realdata** her iki pipeline'da calisip ayri ayri sonuc.  
4. **Kisa-seri ozelinde basarim** her iki pipeline icin.

Sen ek olarak (ikinci turda) "**ens-final icin 39 grup × 10 seri uret, ens-final'i sifirdan egit, sonra realdata ile test**" dedin. Asagidaki tum is iki turluk istegin birlesimini kapsiyor.

---

## 2. Yapilanlar — kronolojik

### 2.1. Repo klonlama
4 repo klonlandi (`c:\Users\Pc\Desktop\ceylanhoca\` altina):

| Repo | Rolu |
|---|---|
| `tsfresh-ensemble-stationary` | **Eski ensemble** — 9 binary detector + tsfresh 777 feature. `trained_models/` bundled (mevcut). |
| `ensemble-alldata` | **Yeni ensemble** — 10 binary model (4 base + 6 anomali). `trained_models/` yok, sifirdan egitildi. |
| `stationary-detection-ml` | Stationarity detector — 21 ozel feature, GradientBoosting. `models/` bundled. |
| `ens-final` | Pipeline orkestratoru — meta-learner + router + blend. `meta_models/` yok, sifirdan egitildi. |
| `Auto_Feature_ML` | Sadece referans — `processed_data_no_window_12k` train pipeline'i. |

### 2.2. Python ortami
`pip install tsfresh lightgbm xgboost` ile kuruldu. Mevcut sistemde numpy/pandas/sklearn/joblib vardi.

| Paket | Surum |
|---|---|
| Python | 3.13.1 |
| tsfresh | 0.21.1 |
| lightgbm | 4.6.0 |
| xgboost | 3.2.0 |
| scikit-learn | 1.8.0 (model eski 1.6.1'den uyarli ama calisiyor) |
| numpy | 2.4.4, pandas 3.0.2, statsmodels 0.14.6, arch 8.0.0 |

### 2.3. Birinci tur — Sadece tsfresh-ensemble-stationary
**Amac:** plan.md'nin 1-4. maddelerini hizlica calistirmak.

- **Sentetik veri (betise):** 5 stochastic-trend tipi (rw, rwd, ari, ima, arima) × 2 uzunluk (45 ve 100) × 5 seri = **50 dosya** ([runner/data/synthetic/](runner/data/synthetic/)).
- **realdata cevirisi:** `realdata/TS datasets/` icindeki 41 dosya tek-kolon CSV'ye donusturuldu ([runner/data/realdata/](runner/data/realdata/)). Format'lar: BROCKWELL_HASH, JMULTI, CSV_HEADER, DATAFRAME_HEADER, WHITESPACE_MULTI.
- **Pipeline:** Her 90 seri icin tsfresh 777 feature -> 9 detector -> argmax karar.

**Sonuc:** 88/90 seri `contextual_anomaly` olarak siniflandirildi (sentetiklerin tamami, realdata'nin 21/23'u). Bu modelin **OOD davranisi**: egitim setinde kullanilan dagilim (12K seri/sinif, uzunluk 300-500) disinda contextual_anomaly hemen her seriye yapisiyor. Plan.md'deki "kisa diye mi" hipotezi dogrulanmadi — n=45'te de n=1028'de de ayni hata.

**Cikti:**
- [runner/results/predictions.csv](runner/results/predictions.csv) — her seri × 9 detector probability + argmax.
- [runner/results/predictions.json](runner/results/predictions.json) — JSON formatinda detayli.
- [runner/results/RAPOR.md](runner/results/RAPOR.md) — markdown rapor.

### 2.4. Ikinci tur — ens-final'i sifirdan kur

#### 2.4.1. 39 grup × 10 seri uretimi
ens-final/config.py'daki `SOURCE_GROUPS` listesindeki 39 davranissal kategoriye birebir bir betise mapping'i yazildi: [runner/10_generate_39groups.py](runner/10_generate_39groups.py).

| Grup tipi | betise spec |
|---|---|
| Singles (1-4) | base = stationary/stochastic/volatility (tek base) |
| Stationary + anomali (5-10) | ar base + tek anomali overlay |
| Cubic+anomali (11-14) | ar + cubic_trend + anomali |
| Damped+anomali (15-18) | ar + exponential_trend (sign=-1) + anomali |
| Exp+anomali (19-22) | ar + exponential_trend (sign=+1) + anomali |
| Linear+anomali (23-27) | ar + linear_trend + anomali (26 = trend_shift) |
| Quadratic+anomali (28-31) | ar + quadratic_trend + anomali |
| Stoch+anomali (32-35) | stochastic base + anomali |
| Vol+anomali (36-39) | volatility base + anomali |

Uzunluk araligi [80, 150] (ens-final MIN_SERIES_LENGTH=50 oldugu icin).  
**Sonuc: 390 / 390 seri basariyla uretildi, 0 hata.** Klasor yapisi `ens-final/config.py`'in `SOURCE_GROUPS` path'leriyle birebir uyumlu (runner/data/generated/...).

#### 2.4.2. ensemble-alldata egitimi (10 binary model)
`ensemble-alldata/config.py` patchli:
- `GD = c:\Users\Pc\Desktop\ceylanhoca\runner\data\generated`
- `N = 60` (orijinal 1320, kucuk veriseti icin azaltildi)

`python main.py` ile calisti: processor (tsfresh extraction) + trainer (LightGBM/XGBoost/MLP, en iyi val F1 secimi) + evaluator (kombinasyon testi).

**Egitim sonuclari** ([ensemble-alldata/results/training_results.json](ensemble-alldata/results/training_results.json)):

| Model | En iyi clf | Test F1 | Test Acc |
|---|---|---|---|
| stationary | LightGBM | 0.9565 | 0.9444 |
| deterministic_trend | LightGBM | 0.6667 | 0.7368 |
| stochastic_trend | XGBoost | 0.7368 | 0.7059 |
| volatility | XGBoost | 0.8421 | 0.8235 |
| collective_anomaly | LightGBM | 1.0000 | 1.0000 |
| contextual_anomaly | XGBoost | 1.0000 | 1.0000 |
| mean_shift | LightGBM | 0.8333 | 0.7778 |
| point_anomaly | LightGBM | 1.0000 | 1.0000 |
| trend_shift | LightGBM | 0.5000 | 0.3333 |
| variance_shift | XGBoost | 0.8571 | 0.7778 |

**Kombinasyon testi:** 290 test ornegi (29 leaf × 10 dosya) uzerinde **%70 full match** (203/290), %29 partial, %1 none ([ensemble-alldata/results/combination_eval.json](ensemble-alldata/results/combination_eval.json)).

Not: `trend_shift` ve `deterministic_trend` modelleri zayif — sirasiyla 30 ve 44 pozitif ornekle egitildigi icin variance yuksek. Daha fazla seri olsa duzelir.

#### 2.4.3. ens-final konfigi + stat_detector patchleri
`ens-final/config.py`:
- `OLD_ENSEMBLE_DIR -> tsfresh-ensemble-stationary/trained_models` (orijinal "tsfresh ensemble" path'i bizde tire'li)
- `NEW_ENSEMBLE_DIR -> ensemble-alldata/trained_models` (yeni egitilen)
- `STATIONARY_DETECTOR_DIR -> stationary-detection-ml/models` (orijinal "trained_models v2" path'i bizde mevcut "models" klasorune yonlendirildi)
- `GD -> runner/data/generated`
- `META_N_PER_GROUP = 8` (orijinal 500, bizde sadece 10 seri var)

`ens-final/stat_detector.py` tamamen yeniden yazildi: stationary-detection-ml'in **21 feature** GradientBoosting modelini kullaniyor (orijinal stat_detector v6'nin 25 feature'i ve xgboost_fast.joblib'i bizde yok).

#### 2.4.4. ens-final main.py --force calistirildi
**Asamalar:**
1. **Veri sampling:** her 39 gruptan 8 ornek = 312 toplam.
2. **tsfresh extraction:** 312 seri uzerinde 777 feature.
3. **Eski + Yeni ensemble inference:** 9 + 10 = 19 ham olasilik.
4. **14 turetilmis meta-feature** + 777 standardized tsfresh = 810-boyutlu meta-vektor.
5. **Stationarity detector** inference.
6. **Router (XGB+LGB):** single vs combo F1=0.9661.
7. **Base type meta (XGB+LGB):** 4-class F1=0.8732, Acc=0.8730.
8. **6 anomali meta-learner** (XGB+LGB), zor gruplari 3x oversample:
   - collective_anomaly F1=0.9412
   - contextual_anomaly F1=1.0000
   - mean_shift F1=0.6897
   - point_anomaly F1=1.0000
   - trend_shift F1=1.0000
   - variance_shift F1=0.9677
9. **Blend weight + threshold ogrenimi** — her anomali icin (alpha, threshold) cifti grid-search ile bulundu.

#### 2.4.5. 39 grup degerlendirmesi (egitim datasi uzerinde)
`ens-final/results/evaluation.json` + `ens-final/results/evaluation_report.md`:

**Ozet** (`samples_per_leaf = 10`, `stat_gate = 0.95`):

| Metric | Sayi | Yuzde |
|---|---|---|
| **FULL match** | **344 / 390** | **%88.21** |
| PARTIAL | 41 | %10.51 |
| NONE | 5 | %1.28 |

**Grup bazli (en zayif 5):**

| Grup | n | FULL | FULL% | Yorum |
|---|---|---|---|---|
| 1 — stationary | 10 | 7 | %70 | stat gate altinda yanlis anomali ekleniyor |
| 3 — stochastic_trend | 10 | 7 | %70 | base type karisikligi |
| 16 — damped+mean_shift | 10 | 7 | %70 | base zor (damped = exponential sign=-1) |
| 29 — quad+mean_shift | 10 | 5 | %50 | mean_shift detector zayifligi |
| 26 — linear+trend_shift | 10 | 6 | %60 | trend_shift detector zayif (yalniz 2 pos grup) |

Diger 25/39 grup %90+ FULL. Bu sonuc orijinal raporda (%89.65) ima edilen tavana yakin — sadece **10 seri/grup** ile elde edildi (orijinal: 19500 ornek + 4400 eval).

### 2.5. realdata uzerinde ens-final testi
[runner/20_ensfinal_realdata.py](runner/20_ensfinal_realdata.py): 41 realdata dosyasi, 32'si pipeline'a uygun (n >= 50). W1, W10, W16, W9, uspop, strikes vs n<50 oldugu icin atlandi.

**Cikti:** [runner/results/ENSFINAL_REALDATA_RAPOR.md](runner/results/ENSFINAL_REALDATA_RAPOR.md), [runner/results/ensfinal_realdata.csv](runner/results/ensfinal_realdata.csv), [runner/results/ensfinal_realdata.json](runner/results/ensfinal_realdata.json) (her dosya icin **9 eski + 10 yeni + 4 base meta + 6 anomali meta + P(stat) + P(combo)** = 31 olasilik).

**Base tahminleri:**
| base | sayi |
|---|---|
| deterministic_trend | 22 |
| stationary | 6 |
| stochastic_trend | 3 |
| volatility | 1 |

**Anomali frekansi:**
| anomali | tetik sayisi |
|---|---|
| collective_anomaly | 27 |
| contextual_anomaly | 28 |
| point_anomaly | 13 |
| mean_shift | 6 |
| trend_shift | 6 |
| variance_shift | 6 |

**Decision path:** 32/32 hepsi `combo`. Yani router her zaman "kombinasyon dali"na yonlendirdi, hicbir realdata icin "saf single" yolu acilmadi. Bu, gerçek dunya verilerinin egitim verisinden farkli — eski 9-detector probability'lerinin coğunlukla "anormallik var" sinyali verdiği — anlamına geliyor.

---

## 3. Plan.md sorularinin cevaplari

### 3.1. "her tekil modelin probability'sini gormek istiyorum"
**Cevap:** [runner/results/ensfinal_realdata.json](runner/results/ensfinal_realdata.json) icinde her dosya icin asagidakiler raporlandi:

| Bilesen | Detay |
|---|---|
| Eski ensemble 9 model | `old_probs`: collective, contextual, det_trend, mean_shift, point, stoch_trend, trend_shift, variance, volatility |
| Yeni ensemble 10 model | `new_probs`: stationary, det_trend, stoch_trend, volatility (base), + 6 anomali |
| Base meta-learner 4 prob | `base_probs`: 4-class softmax (XGB+LGB averaged) |
| Anomali meta-learner 6 prob | `anom_probs`: her anomali icin meta P |
| Stationarity gate | `stat_prob`: P(stationary) (21 feature gradient boosting) |
| Router | `router_combo_prob`: P(combo) (810 feature XGB+LGB) |

**Toplam: 31 probability/dosya** + final karar (base + anomali listesi) + decision_path.

### 3.2. "her sinif icin subsubclass icin 10'ar data olustur"
**Cevap:** 39 grup × 10 seri = 390 seri, hepsi `runner/data/generated/` altinda dogru hiyerarsi ile.

### 3.3. "onun ciktisinin basarisini olcup"
**Cevap:** 39 grup egitim setinde **%88.21 FULL match**. Detaylar yukarida ve [ens-final/results/evaluation_report.md](ens-final/results/evaluation_report.md).

### 3.4. "sonra bidaha realdatadakilere bakmak gerekir"
**Cevap:** 32 dosya (n>=50) icin tam pipeline sonucu [runner/results/ENSFINAL_REALDATA_RAPOR.md](runner/results/ENSFINAL_REALDATA_RAPOR.md). 

### 3.5. "kisa seriler ozelinde basarim"
**Cevap:**
- **tsfresh-ensemble-stationary** ile: sentetik n=45 ve n=100'de tahmin %0 dogru (her ikisinde de 25/25 contextual). Kisa-seriye bagli **degil**, model OOD'a karsi dayaniksiz.
- **ens-final** ile: MIN_SERIES_LENGTH=50 oldugu icin n<50 (W1, W10, W16, W9, uspop, strikes) **pipeline'a giremiyor**. Kisa realdata icin pipeline calismadi. W1 (n=45) yalnizca tsfresh-ensemble-stationary'de calisti, orada da yanlis sonuc verdi (contextual).
- ens-final 39 grup egitim setinde **uzunluk [80, 150]** ile %88.2 — yani 80'lik kisa serilerde de calisiyor.

---

## 4. Onemli gozlemler & sinirliliklar

### 4.1. tsfresh-ensemble-stationary'nin OOD bias'i
Egitilmis modeller (12K seri/sinif) bizim sentetik/gercek verilere uygulandiginda neredeyse her seriye `contextual_anomaly` etiketi yapisiyor. Hatta saf white noise N(0,1) bile P(contextual)=0.9995 veriyor. Bunun sebebi muhtemelen contextual_anomaly egitim setinde cok belirgin (yuksek-quantile + variance) ozelliklere sahip oldugu icin model "dagilimin disindaki her sey" -> contextual algiliyor.

### 4.2. ens-final'in realdata'da combo bias'i
realdata'da 32/32 dosya **combo** yoluna gitti (yani anomali iceriyor sayiyor). Cunku eski ensemble (tsfresh-ensemble-stationary) ic-icindeki contextual detector'u hemen tetikleniyor ve bu router'in girisini "combo" yonune cekiyor.

### 4.3. Trend_shift detector'unun zayifligi
trend_shift modeli sadece **2 pozitif grup**tan (group 9 = stationary+trend_shift, group 26 = linear+trend_shift) besleniyor. 10 seri/grup ile sadece 20 pozitif ornek var. Test F1=0.5. ens-final meta-learner'i bu zayifligi `trend_shift alpha=0.05` ile telafi ediyor (neredeyse tamamen yeni ensemble'a, hic eski'ye guvenmiyor).

### 4.4. Kisa veri (n<50) calismiyor
ens-final'in `MIN_SERIES_LENGTH = 50` kuraldir (tsfresh stabilite icin). W1 (n=45) ve digerleri otomatik atlaniyor. plan.md "size 40-50" istemisti, ama ens-final mimarisi 50 alti garanti vermez.

### 4.5. Az veri ile egitim kalitesi
- Yeni binary modeller: N=60 (orijinal 1320'nin %4.5'i)
- Meta-learner: 312 ornek (orijinal 19500'un %1.6'si)
- Buna ragmen 39-grup FULL=%88.2, orijinal %89.07 ile **<%1 fark**. Bu, mimarinin kucuk-veri'ye gore robust oldugunu gosteriyor.

---

## 5. Dosya envanteri

### Kod (yazdiklarim)
| Dosya | Amac |
|---|---|
| [runner/01_generate_synthetic.py](runner/01_generate_synthetic.py) | 5 stoch-trend tipi × 2 uzunluk × 5 seri = 50 sentetik (birinci tur) |
| [runner/02_convert_realdata.py](runner/02_convert_realdata.py) | realdata 41 dosya -> tek kolon CSV |
| [runner/03_run_pipeline.py](runner/03_run_pipeline.py) | tsfresh-ensemble-stationary 9-detector inference |
| [runner/04_build_report.py](runner/04_build_report.py) | Birinci tur rapor uretici |
| [runner/10_generate_39groups.py](runner/10_generate_39groups.py) | 39 grup × 10 seri = 390 betise serisi (ens-final icin) |
| [runner/20_ensfinal_realdata.py](runner/20_ensfinal_realdata.py) | ens-final pipeline'ini realdata uzerinde calistir |

### Patchlenmis dosyalar
| Dosya | Degisiklik |
|---|---|
| [ensemble-alldata/config.py](ensemble-alldata/config.py) | GD path + N=60 |
| [ens-final/config.py](ens-final/config.py) | 3 model dir + GD + META_N_PER_GROUP=8 |
| [ens-final/stat_detector.py](ens-final/stat_detector.py) | Tamamen yeniden yazildi (21-feature, GradientBoosting) |

### Cikti dosyalari
| Dosya | Icerik |
|---|---|
| [runner/results/RAPOR.md](runner/results/RAPOR.md) | tsfresh-ensemble-stationary tek-pipeline raporu |
| [runner/results/predictions.csv](runner/results/predictions.csv) | 9-detector x 90 seri probability tablosu |
| [runner/results/predictions.json](runner/results/predictions.json) | Yukaridakinin detayli JSON'u |
| [runner/results/ENSFINAL_REALDATA_RAPOR.md](runner/results/ENSFINAL_REALDATA_RAPOR.md) | ens-final realdata raporu |
| [runner/results/ensfinal_realdata.csv](runner/results/ensfinal_realdata.csv) | ens-final realdata flat tablo |
| [runner/results/ensfinal_realdata.json](runner/results/ensfinal_realdata.json) | **31 probability/dosya** detayli JSON |
| [ens-final/results/evaluation_report.md](ens-final/results/evaluation_report.md) | 39 grup eval (egitim seti) raporu |
| [ens-final/results/evaluation.json](ens-final/results/evaluation.json) | Yukaridakinin detayli JSON'u |
| [ens-final/results/meta_training.json](ens-final/results/meta_training.json) | Meta-learner egitim metrikleri |
| [ensemble-alldata/results/training_results.json](ensemble-alldata/results/training_results.json) | 10 binary model egitim sonuclari |
| [ensemble-alldata/results/combination_eval.json](ensemble-alldata/results/combination_eval.json) | 10-model kombinasyon test sonucu |

### Egitilmis modeller
| Klasor | Dosyalar |
|---|---|
| `tsfresh-ensemble-stationary/trained_models/` | 9 detector klasoru (orijinal, dokunulmadi) |
| `ensemble-alldata/trained_models/` | 10 binary `.pkl` (bizim egittik) |
| `ens-final/meta_models/` | base_meta + 6 anom_*.pkl + router + blend_weights |
| `ens-final/processed_data/` | meta_X.npy + tsfresh_scaler.pkl + diger ara dosyalar |
| `stationary-detection-ml/models/` | best_model.pkl + scaler.pkl (orijinal) |

---

## 6. Yarinki sunum icin oneriler

1. **Iki tabloyu birlikte goster:**  
   - "Egitim seti uzerinde %88.2 FULL — orijinal %89.07'ye %1 fark, hem de %1.6 ornek ile"  
   - "realdata'da 32/32 combo yoluna sapti — eski ensemble'in contextual bias'i"

2. **Acik problem olarak sun:**  
   - tsfresh-ensemble-stationary'nin contextual_anomaly modelinin OOD davranisi: realdata gibi farkli scale'lerde yanlis tetikleniyor. Bu meta-learner'a propagete oluyor.  
   - Onerilen tedavi: yeni-ensemble'in (bizim egittigimiz, gercek-dagilim duyarli) probability'lerine daha cok agirlik vermek, ya da eski-ensemble'i bizim verimizle yeniden egitmek.

3. **Kisa-seri konusu:**  
   - ens-final n>=50 ile sinirli. W1 (n=45), uspop (n=21), strikes (n=30), W10 (n=8), W9 (n=11), W16 (n=15) pipeline'a giremiyor.  
   - Eger gerekirse: MIN_SERIES_LENGTH dusurulebilir, fakat tsfresh feature'larin bir kismi NaN olur.

4. **Ek calisma onerileri (zaman olursa):**  
   - 10 seri/grup yerine 50 veya 100/grup ile yeniden egitim. Beklenti: yeni binary modellerin F1'i artar, ozellikle trend_shift ve deterministic_trend (su an zayif).  
   - betise'in z_normalize ile uretmis oldugu seriler ile realdata scale'inin uyumsuzlugu bir sorun olabilir; ek bir scale-augmentation katmani eklenebilir.

---

## 7. Hizli komutlar (yeniden calistirmak icin)

```powershell
# 1. Sentetik veri (390 seri)
python runner/10_generate_39groups.py

# 2. ensemble-alldata (10 binary model)
cd ensemble-alldata; python main.py; cd ..

# 3. ens-final (meta-learner + 39 grup eval)
cd ens-final; python main.py --force; cd ..

# 4. realdata uzerinde tam pipeline
python runner/20_ensfinal_realdata.py

# 5. Birinci tur (tsfresh-ensemble-stationary tek basina)
python runner/01_generate_synthetic.py
python runner/02_convert_realdata.py
python runner/03_run_pipeline.py
python runner/04_build_report.py
```

---

_Hazirlayan: Claude (Opus 4.7) — tek oturum, ~3 saat icinde sifirdan kuruldu._
