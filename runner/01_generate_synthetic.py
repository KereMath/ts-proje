"""
Betise ile stochastic-trendli sentetik veri uretir.
5 stochastic-trend tipi (rw, rwd, ari, ima, arima) x 2 uzunluk (short=45, long=100) x 5 seri.
Output: runner/data/synthetic/<kind>_<len>_<i>.csv
"""
import sys
import os
import random
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from betise.core.generator import TimeSeriesGenerator

OUT_DIR = Path(__file__).resolve().parent / "data" / "synthetic"
OUT_DIR.mkdir(parents=True, exist_ok=True)

KINDS = ["rw", "rwd", "ari", "ima", "arima"]
LENGTHS = [45, 100]
N_PER_CONFIG = 5

random.seed(42)
np.random.seed(42)

manifest = []

for kind in KINDS:
    for length in LENGTHS:
        for i in range(N_PER_CONFIG):
            np.random.seed(42 + hash((kind, length, i)) % 10000)
            random.seed(42 + hash((kind, length, i)) % 10000)
            ts = TimeSeriesGenerator(length=length)
            try:
                df, info = ts.generate_stochastic_trend(kind=kind)
                series = df["data"].values
                if len(series) != length:
                    print(f"  WARN {kind} len={length} i={i}: got {len(series)}")
                fname = f"{kind}_L{length}_{i:02d}.csv"
                fpath = OUT_DIR / fname
                # Save as single column CSV
                with open(fpath, "w") as f:
                    f.write("value\n")
                    for v in series:
                        f.write(f"{v}\n")
                manifest.append({
                    "file": fname,
                    "kind": kind,
                    "length": length,
                    "expected_class": "stochastic_trend",
                })
                print(f"  OK {fname} ({len(series)} vals)")
            except Exception as e:
                print(f"  FAIL {kind} len={length} i={i}: {e}")

# Write manifest
import json
mpath = OUT_DIR / "manifest.json"
with open(mpath, "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\nWrote {len(manifest)} files. Manifest: {mpath}")
