# قدم الخير — Qadam Alkhair · Logo & Brand Kit

## الفكرة الأساسية · The core idea

**نقطة «الخير» قلب.**
في كلمة **الخير** نقطة واحدة (نقطة الخاء)، وفي **Alkhair** نقطة واحدة (نقطة الـ i).
النقطتان صارتا **قلباً ذهبياً** في اللغتين وعلى نفس الكلمة. الاسم نفسه هو الشعار.

The single dot of «الخير» (on خ) and of «Alkhair» (on i) is a gold heart, in both scripts.

---

## الخيارات · The options

كل خيار يطوّر الفكرة نفسها بإشارة خير إضافية واحدة، وله طقم ملفات كامل في `options/`.

| المجلد | الخيار | المعنى |
| --- | --- | --- |
| `options/a-light/` | **أ — القلب يشعّ** | ثلاثة خطوط نور تخرج من القلب: «نور الخير» ينتشر |
| `options/b-wheat/` | **ب — سنبلة وقلب** | لام «الخير» تطلع سنبلة قمح: رزق وبركة، والقلب: عطاء |
| `options/c-cradle/` | **ج — حضن تحت الاسم** | ضربة ذهبية تحمل الاسم من تحت: يد تحمل الخير |
| `options/d-kashida/` | **د — مدّ وإشعاع** | «الخيـر» ممدودة كأنها فاتحة يديها (كرم)، والقلب يشعّ فوقها |
| `options/0-base/` | **الأساس** | القلب وحده مكان النقطة، بلا إضافة |

### داخل كل مجلد

| الملف | الاستخدام |
| --- | --- |
| `logo/qadam-logo.svg` | **الشعار الأساسي**: العربي فوق والإنجليزي تحت |
| `logo/qadam-logo-horizontal.svg` | سطر واحد: الإنجليزي ┃ العربي، للهيدر والمساحات العريضة |
| `logo/qadam-logo-dark.svg` · `-horizontal-dark.svg` | على الخلفيات الداكنة |
| `logo/qadam-logo-on-green.svg` | على الأخضر: لافتات، تيشيرتات، أغلفة |
| `logo/qadam-logo-mono-ink.svg` · `-mono-white.svg` | لون واحد: أختام، حفر، طباعة بلون واحد |
| `logo/qadam-wordmark-ar.svg` · `qadam-wordmark-en.svg` | الاسم بلغة واحدة |
| `logo/qadam-icon.svg` · `qadam-app-icon.svg` | صورة البروفايل وأيقونة التطبيق |
| `logo/qadam-favicon.svg` | أيقونة المتصفح للأحجام الصغيرة جداً |
| `png/` | نفس النسخ PNG بخلفية شفافة + `qadam-favicon.ico` + أيقونة الآيفون `qadam-app-icon-180.png` |

> للطباعة الاحترافية واللوحات الكبيرة استخدم **SVG** دائماً.

---

## الألوان · Colour

| اللون | HEX | الاستخدام |
| --- | --- | --- |
| Khair Green | `#0A5440` | لون الاسم |
| Leaf Green | `#0F7B5A` | الخلفيات الخضراء والأيقونات |
| Khair Gold | `#E3A42B` | **إشارات الخير فقط**: القلب، النور، السنبلة، الحضن |
| Light Gold | `#F6CB6B` | نفس الإشارات على الخلفيات الداكنة والخضراء |
| Ink | `#12241F` | النصوص والخلفية الداكنة |
| Cream | `#FBF7EF` | الخلفية الفاتحة، والاسم على الداكن |

## الخط · Typography

الشعار بخط **El Messiri** (عربي ولاتيني)، ومحوَّل إلى مسارات فلا يحتاج تثبيت أي خط.
للمطبوعات والموقع: **El Messiri** للعناوين، و**IBM Plex Sans Arabic** أو **Tajawal** للنصوص.
بدائل نفس الفكرة بخطوط أخرى (مدوّر، رقعة، عصري) في `_explorations/typefaces/`.

## قواعد الاستخدام · Usage

- **المساحة الحرة:** فراغ حول الشعار لا يقل عن ارتفاع السطر الإنجليزي.
- **أصغر مقاس:** الشعار الأساسي 100px عرضاً (25 مم طباعة)، والأفقي 160px (40 مم).
  أصغر من ذلك استخدم الأيقونة، وتحت 32px الفافيكون.
- **ممنوع:** إرجاع النقطة العادية مكان القلب، تغيير لون الذهبي، إعادة كتابة الاسم بخط آخر، المدّ أو الإمالة أو الظلال، أو وضع النسخة الخضراء على خلفية داكنة.

## الويب · Web

بعد اختيار الخيار (مثلاً `b-wheat`):

```html
<img src="brand/qadam-alkhair/options/b-wheat/logo/qadam-logo-horizontal.svg" alt="قدم الخير" height="44">
<link rel="icon" href="brand/qadam-alkhair/options/b-wheat/logo/qadam-favicon.svg" type="image/svg+xml">
<link rel="icon" href="brand/qadam-alkhair/options/b-wheat/png/qadam-favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="brand/qadam-alkhair/options/b-wheat/png/qadam-app-icon-180.png">
```

افتح `preview.html` لمقارنة كل الخيارات في صفحة واحدة.
