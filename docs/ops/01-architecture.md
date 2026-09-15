# 01 — معمارية المنصة (تشريح كامل)

> هذه هي الحقائق المستخرجة من قراءة الكود نفسه في هذا المستودع، مش من التوثيق العام.

## 1. شنو هي المنصة أصلاً

المنصة هي **Mikhmon V3** (إصدار `3.20` حسب `verson.txt` بتاريخ 06-30-2021) — لوحة إدارة
هوت سبوت مايكروتيك، مكتوبة PHP خام.

| الخاصية | القيمة |
|---|---|
| اللغة | PHP (بدون framework، بدون composer) |
| قاعدة البيانات | **لا توجد** — الحالة في ملفات PHP + داخل الراوتر نفسه |
| الاتصال بالراوتر | RouterOS API عبر socket خام (`lib/routeros_api.class.php`) |
| المنفذ الافتراضي للـ API | `8728` (يمكن تحديد منفذ آخر بصيغة `IP:PORT`) |
| الرخصة | GPL v2 |
| الأصل | fork من `laksa19/mikhmonv3` |

**الأهم:** المنصة دي مجرد *واجهة*. **مصدر الحقيقة الحقيقي هو الراوتر (MikroTik)**:
المستخدمون، البروفايلات، الجلسات النشطة، وحتى **تقارير المبيعات** كلها مخزّنة في
الراوتر. لو ضاع السيرفر، البيانات موجودة. لو ضاع الراوتر، **ضاع كل شيء**.

## 2. خريطة المستودع

```
index.php            الواجهة الرئيسية بعد الدخول (router للصفحات عبر ?session=&hotspot=...)
admin.php            الدخول، إدارة جلسات الراوترات، الإعدادات، logout
include/
  config.php         ★ ملف الحالة الأهم: بيانات دخول الأدمن + كل الراوترات
  readcfg.php        يفك ترميز config.php إلى متغيرات ($iphost, $userhost, ...)
  menu.php           القائمة الجانبية
  headhtml.php       رأس HTML + الثيم
  lang.php/theme.php ★ يُكتبان وقت التشغيل (اللغة والثيم المختارين)
  login.php          نموذج الدخول
  about.php          صفحة حول
lib/
  routeros_api.class.php   ★ كلاس الاتصال بالراوتر + دوال encrypt/decrypt
  formatbytesbites.php     تنسيق الوحدات
dashboard/           لوحة المعلومات (home.php + aload.php للتحديث اللحظي)
hotspot/             المستخدمون، البروفايلات، الجلسات النشطة، الكوكيز، IP binding، توليد كروت
voucher/             ★ قوالب الكروت (template*.php) + الطباعة والمعاينة
report/              تقارير المبيعات، سجل المستخدمين، التقرير اللحظي، الملخص
process/             عمليات التنفيذ (حذف/تفعيل/تعطيل/إعادة تشغيل/إطفاء)
settings/            إعدادات الجلسة، الثيم، اللغة، رفع الشعار، محرر الكروت
status/              ★ صفحة حالة الكرت (عامة، بدون تسجيل دخول) + اختبار ping
traffic/             مراقبة الترافيك (Highcharts)
system/              جدولة المهام (scheduler)
dhcp/                عرض DHCP leases
lang/                en, es, id, tl, tr  (★ لا يوجد ملف عربي — بند تطوير)
css/ js/ img/        الواجهة + الشعارات المرفوعة
docker-compose.yml   مختبر تجريبي (nginx + php7.4-fpm + راوتر وهمي)
nginx.conf           إعداد nginx للمختبر التجريبي
```

## 3. أين تُخزَّن الحالة (State) — حرج جدًا

هذه هي الملفات الوحيدة التي **تتغير أثناء التشغيل**. أي نسخة احتياطية لازم تشملها:

| المسار | المحتوى | من يكتبه |
|---|---|---|
| `include/config.php` | **بيانات دخول الأدمن + IP/user/pass كل راوتر** | `settings/settings.php`, `admin.php` (حذف جلسة) |
| `include/lang.php` | اللغة المختارة | `settings/setlang.php` |
| `include/theme.php` | الثيم المختار | `settings/settheme.php` |
| `voucher/template*.php` | قوالب الكروت المعدّلة | `settings/vouchereditor.php` |
| `voucher/temp.php` | قائمة مؤقتة لآخر كروت مولّدة | `hotspot/generateuser.php` |
| `img/*.png` | الشعارات المرفوعة | `settings/uplogo.php` |

| داخل الراوتر (MikroTik) | المحتوى |
|---|---|
| `/ip/hotspot/user` | المستخدمون/الكروت + تاريخ الانتهاء في حقل `comment` |
| `/ip/hotspot/user/profile` | البروفايلات + سكربتات `on-login` التي تُسجّل المبيعات |
| `/system/script` | ★ **تقارير المبيعات كلها** (كل عملية بيع = script entry) |
| `/system/scheduler` | مهمة مراقبة انتهاء المستخدمين (Monitor Profile) |

> ⚠️ حذف السكربتات من الراوتر (`/system/script`) = **حذف كل تقارير المبيعات**.
> هذا بالضبط ما يفعله `process/removereport.php`. لا يُستخدم إلا بطلب صريح.

## 4. صيغة `include/config.php`

```php
$data['mikhmon'] = array ('1'=>'mikhmon<|<mikhmon','mikhmon>|>aWNlbA==');
//                                      ↑ اسم المستخدم        ↑ كلمة المرور مشفّرة
$data['SESSION_NAME'] = array (
  '1'=>'SESSION!192.168.1.1',       // IP الراوتر (ويمكن IP:PORT)
  'SESSION@|@admin',                // مستخدم الراوتر
  'SESSION#|#<encrypted>',          // كلمة مرور الراوتر (encrypt())
  'SESSION%اسم الهوت سبوت',
  'SESSION^dns-name',
  'SESSION&SDG',                    // العملة
  'SESSION*10',                     // auto reload (ثوانٍ، الحد الأدنى 10)
  'SESSION(ether1',                 // الواجهة المراقَبة
  'SESSION)<hex>',                  // نص معلومات الكرت (unpack H*)
  'SESSION=10+SESSION',             // idle timeout + اسم الجلسة
  'SESSION@!@disable'               // التقرير اللحظي enable/disable
);
```

**التشفير ليس تشفيرًا حقيقيًا:** `encrypt()/decrypt()` في
`lib/routeros_api.class.php:440` هي إزاحة أحرف بمفتاح ثابت `128` ثم Base64.
أي شخص يقرأ `config.php` يقدر يستخرج كلمة مرور الراوتر خلال ثانية.
(القيمة الافتراضية `aWNlbA==` = `1234`).

## 5. كيف تعمل دورة الحياة

1. المستخدم يفتح `admin.php?id=login` ← يقارن مع `$data['mikhmon']`.
2. بعد الدخول: `admin.php?id=sessions` ← قائمة الراوترات من `config.php`.
3. اختيار راوتر ← `admin.php?id=connect&session=X` ← يفتح socket على `8728`.
4. ينتقل إلى `index.php?session=X` ← كل الصفحات تمر من هنا عبر متغيرات `$_GET`.
5. كل صفحة تفتح اتصالًا جديدًا بالراوتر عبر `new RouterosAPI()` ثم تنفّذ `comm()`.

**نتيجة مهمة للأداء:** كل تحميل صفحة = اتصال TCP جديد بالراوتر. لو الراوتر بطيء أو
بعيد (VPN)، المنصة كلها بتبقى بطيئة. وقت التنفيذ للاتصال محدود بـ 5 ثوانٍ
(`ini_set("max_execution_time",5)` في `admin.php`).

## 6. سلوكيات لازم الإيجنت يعرفها قبل ما يشخّص

| السلوك | التفصيل |
|---|---|
| `error_reporting(0)` في كل ملف | **كل الأخطاء مخفية**. الصفحة البيضاء = خطأ PHP صامت. للتشخيص: فعّل الأخطاء مؤقتًا أو اقرأ `php-fpm`/`nginx` error log |
| `status/status.php` عامة | لا تتحقق من الجلسة (بالتصميم — عشان الزبون يفحص كرته). لكنها تتصل بالراوتر ببيانات الأدمن |
| `include/config.php` يُكتب من الويب | التطبيق يعدّل ملف PHP قابل للتنفيذ وقت التشغيل. صلاحيات الكتابة إلزامية، وخطرة |
| `.profile` فيه `chmod -R 777 Storage` | مجلد `Storage` غير موجود أصلاً في المستودع — سطر ميت من نشر سابق |
| التوافق مع PHP | مكتوب لـ PHP 7.x. الملفات تمر من `php -l` على 8.4 بلا أخطاء صياغة، لكن سلوك `$_GET` غير المعرّف و `explode()` على null يولّد تنبيهات مكتومة |

## 7. ملفات ناقصة في هذا الـ fork (مؤكدة)

هذه الملفات **مُستدعاة في الكود لكنها غير موجودة** — أي ميزة تعتمد عليها تظهر فارغة بصمت:

```
ppp/pppsecrets.php  ppp/addsecret.php  ppp/secretbyname.php
ppp/pppprofile.php  ppp/addpppprofile.php  ppp/profilebyname.php  ppp/pppactive.php
process/psecret.php  process/removepprofile.php  process/makebinding.php
hotspot/binding.php  report/export.php  include/info.php
```

**الأثر:** كل قسم **PPP** في القائمة معطّل، وتصدير التقارير معطّل، وربط MAC
(`makebinding`) معطّل. إذا احتاج العميل هذه الميزات → تُجلب من المشروع الأصلي
(`laksa19/mikhmonv3` v3.20) مع مراجعة أمنية، لا تُكتب من الصفر.

## 8. المختبر التجريبي (للاختبار قبل الإنتاج)

```bash
docker compose up -d
# اللوحة:      http://localhost:8080   (mikhmon / 1234)
# راوتر وهمي:  http://localhost:8081   (IP داخلي 172.27.0.7، admin / 12345)
```
استخدمه **دائمًا** لتجربة أي تعديل قبل لمس الإنتاج.
