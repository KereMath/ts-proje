"""
ens-final (CONTEXTUAL-OFF) - Konfigurasyon
Meta-stacking 8 eski + 9 yeni ensemble probability, 5 anomali.
Grup 6 (contextual_anomaly) cikarildi -> 38 grup.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent.parent   # ceylanhoca/
GD       = Path(r"c:\Users\Pc\Desktop\ceylanhoca\contextual-off\data_10x\generated")
COMB     = GD / "Combinations"

# Eski ensemble: ts-proje'deki orjinal trained_models (degismez)
OLD_ENSEMBLE_DIR = ROOT_DIR / "tsfresh-ensemble-stationary" / "trained_models"
# Yeni ensemble: kendi 9-modelimiz
NEW_ENSEMBLE_DIR = ROOT_DIR / "contextual-off-10x" / "ensemble-alldata" / "trained_models"
# Stationarity detector: degismez
STATIONARY_DETECTOR_DIR = ROOT_DIR / "stationary-detection-ml" / "models"

META_MODELS_DIR = BASE_DIR / "meta_models"
PROCESSED_DIR   = BASE_DIR / "processed_data"
RESULTS_DIR     = BASE_DIR / "results"

META_N_PER_GROUP   = 80  # 10x
MIN_SERIES_LENGTH  = 50
RANDOM_STATE       = 42
TEST_SIZE          = 0.20

# -------------------------------------------------------------------
# 38 Kaynak Grubu (Grup 6 = contextual_anomaly CIKARILDI)
# -------------------------------------------------------------------
SOURCE_GROUPS = [
    (1,  "stationary",           [GD / "stationary"]),
    (2,  "deterministic_trend",  [GD / "deterministic_trend"]),
    (3,  "stochastic_trend",     [GD / "Stochastic Trend"]),
    (4,  "volatility",           [GD / "Volatility"]),
    (5,  "collective_anomaly",   [GD / "collective_anomaly"]),
    # (6,  "contextual_anomaly" --- CIKARILDI ---
    (7,  "mean_shift",           [GD / "mean_shift"]),
    (8,  "point_anomaly",        [GD / "point_anomaly"]),
    (9,  "trend_shift",          [GD / "trend_shift"]),
    (10, "variance_shift",       [GD / "variance_shift"]),
    (11, "cubic+collective",     [COMB / "Cubic Base" / "Cubic Base" / "cubic_collective_anomaly"]),
    (12, "cubic+mean_shift",     [COMB / "Cubic Base" / "Cubic Base" / "Cubic + Mean Shift"]),
    (13, "cubic+point_anomaly",  [COMB / "Cubic Base" / "Cubic Base" / "Cubic + Point Anomaly"]),
    (14, "cubic+variance_shift", [COMB / "Cubic Base" / "Cubic Base" / "Cubic + Variance Shift"]),
    (15, "damped+collective",    [COMB / "Damped Base" / "Damped Base" / "Damped + Collective Anomaly"]),
    (16, "damped+mean_shift",    [COMB / "Damped Base" / "Damped Base" / "Damped + Mean Shift"]),
    (17, "damped+point_anomaly", [COMB / "Damped Base" / "Damped Base" / "Damped + Point Anomaly"]),
    (18, "damped+variance_shift",[COMB / "Damped Base" / "Damped Base" / "Damped + Variance Shift"]),
    (19, "exp+collective",       [COMB / "Exponential Base" / "Exponential Base" / "exponential_collective_anomaly"]),
    (20, "exp+mean_shift",       [COMB / "Exponential Base" / "Exponential Base" / "Exponential + Mean Shift"]),
    (21, "exp+point_anomaly",    [COMB / "Exponential Base" / "Exponential Base" / "exponential_point_anomaly"]),
    (22, "exp+variance_shift",   [COMB / "Exponential Base" / "Exponential Base" / "exponential_variance_shift"]),
    (23, "linear+collective",    [COMB / "Linear Base" / "Linear Base" / "Linear + Collective Anomaly"]),
    (24, "linear+mean_shift",    [COMB / "Linear Base" / "Linear Base" / "Linear + Mean Shift"]),
    (25, "linear+point_anomaly", [COMB / "Linear Base" / "Linear Base" / "Linear + Point Anomaly"]),
    (26, "linear+trend_shift",   [COMB / "Linear Base" / "Linear Base" / "Linear + Trend Shift"]),
    (27, "linear+variance_shift",[COMB / "Linear Base" / "Linear Base" / "Linear + Variance Shift"]),
    (28, "quad+collective",      [COMB / "Quadratic Base" / "Quadratic Base" / "Quadratic + Collective anomaly"]),
    (29, "quad+mean_shift",      [COMB / "Quadratic Base" / "Quadratic Base" / "Quadratic + Mean Shift"]),
    (30, "quad+point_anomaly",   [COMB / "Quadratic Base" / "Quadratic Base" / "Quadratic + Point Anomaly"]),
    (31, "quad+variance_shift",  [COMB / "Quadratic Base" / "Quadratic Base" / "Quadratic + Variance Shift"]),
    (32, "stoch+collective",     [COMB / "Stochastic Trend + Collective Anomaly"]),
    (33, "stoch+mean_shift",     [COMB / "Stochastic Trend + Mean Shift"]),
    (34, "stoch+point_anomaly",  [COMB / "Stochastic Trend + Point Anomaly"]),
    (35, "stoch+variance_shift", [COMB / "Stochastic Trend + Variance Shift" / "Stochastic Trend + Variance Shift"]),
    (36, "vol+collective",       [COMB / "Volatility + Collective Anomaly"]),
    (37, "vol+mean_shift",       [COMB / "Volatility + Mean Shift"]),
    (38, "vol+point_anomaly",    [COMB / "Volatility + Point Anomaly"]),
    (39, "vol+variance_shift",   [COMB / "Volatility + Variance Shift"]),
]

GROUP_PATHS = {gid: paths for gid, _, paths in SOURCE_GROUPS}
GROUP_NAMES = {gid: name  for gid, name, _ in SOURCE_GROUPS}

# -------------------------------------------------------------------
# Eski ensemble (8 class, contextual_anomaly CIKARILDI)
# -------------------------------------------------------------------
OLD_CLASSES = [
    "collective_anomaly", "deterministic_trend",
    "mean_shift", "point_anomaly", "stochastic_trend",
    "trend_shift", "variance_shift", "volatility",
]

# -------------------------------------------------------------------
# Yeni ensemble (9 model, contextual_anomaly CIKARILDI)
# -------------------------------------------------------------------
NEW_ALL_MODELS = [
    "stationary", "deterministic_trend", "stochastic_trend", "volatility",
    "collective_anomaly", "mean_shift",
    "point_anomaly", "trend_shift", "variance_shift",
]
NEW_BASE_MODELS    = ["stationary", "deterministic_trend", "stochastic_trend", "volatility"]
NEW_ANOMALY_MODELS = ["collective_anomaly", "mean_shift",
                      "point_anomaly", "trend_shift", "variance_shift"]

BASE_LABELS = ["stationary", "deterministic_trend", "stochastic_trend", "volatility"]
ANOM_LABELS = ["collective_anomaly", "mean_shift",
               "point_anomaly", "trend_shift", "variance_shift"]

# -------------------------------------------------------------------
# Grup beklenen etiketleri (ground truth)
# Grup 6 yok
# -------------------------------------------------------------------
GROUP_EXPECTED = {
    1:  {"base": "stationary",          "anomalies": []},
    2:  {"base": "deterministic_trend", "anomalies": []},
    3:  {"base": "stochastic_trend",    "anomalies": []},
    4:  {"base": "volatility",          "anomalies": []},
    5:  {"base": "stationary",          "anomalies": ["collective_anomaly"]},
    7:  {"base": "stationary",          "anomalies": ["mean_shift"]},
    8:  {"base": "stationary",          "anomalies": ["point_anomaly"]},
    9:  {"base": "stationary",          "anomalies": ["trend_shift"]},
    10: {"base": "stationary",          "anomalies": ["variance_shift"]},
    11: {"base": "deterministic_trend", "anomalies": ["collective_anomaly"]},
    12: {"base": "deterministic_trend", "anomalies": ["mean_shift"]},
    13: {"base": "deterministic_trend", "anomalies": ["point_anomaly"]},
    14: {"base": "deterministic_trend", "anomalies": ["variance_shift"]},
    15: {"base": "deterministic_trend", "anomalies": ["collective_anomaly"]},
    16: {"base": "deterministic_trend", "anomalies": ["mean_shift"]},
    17: {"base": "deterministic_trend", "anomalies": ["point_anomaly"]},
    18: {"base": "deterministic_trend", "anomalies": ["variance_shift"]},
    19: {"base": "deterministic_trend", "anomalies": ["collective_anomaly"]},
    20: {"base": "deterministic_trend", "anomalies": ["mean_shift"]},
    21: {"base": "deterministic_trend", "anomalies": ["point_anomaly"]},
    22: {"base": "deterministic_trend", "anomalies": ["variance_shift"]},
    23: {"base": "deterministic_trend", "anomalies": ["collective_anomaly"]},
    24: {"base": "deterministic_trend", "anomalies": ["mean_shift"]},
    25: {"base": "deterministic_trend", "anomalies": ["point_anomaly"]},
    26: {"base": "deterministic_trend", "anomalies": ["trend_shift"]},
    27: {"base": "deterministic_trend", "anomalies": ["variance_shift"]},
    28: {"base": "deterministic_trend", "anomalies": ["collective_anomaly"]},
    29: {"base": "deterministic_trend", "anomalies": ["mean_shift"]},
    30: {"base": "deterministic_trend", "anomalies": ["point_anomaly"]},
    31: {"base": "deterministic_trend", "anomalies": ["variance_shift"]},
    32: {"base": "stochastic_trend",    "anomalies": ["collective_anomaly"]},
    33: {"base": "stochastic_trend",    "anomalies": ["mean_shift"]},
    34: {"base": "stochastic_trend",    "anomalies": ["point_anomaly"]},
    35: {"base": "stochastic_trend",    "anomalies": ["variance_shift"]},
    36: {"base": "volatility",          "anomalies": ["collective_anomaly"]},
    37: {"base": "volatility",          "anomalies": ["mean_shift"]},
    38: {"base": "volatility",          "anomalies": ["point_anomaly"]},
    39: {"base": "volatility",          "anomalies": ["variance_shift"]},
}

# Meta-feature isimleri (17 boyut: 8 old + 9 new)
META_FEATURE_NAMES = (
    [f"old_{c}" for c in OLD_CLASSES] +
    [f"new_{c}" for c in NEW_ALL_MODELS]
)
