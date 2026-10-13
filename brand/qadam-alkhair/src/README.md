# إعادة توليد الشعار · Regenerating

```bash
pip install fonttools uharfbuzz
mkdir -p fonts && cd fonts
curl -L -o "ElMessiri[wght].ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/elmessiri/ElMessiri%5Bwght%5D.ttf"
cd ..
OUT=out3 python3 options.py     # SVG للخيارات الأربعة
python3 export3.py out3         # PNG + ICO (يحتاج Chromium)
```

| الملف | الدور |
| --- | --- |
| `glyphs.py` | تشكيل النص (HarfBuzz) واستخراج النقطة كشكل مستقل لتبديلها بالقلب |
| `wordmark.py` | الفكرة الأساسية والألوان والتكوينات (نسخة الأساس) |
| `options.py` | الخيارات الأربعة: النور، السنبلة، الحضن، المدّ |
| `export3.py` | تصدير PNG وICO لكل خيار |
