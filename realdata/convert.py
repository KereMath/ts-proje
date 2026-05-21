"""
realdata → standart CSV dönüştürücü.
Sadece etiketli + n>=50 olan 16 dosyayı işler.

Çıktı: testingrealdata/data/<dosya_adi>.csv  (tek 'data' sütunu)
"""
import csv
import re
from pathlib import Path

SRC = Path(__file__).parent / "TS datasets" / "TS datasets"
OUT = Path(__file__).parent.parent / "STATIONARY" / "testingrealdata" / "data"
OUT.mkdir(parents=True, exist_ok=True)

# Sadece bu 16 etiketli + n>=50 dosyayı işle
TARGET_FILES = [
    "airpass.txt",
    "deaths.txt",
    "German_consumption.dat.txt",
    "German_income.dat.txt",
    "GermanGNP.dat.txt",
    "INDPRO.csv",
    "Polish_productivity.dat.txt",
    "RealInt_dataframe.txt",
    "soi_dataframe.txt",
    "sunspots.txt",
    "UNRATE.csv",
    "US_investment.dat.txt",
    "W2.txt",
    "W3.txt",
    "W5.txt",
    "W6.txt",
]


def parse_jmulti(text):
    """JMulTi formatı: /* ... */ yorum + sayı bloğu."""
    # Yorumları kaldır
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)  # <1960 Q1> gibi tarih başlıklarını sil
    # Header satırını atla (örn. "invest income cons")
    nums = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        # Tüm parçalar sayısal mı?
        try:
            row_nums = [float(p) for p in parts]
        except ValueError:
            continue
        # Multivariate ise sadece ilk sütunu al (genelde ana değişken)
        # GermanGNP/US_investment/German_consumption/Polish_productivity tek-değişkenli
        # e1.dat (etiketsiz, atlandı) multivariate
        nums.extend(row_nums)
    return nums


def parse_brockwell(text):
    """Brockwell: # yorum + tek sütun."""
    nums = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Bazıları "Year Month Value" gibi 3-kolon (beer)
        # Bazıları tek sayı (airpass, sunspots)
        parts = line.split()
        try:
            vals = [float(p) for p in parts]
        except ValueError:
            continue
        # Tek sütun → o değer; 2+ sütun → SON sütun (değer genelde sondadır)
        # airpass tek sütun (sadece 112, 118 vb.)
        # deaths.txt'i kontrol etmedim, ama Brockwell konvansiyonu: tek değer/satır
        nums.append(vals[-1] if len(vals) > 1 else vals[0])
    return nums


def parse_csv_header(text):
    """observation_date,Value tarzı CSV."""
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return []
    header = rows[0]
    # İlk sayısal sütunu bul
    nums = []
    for row in rows[1:]:
        for cell in row:
            cell = cell.strip()
            try:
                nums.append(float(cell))
                break  # ilk sayısal hücreyi al, sonrakilerini geç
            except ValueError:
                continue
    return nums


def parse_dataframe_header(text):
    """Tek başlık + tek sütun değer."""
    lines = text.splitlines()
    nums = []
    for i, line in enumerate(lines):
        if i == 0:
            continue  # header
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        try:
            nums.append(float(parts[0]))
        except ValueError:
            continue
    return nums


def parse_whitespace(text):
    """W-serileri: bir satırda çok sayı, tek seri olarak flatten."""
    nums = []
    for line in text.splitlines():
        for tok in line.split():
            try:
                nums.append(float(tok))
            except ValueError:
                pass
    return nums


def detect_and_parse(fname, text):
    if fname.endswith(".csv"):
        return parse_csv_header(text), "csv_header"
    if "/*" in text or "*/" in text:
        return parse_jmulti(text), "jmulti"
    first = next((l.strip() for l in text.splitlines() if l.strip()), "")
    if first.startswith("#"):
        return parse_brockwell(text), "brockwell"
    # dataframe header
    if first and not first[0].isdigit() and first[0] not in "-.":
        return parse_dataframe_header(text), "dataframe_header"
    return parse_whitespace(text), "whitespace_flatten"


def write_csv(out_path, values):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["data"])
        for v in values:
            w.writerow([v])


def main():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(f"Çıktı klasörü: {OUT}\n")
    summary = []
    for fname in TARGET_FILES:
        src = SRC / fname
        if not src.exists():
            print(f"  ✗ {fname}: dosya yok")
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        values, fmt = detect_and_parse(fname, text)
        # Çıktı adı: uzantıyı .csv yap, .dat varsa temizle
        out_name = fname.replace(".dat.txt", "").replace(".txt", "").replace(".csv", "") + ".csv"
        out = OUT / out_name
        write_csv(out, values)
        summary.append({"src": fname, "out": out_name, "format": fmt, "n": len(values)})
        print(f"  ✓ {fname:<32} → {out_name:<32}  ({fmt:<20} n={len(values)})")

    print(f"\nToplam {len(summary)} dosya dönüştürüldü.")

    # Özet CSV yaz
    sum_path = Path(__file__).parent / "conversion_summary.csv"
    with open(sum_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["src", "out", "format", "n"])
        w.writeheader()
        w.writerows(summary)
    print(f"Özet: {sum_path}")


if __name__ == "__main__":
    main()
