# Hybrid Stacking v3 - Test Sonuclari

Base: meta-learner | Anomali: meta-learner + safety net (new ensemble >= 0.80 override)

## Ozet

| Metrik | Deger |
|---|---|
| Toplam test | 380 |
| Full match | 320 (84.21%) |
| Partial match | 54 (14.2%) |
| No match | 6 (1.6%) |

## Grup Bazli Ozet

| # | Grup | Beklenen | Ornek | Full | Partial | None | Full% |
|---|---|---|---|---|---|---|---|
| 1 | stationary | stationary | 10 | 9 | 0 | 1 | %90 |
| 2 | deterministic_trend | deterministic_trend | 10 | 8 | 2 | 0 | %80 |
| 3 | stochastic_trend | stochastic_trend | 10 | 2 | 6 | 2 | %20 |
| 4 | volatility | volatility | 10 | 8 | 2 | 0 | %80 |
| 5 | collective_anomaly | stationary + collective_anomaly | 10 | 8 | 2 | 0 | %80 |
| 7 | mean_shift | stationary + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 8 | point_anomaly | stationary + point_anomaly | 10 | 9 | 1 | 0 | %90 |
| 9 | trend_shift | stationary + trend_shift | 10 | 3 | 6 | 1 | %30 |
| 10 | variance_shift | stationary + variance_shift | 10 | 5 | 5 | 0 | %50 |
| 11 | cubic+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 12 | cubic+mean_shift | deterministic_trend + mean_shift | 10 | 10 | 0 | 0 | %100 |
| 13 | cubic+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 14 | cubic+variance_shift | deterministic_trend + variance_shift | 10 | 10 | 0 | 0 | %100 |
| 15 | damped+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 16 | damped+mean_shift | deterministic_trend + mean_shift | 10 | 10 | 0 | 0 | %100 |
| 17 | damped+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 18 | damped+variance_shift | deterministic_trend + variance_shift | 10 | 9 | 1 | 0 | %90 |
| 19 | exp+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 20 | exp+mean_shift | deterministic_trend + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 21 | exp+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 22 | exp+variance_shift | deterministic_trend + variance_shift | 10 | 10 | 0 | 0 | %100 |
| 23 | linear+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 24 | linear+mean_shift | deterministic_trend + mean_shift | 10 | 8 | 2 | 0 | %80 |
| 25 | linear+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 26 | linear+trend_shift | deterministic_trend + trend_shift | 10 | 5 | 4 | 1 | %50 |
| 27 | linear+variance_shift | deterministic_trend + variance_shift | 10 | 10 | 0 | 0 | %100 |
| 28 | quad+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 29 | quad+mean_shift | deterministic_trend + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 30 | quad+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 31 | quad+variance_shift | deterministic_trend + variance_shift | 10 | 8 | 2 | 0 | %80 |
| 32 | stoch+collective | stochastic_trend + collective_anomaly | 10 | 8 | 2 | 0 | %80 |
| 33 | stoch+mean_shift | stochastic_trend + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 34 | stoch+point_anomaly | stochastic_trend + point_anomaly | 10 | 6 | 4 | 0 | %60 |
| 35 | stoch+variance_shift | stochastic_trend + variance_shift | 10 | 8 | 2 | 0 | %80 |
| 36 | vol+collective | volatility + collective_anomaly | 10 | 8 | 2 | 0 | %80 |
| 37 | vol+mean_shift | volatility + mean_shift | 10 | 7 | 3 | 0 | %70 |
| 38 | vol+point_anomaly | volatility + point_anomaly | 10 | 8 | 2 | 0 | %80 |
| 39 | vol+variance_shift | volatility + variance_shift | 10 | 7 | 2 | 1 | %70 |

---

## Grup 1: stationary
**Beklenen:** `stationary`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `stationary` | `stationary_654.csv` | `stationary` | FULL |
| `stationary` | `stationary_114.csv` | `stationary` | FULL |
| `stationary` | `stationary_025.csv` | `stationary` | FULL |
| `stationary` | `stationary_759.csv` | `stationary` | FULL |
| `stationary` | `stationary_281.csv` | `stationary` | FULL |
| `stationary` | `stationary_250.csv` | `stationary` | FULL |
| `stationary` | `stationary_228.csv` | `stationary` | FULL |
| `stationary` | `stationary_142.csv` | `stationary` | FULL |
| `stationary` | `stationary_754.csv` | `volatility` | x NONE |
| `stationary` | `stationary_104.csv` | `stationary` | FULL |
---

## Grup 2: deterministic_trend
**Beklenen:** `deterministic_trend`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `deterministic_trend` | `deterministic_trend_692.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_758.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_913.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_558.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_089.csv` | `deterministic_trend + variance_shift` | ~ PARTIAL |
| `deterministic_trend` | `deterministic_trend_604.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_432.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_032.csv` | `deterministic_trend + mean_shift` | ~ PARTIAL |
| `deterministic_trend` | `deterministic_trend_030.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_095.csv` | `deterministic_trend` | FULL |
---

## Grup 3: stochastic_trend
**Beklenen:** `stochastic_trend`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend` | `stochastic_trend_223.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_238.csv` | `stationary + mean_shift` | x NONE |
| `Stochastic Trend` | `stochastic_trend_517.csv` | `stochastic_trend + variance_shift` | ~ PARTIAL |
| `Stochastic Trend` | `stochastic_trend_616.csv` | `deterministic_trend + mean_shift` | x NONE |
| `Stochastic Trend` | `stochastic_trend_027.csv` | `stochastic_trend + mean_shift` | ~ PARTIAL |
| `Stochastic Trend` | `stochastic_trend_574.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_203.csv` | `stochastic_trend + mean_shift` | ~ PARTIAL |
| `Stochastic Trend` | `stochastic_trend_733.csv` | `stochastic_trend + variance_shift` | ~ PARTIAL |
| `Stochastic Trend` | `stochastic_trend_665.csv` | `stochastic_trend + mean_shift` | ~ PARTIAL |
| `Stochastic Trend` | `stochastic_trend_718.csv` | `stochastic_trend + variance_shift` | ~ PARTIAL |
---

## Grup 4: volatility
**Beklenen:** `volatility`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility` | `volatility_558.csv` | `volatility` | FULL |
| `Volatility` | `volatility_429.csv` | `volatility` | FULL |
| `Volatility` | `volatility_225.csv` | `volatility` | FULL |
| `Volatility` | `volatility_459.csv` | `volatility` | FULL |
| `Volatility` | `volatility_603.csv` | `volatility` | FULL |
| `Volatility` | `volatility_284.csv` | `volatility` | FULL |
| `Volatility` | `volatility_828.csv` | `volatility + mean_shift` | ~ PARTIAL |
| `Volatility` | `volatility_890.csv` | `volatility` | FULL |
| `Volatility` | `volatility_006.csv` | `volatility + variance_shift` | ~ PARTIAL |
| `Volatility` | `volatility_777.csv` | `volatility` | FULL |
---

## Grup 5: collective_anomaly
**Beklenen:** `stationary + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `collective_anomaly` | `collective_anomaly_825.csv` | `volatility + collective_anomaly` | ~ PARTIAL |
| `collective_anomaly` | `collective_anomaly_163.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_714.csv` | `volatility + collective_anomaly` | ~ PARTIAL |
| `collective_anomaly` | `collective_anomaly_432.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_348.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_284.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_159.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_220.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_980.csv` | `stationary + collective_anomaly` | FULL |
| `collective_anomaly` | `collective_anomaly_781.csv` | `stationary + collective_anomaly` | FULL |
---

## Grup 7: mean_shift
**Beklenen:** `stationary + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `mean_shift` | `mean_shift_344.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_104.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_094.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_389.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_099.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_367.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_867.csv` | `deterministic_trend + mean_shift` | ~ PARTIAL |
| `mean_shift` | `mean_shift_352.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_618.csv` | `stationary + mean_shift` | FULL |
| `mean_shift` | `mean_shift_270.csv` | `stationary + mean_shift` | FULL |
---

## Grup 8: point_anomaly
**Beklenen:** `stationary + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `point_anomaly` | `point_anomaly_826.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_044.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_747.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_470.csv` | `volatility + point_anomaly` | ~ PARTIAL |
| `point_anomaly` | `point_anomaly_549.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_127.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_996.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_944.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_387.csv` | `stationary + point_anomaly` | FULL |
| `point_anomaly` | `point_anomaly_080.csv` | `stationary + point_anomaly` | FULL |
---

## Grup 9: trend_shift
**Beklenen:** `stationary + trend_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `trend_shift` | `trend_shift_565.csv` | `deterministic_trend + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_300.csv` | `deterministic_trend + mean_shift` | x NONE |
| `trend_shift` | `trend_shift_849.csv` | `deterministic_trend + mean_shift + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_643.csv` | `deterministic_trend + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_633.csv` | `deterministic_trend + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_906.csv` | `deterministic_trend + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_882.csv` | `stationary + trend_shift` | FULL |
| `trend_shift` | `trend_shift_370.csv` | `deterministic_trend + mean_shift + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_591.csv` | `stationary + trend_shift` | FULL |
| `trend_shift` | `trend_shift_196.csv` | `stationary + trend_shift` | FULL |
---

## Grup 10: variance_shift
**Beklenen:** `stationary + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `variance_shift` | `variance_shift_721.csv` | `stationary + variance_shift` | FULL |
| `variance_shift` | `variance_shift_071.csv` | `deterministic_trend + variance_shift` | ~ PARTIAL |
| `variance_shift` | `variance_shift_046.csv` | `volatility + variance_shift` | ~ PARTIAL |
| `variance_shift` | `variance_shift_677.csv` | `stationary + variance_shift` | FULL |
| `variance_shift` | `variance_shift_233.csv` | `volatility + variance_shift` | ~ PARTIAL |
| `variance_shift` | `variance_shift_791.csv` | `stationary + variance_shift` | FULL |
| `variance_shift` | `variance_shift_296.csv` | `volatility + variance_shift` | ~ PARTIAL |
| `variance_shift` | `variance_shift_081.csv` | `stationary` | ~ PARTIAL |
| `variance_shift` | `variance_shift_875.csv` | `stationary + variance_shift` | FULL |
| `variance_shift` | `variance_shift_238.csv` | `stationary + variance_shift` | FULL |
---

## Grup 11: cubic+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `cubic_collective_anomaly` | `cubic_collective_887.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_103.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_389.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_284.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_464.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_650.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_854.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_373.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_166.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_379.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 12: cubic+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Cubic + Mean Shift` | `cubic_mean_shift_363.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_214.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_686.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_273.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_718.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_959.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_699.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_663.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_073.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_623.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 13: cubic+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Cubic + Point Anomaly` | `cubic_point_anomaly_650.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_175.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_546.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_746.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_250.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_167.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_473.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_388.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_276.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_947.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 14: cubic+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Cubic + Variance Shift` | `cubic_variance_shift_655.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_704.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_570.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_224.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_701.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_332.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_863.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_786.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_794.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_057.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 15: damped+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Collective Anomaly` | `damped_collective_234.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_841.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_032.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_824.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_323.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_410.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_274.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_067.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_216.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_935.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 16: damped+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Mean Shift` | `damped_mean_shift_965.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_580.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_897.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_735.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_322.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_217.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_671.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_511.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_405.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_905.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 17: damped+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Point Anomaly` | `damped_point_anomaly_936.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_658.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_469.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_146.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_271.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_142.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_252.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_762.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_574.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_551.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 18: damped+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Variance Shift` | `damped_variance_shift_269.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_764.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_598.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_438.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_919.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_597.csv` | `deterministic_trend` | ~ PARTIAL |
| `Damped + Variance Shift` | `damped_variance_shift_408.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_370.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_224.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_141.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 19: exp+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `exponential_collective_anomaly` | `exp_collective_521.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_505.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_093.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_773.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_048.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_881.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_112.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_156.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_642.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_163.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 20: exp+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Exponential + Mean Shift` | `exp_mean_shift_811.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_696.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_432.csv` | `deterministic_trend + mean_shift + variance_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_610.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_065.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_394.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_390.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_479.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_541.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_257.csv` | `volatility + mean_shift` | ~ PARTIAL |
---

## Grup 21: exp+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `exponential_point_anomaly` | `exp_point_anomaly_994.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_566.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_881.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_965.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_011.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_696.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_738.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_117.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_698.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_906.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 22: exp+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `exponential_variance_shift` | `exp_variance_shift_549.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_768.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_273.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_787.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_656.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_348.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_114.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_300.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_445.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_161.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 23: linear+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Collective Anomaly` | `linear_collective_464.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_003.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_976.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_739.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_896.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_736.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_269.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_995.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_512.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_780.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 24: linear+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Mean Shift` | `linear_mean_shift_182.csv` | `deterministic_trend` | ~ PARTIAL |
| `Linear + Mean Shift` | `linear_mean_shift_519.csv` | `deterministic_trend` | ~ PARTIAL |
| `Linear + Mean Shift` | `linear_mean_shift_934.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_108.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_891.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_640.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_305.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_861.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_654.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_623.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 25: linear+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Point Anomaly` | `linear_point_anomaly_203.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_156.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_382.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_780.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_165.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_552.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_976.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_797.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_944.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_543.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 26: linear+trend_shift
**Beklenen:** `deterministic_trend + trend_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Trend Shift` | `linear_trend_shift_940.csv` | `deterministic_trend + mean_shift + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_000.csv` | `volatility` | x NONE |
| `Linear + Trend Shift` | `linear_trend_shift_613.csv` | `stationary + trend_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_331.csv` | `stationary + trend_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_500.csv` | `deterministic_trend + mean_shift + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_019.csv` | `deterministic_trend + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_114.csv` | `deterministic_trend + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_951.csv` | `stationary + trend_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_371.csv` | `deterministic_trend + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_899.csv` | `volatility + trend_shift` | ~ PARTIAL |
---

## Grup 27: linear+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Variance Shift` | `linear_variance_shift_851.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_826.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_314.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_245.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_059.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_246.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_899.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_580.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_969.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_080.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 28: quad+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Collective anomaly` | `quad_collective_087.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_749.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_497.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_835.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_070.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_778.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_545.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_784.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_128.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_131.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 29: quad+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Mean Shift` | `quad_mean_shift_675.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_486.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_969.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_562.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_169.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_271.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_540.csv` | `deterministic_trend + mean_shift + trend_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_893.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_621.csv` | `deterministic_trend + trend_shift` | ~ PARTIAL |
| `Quadratic + Mean Shift` | `quad_mean_shift_433.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 30: quad+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Point Anomaly` | `quad_point_anomaly_987.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_216.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_951.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_552.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_773.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_747.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_706.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_205.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_730.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_319.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 31: quad+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Variance Shift` | `quad_variance_shift_408.csv` | `deterministic_trend` | ~ PARTIAL |
| `Quadratic + Variance Shift` | `quad_variance_shift_687.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_665.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_382.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_448.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_921.csv` | `deterministic_trend + trend_shift + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_529.csv` | `stationary + variance_shift` | ~ PARTIAL |
| `Quadratic + Variance Shift` | `quad_variance_shift_462.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_123.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_253.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 32: stoch+collective
**Beklenen:** `stochastic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_230.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_065.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_346.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_021.csv` | `volatility + collective_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_602.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_567.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_235.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_225.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_007.csv` | `deterministic_trend + collective_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_072.csv` | `stochastic_trend + collective_anomaly` | FULL |
---

## Grup 33: stoch+mean_shift
**Beklenen:** `stochastic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_724.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_646.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_060.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_234.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_069.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_927.csv` | `deterministic_trend + mean_shift` | ~ PARTIAL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_032.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_880.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_338.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_072.csv` | `stochastic_trend + mean_shift` | FULL |
---

## Grup 34: stoch+point_anomaly
**Beklenen:** `stochastic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_526.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_243.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_285.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_685.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_497.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_219.csv` | `stationary + point_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_552.csv` | `deterministic_trend + point_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_135.csv` | `deterministic_trend + point_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_740.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_957.csv` | `stationary + point_anomaly` | ~ PARTIAL |
---

## Grup 35: stoch+variance_shift
**Beklenen:** `stochastic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_903.csv` | `stochastic_trend + mean_shift` | ~ PARTIAL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_584.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_590.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_484.csv` | `stochastic_trend + mean_shift + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_248.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_803.csv` | `stochastic_trend + mean_shift + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_826.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_416.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_194.csv` | `stationary + variance_shift` | ~ PARTIAL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_096.csv` | `stochastic_trend + variance_shift` | FULL |
---

## Grup 36: vol+collective
**Beklenen:** `volatility + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Collective Anomaly` | `vol_collective_099.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_674.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_441.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_362.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_433.csv` | `volatility + collective_anomaly + point_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_420.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_478.csv` | `stationary + collective_anomaly` | ~ PARTIAL |
| `Volatility + Collective Anomaly` | `vol_collective_884.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_746.csv` | `stationary + collective_anomaly` | ~ PARTIAL |
| `Volatility + Collective Anomaly` | `vol_collective_055.csv` | `volatility + collective_anomaly` | FULL |
---

## Grup 37: vol+mean_shift
**Beklenen:** `volatility + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Mean Shift` | `vol_mean_shift_689.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_669.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_661.csv` | `stationary + mean_shift` | ~ PARTIAL |
| `Volatility + Mean Shift` | `vol_mean_shift_100.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_062.csv` | `stationary + mean_shift` | ~ PARTIAL |
| `Volatility + Mean Shift` | `vol_mean_shift_412.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_745.csv` | `stationary + mean_shift` | ~ PARTIAL |
| `Volatility + Mean Shift` | `vol_mean_shift_347.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_819.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_882.csv` | `volatility + mean_shift` | FULL |
---

## Grup 38: vol+point_anomaly
**Beklenen:** `volatility + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Point Anomaly` | `vol_point_anomaly_111.csv` | `stationary + point_anomaly` | ~ PARTIAL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_254.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_196.csv` | `stationary + point_anomaly` | ~ PARTIAL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_194.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_549.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_459.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_143.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_432.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_187.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_285.csv` | `volatility + point_anomaly` | FULL |
---

## Grup 39: vol+variance_shift
**Beklenen:** `volatility + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Variance Shift` | `vol_variance_shift_473.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_255.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_895.csv` | `volatility` | ~ PARTIAL |
| `Volatility + Variance Shift` | `vol_variance_shift_945.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_077.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_453.csv` | `stationary + variance_shift` | ~ PARTIAL |
| `Volatility + Variance Shift` | `vol_variance_shift_827.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_882.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_876.csv` | `deterministic_trend + mean_shift` | x NONE |
| `Volatility + Variance Shift` | `vol_variance_shift_563.csv` | `volatility + variance_shift` | FULL |
---
