# ens-final Pipeline: KISA realdata (n<50) Sonuclari

Toplam 5 kisa dosya. (n<20 olanlar tsfresh stabilite icin atlandi.)


## Ozet Tablo

| dosya | n | yol | base | anomaliler | P(stat) | P(combo) |
|---|---|---|---|---|---|---|
| uspop.csv | 21 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.014 | 0.951 |
| strikes.csv | 30 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.007 | 0.982 |
| W1.csv | 45 | combo | stochastic_trend | collective_anomaly, variance_shift | 0.051 | 0.997 |
| W15-1.csv | 46 | combo | stochastic_trend | collective_anomaly | 0.824 | 0.938 |
| W15-2.csv | 46 | combo | stochastic_trend | collective_anomaly | 0.839 | 0.916 |


## W1 Detayli (plan.md'de ozellikle istenmis)

**n = 45**
**Tahmin:** stochastic_trend + ['collective_anomaly', 'variance_shift']
**Path:** combo, P(stat)=0.0507, P(combo)=0.9967

### Eski ensemble 9 detector P(class=1):
```
  collective_anomaly       0.0
  contextual_anomaly       0.5718
  deterministic_trend      0.002
  mean_shift               0.0
  point_anomaly            0.0001
  stochastic_trend         0.0001
  trend_shift              0.0
  variance_shift           0.0001
  volatility               0.0
```

### Yeni ensemble 10 model P(class=1):
```
  stationary               0.3108
  deterministic_trend      0.2191
  stochastic_trend         0.1302
  volatility               0.6224
  collective_anomaly       0.9665
  contextual_anomaly       0.0391
  mean_shift               0.4111
  point_anomaly            0.0021
  trend_shift              0.5
  variance_shift           0.9115
```

### Base type meta-learner (4-class softmax):
```
  stationary               0.0778
  deterministic_trend      0.2812
  stochastic_trend         0.3966
  volatility               0.2445
```

### Anomali meta-learner (6 binary):
```
  collective_anomaly       0.9767
  contextual_anomaly       0.0052
  mean_shift               0.0023
  point_anomaly            0.0034
  trend_shift              0.0032
  variance_shift           0.3436
```

