# ens-final Pipeline: realdata Sonuclari

Toplam 32 realdata dosyasi pipeline'dan gecti.


## Tahmin Tablosu

| dosya | n | yol | base | anomaliler | P(stat) | P(combo) |
|---|---|---|---|---|---|---|
| W12-1.csv | 54 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.003 | 0.946 |
| W12-2.csv | 54 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.002 | 0.969 |
| W5.csv | 71 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.001 | 0.995 |
| deaths.csv | 72 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.004 | 0.997 |
| W13-1.csv | 82 | combo | deterministic_trend | contextual_anomaly | 0.001 | 0.988 |
| W13-2.csv | 82 | combo | deterministic_trend | contextual_anomaly | 0.002 | 0.996 |
| W13-3.csv | 82 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.002 | 0.993 |
| W13-4.csv | 82 | combo | deterministic_trend | contextual_anomaly | 0.005 | 0.998 |
| W13-5.csv | 82 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.002 | 0.989 |
| W3.csv | 82 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.002 | 0.991 |
| W14.csv | 87 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.004 | 0.996 |
| GermanGNP.csv | 88 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.004 | 0.994 |
| e1.csv | 92 | combo | stochastic_trend | collective_anomaly, contextual_anomaly | 0.003 | 0.988 |
| German_consumption.csv | 93 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.005 | 0.997 |
| sunspots.csv | 100 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.013 | 0.998 |
| RealInt_dataframe.csv | 103 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.004 | 0.999 |
| e2.csv | 104 | combo | deterministic_trend | contextual_anomaly | 0.083 | 0.991 |
| US_investment.csv | 104 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.001 | 0.994 |
| German_income.csv | 113 | combo | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | 0.025 | 0.993 |
| W6.csv | 114 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.015 | 0.991 |
| Polish_productivity.csv | 117 | combo | volatility | collective_anomaly, point_anomaly | 0.871 | 0.998 |
| wine.csv | 142 | combo | deterministic_trend | collective_anomaly, contextual_anomaly | 0.016 | 0.998 |
| airpass.csv | 144 | combo | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | 0.046 | 0.989 |
| W8.csv | 150 | combo | deterministic_trend | contextual_anomaly, point_anomaly | 0.029 | 0.997 |
| W11.csv | 166 | combo | stochastic_trend | collective_anomaly, contextual_anomaly | 0.004 | 0.998 |
| W2.csv | 302 | combo | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | 0.005 | 0.981 |
| INDPRO.csv | 372 | combo | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | 0.259 | 0.997 |
| UNRATE.csv | 372 | combo | deterministic_trend | collective_anomaly | 0.648 | 0.988 |
| beer.csv | 422 | combo | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | 0.069 | 0.998 |
| soi_dataframe.csv | 453 | combo | stochastic_trend | collective_anomaly | 0.319 | 0.991 |
| NP_AWHours.csv | 479 | combo | deterministic_trend | collective_anomaly | 0.507 | 0.997 |
| NP_xetradax_returns100.csv | 1028 | combo | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | 0.006 | 0.992 |


## Base Type Dagilimi

```
deterministic_trend    22
stationary              6
stochastic_trend        3
volatility              1
```


## Decision Path Dagilimi

```
combo    32
```


## Anomaly Frekansi

```
collective_anomaly       27
contextual_anomaly       28
mean_shift               6
point_anomaly            13
trend_shift              6
variance_shift           6
```


## Kisa Seriler (n<=100) Detayi

| dosya | n | base | anomaliler | path |
|---|---|---|---|---|
| W12-1.csv | 54 | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | combo |
| W12-2.csv | 54 | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | combo |
| W5.csv | 71 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
| deaths.csv | 72 | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | combo |
| W13-1.csv | 82 | deterministic_trend | contextual_anomaly | combo |
| W13-2.csv | 82 | deterministic_trend | contextual_anomaly | combo |
| W13-3.csv | 82 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
| W13-4.csv | 82 | deterministic_trend | contextual_anomaly | combo |
| W13-5.csv | 82 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
| W3.csv | 82 | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | combo |
| W14.csv | 87 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
| GermanGNP.csv | 88 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
| e1.csv | 92 | stochastic_trend | collective_anomaly, contextual_anomaly | combo |
| German_consumption.csv | 93 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
| sunspots.csv | 100 | deterministic_trend | collective_anomaly, contextual_anomaly | combo |
