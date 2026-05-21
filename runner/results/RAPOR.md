# tsfresh-ensemble-stationary Pipeline Raporu

Pipeline: 9 binary detector (one-vs-rest), her detector tsfresh 777-feature uzerinde calisir.
Karar: argmax(P_collective, P_contextual, P_det_trend, P_mean_shift, P_point, P_stoch_trend, P_trend_shift, P_var_shift, P_volatility).

Toplam 90 seri (synthetic + realdata) test edildi.

---

## 1. Sentetik (betise) Sonuclar - Stochastic Trend tiplere gore

Beklenen sinif: `stochastic_trend` (hepsi icin)

| kind | n | seri | accuracy | ort. P(stoch_trend) | ort. P(pred) |
|---|---|---|---|---|---|
| ari | 45 | 5 | 0.00% | 0.004 | 1.000 |
| ari | 100 | 5 | 0.00% | 0.007 | 1.000 |
| arima | 45 | 5 | 0.00% | 0.006 | 1.000 |
| arima | 100 | 5 | 0.00% | 0.002 | 1.000 |
| ima | 45 | 5 | 0.00% | 0.016 | 1.000 |
| ima | 100 | 5 | 0.00% | 0.024 | 1.000 |
| rw | 45 | 5 | 0.00% | 0.001 | 1.000 |
| rw | 100 | 5 | 0.00% | 0.010 | 1.000 |
| rwd | 45 | 5 | 0.00% | 0.001 | 1.000 |
| rwd | 100 | 5 | 0.00% | 0.003 | 1.000 |

### Tahmin sinifi dagilimi (sentetik):

```
pred       contextual_anomaly
kind  n                      
ari   45                    5
      100                   5
arima 45                    5
      100                   5
ima   45                    5
      100                   5
rw    45                    5
      100                   5
rwd   45                    5
      100                   5
```

---

## 2. realdata Tahminleri

Beklenen sinif yok (labeled degil); pipeline'in ne dedigini gosterir.

| dosya | n | pred | P(pred) | P(stoch) | P(context) | P(volat) | P(det_trend) |
|---|---|---|---|---|---|---|---|
| W10.csv | 8 | contextual_anomaly | 0.926 | 0.000 | 0.926 | 0.000 | 0.030 |
| W9.csv | 11 | contextual_anomaly | 0.918 | 0.001 | 0.918 | 0.000 | 0.059 |
| W16.csv | 15 | contextual_anomaly | 0.941 | 0.000 | 0.941 | 0.000 | 0.039 |
| uspop.csv | 21 | deterministic_trend | 0.510 | 0.002 | 0.303 | 0.000 | 0.510 |
| strikes.csv | 30 | contextual_anomaly | 0.356 | 0.000 | 0.356 | 0.000 | 0.132 |
| W1.csv | 45 | contextual_anomaly | 0.572 | 0.000 | 0.572 | 0.000 | 0.001 |
| W15-1.csv | 46 | contextual_anomaly | 0.980 | 0.000 | 0.980 | 0.001 | 0.010 |
| W15-2.csv | 46 | contextual_anomaly | 0.980 | 0.000 | 0.980 | 0.000 | 0.003 |
| W12-1.csv | 54 | contextual_anomaly | 0.926 | 0.002 | 0.926 | 0.000 | 0.202 |
| W12-2.csv | 54 | contextual_anomaly | 0.954 | 0.011 | 0.954 | 0.000 | 0.063 |
| W5.csv | 71 | contextual_anomaly | 0.948 | 0.000 | 0.948 | 0.000 | 0.042 |
| deaths.csv | 72 | deterministic_trend | 0.785 | 0.003 | 0.356 | 0.000 | 0.785 |
| W13-2.csv | 82 | contextual_anomaly | 0.330 | 0.006 | 0.330 | 0.000 | 0.257 |
| W13-1.csv | 82 | contextual_anomaly | 0.942 | 0.005 | 0.942 | 0.001 | 0.286 |
| W13-3.csv | 82 | contextual_anomaly | 0.330 | 0.000 | 0.330 | 0.000 | 0.104 |
| W13-4.csv | 82 | contextual_anomaly | 0.944 | 0.014 | 0.944 | 0.000 | 0.129 |
| W3.csv | 82 | contextual_anomaly | 0.356 | 0.000 | 0.356 | 0.000 | 0.172 |
| W13-5.csv | 82 | contextual_anomaly | 0.330 | 0.000 | 0.330 | 0.000 | 0.229 |
| W14.csv | 87 | contextual_anomaly | 0.942 | 0.002 | 0.942 | 0.000 | 0.031 |
| GermanGNP.csv | 88 | contextual_anomaly | 0.330 | 0.002 | 0.330 | 0.000 | 0.033 |
| e1.csv | 92 | contextual_anomaly | 0.330 | 0.006 | 0.330 | 0.000 | 0.052 |
| German_consumption.csv | 93 | contextual_anomaly | 0.353 | 0.009 | 0.353 | 0.000 | 0.047 |
| sunspots.csv | 100 | contextual_anomaly | 0.413 | 0.001 | 0.413 | 0.000 | 0.081 |
| RealInt_dataframe.csv | 103 | contextual_anomaly | 1.000 | 0.007 | 1.000 | 0.000 | 0.000 |
| e2.csv | 104 | contextual_anomaly | 0.303 | 0.000 | 0.303 | 0.000 | 0.080 |
| US_investment.csv | 104 | contextual_anomaly | 1.000 | 0.000 | 1.000 | 0.000 | 0.001 |
| German_income.csv | 113 | contextual_anomaly | 0.936 | 0.006 | 0.936 | 0.000 | 0.116 |
| W6.csv | 114 | contextual_anomaly | 0.936 | 0.001 | 0.936 | 0.000 | 0.141 |
| Polish_productivity.csv | 117 | contextual_anomaly | 0.949 | 0.008 | 0.949 | 0.027 | 0.072 |
| wine.csv | 142 | contextual_anomaly | 0.330 | 0.013 | 0.330 | 0.000 | 0.076 |
| airpass.csv | 144 | contextual_anomaly | 0.303 | 0.019 | 0.303 | 0.000 | 0.174 |
| W8.csv | 150 | contextual_anomaly | 0.382 | 0.002 | 0.382 | 0.000 | 0.077 |
| W11.csv | 166 | contextual_anomaly | 0.953 | 0.001 | 0.953 | 0.000 | 0.017 |
| W2.csv | 302 | contextual_anomaly | 0.386 | 0.014 | 0.386 | 0.000 | 0.093 |
| UNRATE.csv | 372 | contextual_anomaly | 0.330 | 0.005 | 0.330 | 0.000 | 0.017 |
| INDPRO.csv | 372 | contextual_anomaly | 0.353 | 0.000 | 0.353 | 0.000 | 0.074 |
| beer.csv | 422 | contextual_anomaly | 0.936 | 0.005 | 0.936 | 0.000 | 0.427 |
| soi_dataframe.csv | 453 | contextual_anomaly | 0.998 | 0.015 | 0.998 | 0.000 | 0.000 |
| NP_AWHours.csv | 479 | contextual_anomaly | 0.356 | 0.001 | 0.356 | 0.000 | 0.131 |
| NP_xetradax_returns100.csv | 1028 | contextual_anomaly | 0.999 | 0.009 | 0.999 | 0.000 | 0.002 |

---

## 3. Her Detector'un Ortalama Probability Dagilimi

Sentetik (hepsi stoch_trend), realdata ve gruplu ortalamalar.

| detector | sentetik ort. | realdata ort. | sentetik max | realdata max |
|---|---|---|---|---|
| collective_anomaly | 0.000 | 0.000 | 0.000 | 0.000 |
| contextual_anomaly | 1.000 | 0.655 | 1.000 | 1.000 |
| deterministic_trend | 0.000 | 0.120 | 0.001 | 0.785 |
| mean_shift | 0.001 | 0.000 | 0.012 | 0.004 |
| point_anomaly | 0.000 | 0.000 | 0.000 | 0.000 |
| stochastic_trend | 0.007 | 0.004 | 0.098 | 0.019 |
| trend_shift | 0.000 | 0.000 | 0.000 | 0.000 |
| variance_shift | 0.001 | 0.000 | 0.023 | 0.003 |
| volatility | 0.000 | 0.001 | 0.000 | 0.027 |

---

## 4. Kisa-seri (n<=100) Performans Analizi

Kisa serilerin (n<=100) sayisi: 73

### Sentetik kisa-seri (n=45 vs n=100):

- n=45: accuracy=0.00%
- n=100: accuracy=0.00%

### Sentetik n=45'te tahmin sinifi dagilimi:

```
pred
contextual_anomaly    25
```


### Sentetik n=100'de tahmin sinifi dagilimi:

```
pred
contextual_anomaly    25
```


### realdata kisa (n<=100) tahmin sinifi dagilimi (23 dosya):

```
pred
contextual_anomaly     21
deterministic_trend     2
```


### W1 (n=45) detayli probability'leri:

```
  P_collective_anomaly       = 0.0000
  P_contextual_anomaly       = 0.5718
  P_deterministic_trend      = 0.0011
  P_mean_shift               = 0.0000
  P_point_anomaly            = 0.0000
  P_stochastic_trend         = 0.0000
  P_trend_shift              = 0.0000
  P_variance_shift           = 0.0003
  P_volatility               = 0.0000

  ARGMAX -> contextual_anomaly  (P=0.5718)
```


---

## 5. Gozlemler

Tum verisetinde tahmin sinifi dagilimi:
```
pred
contextual_anomaly     88
deterministic_trend     2
```


### Onemli not

- Model neredeyse her seri icin yuksek `P(contextual_anomaly)` veriyor.
- Bu modelin egitim setinde (sentetik 12K seri/sinif, uzunluk 300-500) contextual_anomaly siniflarinin
  cok belirgin (ayrismis) sinyallere sahip oldugunu, gercek/farkli uzunlukta veride yanlis bir sekilde
  bu sinifin tetiklendigini gosteriyor (OOD davranisi).
- Bu nedenle kisa seriler ozelinde, kisa-seri ozellikle sorun degil — model her uzunlukta benzer hata yapiyor.
- `stochastic_trend` detector'u sentetik random-walk/ARIMA serilerinde bile P~0 verdi:
  modelin egitim datasiyla bizim uretti(gimiz daginim arasinda buyuk fark var.
