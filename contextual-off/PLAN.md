# contextual-off Pipeline Plani

## Amac
ts-proje'de mevcut tum cesitli bias kaynaklarindan (ozellikle eski ensemble'in
contextual_anomaly OOD bias'i) kurtulmak icin **contextual_anomaly siniflari
tamamen kaldirilmis** bir varyant kurmak ve ayni egitim metoduyla yeniden
denemek. Sonuc, gercek-dunya verisinde contextual'sız bir baseline saglar.

## Cikarilacak unsurlar

### Eski ensemble (tsfresh-ensemble-stationary) — 9 → 8 detector
- `contextual_anomaly` detector'unu YUKLEMEYECEGIZ (model dosyalari kalır ama
  CLASSES listesinden cikarilacak)
- Inference'da 8 detector probability uretilecek

### Yeni ensemble (ensemble-alldata) — 10 → 9 model
- `contextual_anomaly` binary modelini **egitmeyecegiz**
- Sadece 9 binary model (4 base + 5 anomali)
- ANOMALY_MODELS: collective, mean_shift, point_anomaly, trend_shift, variance_shift

### ens-final — meta-stacking
- ANOM_LABELS: 6 → **5** anomali
- 39 grup → **38 grup** (Grup 6 = saf contextual_anomaly cikarildi)
  - Combinations'da contextual_anomaly+X yok (zaten yok), o yuzden sadece grup 6 cikar
- Meta-vektor boyutu: 19 → **17 ham olasilik** (8 eski + 9 yeni) + 14 derived + 777 tsfresh = **808 boyut**
- GROUP_EXPECTED'tan grup 6 cikarilacak

## Klasor yapisi

```
contextual-off/
├── PLAN.md                          # bu dosya
├── ensemble-alldata/                # config + main + trainer kopya (modifie)
│   ├── config.py                    # ALL_MODEL_NAMES'ten contextual cikarildi
│   ├── processor.py                 # (kaynak repo'dan kopya)
│   ├── trainer.py                   # (kaynak repo'dan kopya)
│   ├── main.py                      # (kaynak repo'dan kopya)
│   ├── evaluator.py                 # (kaynak repo'dan kopya)
│   ├── processed_data/              # tsfresh feature cache
│   ├── trained_models/              # 9 binary .pkl
│   └── results/
│       └── training_results.json
├── ens-final/                       # config + tum scriptler kopya (modifie)
│   ├── config.py                    # OLD_CLASSES, NEW_ALL_MODELS, ANOM_LABELS, SOURCE_GROUPS modifie
│   ├── processor.py                 # (kopya, modifie: 8 old + 9 new)
│   ├── trainer.py                   # (kopya)
│   ├── evaluator.py                 # (kopya, modifie: 5 anomali)
│   ├── stat_detector.py             # (kopya — degismiyor)
│   ├── main.py                      # (kopya)
│   ├── meta_models/                 # base_meta + 5 anom + router + blend
│   ├── processed_data/
│   └── results/
└── runner/                          # bizim yeni scriptler
    ├── 20_realdata.py               # realdata icin ens-final pipeline (no contextual)
    ├── 22_synthetic.py              # sentetik icin
    ├── 30_compare.py                # ground truth karsilastirma
    ├── 40_build_readme.py           # contextual-off README
    └── results/
        ├── ensfinal_realdata.json
        ├── ensfinal_short.json
        ├── ensfinal_synthetic.json
        ├── label_comparison.csv
        └── LABEL_KARSILASTIRMA.md
```

## Veri kaynagi
- **Sentetik egitim:** `c:\Users\Pc\Desktop\ceylanhoca\runner\data\generated\`
  altindaki 380 seri (39 grup × 10, AMA Grup 6 = `contextual_anomaly/`
  klasoru atlanir)
- **realdata test:** `c:\Users\Pc\Desktop\ceylanhoca\runner\data\realdata\`
  (degismiyor)
- **Sentetik kisa stochastic test:** `c:\Users\Pc\Desktop\ceylanhoca\runner\data\synthetic\`

## Adim adim plan

### Faz 1 — Klasor ve config kurulumu
1. `contextual-off/ensemble-alldata/` olustur:
   - `config.py` modifie: ALL_MODEL_NAMES = 9 model (contextual cikar);
     MODEL_POSITIVE_GROUPS'tan contextual_anomaly key'i cikar;
     SOURCE_GROUPS'tan Grup 6 cikar; GD path runner/data/generated; N=60 mi
     onceki ile ayni
   - processor.py, trainer.py, main.py, evaluator.py: kaynak repo'dan kopya
2. `contextual-off/ens-final/` olustur:
   - `config.py` modifie: 38 grup, 5 anomali, paths contextual-off'a yonelt
   - processor.py modifie: 8 old + 9 new, 14 derived hala 19 yerine 17 prob'tan
     turetilir (compute_derived_features icindeki 'contextual' referanslari kontrol)
   - evaluator.py modifie: ANOM_LABELS 5, threshold mantigi sabit
   - stat_detector.py: degisiklik yok (sadece kopya)
   - main.py, trainer.py: kopya
3. Eski ensemble icin: `contextual-off` ic'inde KOPYA yok — ens-final config'i
   `c:\Users\Pc\Desktop\ceylanhoca\tsfresh-ensemble-stationary\trained_models\`
   path'ine isaret eder ama YALNIZCA 8 detector'u yukler

### Faz 2 — ensemble-alldata yeniden egitim
1. `cd contextual-off/ensemble-alldata; python main.py`
2. Cikti: 9 binary .pkl model
3. Beklenen sure: ~5-10 dakika

### Faz 3 — ens-final yeniden egitim
1. `cd contextual-off/ens-final; python main.py --force`
2. Cikti:
   - Meta features: 808 boyut
   - 1 base meta-learner (XGB+LGB, 4-class)
   - 5 anomali meta-learner (XGB+LGB binary)
   - Router (XGB+LGB)
   - Blend weights (5 anomali)
3. 38-grup eval raporu
4. Beklenen sure: ~5-10 dakika

### Faz 4 — Inference scriptleri
1. `runner/22_synthetic.py`: 50 sentetik -> 17 olasilik + meta + karar
2. `runner/20_realdata.py`: realdata (n>=50) ile beraber kisa olanlar (20<=n<50)
3. `runner/30_compare.py`: label karsilastirma (contextual GT olan dosyalar otomatik
   atlanir — bizde yok zaten cunku contextual'i kaldirdik)
4. `runner/40_build_readme.py`: contextual-off README

### Faz 5 — Karsilastirma raporu
Ground truth karsilastirma + on-vs-after tablosu:
- Sentetik accuracy: %72 → ?
- realdata FULL: 3 → ?
- Base accuracy: 8/20 → ?

## Onemli teknik kararlar

1. **compute_derived_features**: ens-final/processor.py'da 14 derived feature
   eski ensemble'in 9 olasiligindan ve yeni ensemble'in 10 olasiligindan
   uretiliyor. Bizim sürumde 8 + 9 = 17 olasilik. Function'in icini incele;
   sabit indeks varsa (orn `new_probs[5] = contextual_anomaly_index`) duzelt.

2. **Path overrides**: contextual-off/ens-final/config.py icinde
   `NEW_ENSEMBLE_DIR = contextual-off/ensemble-alldata/trained_models`
   `OLD_ENSEMBLE_DIR = c:\Users\Pc\Desktop\ceylanhoca\tsfresh-ensemble-stationary\trained_models`
   (eski ensemble degisiklik yok, sadece contextual yuklenmiyor)
   `STATIONARY_DETECTOR_DIR = c:\Users\Pc\Desktop\ceylanhoca\stationary-detection-ml\models`

3. **Ground truth karsilastirma**:
   - `contextual_anomaly` etiketli realdata var mi? PDF'i incele.
   - Datasets.pdf'te `contextual_anomaly` olarak etiketlenmis dosya YOK.
     (En cok mevsimsel + breaks gormus, bunlar contextual'a mapleniyordu.)
   - Bu yuzden ground truth karsilastirma da contextual'sız tutarli.

## Hedef metrikler

| Metrik | Once (ts-proje) | Hedef (contextual-off) |
|---|---|---|
| Sentetik base acc | %72 | >=%72 |
| realdata FULL | 3/20 | >=3/20 (umit: 5+) |
| Base type dogru | 8/20 | >=8/20 |
| 38-grup eval FULL | (yeni) | hedef: >=%80 |

contextual_anomaly bias'inin kalkmasi su iyilesmeyi getirir:
- airpass, INDPRO, deaths, sunspots gibi seasonal seriler artik "contextual"
  etiketi alamayacagi icin daha temiz tahmin
- Meta-learner'in 14 derived feature'i 17 ham prob'tan hesaplanacak (daha az
  gurultu)

## Risk

- Old ensemble'in contextual'sız 8-detector'u meta-learner icin yeterli sinyal
  saglar mi? — Onceden 9 detector ile %88.2 idi, 8 ile birkac puan kaybedebiliriz
- Saf stationary tanima daha kotu olabilir cunku contextual_anomaly modeli bazi
  durumlarda stationary serileri "stationary degil" sinyali olarak hizmet
  ediyordu — bu bias kaldirildiginda diger detector'lere yuk biner
