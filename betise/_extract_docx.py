import zipfile, re, sys
from pathlib import Path

p = Path(r'c:\Users\Pc\Desktop\betise\TUBİTAK_1001_2_Gelisme_Raporu_DETAYLI (2).docx')
with zipfile.ZipFile(p) as z:
    with z.open('word/document.xml') as f:
        xml = f.read().decode('utf-8', errors='ignore')

paras = re.split(r'</w:p>', xml)
out = []
for para in paras:
    texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', para)
    line = ''.join(texts).strip()
    if line:
        out.append(line)

Path(r'c:\Users\Pc\Desktop\betise\tubitak_text.txt').write_text('\n'.join(out), encoding='utf-8')
print(f'Wrote {len(out)} non-empty lines')
