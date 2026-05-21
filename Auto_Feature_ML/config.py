"""
Auto Feature Extraction ML - Configuration Module
Automatic feature extraction using tsfresh (700+ features)
9-class time series classification
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
GENERATED_DATA_DIR = BASE_DIR / "Generated Data"
ML_DIR = BASE_DIR / "Auto_Feature_ML_No_Window_12K"

# Output directories
PROCESSED_DATA_DIR = ML_DIR / "processed_data_no_window_12k"
MODELS_DIR = ML_DIR / "trained_models_no_window_12k"
REPORTS_DIR = ML_DIR / "reports_no_window_12k"

# 9 classes (excluding stationary)
CLASSES = [
    'collective_anomaly',
    'contextual_anomaly',
    'deterministic_trend',
    'mean_shift',
    'point_anomaly',
    'Stochastic Trend',
    'trend_shift',
    'variance_shift',
    'Volatility'
]

# Label mapping: folder name -> class index
LABEL_MAP = {class_name: idx for idx, class_name in enumerate(CLASSES)}

# Data Processing Settings
SAMPLES_PER_CLASS = 12000  # Balanced sampling (12K per class) - NO WINDOWING
RANDOM_STATE = 42

# tsfresh Feature Extraction Settings (NO WINDOWING)
TSFRESH_SETTINGS = {
    'default_fc_parameters': 'efficient',  # Use efficient for better features
    'n_jobs': 4,  # Use all CPU cores
    'chunksize': 500,  # Process in chunks
    'disable_progressbar': False,
    'show_warnings': False
}

# Model Training Settings
TRAIN_SIZE = 0.8
VAL_SIZE = 0.1
TEST_SIZE = 0.1
CROSS_VALIDATION_FOLDS = 3  # For hyperparameter tuning

# Models to train (same as single detector ml)
MODELS_TO_TRAIN = [
    'lightgbm',
    'xgboost',
    'random_forest',
    'mlp'
]

# Hyperparameter grids (same as single detector ml)
HYPERPARAM_GRIDS = {
    'lightgbm': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05],
        'max_depth': [7, 10],
        'num_leaves': [31, 50]
    },
    'xgboost': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05],
        'max_depth': [5, 10],
        'subsample': [0.8, 1.0]
    },
    'random_forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [15, 20],
        'min_samples_split': [2, 5]
    },
    'mlp': {
        'hidden_layer_sizes': [(128, 64), (256, 128)],
        'activation': ['relu', 'tanh'],
        'alpha': [0.0001, 0.001],
        'learning_rate_init': [0.001, 0.01]
    }
}

# Feature importance settings
FEATURE_IMPORTANCE_TOP_N = 20  # Top N features to report per class
