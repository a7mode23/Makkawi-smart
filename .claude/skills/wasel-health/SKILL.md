---
name: wasel-health
description: فحص صحة شامل لمنصة واصل والسيرفر — اللوحة، الراوترات، SSL، الموارد، النسخ الاحتياطية، والأمان. Run a full health check of the Wasel platform and its server, then report status in Arabic. استخدمه عند "افحص المنصة"، "كل شيء تمام؟"، "شنو وضع السيرفر".
---

# فحص صحة منصة واصل

## نفّذ

```bash
bash ops/health-check.sh; echo "EXIT=$?"
```

رموز الخروج: `0` سليم · `1` فيه تحذيرات · `2` فيه فشل حرج.

## إذا ظهر `SKIP` بسبب إعدادات ناقصة

الفحوص المتخطّاة تعني أن `ops/inventory.local.env` غير مضبوط. أنشئه:

```bash
cp ops/inventory.example.env ops/inventory.local.env
```
ثم اسأل المالك عن القيم الناقصة (رابط اللوحة، الدومين، أسماء الخدمات، مجلد النسخ)
وحدّث كمان `docs/ops/02-inventory.md`. **لا تخمّن أي قيمة.**

## زيادة على السكربت، افحص يدويًا

```bash
tail -50 /var/log/nginx/error.log 2>/dev/null
tail -50 /var/log/php*-fpm.log 2>/dev/null
df -h; free -h 2>/dev/null
```

ولو عندك وصول للراوتر:
```
/system resource print          # CPU وذاكرة الراوتر
/ip hotspot active print count-only
/system license print
```

## التقرير النهائي (بالعربي)

1. **الخلاصة في سطر:** المنصة سليمة / فيها تحذيرات / فيها عطل.
2. جدول بالفحوص الفاشلة والتحذيرات فقط (السليم يُلخَّص بعدد).
3. لكل فشل: السبب المرجّح + الإصلاح المقترح + هل يحتاج إذن (راجع `.claude/agents/wasel-ops.md`).
4. أي شيء ينتهي خلال 30 يوم من `docs/ops/05-renewals.md`.
5. الخطوة التالية المقترحة.

أي فشل → انتقل مباشرة إلى `docs/ops/03-incidents.md` للحالة المطابقة.
