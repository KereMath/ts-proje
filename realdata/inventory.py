"""
realdata/TS datasets envanter script — her dosyanın formatını ve parse edilebilirliğini kontrol et.

Çıktı: inventory.csv  +  konsola özet
"""
import csv
import re
from pathlib import Path

SRC = Path(__file__).parent / "TS datasets" / "TS datasets"
OUT = Path(__file__).parent / "inventory.csv"


def detect_format(text):
    """Format tipini tespit et."""
    lines = text.splitlines()
    # Boş satırları at, ilk anlamlı satırlara bak
    non_empty = [l.strip() for l in lines if l.strip()]
    if not non_empty:
        return "EMPTY"

    first = non_empty[0]
    # JMulTi: /* */ yorum bloğu
    if "/*" in text or "*/" in text:
        return "JMULTI"
    # Brockwell: # comment
    if first.startswith("#"):
        return "BROCKWELL_HASH"
    # CSV: ilk satır virgüllü header
    if "," in first and not first[0].isdigit() and first[0] != "-":
        return "CSV_HEADER"
    # Dataframe: ilk satır kelime, sonra sayılar
    if not first[0].isdigit() and first[0] not in "-.":
        return "DATAFRAME_HEADER"
    # W-serileri: whitespace-separated multi-column
    parts = first.split()
    if len(parts) > 3:
        try:
            [float(p) for p in parts]
            return "WHITESPACE_MULTI"
        except ValueError:
            pass
    # Tek sütun: her satır bir sayı
    try:
        float(parts[0])
        return "SINGLE_COL"
    except ValueError:
        return "UNKNOWN"


def extract_numbers(text, fmt):
    """Format tipine göre sayısal değerleri çıkar."""
    if fmt == "EMPTY":
        return []

    if fmt == "JMULTI":
        # /* ... */ yorumlarını sil
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        # Sayıları al
        nums = []
        for line in text.splitlines():
            for tok in line.split():
                try:
                    nums.append(float(tok))
                except ValueError:
                    pass
        return nums

    if fmt == "BROCKWELL_HASH":
        nums = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for tok in line.split():
                try:
                    nums.append(float(tok))
                except ValueError:
                    pass
        return nums

    if fmt == "CSV_HEADER":
        nums = []
        rows = list(csv.reader(text.splitlines()))
        if not rows:
            return []
        header = rows[0]
        # İlk sayısal sütunu bul (genelde 2., çünkü 1. tarih)
        for ri, row in enumerate(rows[1:], 1):
            for cell in row:
                cell = cell.strip()
                try:
                    nums.append(float(cell))
                    break  # her satırda sadece 1 sayı (ilk sayısal)
                except ValueError:
                    continue
        return nums

    if fmt == "DATAFRAME_HEADER":
        nums = []
        lines = text.splitlines()
        if len(lines) < 2:
            return []
        # 1. satır header, 2.+ satır sayı
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            for tok in line.split():
                try:
                    nums.append(float(tok))
                    break
                except ValueError:
                    pass
        return nums

    if fmt in ("WHITESPACE_MULTI", "SINGLE_COL"):
        nums = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            for tok in line.split():
                try:
                    nums.append(float(tok))
                except ValueError:
                    pass
        return nums

    return []


def check_multivariate(text, fmt):
    """Dosya birden fazla zaman serisi içeriyor olabilir mi?"""
    lines = [l for l in text.splitlines() if l.strip() and not l.strip().startswith("#") and "/*" not in l]
    if len(lines) < 3:
        return False
    # JMulTi'nin yorumsuz hali
    if fmt == "JMULTI":
        cleaned = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        sample_lines = [l for l in cleaned.splitlines() if l.strip()][:5]
    else:
        sample_lines = lines[:5] if fmt != "DATAFRAME_HEADER" and fmt != "CSV_HEADER" else lines[1:6]
    # Her satırın token sayısı tutarlı ve 2+ ise multivariate olabilir
    counts = []
    for line in sample_lines:
        parts = line.split() if "," not in line else line.split(",")
        n = 0
        for p in parts:
            try:
                float(p.strip())
                n += 1
            except ValueError:
                pass
        counts.append(n)
    if not counts:
        return False
    # En az 2 sütun ve tutarlı
    return min(counts) >= 2 and max(counts) - min(counts) <= 1


def main():
    rows = []
    for f in sorted(SRC.iterdir()):
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            rows.append({"file": f.name, "format": "ERROR", "n_values": 0,
                         "multivariate": False, "note": str(e)})
            continue
        fmt = detect_format(text)
        nums = extract_numbers(text, fmt)
        multi = check_multivariate(text, fmt) if len(nums) > 50 else False
        note = ""
        if len(nums) == 0:
            note = "veri çıkartılamadı"
        elif len(nums) < 50:
            note = f"min uzunluk altında (< 50)"
        if multi:
            note = (note + " | " if note else "") + "multivariate olabilir"
        rows.append({
            "file": f.name, "format": fmt,
            "n_values": len(nums), "multivariate": multi, "note": note,
        })

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "format", "n_values", "multivariate", "note"])
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(rows)} dosya tarandı, {OUT}")
    print("\n=== ÖZET ===")
    fmt_counts = {}
    for r in rows:
        fmt_counts[r["format"]] = fmt_counts.get(r["format"], 0) + 1
    for f, c in sorted(fmt_counts.items()):
        print(f"  {f:25} {c}")

    print("\n=== ATILACAKLAR (n < 50 veya boş) ===")
    for r in rows:
        if r["n_values"] < 50:
            print(f"  {r['file']:35} n={r['n_values']:>4}  ({r['note']})")

    print("\n=== MULTIVARIATE ŞÜPHELİSİ ===")
    for r in rows:
        if r["multivariate"]:
            print(f"  {r['file']:35} n={r['n_values']:>4}")

    print(f"\nTOPLAM: {len(rows)} | parse OK: {sum(1 for r in rows if r['n_values'] >= 50)}")


if __name__ == "__main__":
    main()
