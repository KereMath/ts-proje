# realdata Ground Truth vs ens-final Tahminleri

Ground truth Datasets.pdf'ten cikarildi (Wei, Brockwell, Lutkepohl, Shumway & Stoffer, Bai-Perron).


**Etiket eslesimi notlari:**
- Pipeline sadece 4 base sinif tahmin eder: stationary / deterministic_trend / stochastic_trend / volatility
- 'Seasonal unit root' ve 'regular+seasonal stochastic trend' → `stochastic_trend` olarak esledim
- 'AO/IO outliers' (Wei) → `point_anomaly`
- 'TC (temporary change)' → `mean_shift` (ya da `trend_shift`)
- 'structural break' → `trend_shift` veya `mean_shift`


## Ozet

| Match | Sayi |
|---|---|
| FULL | 0 |
| PARTIAL | 8 |
| NONE | 11 |
| MISSING | 2 |
| **TOPLAM** | **21** |

**Base type dogru: 8 / 19** (MISSING dosyalar haric)

## Tum karsilastirma

| dosya | n | kaynak | GT base | GT anomali | model base | model anomali | base✓ | match |
|---|---|---|---|---|---|---|---|---|
| W1.csv | 45 | Wei | stationary | point_anomaly | stochastic_trend | collective_anomaly, variance_shift | ✗ | NONE |
| W2.csv | 302 | Wei | stationary | variance_shift | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | ✗ | NONE |
| W3.csv | 82 | Wei | stationary | variance_shift | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
| W5.csv | 71 | Wei | deterministic_trend | mean_shift | deterministic_trend | collective_anomaly, contextual_anomaly | ✓ | PARTIAL |
| W6.csv | 114 | Wei | deterministic_trend | variance_shift | deterministic_trend | collective_anomaly, contextual_anomaly | ✓ | PARTIAL |
| W10.csv | - | Wei | stochastic_trend | point_anomaly | (pipeline'a girmedi) | - | ✗ | MISSING |
| uspop.csv | 21 | Brockwell | deterministic_trend | - | deterministic_trend | collective_anomaly, contextual_anomaly | ✓ | PARTIAL |
| strikes.csv | 30 | Brockwell | stationary | - | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
| sunspots.csv | 100 | Brockwell | stationary | - | deterministic_trend | collective_anomaly, contextual_anomaly | ✗ | NONE |
| airpass.csv | 144 | Brockwell | stochastic_trend | - | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | ✗ | NONE |
| deaths.csv | 72 | Brockwell | stochastic_trend | - | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✗ | NONE |
| INDPRO.csv | 372 | Shumway | stochastic_trend | - | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | ✗ | NONE |
| UNRATE.csv | 372 | Shumway | stochastic_trend | - | deterministic_trend | collective_anomaly | ✗ | NONE |
| soi_dataframe.csv | 453 | Shumway | stationary | - | stochastic_trend | collective_anomaly | ✗ | NONE |
| rec_dataframe.csv | - | Shumway | stationary | - | (pipeline'a girmedi) | - | ✗ | MISSING |
| GermanGNP.csv | 88 | JMulTi | deterministic_trend | trend_shift | deterministic_trend | collective_anomaly, contextual_anomaly | ✓ | PARTIAL |
| US_investment.csv | 104 | JMulTi | stationary | - | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
| German_consumption.csv | 93 | JMulTi | stochastic_trend | - | deterministic_trend | collective_anomaly, contextual_anomaly | ✗ | NONE |
| Polish_productivity.csv | 117 | JMulTi | stochastic_trend | trend_shift | volatility | collective_anomaly, point_anomaly | ✗ | NONE |
| RealInt_dataframe.csv | 103 | Bai-Perron | stationary | mean_shift | deterministic_trend | collective_anomaly, contextual_anomaly | ✗ | NONE |
| NP_xetradax_returns100.csv | 1028 | Lutkepohl | stationary | - | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |

## Detayli notlar (PDF'ten)

| dosya | not |
|---|---|
| W1.csv | stationary, AO/IO outliers at t=4,7,9,36 |
| W2.csv | stationary in mean, possibly variance shift |
| W3.csv | stationary in mean, possibly variance shift |
| W5.csv | non-stat in mean, increasing trend, TC at t=81,82 |
| W6.csv | non-stat in mean AND variance |
| W10.csv | seasonal unit root, outliers t=12,27 (cok kisa n=32) |
| uspop.csv | exponentially increasing (US population) |
| strikes.csv | erratic, slowly rising level — pratikte stationary |
| sunspots.csv | Wolfer sunspots, cyclic period ~11 years |
| airpass.csv | regular + seasonal stochastic trend |
| deaths.csv | regular + seasonal unit root (period 12) |
| INDPRO.csv | ARIMA(0,1,1)(0,1,1)_12 — seasonal stochastic trend |
| UNRATE.csv | Monthly Fed Unemployment 1948-1978 |
| soi_dataframe.csv | Southern Oscillation Index, cyclic ~1/yr |
| rec_dataframe.csv | Recruitment series — stationary (BIZDE n=0) |
| GermanGNP.csv | structural break at 1990Q3 (German unification) |
| US_investment.csv | better as I(0) than I(1) |
| German_consumption.csv | log consumption has unit root |
| Polish_productivity.csv | structural shift 1990Q1 |
| RealInt_dataframe.csv | US real interest rate, breaks at 1966,1972,1980 |
| NP_xetradax_returns100.csv | DAX log returns (finansal teori: stationary) |

## KESIN STATIONARY oldugu bilinen dosyalar

PDF'te acikca 'stationary' diye etiketlenmis dosyalar:

| dosya | n | kaynak | model base | model anomali | base✓ | match |
|---|---|---|---|---|---|---|
| W1.csv | 45 | Wei | stochastic_trend | collective_anomaly, variance_shift | ✗ | NONE |
| W2.csv | 302 | Wei | deterministic_trend | collective_anomaly, contextual_anomaly, point_anomaly | ✗ | NONE |
| W3.csv | 82 | Wei | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
| strikes.csv | 30 | Brockwell | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
| sunspots.csv | 100 | Brockwell | deterministic_trend | collective_anomaly, contextual_anomaly | ✗ | NONE |
| soi_dataframe.csv | 453 | Shumway | stochastic_trend | collective_anomaly | ✗ | NONE |
| rec_dataframe.csv | - | Shumway | (pipeline'a girmedi) | - | ✗ | MISSING |
| US_investment.csv | 104 | JMulTi | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
| RealInt_dataframe.csv | 103 | Bai-Perron | deterministic_trend | collective_anomaly, contextual_anomaly | ✗ | NONE |
| NP_xetradax_returns100.csv | 1028 | Lutkepohl | stationary | collective_anomaly, contextual_anomaly, mean_shift, point_anomaly, trend_shift, variance_shift | ✓ | PARTIAL |
