"""
contextual-off icin 38 grup x 100 = 3800 seri uret.
Grup 6 (contextual_anomaly) zaten dahil degil.
"""
import json
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent  # ceylanhoca/
sys.path.insert(0, str(ROOT))

from betise.core.generator import TimeSeriesGenerator

OUT_BASE = Path(__file__).resolve().parent.parent / "data_10x" / "generated"
OUT_BASE.mkdir(parents=True, exist_ok=True)
COMB = OUT_BASE / "Combinations"

N_PER_GROUP = 1000  # 38 x 1000 = 38000 seri
LEN_RANGE = (80, 150)
SEED_BASE = 1000

# 38 grup (Grup 6 contextual_anomaly cikarildi)
GROUPS = [
    (1, "stationary", "stationary", {"base": "stationary"}),
    (2, "deterministic_trend", "deterministic_trend", {"base": "stationary", "trend": "linear"}),
    (3, "stochastic_trend", "Stochastic Trend", {"base": "stochastic"}),
    (4, "volatility", "Volatility", {"base": "volatility"}),
    (5, "collective_anomaly", "collective_anomaly", {"base": "stationary", "anomaly": "collective"}),
    # 6 CIKARILDI
    (7, "mean_shift", "mean_shift", {"base": "stationary", "break": "mean_shift"}),
    (8, "point_anomaly", "point_anomaly", {"base": "stationary", "anomaly": "point"}),
    (9, "trend_shift", "trend_shift", {"base": "stationary", "break": "trend_shift"}),
    (10, "variance_shift", "variance_shift", {"base": "stationary", "break": "variance_shift"}),
    (11, "cubic+collective", "Combinations/Cubic Base/Cubic Base/cubic_collective_anomaly",
        {"base": "stationary", "trend": "cubic", "anomaly": "collective"}),
    (12, "cubic+mean_shift", "Combinations/Cubic Base/Cubic Base/Cubic + Mean Shift",
        {"base": "stationary", "trend": "cubic", "break": "mean_shift"}),
    (13, "cubic+point_anomaly", "Combinations/Cubic Base/Cubic Base/Cubic + Point Anomaly",
        {"base": "stationary", "trend": "cubic", "anomaly": "point"}),
    (14, "cubic+variance_shift", "Combinations/Cubic Base/Cubic Base/Cubic + Variance Shift",
        {"base": "stationary", "trend": "cubic", "break": "variance_shift"}),
    (15, "damped+collective", "Combinations/Damped Base/Damped Base/Damped + Collective Anomaly",
        {"base": "stationary", "trend": "exponential", "trend_sign": -1, "anomaly": "collective"}),
    (16, "damped+mean_shift", "Combinations/Damped Base/Damped Base/Damped + Mean Shift",
        {"base": "stationary", "trend": "exponential", "trend_sign": -1, "break": "mean_shift"}),
    (17, "damped+point_anomaly", "Combinations/Damped Base/Damped Base/Damped + Point Anomaly",
        {"base": "stationary", "trend": "exponential", "trend_sign": -1, "anomaly": "point"}),
    (18, "damped+variance_shift", "Combinations/Damped Base/Damped Base/Damped + Variance Shift",
        {"base": "stationary", "trend": "exponential", "trend_sign": -1, "break": "variance_shift"}),
    (19, "exp+collective", "Combinations/Exponential Base/Exponential Base/exponential_collective_anomaly",
        {"base": "stationary", "trend": "exponential", "anomaly": "collective"}),
    (20, "exp+mean_shift", "Combinations/Exponential Base/Exponential Base/Exponential + Mean Shift",
        {"base": "stationary", "trend": "exponential", "break": "mean_shift"}),
    (21, "exp+point_anomaly", "Combinations/Exponential Base/Exponential Base/exponential_point_anomaly",
        {"base": "stationary", "trend": "exponential", "anomaly": "point"}),
    (22, "exp+variance_shift", "Combinations/Exponential Base/Exponential Base/exponential_variance_shift",
        {"base": "stationary", "trend": "exponential", "break": "variance_shift"}),
    (23, "linear+collective", "Combinations/Linear Base/Linear Base/Linear + Collective Anomaly",
        {"base": "stationary", "trend": "linear", "anomaly": "collective"}),
    (24, "linear+mean_shift", "Combinations/Linear Base/Linear Base/Linear + Mean Shift",
        {"base": "stationary", "trend": "linear", "break": "mean_shift"}),
    (25, "linear+point_anomaly", "Combinations/Linear Base/Linear Base/Linear + Point Anomaly",
        {"base": "stationary", "trend": "linear", "anomaly": "point"}),
    (26, "linear+trend_shift", "Combinations/Linear Base/Linear Base/Linear + Trend Shift",
        {"base": "stationary", "trend": "linear", "break": "trend_shift"}),
    (27, "linear+variance_shift", "Combinations/Linear Base/Linear Base/Linear + Variance Shift",
        {"base": "stationary", "trend": "linear", "break": "variance_shift"}),
    (28, "quad+collective", "Combinations/Quadratic Base/Quadratic Base/Quadratic + Collective anomaly",
        {"base": "stationary", "trend": "quadratic", "anomaly": "collective"}),
    (29, "quad+mean_shift", "Combinations/Quadratic Base/Quadratic Base/Quadratic + Mean Shift",
        {"base": "stationary", "trend": "quadratic", "break": "mean_shift"}),
    (30, "quad+point_anomaly", "Combinations/Quadratic Base/Quadratic Base/Quadratic + Point Anomaly",
        {"base": "stationary", "trend": "quadratic", "anomaly": "point"}),
    (31, "quad+variance_shift", "Combinations/Quadratic Base/Quadratic Base/Quadratic + Variance Shift",
        {"base": "stationary", "trend": "quadratic", "break": "variance_shift"}),
    (32, "stoch+collective", "Combinations/Stochastic Trend + Collective Anomaly",
        {"base": "stochastic", "anomaly": "collective"}),
    (33, "stoch+mean_shift", "Combinations/Stochastic Trend + Mean Shift",
        {"base": "stochastic", "break": "mean_shift"}),
    (34, "stoch+point_anomaly", "Combinations/Stochastic Trend + Point Anomaly",
        {"base": "stochastic", "anomaly": "point"}),
    (35, "stoch+variance_shift", "Combinations/Stochastic Trend + Variance Shift/Stochastic Trend + Variance Shift",
        {"base": "stochastic", "break": "variance_shift"}),
    (36, "vol+collective", "Combinations/Volatility + Collective Anomaly",
        {"base": "volatility", "anomaly": "collective"}),
    (37, "vol+mean_shift", "Combinations/Volatility + Mean Shift",
        {"base": "volatility", "break": "mean_shift"}),
    (38, "vol+point_anomaly", "Combinations/Volatility + Point Anomaly",
        {"base": "volatility", "anomaly": "point"}),
    (39, "vol+variance_shift", "Combinations/Volatility + Variance Shift",
        {"base": "volatility", "break": "variance_shift"}),
]


def gen_one_series(length, spec, seed):
    random.seed(seed)
    np.random.seed(seed)
    ts = TimeSeriesGenerator(length=length)
    base = spec.get("base", "stationary")
    if base == "stationary":
        df, _ = ts.generate_stationary_base_series(distribution="ar")
    elif base == "stochastic":
        kinds = ["rw", "rwd", "ari", "ima", "arima"]
        df, _ = ts.generate_stochastic_trend(kind=random.choice(kinds))
    elif base == "volatility":
        kinds = ["arch", "garch", "egarch", "aparch"]
        df, _ = ts.generate_volatility(kind=random.choice(kinds))
    else:
        raise ValueError(f"Unknown base: {base}")
    if "trend" in spec:
        sign = spec.get("trend_sign", 1)
        kind = spec["trend"]
        if kind == "linear":
            df, _ = ts.generate_deterministic_trend_linear(df, sign=sign)
        elif kind == "quadratic":
            df, _ = ts.generate_deterministic_trend_quadratic(df, sign=sign, location="center")
        elif kind == "cubic":
            df, _ = ts.generate_deterministic_trend_cubic(df, sign=sign, amplitude=10.0, location="center")
        elif kind == "exponential":
            df, _ = ts.generate_deterministic_trend_exponential(df, sign=sign)
    if "break" in spec:
        kind = spec["break"]
        sign = random.choice([-1, 1])
        if kind == "mean_shift":
            df, _ = ts.generate_mean_shift(df, signs=[sign], location="middle", num_breaks=1, scale_factor=1.5)
        elif kind == "variance_shift":
            df, _ = ts.generate_variance_shift(df, signs=[sign], location="middle", num_breaks=1, scale_factor=1.5)
        elif kind == "trend_shift":
            df, _ = ts.generate_trend_shift(df, sign=sign, location="middle", num_breaks=1,
                                              change_types=["direction_change"], scale_factor=1.0)
    if "anomaly" in spec:
        kind = spec["anomaly"]
        if kind == "point":
            df, _ = ts.generate_point_anomaly(df, location="middle", scale_factor=2.0, is_spike=True)
        elif kind == "collective":
            df, _ = ts.generate_collective_anomalies(df, num_anomalies=1, location="middle", scale_factor=2.0)
    return df["data"].values


def main():
    random.seed(SEED_BASE)
    np.random.seed(SEED_BASE)
    manifest = []
    fail = 0
    for gid, gname, subpath, spec in GROUPS:
        out_dir = OUT_BASE / subpath
        out_dir.mkdir(parents=True, exist_ok=True)
        ok = 0
        for i in range(N_PER_GROUP):
            length = random.randint(LEN_RANGE[0], LEN_RANGE[1])
            seed = SEED_BASE + gid * 10000 + i
            try:
                series = gen_one_series(length, spec, seed)
                if len(series) < 50:
                    fail += 1
                    continue
                fname = f"{gname.replace('+', '_')}_{i:03d}.csv"
                pd.DataFrame({"value": series}).to_csv(out_dir / fname, index=False)
                manifest.append({"gid": gid, "name": gname, "subpath": subpath,
                                 "file": fname, "length": int(len(series)), "spec": spec})
                ok += 1
            except Exception as e:
                fail += 1
        print(f"Grup {gid:2d} ({gname:<28}) {ok}/{N_PER_GROUP}")
    with open(OUT_BASE / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, default=str)
    print(f"\nToplam: {len(manifest)} seri, {fail} hata")


if __name__ == "__main__":
    main()
