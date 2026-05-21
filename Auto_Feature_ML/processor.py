"""
Auto Feature Extraction Processor - NO WINDOWING
Uses tsfresh to extract features directly from entire time series
Each time series = 1 sample (not windowed)
"""
import numpy as np
import pandas as pd
from pathlib import Path
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute
from sklearn.preprocessing import StandardScaler
import joblib
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

from config import (
    GENERATED_DATA_DIR, PROCESSED_DATA_DIR, CLASSES, LABEL_MAP,
    SAMPLES_PER_CLASS, RANDOM_STATE, TSFRESH_SETTINGS
)


class AutoFeatureProcessor:
    """Automatic feature extraction using tsfresh - NO WINDOWING"""

    def __init__(self):
        self.scaler = None
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    def load_and_sample_data(self):
        """Load balanced samples from each class"""
        print("\n" + "="*70)
        print("LOADING AND SAMPLING DATA")
        print("="*70)

        all_samples = []
        all_labels = []

        np.random.seed(RANDOM_STATE)

        for class_name in CLASSES:
            class_dir = GENERATED_DATA_DIR / class_name
            if not class_dir.exists():
                print(f"[WARNING] {class_name} folder not found!")
                continue

            # Get all CSV files (including subdirectories)
            csv_files = list(class_dir.glob("**/*.csv"))

            if len(csv_files) == 0:
                print(f"[WARNING] No CSV files in {class_name}!")
                continue

            # Sample SAMPLES_PER_CLASS files
            n_available = len(csv_files)
            n_to_sample = min(SAMPLES_PER_CLASS, n_available)

            sampled_files = np.random.choice(csv_files, size=n_to_sample, replace=False)

            print(f"{class_name:25s}: {n_to_sample:5d} samples (from {n_available})")

            # Load sampled files
            for file_path in sampled_files:
                try:
                    df = pd.read_csv(file_path)

                    # Get time series data (first numerical column)
                    if 'data' in df.columns:
                        ts_data = df['data'].values
                    elif 'value' in df.columns:
                        ts_data = df['value'].values
                    else:
                        ts_data = df.iloc[:, 0].values

                    # Ensure numeric and remove NaN
                    ts_data = pd.to_numeric(ts_data, errors='coerce')
                    ts_data = ts_data[~np.isnan(ts_data)]

                    if len(ts_data) > 0:
                        all_samples.append(ts_data)
                        all_labels.append(LABEL_MAP[class_name])

                except Exception as e:
                    print(f"[ERROR] Failed to load {file_path}: {e}")
                    continue

        print(f"\n[OK] Total samples loaded: {len(all_samples)}")
        print(f"[OK] Classes: {len(CLASSES)}")

        return all_samples, np.array(all_labels)

    def extract_tsfresh_features(self, all_samples, all_labels):
        """Extract features using tsfresh - NO WINDOWING"""
        print("\n" + "="*70)
        print("EXTRACTING FEATURES WITH TSFRESH (NO WINDOWING)")
        print("="*70)
        print(f"tsfresh mode: {TSFRESH_SETTINGS['default_fc_parameters']}")
        print(f"Each time series = 1 sample (entire series used)")

        # Prepare data for tsfresh (requires specific format)
        df_list = []

        print("\n[1/3] Converting time series to tsfresh format...")

        for sample_id, ts_data in enumerate(tqdm(all_samples)):
            # Each time series becomes ONE sample (no windowing)
            for time_idx, value in enumerate(ts_data):
                df_list.append({
                    'id': sample_id,  # Unique sample ID
                    'time': time_idx,  # Time index within series
                    'value': value,  # Time series value
                })

        df_ts = pd.DataFrame(df_list)

        # Ensure correct data types for tsfresh
        df_ts['id'] = df_ts['id'].astype(int)
        df_ts['time'] = df_ts['time'].astype(int)
        df_ts['value'] = df_ts['value'].astype(float)  # Critical: must be float

        print(f"[OK] Created time series dataframe: {len(df_ts)} rows")
        print(f"[OK] Total samples: {len(all_samples)}")
        print(f"[OK] Data types: {df_ts.dtypes.to_dict()}")

        # Extract features using tsfresh
        print("\n[2/3] Running tsfresh feature extraction...")
        print("This may take 10-30 minutes depending on CPU...")

        # Use feature set from config
        if TSFRESH_SETTINGS['default_fc_parameters'] == 'minimal':
            fc_parameters = MinimalFCParameters()
        elif TSFRESH_SETTINGS['default_fc_parameters'] == 'efficient':
            fc_parameters = EfficientFCParameters()
        else:
            fc_parameters = TSFRESH_SETTINGS['default_fc_parameters']

        extracted_features = extract_features(
            df_ts,
            column_id='id',
            column_sort='time',
            column_value='value',
            default_fc_parameters=fc_parameters,
            n_jobs=TSFRESH_SETTINGS['n_jobs'],
            chunksize=TSFRESH_SETTINGS['chunksize'],
            disable_progressbar=TSFRESH_SETTINGS['disable_progressbar'],
            show_warnings=TSFRESH_SETTINGS['show_warnings']
        )

        print(f"\n[OK] Extracted features shape: {extracted_features.shape}")
        print(f"[OK] Number of features: {extracted_features.shape[1]}")

        # Impute NaN values (tsfresh sometimes generates NaN)
        print("\n[3/3] Imputing NaN values...")
        impute(extracted_features)

        # Labels are already in correct order (sample_id matches index)
        return extracted_features.values, all_labels, list(extracted_features.columns)

    def scale_features(self, X_train, X_test):
        """Standardize features"""
        print("\n" + "="*70)
        print("SCALING FEATURES")
        print("="*70)

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print(f"[OK] Scaled features using StandardScaler")
        print(f"[OK] Train shape: {X_train_scaled.shape}")
        print(f"[OK] Test shape: {X_test_scaled.shape}")

        return X_train_scaled, X_test_scaled

    def save_processed_data(self, X_train, X_test, y_train, y_test, feature_names):
        """Save processed data and scaler"""
        print("\n" + "="*70)
        print("SAVING PROCESSED DATA")
        print("="*70)

        np.save(PROCESSED_DATA_DIR / 'X_train.npy', X_train)
        np.save(PROCESSED_DATA_DIR / 'X_test.npy', X_test)
        np.save(PROCESSED_DATA_DIR / 'y_train.npy', y_train)
        np.save(PROCESSED_DATA_DIR / 'y_test.npy', y_test)

        # Save feature names
        with open(PROCESSED_DATA_DIR / 'feature_names.txt', 'w') as f:
            for name in feature_names:
                f.write(f"{name}\n")

        # Save scaler
        joblib.dump(self.scaler, PROCESSED_DATA_DIR / 'scaler.pkl')

        print(f"[OK] Saved to {PROCESSED_DATA_DIR}")
        print(f"[OK] X_train: {X_train.shape}")
        print(f"[OK] X_test: {X_test.shape}")
        print(f"[OK] y_train: {y_train.shape}")
        print(f"[OK] y_test: {y_test.shape}")
        print(f"[OK] Features: {len(feature_names)}")

    def process_all(self):
        """Main processing pipeline"""
        print("\n" + "="*70)
        print("AUTO FEATURE EXTRACTION PIPELINE - NO WINDOWING")
        print("="*70)

        # Load balanced samples
        all_samples, all_labels = self.load_and_sample_data()

        # Extract tsfresh features (NO WINDOWING)
        X, y, feature_names = self.extract_tsfresh_features(all_samples, all_labels)

        # Train/test split (stratified)
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
        )

        print("\n" + "="*70)
        print("TRAIN/TEST SPLIT")
        print("="*70)
        print(f"Train samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")

        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)

        # Save
        self.save_processed_data(X_train_scaled, X_test_scaled, y_train, y_test, feature_names)

        print("\n" + "="*70)
        print("PROCESSING COMPLETE!")
        print("="*70)
        print(f"Next step: Run trainer.py to train models")


if __name__ == "__main__":
    processor = AutoFeatureProcessor()
    processor.process_all()
