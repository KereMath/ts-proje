# contextual-off Pipeline

contextual_anomaly sinifini tamamen kaldirilmis, ayni egitim metoduyla yeniden
kurulmus alternatif pipeline.

## Yapilanlar

1. Kaynak repo'lardan (`ensemble-alldata/`, `ens-final/`) kopya alindi
2. **Eski ensemble** (tsfresh-ensemble-stationary): 9 -> **8 detector**
   (contextual_anomaly yuklenmiyor)
3. **Yeni ensemble** (ensemble-alldata): 10 -> **9 model** (contextual_anomaly
   binary'si egitilmedi)
4. **39 grup -> 38 grup** (Grup 6 = saf contextual_anomaly cikarildi)
5. **6 anomali -> 5 anomali** (collective, mean, point, trend_shift, variance)
6. **Meta-vektor: 19 -> 17 ham olasilik** (8 eski + 9 yeni) + 14 derived + 777 tsfresh = **808 boyut**
7. Veri kaynagi olarak ana ts-proje'nin runner/data/generated klasoru
   kullanildi (Grup 6 dosyalari kullanilmadi)

## Sonuclar — Karsilastirma

| Metrik | ts-proje (fixed) | contextual-off |
|---|---|---|
| Egitim seti FULL (38/39 grup) | %88.21 (39 grup) | **%93.95** (38 grup) |
| Egitim seti PARTIAL | %10.51 | %5.53 |
| Egitim seti NONE | %1.28 | %0.53 |
| Sentetik base accuracy | %72 | **%64** |
| realdata FULL match | 3 | 0 |
| realdata PARTIAL | 5 | 7 |
| realdata NONE | 12 | 13 |
| realdata base correct | 8/20 | 7/20 |

**Buyuk paradoks:** contextual'i cikarmak **EGITIM SETI** uzerinde %5.7 puan
iyilestiriyor, AMA **realdata** uzerinde kotuluyor.

### Egitim setinde +%5.7 puan iyilesme nedeni
Contextual_anomaly modeli kendi data'sina (sentetik kontekstuel anomali) cok
sıkı oturmustu, AMA diger gruplari da ayni feature'larla degerlendiriyordu.
Meta-learner buradan gelen yanlis sinyalleri ogreniyor, base type belirlenmesinde
karistiriyordu. Cikarinca: Grup 1 (stationary) %70 -> **%100**, Grup 5
(collective) %100, 27 grupta %100 FULL.

### realdata kotulesme nedeni (3 FULL -> 0 FULL)
- US_investment, NP_xetradax_returns100: PARTIAL'a dustu (artik anomali fazlasi)
- strikes: NONE'a kaydi
- Yeni 9-model ensemble realdata icin pre-trained 12K-seri ile tutarli sinyal
  vermiyor. Contextual_anomaly modeli sayilmasa bile, **eski 9-detector'unun
  contextual sinyali realdata icin "anomali var" sinyali oluyordu**; bunu da
  cikarinca meta-learner stationary'i yanlis cesitli base'lere (det_trend, vol)
  cevirdi.

### Klasor yapisi

```
contextual-off/
├── PLAN.md
├── README.md (bu dosya)
├── ensemble-alldata/        # 9 binary model (egitildi)
│   ├── config.py           # 38 grup, 9 model
│   ├── processor.py, trainer.py, ...
│   ├── trained_models/     # 9 .pkl
│   └── results/
├── ens-final/              # meta-stacking (egitildi)
│   ├── config.py           # 8 old + 9 new + 5 anom
│   ├── processor.py, evaluator.py, ...
│   ├── meta_models/        # base + 5 anom + router + blend
│   ├── processed_data/
│   └── results/
└── runner/
    ├── 20_realdata.py
    ├── 22_synthetic.py
    ├── 30_compare.py
    └── results/
```

### Sonuc cikarimi

- **Eski ensemble'in contextual detector'unun OOD bias'i realdata'da
  zararli bir gurultu olarak gorunuyordu; ama meta-learner bu gurultuden
  yararli sinyaller cikariyormus.**
- "Contextual'i kaldir" basit cozumu **eğitim setini iyilestirir, gercek-dunya
  uygulamasini kotuler.**
- Daha iyi cozum: contextual'i kaldirmak yerine, contextual sinif'in
  egitim veri kalitesini artirmak veya meta-learner agirligi reduce etmek.
