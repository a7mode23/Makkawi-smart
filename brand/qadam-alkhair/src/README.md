# إعادة توليد الشعار · Regenerating

```bash
pip install fonttools uharfbuzz
mkdir -p fonts && curl -L -o "fonts/ElMessiri[wght].ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/elmessiri/ElMessiri%5Bwght%5D.ttf"
OUT=kit python3 kit.py      # SVG
python3 export_kit.py kit   # PNG + ICO (يحتاج Chromium)
```

| الملف | الدور |
| --- | --- |
| `foot.py` | رسم القدم والأصابع، و`steps_left()` = أيقونة خطوات الخير |
| `kit.py` | الألوان وكل التكوينات (أفقي، عمودي، أيقونات) |
| `glyphs.py` | تشكيل الاسم العربي بـ HarfBuzz وتحويله لمسارات |
| `export_kit.py` | تصدير PNG وICO |
