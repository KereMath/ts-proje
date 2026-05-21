"""
Standalone Stationary Detector Wrapper.
Uses stationary-detection-ml/models/ (GradientBoosting + scaler).
Feature extraction matches stationary-detection-ml/feature_extraction.py (21 features).
"""
import json
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
from scipy import stats

from config import STATIONARY_DETECTOR_DIR


# ===================================================================
# Feature Extraction (21 features - matches training)
# ===================================================================
def _autocorr(series, lag):
    if lag >= len(series) or lag < 1:
        return 0
    n = len(series)
    mean = np.mean(series)
    c0 = np.sum((series - mean) ** 2) / n
    if c0 == 0:
        return 0
    ck = np.sum((series[:-lag] - mean) * (series[lag:] - mean)) / n
    return ck / c0


def extract_feature_vector(series: np.ndarray) -> Optional[np.ndarray]:
    """21 feature: mean, std, var, skewness, kurtosis, min, max, range,
       q25, q75, iqr, diff_mean, diff_std, diff_var, diff2_mean, diff2_std,
       acf_1, acf_5, trend_slope, trend_r2, length."""
    if len(series) < 2:
        return None
    try:
        features = []
        features.append(float(np.mean(series)))
        features.append(float(np.std(series)))
        features.append(float(np.var(series)))
        features.append(float(stats.skew(series)))
        features.append(float(stats.kurtosis(series)))
        features.append(float(np.min(series)))
        features.append(float(np.max(series)))
        features.append(float(np.max(series) - np.min(series)))
        features.append(float(np.percentile(series, 25)))
        features.append(float(np.percentile(series, 75)))
        features.append(float(features[9] - features[8]))

        diff1 = np.diff(series)
        if len(diff1) > 0:
            features.append(float(np.mean(diff1)))
            features.append(float(np.std(diff1)))
            features.append(float(np.var(diff1)))
        else:
            features.extend([0.0, 0.0, 0.0])

        if len(diff1) > 1:
            diff2 = np.diff(diff1)
            features.append(float(np.mean(diff2)))
            features.append(float(np.std(diff2)))
        else:
            features.extend([0.0, 0.0])

        a1 = _autocorr(series, 1)
        a5 = _autocorr(series, 5)
        features.append(float(a1) if not np.isnan(a1) else 0.0)
        features.append(float(a5) if not np.isnan(a5) else 0.0)

        try:
            x = np.arange(len(series))
            slope, intercept, r, _, _ = stats.linregress(x, series)
            features.append(float(slope))
            features.append(float(r ** 2))
        except Exception:
            features.append(0.0)
            features.append(0.0)

        features.append(float(len(series)))
        return np.array(features)
    except Exception:
        return None


# ===================================================================
# Model loading
# ===================================================================
def load_stationary_detector():
    """Loads GradientBoosting model + StandardScaler."""
    model = joblib.load(STATIONARY_DETECTOR_DIR / "best_model.pkl")
    scaler = joblib.load(STATIONARY_DETECTOR_DIR / "scaler.pkl")
    print(f"  Stationary detector yuklendi (GradientBoosting, {scaler.n_features_in_} feature)")
    # No selector for this model; pass None for compatibility
    return model, scaler, None


def predict_stationary(model, scaler, selector, series: np.ndarray) -> float:
    """Returns P(stationary). Training labels: 0=stationary, 1=non_stationary,
       so we return predict_proba[0, 0]."""
    fv = extract_feature_vector(series)
    if fv is None:
        return 0.0
    expected = scaler.n_features_in_
    if len(fv) != expected:
        if len(fv) < expected:
            fv = np.pad(fv, (0, expected - len(fv)), 'constant')
        else:
            fv = fv[:expected]
    scaled = scaler.transform(fv.reshape(1, -1))
    if selector is not None:
        scaled = selector.transform(scaled)
    probs = model.predict_proba(scaled)[0]
    # Index 0 = stationary
    return float(probs[0])


def predict_stationary_batch(model, scaler, selector, series_list) -> np.ndarray:
    expected = scaler.n_features_in_
    feat = np.zeros((len(series_list), expected))
    for i, s in enumerate(series_list):
        fv = extract_feature_vector(s)
        if fv is None:
            continue
        if len(fv) != expected:
            if len(fv) < expected:
                fv = np.pad(fv, (0, expected - len(fv)), 'constant')
            else:
                fv = fv[:expected]
        feat[i] = fv
    scaled = scaler.transform(feat)
    if selector is not None:
        scaled = selector.transform(scaled)
    probs = model.predict_proba(scaled)
    return probs[:, 0]
