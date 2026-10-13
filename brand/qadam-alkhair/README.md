# قدم الخير — Qadam Alkhair · Logo & Brand Kit

## الفكرة · The idea

**نقطة «الخير» قلب.**
في كلمة **الخير** نقطة واحدة (نقطة الخاء)، وفي **Alkhair** نقطة واحدة (نقطة الـ i).
النقطتان صارتا **قلباً ذهبياً** — في اللغتين، وفي نفس الكلمة: كلمة الخير.

The single dot in «الخير» (on خ) and the single dot in «Alkhair» (on i) are both
a gold heart. Everything else is plain, quiet type — one idea, nothing added.

- **البساطة:** الشعار هو الاسم نفسه، بلا رموز إضافية.
- **الخير:** القلب يقف مكان النقطة داخل كلمة «الخير» تحديداً.
- **ثنائي اللغة:** نفس الفكرة تعمل بالعربي والإنجليزي، فالنسختان عائلة واحدة.

---

## الملفات · Files

### `logo/` — SVG (المصدر الأساسي، يكبر بلا حدود)

| الملف | الاستخدام |
| --- | --- |
| `qadam-logo.svg` | **الشعار الأساسي** — العربي فوق والإنجليزي تحت |
| `qadam-logo-horizontal.svg` | سطر واحد: الإنجليزي ┃ العربي — للهيدر والمساحات العريضة |
| `qadam-logo-dark.svg` · `qadam-logo-horizontal-dark.svg` | على الخلفيات الداكنة |
| `qadam-logo-on-green.svg` | على الأخضر (لافتات، تيشيرتات، أغلفة) |
| `qadam-logo-mono-ink.svg` · `qadam-logo-mono-white.svg` | لون واحد: أسود / أبيض (أختام، طباعة رخيصة، حفر) |
| `qadam-wordmark-ar.svg` · `qadam-wordmark-en.svg` | الاسم بلغة واحدة فقط |
| `qadam-icon.svg` | صورة البروفايل (دائرة) — كلمة «خير» بقلبها |
| `qadam-app-icon.svg` | أيقونة تطبيق (مربع بزوايا مدوّرة) |
| `qadam-favicon.svg` | أيقونة المتصفح — القلب وحده للأحجام الصغيرة جداً |
| `qadam-alt-rounded.svg` · `qadam-alt-ruqaa.svg` · `qadam-alt-modern.svg` | نفس الفكرة بخطوط أخرى: مدوّر دافئ · رقعة بخط اليد · عصري |

### `png/` — PNG بخلفية شفافة
أحجام جاهزة للسوشيال والطباعة الخفيفة + `qadam-favicon.ico`
و`qadam-app-icon-180.png` لأيقونة الآيفون.

> للطباعة الاحترافية واللوحات الكبيرة استخدم **SVG** دائماً.

---

## الألوان · Colour

| اللون | HEX | الاستخدام |
| --- | --- | --- |
| Khair Green | `#0A5440` | لون الاسم |
| Leaf Green | `#0F7B5A` | الخلفيات الخضراء والأيقونات |
| Khair Gold | `#E3A42B` | **القلب فقط** — اللون المميّز الوحيد |
| Light Gold | `#F6CB6B` | القلب على الخلفيات الداكنة والخضراء |
| Ink | `#12241F` | النصوص والخلفية الداكنة |
| Cream | `#FBF7EF` | الخلفية الفاتحة، والاسم على الداكن |

---

## الخط · Typography

- الشعار مرسوم بخط **El Messiri** (عربي + لاتيني) ومحوَّل إلى مسارات، فلا يحتاج تثبيت أي خط.
- للعناوين في المطبوعات والموقع: **El Messiri** — وللنصوص الطويلة: **IBM Plex Sans Arabic** أو **Tajawal**. كلها مجانية على Google Fonts.

---

## قواعد الاستخدام · Usage

**المساحة الحرة:** اترك حول الشعار فراغاً لا يقل عن **ارتفاع السطر الإنجليزي** من كل جهة.

**أصغر مقاس:**
- الشعار الأساسي: **100px** عرضاً على الشاشة / **25 مم** في الطباعة.
- الشعار الأفقي: **160px** / **40 مم**.
- أصغر من ذلك ← استخدم `qadam-icon.svg` (كلمة «خير»)، وتحت 32px ← `qadam-favicon.svg` (القلب).

**ممنوع:**
1. لا تُرجع النقطة العادية مكان القلب، ولا تضع القلب على حرف آخر.
2. لا تغيّر لون القلب — الذهبي هو توقيع العلامة (إلا في نسخ اللون الواحد).
3. لا تعِد كتابة الاسم بخط آخر، ولا تمدّه أو تميّله أو تضف له ظلاً.
4. لا تضع النسخة الخضراء على خلفية داكنة أو مزدحمة — استخدم `-dark` أو `-on-green` أو `-mono-white`.

---

## الويب · Web

```html
<img src="brand/qadam-alkhair/logo/qadam-logo-horizontal.svg" alt="قدم الخير" height="44">

<link rel="icon" href="brand/qadam-alkhair/logo/qadam-favicon.svg" type="image/svg+xml">
<link rel="icon" href="brand/qadam-alkhair/png/qadam-favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="brand/qadam-alkhair/png/qadam-app-icon-180.png">
```

افتح `preview.html` لمعاينة كل النسخ في صفحة واحدة.
