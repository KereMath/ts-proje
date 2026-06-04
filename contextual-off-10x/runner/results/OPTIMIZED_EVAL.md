# Optimized Blend Evaluation

Baseline (trainer-learned blend, STAT_GATE=0.95) vs Optimized (sweep'ten).

## Optimized config

- STAT_GATE = **0.9**
- Blend:
  - collective_anomaly: alpha=0.20, t=0.85
  - mean_shift: alpha=0.50, t=0.80
  - point_anomaly: alpha=0.20, t=0.75
  - trend_shift: alpha=0.20, t=0.90
  - variance_shift: alpha=0.35, t=0.90

## Sonuclar

| Metrik | Baseline | Optimized | Δ |
|---|---|---|---|
| Realdata base accuracy (20 dosya) | 6/20 | 6/20 | +0 |
| Realdata FULL (stat GT, 10 dosya) | 0/10 | 0/10 | +0 |
| Sentetik base accuracy (500 dosya) | 385/500 (77.0%) | 385/500 (77.0%) | +0 |

## Realdata detayli (stationary GT)

| dosya | n | GT | baseline pred | optim pred | optim anom |
|---|---|---|---|---|---|
| NP_xetradax_returns100.csv | 1028 | stationary | stationary | stationary | point_anomaly |
| RealInt_dataframe.csv | 103 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| rec_dataframe.csv | 453 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| soi_dataframe.csv | 453 | stationary | stochastic_trend | stochastic_trend | collective_anomaly |
| strikes.csv | 30 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| sunspots.csv | 100 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| US_investment.csv | 104 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| W1.csv | 45 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| W2.csv | 302 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
| W3.csv | 82 | stationary | deterministic_trend | deterministic_trend | collective_anomaly |
