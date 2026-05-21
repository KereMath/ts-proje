"""
realdata/TS datasets/* dosyalarini standart tek-kolon CSV'ye donusturur.
TUM dosyalar dahil (multivariate dahil; multivariate'te ilk numeric kolonu al).
Output: runner/data/realdata/<name>.csv
"""
import csv
import re
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "realdata" / "TS datasets" / "TS datasets"
OUT = Path(__file__).resolve().parent / "data" / "realdata"
OUT.mkdir(parents=True, exist_ok=True)


def parse_jmulti(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    nums = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        try:
            row_nums = [float(p) for p in parts]
        except ValueError:
            continue
        if row_nums:
            nums.append(row_nums[0])  # ilk kolon
    return nums


def parse_brockwell(text):
    nums = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        try:
            vals = [float(p) for p in parts]
        except ValueError:
            continue
        if vals:
            nums.append(vals[-1] if len(vals) > 1 else vals[0])
    return nums


def parse_csv_header(text):
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return []
    nums = []
    for row in rows[1:]:
        for cell in row:
            cell = cell.strip()
            try:
                nums.append(float(cell))
                break
            except ValueError:
                continue
    return nums


def parse_dataframe_header(text):
    lines = text.splitlines()
    nums = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        try:
            nums.append(float(parts[0]))
        except ValueError:
            continue
    return nums


def parse_whitespace_multi(text):
    """W serileri: bir satirda cok sayi. Multivariate ise, satir uzunlugu
    ile kolon sayisini tahmin et; satir sayisi=length, kolon sayisi=variates.
    Ilk kolonu al."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        try:
            row_nums = [float(p) for p in parts]
        except ValueError:
            continue
        if row_nums:
            rows.append(row_nums)
    if not rows:
        return []
    # Tahmin: cogu satir 1 sayi varsa univariate
    lengths = [len(r) for r in rows]
    if max(lengths) == 1:
        # tek sutun, hepsini birlestir
        return [r[0] for r in rows]
    # Multivariate gibi gorunse de, eski convert.py'da "whitespace_flatten" yapiyor.
    # Tutarlilik icin: eger tum satirlar ayni uzunluktaysa kolonlari ayir, ilkini al
    # degilse flatten
    if len(set(lengths)) == 1:
        return [r[0] for r in rows]
    # flatten
    flat = []
    for r in rows:
        flat.extend(r)
    return flat


def detect_and_parse(fname, text):
    if fname.endswith(".csv"):
        return parse_csv_header(text), "csv_header"
    if "/*" in text or "*/" in text:
        return parse_jmulti(text), "jmulti"
    first = next((l.strip() for l in text.splitlines() if l.strip()), "")
    if first.startswith("#"):
        return parse_brockwell(text), "brockwell"
    if first and first[0].isalpha():
        return parse_dataframe_header(text), "dataframe_header"
    return parse_whitespace_multi(text), "whitespace_multi"


def write_csv(out_path, values):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["value"])
        for v in values:
            w.writerow([v])


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    files = sorted(SRC.glob("*.txt")) + sorted(SRC.glob("*.csv"))
    summary = []
    for src in files:
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  FAIL {src.name}: {e}")
            continue
        values, fmt = detect_and_parse(src.name, text)
        out_name = src.name.replace(".dat.txt", "").replace(".txt", "").replace(".csv", "") + ".csv"
        out_path = OUT / out_name
        write_csv(out_path, values)
        summary.append({"src": src.name, "out": out_name, "format": fmt, "n": len(values)})
        print(f"  OK {src.name:<32} -> {out_name:<32} ({fmt:<20} n={len(values)})")

    print(f"\nTotal: {len(summary)} files")
    with open(OUT.parent / "realdata_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
