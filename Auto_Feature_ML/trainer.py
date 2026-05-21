"""
Auto Feature ML - Model Trainer
Trains LightGBM, XGBoost, Random Forest, and MLP with feature importance analysis
"""
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import lightgbm as lgb
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from config import (
    PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, CLASSES,
    MODELS_TO_TRAIN, HYPERPARAM_GRIDS, CROSS_VALIDATION_FOLDS,
    RANDOM_STATE, FEATURE_IMPORTANCE_TOP_N
)


class AutoFeatureMLTrainer:
    """Train ML models with automatic feature extraction"""

    def __init__(self):
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None

    def load_data(self):
        """Load processed data"""
        print("\n" + "="*70)
        print("LOADING PROCESSED DATA")
        print("="*70)

        self.X_train = np.load(PROCESSED_DATA_DIR / 'X_train.npy')
        self.X_test = np.load(PROCESSED_DATA_DIR / 'X_test.npy')
        self.y_train = np.load(PROCESSED_DATA_DIR / 'y_train.npy')
        self.y_test = np.load(PROCESSED_DATA_DIR / 'y_test.npy')

        # Load feature names
        with open(PROCESSED_DATA_DIR / 'feature_names.txt', 'r') as f:
            self.feature_names = [line.strip() for line in f.readlines()]

        print(f"[OK] X_train: {self.X_train.shape}")
        print(f"[OK] X_test: {self.X_test.shape}")
        print(f"[OK] y_train: {self.y_train.shape}")
        print(f"[OK] y_test: {self.y_test.shape}")
        print(f"[OK] Features: {len(self.feature_names)}")

    def get_model(self, model_name):
        """Get model instance"""
        if model_name == 'lightgbm':
            return lgb.LGBMClassifier(random_state=RANDOM_STATE, verbose=-1)
        elif model_name == 'xgboost':
            return xgb.XGBClassifier(random_state=RANDOM_STATE, verbosity=0)
        elif model_name == 'random_forest':
            return RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)
        elif model_name == 'mlp':
            return MLPClassifier(random_state=RANDOM_STATE, max_iter=500, early_stopping=True)
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def train_model(self, model_name):
        """Train a single model with GridSearchCV"""
        print("\n" + "="*70)
        print(f"TRAINING: {model_name.upper()}")
        print("="*70)

        # Get model and param grid
        base_model = self.get_model(model_name)
        param_grid = HYPERPARAM_GRIDS[model_name]

        print(f"Model: {model_name}")
        print(f"Hyperparameter combinations: {np.prod([len(v) for v in param_grid.values()])}")
        print(f"Cross-validation folds: {CROSS_VALIDATION_FOLDS}")

        # GridSearchCV
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=CROSS_VALIDATION_FOLDS,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )

        print("\nStarting GridSearchCV...")
        grid_search.fit(self.X_train, self.y_train)

        print(f"\n[OK] Best parameters: {grid_search.best_params_}")
        print(f"[OK] Best CV score: {grid_search.best_score_:.4f}")

        # Get best model
        best_model = grid_search.best_estimator_

        # Test accuracy
        y_pred = best_model.predict(self.X_test)
        test_acc = accuracy_score(self.y_test, y_pred)

        print(f"[OK] Test accuracy: {test_acc:.4f}")

        # Save model
        model_path = MODELS_DIR / f"{model_name}_best.pkl"
        joblib.dump(best_model, model_path)
        print(f"[OK] Model saved to {model_path}")

        return best_model, y_pred, test_acc, grid_search.best_params_

    def analyze_feature_importance(self, model, model_name):
        """Analyze feature importance (tree-based models only)"""
        print("\n" + "="*70)
        print(f"FEATURE IMPORTANCE ANALYSIS - {model_name.upper()}")
        print("="*70)

        if model_name not in ['lightgbm', 'xgboost', 'random_forest']:
            print("[SKIP] Feature importance only for tree-based models")
            return None

        # Get feature importances
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        else:
            print("[SKIP] Model does not have feature_importances_")
            return None

        # Create dataframe
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)

        print(f"\n[Top {FEATURE_IMPORTANCE_TOP_N} Most Important Features]")
        print(importance_df.head(FEATURE_IMPORTANCE_TOP_N).to_string(index=False))

        # Save to file
        importance_df.to_csv(REPORTS_DIR / f'{model_name}_feature_importance.csv', index=False)
        print(f"\n[OK] Saved full feature importance to {model_name}_feature_importance.csv")

        # Plot top features
        plt.figure(figsize=(12, 8))
        top_features = importance_df.head(FEATURE_IMPORTANCE_TOP_N)
        plt.barh(range(len(top_features)), top_features['importance'].values)
        plt.yticks(range(len(top_features)), top_features['feature'].values)
        plt.xlabel('Importance')
        plt.title(f'{model_name.upper()} - Top {FEATURE_IMPORTANCE_TOP_N} Features')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / f'{model_name}_feature_importance.png', dpi=150)
        plt.close()

        return importance_df

    def analyze_feature_importance_per_class(self, model, model_name):
        """Analyze which features are most important for each class"""
        print("\n" + "="*70)
        print(f"PER-CLASS FEATURE IMPORTANCE - {model_name.upper()}")
        print("="*70)

        if model_name not in ['lightgbm', 'xgboost', 'random_forest']:
            print("[SKIP] Per-class analysis only for tree-based models")
            return

        # Train separate models for each class (one-vs-rest)
        per_class_importance = {}

        for class_idx, class_name in enumerate(CLASSES):
            print(f"\n[{class_idx+1}/{len(CLASSES)}] Analyzing {class_name}...")

            # Binary labels (one-vs-rest)
            y_binary = (self.y_train == class_idx).astype(int)

            # Train simple model (no GridSearch, just default + best overall params)
            if model_name == 'lightgbm':
                clf = lgb.LGBMClassifier(random_state=RANDOM_STATE, verbose=-1, n_estimators=200)
            elif model_name == 'xgboost':
                clf = xgb.XGBClassifier(random_state=RANDOM_STATE, verbosity=0, n_estimators=200)
            else:  # random_forest
                clf = RandomForestClassifier(random_state=RANDOM_STATE, n_estimators=200, n_jobs=-1)

            clf.fit(self.X_train, y_binary)

            # Get importances
            importances = clf.feature_importances_
            importance_df = pd.DataFrame({
                'feature': self.feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)

            per_class_importance[class_name] = importance_df.head(10)  # Top 10 per class

            print(f"[Top 5 features for {class_name}]")
            print(importance_df.head(5)[['feature', 'importance']].to_string(index=False))

        # Save per-class importance
        with open(REPORTS_DIR / f'{model_name}_per_class_importance.txt', 'w') as f:
            f.write(f"PER-CLASS FEATURE IMPORTANCE - {model_name.upper()}\n")
            f.write("="*70 + "\n\n")

            for class_name, df in per_class_importance.items():
                f.write(f"\n{class_name}:\n")
                f.write(df[['feature', 'importance']].to_string(index=False))
                f.write("\n" + "-"*70 + "\n")

        print(f"\n[OK] Saved per-class importance to {model_name}_per_class_importance.txt")

    def generate_reports(self, model_name, y_pred, test_acc, best_params):
        """Generate confusion matrix and classification report"""
        print("\n" + "="*70)
        print(f"GENERATING REPORTS - {model_name.upper()}")
        print("="*70)

        # Confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)

        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=CLASSES, yticklabels=CLASSES)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title(f'{model_name.upper()} - Confusion Matrix\nTest Accuracy: {test_acc:.4f}')
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / f'{model_name}_confusion_matrix.png', dpi=150)
        plt.close()

        # Classification report
        report = classification_report(self.y_test, y_pred, target_names=CLASSES, output_dict=True)

        # Save report
        report_data = {
            'model': model_name,
            'test_accuracy': float(test_acc),
            'best_params': best_params,
            'classification_report': report,
            'confusion_matrix': cm.tolist()
        }

        import json
        with open(REPORTS_DIR / f'{model_name}_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"[OK] Confusion matrix saved")
        print(f"[OK] Classification report saved")

    def train_all_models(self):
        """Train all models and analyze features"""
        print("\n" + "="*70)
        print("AUTO FEATURE ML - TRAINING ALL MODELS")
        print("="*70)

        results = {}

        for model_name in MODELS_TO_TRAIN:
            # Train model
            model, y_pred, test_acc, best_params = self.train_model(model_name)
            results[model_name] = test_acc

            # Feature importance (overall)
            self.analyze_feature_importance(model, model_name)

            # Per-class feature importance
            self.analyze_feature_importance_per_class(model, model_name)

            # Generate reports
            self.generate_reports(model_name, y_pred, test_acc, best_params)

        # Summary
        print("\n" + "="*70)
        print("TRAINING COMPLETE - SUMMARY")
        print("="*70)
        for model_name, acc in sorted(results.items(), key=lambda x: x[1], reverse=True):
            print(f"{model_name:20s}: {acc:.4f} ({acc*100:.2f}%)")


if __name__ == "__main__":
    trainer = AutoFeatureMLTrainer()
    trainer.load_data()
    trainer.train_all_models()
