# Hybrid Stacking v3 - Test Sonuclari

Base: meta-learner | Anomali: meta-learner + safety net (new ensemble >= 0.80 override)

## Ozet

| Metrik | Deger |
|---|---|
| Toplam test | 390 |
| Full match | 344 (88.21%) |
| Partial match | 41 (10.5%) |
| No match | 5 (1.3%) |

## Grup Bazli Ozet

| # | Grup | Beklenen | Ornek | Full | Partial | None | Full% |
|---|---|---|---|---|---|---|---|
| 1 | stationary | stationary | 10 | 7 | 3 | 0 | %70 |
| 2 | deterministic_trend | deterministic_trend | 10 | 9 | 1 | 0 | %90 |
| 3 | stochastic_trend | stochastic_trend | 10 | 7 | 1 | 2 | %70 |
| 4 | volatility | volatility | 10 | 9 | 1 | 0 | %90 |
| 5 | collective_anomaly | stationary + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 6 | contextual_anomaly | stationary + contextual_anomaly | 10 | 10 | 0 | 0 | %100 |
| 7 | mean_shift | stationary + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 8 | point_anomaly | stationary + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 9 | trend_shift | stationary + trend_shift | 10 | 8 | 2 | 0 | %80 |
| 10 | variance_shift | stationary + variance_shift | 10 | 10 | 0 | 0 | %100 |
| 11 | cubic+collective | deterministic_trend + collective_anomaly | 10 | 9 | 1 | 0 | %90 |
| 12 | cubic+mean_shift | deterministic_trend + mean_shift | 10 | 10 | 0 | 0 | %100 |
| 13 | cubic+point_anomaly | deterministic_trend + point_anomaly | 10 | 9 | 1 | 0 | %90 |
| 14 | cubic+variance_shift | deterministic_trend + variance_shift | 10 | 9 | 0 | 1 | %90 |
| 15 | damped+collective | deterministic_trend + collective_anomaly | 10 | 9 | 1 | 0 | %90 |
| 16 | damped+mean_shift | deterministic_trend + mean_shift | 10 | 7 | 3 | 0 | %70 |
| 17 | damped+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 18 | damped+variance_shift | deterministic_trend + variance_shift | 10 | 8 | 2 | 0 | %80 |
| 19 | exp+collective | deterministic_trend + collective_anomaly | 10 | 8 | 2 | 0 | %80 |
| 20 | exp+mean_shift | deterministic_trend + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 21 | exp+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 22 | exp+variance_shift | deterministic_trend + variance_shift | 10 | 10 | 0 | 0 | %100 |
| 23 | linear+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 24 | linear+mean_shift | deterministic_trend + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 25 | linear+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 26 | linear+trend_shift | deterministic_trend + trend_shift | 10 | 6 | 4 | 0 | %60 |
| 27 | linear+variance_shift | deterministic_trend + variance_shift | 10 | 10 | 0 | 0 | %100 |
| 28 | quad+collective | deterministic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 29 | quad+mean_shift | deterministic_trend + mean_shift | 10 | 5 | 4 | 1 | %50 |
| 30 | quad+point_anomaly | deterministic_trend + point_anomaly | 10 | 10 | 0 | 0 | %100 |
| 31 | quad+variance_shift | deterministic_trend + variance_shift | 10 | 7 | 3 | 0 | %70 |
| 32 | stoch+collective | stochastic_trend + collective_anomaly | 10 | 10 | 0 | 0 | %100 |
| 33 | stoch+mean_shift | stochastic_trend + mean_shift | 10 | 9 | 1 | 0 | %90 |
| 34 | stoch+point_anomaly | stochastic_trend + point_anomaly | 10 | 7 | 3 | 0 | %70 |
| 35 | stoch+variance_shift | stochastic_trend + variance_shift | 10 | 9 | 0 | 1 | %90 |
| 36 | vol+collective | volatility + collective_anomaly | 10 | 9 | 1 | 0 | %90 |
| 37 | vol+mean_shift | volatility + mean_shift | 10 | 8 | 2 | 0 | %80 |
| 38 | vol+point_anomaly | volatility + point_anomaly | 10 | 9 | 1 | 0 | %90 |
| 39 | vol+variance_shift | volatility + variance_shift | 10 | 9 | 1 | 0 | %90 |

---

## Grup 1: stationary
**Beklenen:** `stationary`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `stationary` | `stationary_01.csv` | `stationary` | FULL |
| `stationary` | `stationary_00.csv` | `stationary` | FULL |
| `stationary` | `stationary_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `stationary` | `stationary_09.csv` | `stationary` | FULL |
| `stationary` | `stationary_06.csv` | `stationary` | FULL |
| `stationary` | `stationary_05.csv` | `stationary` | FULL |
| `stationary` | `stationary_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `stationary` | `stationary_02.csv` | `stationary` | FULL |
| `stationary` | `stationary_03.csv` | `stationary` | FULL |
| `stationary` | `stationary_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
---

## Grup 2: deterministic_trend
**Beklenen:** `deterministic_trend`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `deterministic_trend` | `deterministic_trend_00.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_09.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_01.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_07.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_06.csv` | `deterministic_trend + variance_shift` | ~ PARTIAL |
| `deterministic_trend` | `deterministic_trend_04.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_08.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_02.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_03.csv` | `deterministic_trend` | FULL |
| `deterministic_trend` | `deterministic_trend_05.csv` | `deterministic_trend` | FULL |
---

## Grup 3: stochastic_trend
**Beklenen:** `stochastic_trend`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend` | `stochastic_trend_03.csv` | `stochastic_trend + variance_shift` | ~ PARTIAL |
| `Stochastic Trend` | `stochastic_trend_07.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_04.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_06.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_00.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_01.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_09.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_08.csv` | `stochastic_trend` | FULL |
| `Stochastic Trend` | `stochastic_trend_02.csv` | `stationary` | x NONE |
| `Stochastic Trend` | `stochastic_trend_05.csv` | `stationary` | x NONE |
---

## Grup 4: volatility
**Beklenen:** `volatility`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility` | `volatility_03.csv` | `volatility` | FULL |
| `Volatility` | `volatility_05.csv` | `volatility` | FULL |
| `Volatility` | `volatility_01.csv` | `volatility` | FULL |
| `Volatility` | `volatility_00.csv` | `volatility` | FULL |
| `Volatility` | `volatility_09.csv` | `volatility + variance_shift` | ~ PARTIAL |
| `Volatility` | `volatility_06.csv` | `volatility` | FULL |
| `Volatility` | `volatility_02.csv` | `volatility` | FULL |
| `Volatility` | `volatility_07.csv` | `volatility` | FULL |
| `Volatility` | `volatility_08.csv` | `volatility` | FULL |
| `Volatility` | `volatility_04.csv` | `volatility` | FULL |
---

## Grup 5: collective_anomaly
**Beklenen:** `stationary + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `collective_anomaly` | `collective_anomaly_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_01.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_00.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_02.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_09.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `collective_anomaly` | `collective_anomaly_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
---

## Grup 6: contextual_anomaly
**Beklenen:** `stationary + contextual_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `contextual_anomaly` | `contextual_anomaly_01.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_00.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_02.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_09.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `contextual_anomaly` | `contextual_anomaly_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
---

## Grup 7: mean_shift
**Beklenen:** `stationary + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `mean_shift` | `mean_shift_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_02.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_09.csv` | `deterministic_trend + mean_shift` | ~ PARTIAL |
| `mean_shift` | `mean_shift_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_01.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_00.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `mean_shift` | `mean_shift_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
---

## Grup 8: point_anomaly
**Beklenen:** `stationary + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `point_anomaly` | `point_anomaly_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_02.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_09.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_01.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `point_anomaly` | `point_anomaly_00.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
---

## Grup 9: trend_shift
**Beklenen:** `stationary + trend_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `trend_shift` | `trend_shift_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_00.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_09.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_02.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_01.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `trend_shift` | `trend_shift_06.csv` | `deterministic_trend + mean_shift + trend_shift` | ~ PARTIAL |
| `trend_shift` | `trend_shift_04.csv` | `deterministic_trend + trend_shift` | ~ PARTIAL |
---

## Grup 10: variance_shift
**Beklenen:** `stationary + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `variance_shift` | `variance_shift_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_09.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_01.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_02.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_08.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
| `variance_shift` | `variance_shift_00.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | FULL |
---

## Grup 11: cubic+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `cubic_collective_anomaly` | `cubic_collective_09.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_06.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_05.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_01.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_08.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_04.csv` | `stochastic_trend + collective_anomaly` | ~ PARTIAL |
| `cubic_collective_anomaly` | `cubic_collective_03.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_00.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_02.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `cubic_collective_anomaly` | `cubic_collective_07.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 12: cubic+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Cubic + Mean Shift` | `cubic_mean_shift_02.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_09.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_06.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_04.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_00.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_03.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_07.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_08.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_01.csv` | `deterministic_trend + mean_shift` | FULL |
| `Cubic + Mean Shift` | `cubic_mean_shift_05.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 13: cubic+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Cubic + Point Anomaly` | `cubic_point_anomaly_08.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_00.csv` | `deterministic_trend` | ~ PARTIAL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_01.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_05.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_04.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_02.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_06.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_09.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_07.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Cubic + Point Anomaly` | `cubic_point_anomaly_03.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 14: cubic+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Cubic + Variance Shift` | `cubic_variance_shift_02.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_07.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_00.csv` | `stationary` | x NONE |
| `Cubic + Variance Shift` | `cubic_variance_shift_05.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_06.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_09.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_01.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_04.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_08.csv` | `deterministic_trend + variance_shift` | FULL |
| `Cubic + Variance Shift` | `cubic_variance_shift_03.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 15: damped+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Collective Anomaly` | `damped_collective_08.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_03.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_02.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_07.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_01.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_04.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_00.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_06.csv` | `stochastic_trend + collective_anomaly` | ~ PARTIAL |
| `Damped + Collective Anomaly` | `damped_collective_05.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Damped + Collective Anomaly` | `damped_collective_09.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 16: damped+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Mean Shift` | `damped_mean_shift_00.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_01.csv` | `deterministic_trend` | ~ PARTIAL |
| `Damped + Mean Shift` | `damped_mean_shift_05.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_06.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_02.csv` | `deterministic_trend` | ~ PARTIAL |
| `Damped + Mean Shift` | `damped_mean_shift_08.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_09.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_03.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_07.csv` | `deterministic_trend + mean_shift` | FULL |
| `Damped + Mean Shift` | `damped_mean_shift_04.csv` | `deterministic_trend` | ~ PARTIAL |
---

## Grup 17: damped+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Point Anomaly` | `damped_point_anomaly_07.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_01.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_02.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_08.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_05.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_03.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_06.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_04.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_09.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Damped + Point Anomaly` | `damped_point_anomaly_00.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 18: damped+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Damped + Variance Shift` | `damped_variance_shift_08.csv` | `deterministic_trend` | ~ PARTIAL |
| `Damped + Variance Shift` | `damped_variance_shift_03.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_04.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_09.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_05.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_02.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_06.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_07.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_01.csv` | `deterministic_trend + variance_shift` | FULL |
| `Damped + Variance Shift` | `damped_variance_shift_00.csv` | `deterministic_trend` | ~ PARTIAL |
---

## Grup 19: exp+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `exponential_collective_anomaly` | `exp_collective_03.csv` | `stochastic_trend + collective_anomaly` | ~ PARTIAL |
| `exponential_collective_anomaly` | `exp_collective_09.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_01.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_02.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_00.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_04.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_07.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_06.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `exponential_collective_anomaly` | `exp_collective_05.csv` | `deterministic_trend` | ~ PARTIAL |
| `exponential_collective_anomaly` | `exp_collective_08.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 20: exp+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Exponential + Mean Shift` | `exp_mean_shift_01.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_00.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_03.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_08.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_06.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_02.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_05.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_04.csv` | `deterministic_trend + mean_shift` | FULL |
| `Exponential + Mean Shift` | `exp_mean_shift_07.csv` | `deterministic_trend` | ~ PARTIAL |
| `Exponential + Mean Shift` | `exp_mean_shift_09.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 21: exp+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `exponential_point_anomaly` | `exp_point_anomaly_07.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_03.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_02.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_05.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_04.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_06.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_08.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_00.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_01.csv` | `deterministic_trend + point_anomaly` | FULL |
| `exponential_point_anomaly` | `exp_point_anomaly_09.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 22: exp+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `exponential_variance_shift` | `exp_variance_shift_03.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_01.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_08.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_05.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_09.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_02.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_06.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_07.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_04.csv` | `deterministic_trend + variance_shift` | FULL |
| `exponential_variance_shift` | `exp_variance_shift_00.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 23: linear+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Collective Anomaly` | `linear_collective_01.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_00.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_06.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_05.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_02.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_08.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_09.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_04.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_07.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Linear + Collective Anomaly` | `linear_collective_03.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 24: linear+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Mean Shift` | `linear_mean_shift_02.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_06.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_09.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_07.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_03.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_01.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_00.csv` | `deterministic_trend` | ~ PARTIAL |
| `Linear + Mean Shift` | `linear_mean_shift_04.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_05.csv` | `deterministic_trend + mean_shift` | FULL |
| `Linear + Mean Shift` | `linear_mean_shift_08.csv` | `deterministic_trend + mean_shift` | FULL |
---

## Grup 25: linear+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Point Anomaly` | `linear_point_anomaly_08.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_00.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_01.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_06.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_07.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_05.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_03.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_04.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_02.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Linear + Point Anomaly` | `linear_point_anomaly_09.csv` | `deterministic_trend + point_anomaly` | FULL |
---

## Grup 26: linear+trend_shift
**Beklenen:** `deterministic_trend + trend_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Trend Shift` | `linear_trend_shift_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_00.csv` | `deterministic_trend + mean_shift + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_02.csv` | `deterministic_trend + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_03.csv` | `deterministic_trend + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_08.csv` | `deterministic_trend + trend_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_09.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_01.csv` | `deterministic_trend + trend_shift + variance_shift` | FULL |
| `Linear + Trend Shift` | `linear_trend_shift_04.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Linear + Trend Shift` | `linear_trend_shift_05.csv` | `deterministic_trend + trend_shift` | FULL |
---

## Grup 27: linear+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Linear + Variance Shift` | `linear_variance_shift_08.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_07.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_02.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_01.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_09.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_06.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_00.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_05.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_03.csv` | `deterministic_trend + variance_shift` | FULL |
| `Linear + Variance Shift` | `linear_variance_shift_04.csv` | `deterministic_trend + variance_shift` | FULL |
---

## Grup 28: quad+collective
**Beklenen:** `deterministic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Collective anomaly` | `quad_collective_00.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_09.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_07.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_04.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_06.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_01.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_08.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_02.csv` | `deterministic_trend + collective_anomaly + contextual_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_03.csv` | `deterministic_trend + collective_anomaly` | FULL |
| `Quadratic + Collective anomaly` | `quad_collective_05.csv` | `deterministic_trend + collective_anomaly` | FULL |
---

## Grup 29: quad+mean_shift
**Beklenen:** `deterministic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Mean Shift` | `quad_mean_shift_01.csv` | `deterministic_trend` | ~ PARTIAL |
| `Quadratic + Mean Shift` | `quad_mean_shift_09.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_03.csv` | `deterministic_trend` | ~ PARTIAL |
| `Quadratic + Mean Shift` | `quad_mean_shift_07.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_00.csv` | `stationary` | x NONE |
| `Quadratic + Mean Shift` | `quad_mean_shift_04.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_08.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_02.csv` | `deterministic_trend` | ~ PARTIAL |
| `Quadratic + Mean Shift` | `quad_mean_shift_05.csv` | `deterministic_trend + mean_shift` | FULL |
| `Quadratic + Mean Shift` | `quad_mean_shift_06.csv` | `deterministic_trend` | ~ PARTIAL |
---

## Grup 30: quad+point_anomaly
**Beklenen:** `deterministic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Point Anomaly` | `quad_point_anomaly_06.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_08.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_05.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_02.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_01.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_09.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_07.csv` | `deterministic_trend + collective_anomaly + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_03.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_04.csv` | `deterministic_trend + point_anomaly` | FULL |
| `Quadratic + Point Anomaly` | `quad_point_anomaly_00.csv` | `deterministic_trend + collective_anomaly + point_anomaly` | FULL |
---

## Grup 31: quad+variance_shift
**Beklenen:** `deterministic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Quadratic + Variance Shift` | `quad_variance_shift_04.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_07.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_05.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Quadratic + Variance Shift` | `quad_variance_shift_06.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_00.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_08.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_03.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_02.csv` | `volatility + variance_shift` | ~ PARTIAL |
| `Quadratic + Variance Shift` | `quad_variance_shift_09.csv` | `deterministic_trend + variance_shift` | FULL |
| `Quadratic + Variance Shift` | `quad_variance_shift_01.csv` | `deterministic_trend` | ~ PARTIAL |
---

## Grup 32: stoch+collective
**Beklenen:** `stochastic_trend + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_08.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_03.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_04.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_01.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_02.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_00.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_06.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_09.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_05.csv` | `stochastic_trend + collective_anomaly` | FULL |
| `Stochastic Trend + Collective Anomaly` | `stoch_collective_07.csv` | `stochastic_trend + collective_anomaly` | FULL |
---

## Grup 33: stoch+mean_shift
**Beklenen:** `stochastic_trend + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_07.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_08.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_04.csv` | `stochastic_trend` | ~ PARTIAL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_09.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_05.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_06.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_00.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_02.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_01.csv` | `stochastic_trend + mean_shift` | FULL |
| `Stochastic Trend + Mean Shift` | `stoch_mean_shift_03.csv` | `stochastic_trend + mean_shift` | FULL |
---

## Grup 34: stoch+point_anomaly
**Beklenen:** `stochastic_trend + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_02.csv` | `deterministic_trend + point_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_04.csv` | `deterministic_trend + point_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_01.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_00.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_05.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_08.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_07.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_03.csv` | `stochastic_trend + point_anomaly` | FULL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_09.csv` | `deterministic_trend + point_anomaly` | ~ PARTIAL |
| `Stochastic Trend + Point Anomaly` | `stoch_point_anomaly_06.csv` | `stochastic_trend + point_anomaly` | FULL |
---

## Grup 35: stoch+variance_shift
**Beklenen:** `stochastic_trend + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_05.csv` | `stationary` | x NONE |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_03.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_04.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_07.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_08.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_02.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_00.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_09.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_01.csv` | `stochastic_trend + variance_shift` | FULL |
| `Stochastic Trend + Variance Shift` | `stoch_variance_shift_06.csv` | `stochastic_trend + variance_shift` | FULL |
---

## Grup 36: vol+collective
**Beklenen:** `volatility + collective_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Collective Anomaly` | `vol_collective_00.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_09.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_05.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_06.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Volatility + Collective Anomaly` | `vol_collective_01.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_02.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_07.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_04.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_03.csv` | `volatility + collective_anomaly` | FULL |
| `Volatility + Collective Anomaly` | `vol_collective_08.csv` | `volatility + collective_anomaly` | FULL |
---

## Grup 37: vol+mean_shift
**Beklenen:** `volatility + mean_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Mean Shift` | `vol_mean_shift_08.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_00.csv` | `volatility` | ~ PARTIAL |
| `Volatility + Mean Shift` | `vol_mean_shift_01.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_09.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_05.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_07.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_06.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_04.csv` | `volatility + mean_shift` | FULL |
| `Volatility + Mean Shift` | `vol_mean_shift_03.csv` | `deterministic_trend + mean_shift` | ~ PARTIAL |
| `Volatility + Mean Shift` | `vol_mean_shift_02.csv` | `volatility + mean_shift` | FULL |
---

## Grup 38: vol+point_anomaly
**Beklenen:** `volatility + point_anomaly`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Point Anomaly` | `vol_point_anomaly_02.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_00.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_04.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_09.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_08.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_06.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_01.csv` | `volatility + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_07.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_05.csv` | `volatility + collective_anomaly + point_anomaly` | FULL |
| `Volatility + Point Anomaly` | `vol_point_anomaly_03.csv` | `volatility + point_anomaly` | FULL |
---

## Grup 39: vol+variance_shift
**Beklenen:** `volatility + variance_shift`

| Leaf | CSV | Tahmin | Sonuc |
|---|---|---|---|
| `Volatility + Variance Shift` | `vol_variance_shift_05.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_08.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_06.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_04.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_09.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_01.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_07.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_00.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_02.csv` | `volatility + variance_shift` | FULL |
| `Volatility + Variance Shift` | `vol_variance_shift_03.csv` | `stationary + collective_anomaly + contextual_anomaly + mean_shift + point_anomaly + trend_shift + variance_shift` | ~ PARTIAL |
---
