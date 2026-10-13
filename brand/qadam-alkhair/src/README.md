# إعادة توليد الشعار · Regenerating the logo

كل الملفات مولّدة من هذه السكربتات: أي تعديل (لون، حجم القلب، المسافات، الخط) يتم في
`wordmark.py` ثم يُعاد التوليد.

```bash
pip install fonttools uharfbuzz
mkdir -p fonts && cd fonts
curl -LO "https://raw.githubusercontent.com/google/fonts/main/ofl/elmessiri/ElMessiri%5Bwght%5D.ttf"
curl -LO "https://raw.githubusercontent.com/google/fonts/main/ofl/baloobhaijaan2/BalooBhaijaan2%5Bwght%5D.ttf"
curl -LO "https://raw.githubusercontent.com/google/fonts/main/ofl/arefruqaa/ArefRuqaa-Bold.ttf"
curl -LO "https://raw.githubusercontent.com/google/fonts/main/ofl/readexpro/ReadexPro%5BHEXP%2Cwght%5D.ttf"
for f in *%5B*; do mv "$f" "$(python3 -c 'import sys,urllib.parse;print(urllib.parse.unquote(sys.argv[1]))' "$f")"; done
cd ..

OUT=out2 python3 wordmark.py   # SVG
python3 export2.py             # PNG + ICO (يحتاج Chromium)
```

| الملف | الدور |
| --- | --- |
| `glyphs.py` | تشكيل النص (HarfBuzz) واستخراج كل نقطة كشكل مستقل لتبديلها |
| `wordmark.py` | الفكرة نفسها: نقطة «الخير» قلب — وكل التكوينات والألوان |
| `export2.py` | تصدير PNG وICO |
