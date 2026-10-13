# إعادة توليد الشعار · Regenerating the logo

كل ملفات الشعار مولّدة من هذه السكربتات، فأي تعديل (لون، سماكة، تباعد) يتم هنا
ثم يُعاد التوليد — بدون برامج تصميم.

```bash
pip install fonttools uharfbuzz

# خط تجول (OFL) — يُستخدم وقت التوليد فقط، ثم يتحوّل النص إلى مسارات
mkdir -p fonts && cd fonts
curl -LO https://raw.githubusercontent.com/google/fonts/main/ofl/tajawal/Tajawal-Bold.ttf
curl -LO https://raw.githubusercontent.com/google/fonts/main/ofl/tajawal/Tajawal-ExtraBold.ttf
cd ..

OUT=../ python3 make_files.py     # يكتب logo/*.svg
python3 export_png.py             # يكتب png/*.png  (يحتاج Chromium)
```

| الملف | الدور |
| --- | --- |
| `build.py` | هندسة العلامة (الحلقة، الورقة، النقطتان) + الألوان + المقترحات البديلة |
| `textpath.py` | تشكيل النص العربي (HarfBuzz) وتحويله إلى مسارات SVG |
| `make_files.py` | تركيب النسخ (أفقي، عمودي، أيقونة، فافيكون…) |
| `export_png.py` | تصدير PNG بخلفية شفافة عبر Chromium |

الألوان كلها في `build.py` داخل القاموس `C`.
