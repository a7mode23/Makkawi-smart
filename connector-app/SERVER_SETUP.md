# إعداد سيرفر منصة مكاوي سمارت للإنتاج

التطبيق (`main.py`) جاهز من جهته للـ HTTPS والمصادقة، لكن في خطوتين لازم
تتنفذا **على السيرفر** (`167.233.202.51`) قبل النشر:

1. تفعيل HTTPS — حالياً بيانات الحساب وسكربت WireGuard بتمشي مكشوفة
   على الإنترنت بـ HTTP عادي.
2. تفعيل التحقق من كلمة المرور في الـ API — حالياً أي شخص عارف اسم
   المستخدم يقدر يسجّل راوتر على الحساب.

---

## 1) تفعيل HTTPS

شهادات SSL المجانية (Let's Encrypt) بتحتاج **اسم دومين** — ما بتشتغل على
IP مجرد. لو ما عندك دومين، سجّل واحد مجاني من DuckDNS
(مثلاً `makkawi.duckdns.org` موجّه للـ IP بتاعك).

أسهل طريقة: Caddy كبروكسي عكسي قدام FastAPI — بيجيب الشهادة ويجددها
تلقائياً:

```bash
# على السيرفر (Ubuntu/Debian)
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy
```

`/etc/caddy/Caddyfile`:

```caddyfile
makkawi.duckdns.org {
    reverse_proxy 127.0.0.1:8000
}
```

```bash
sudo systemctl reload caddy
```

ملاحظات:

- افتح المنفذين 80 و 443 في الجدار الناري، وبعد التأكد اقفل 8000
  عن العالم الخارجي (خليهو على 127.0.0.1 بس):
  `uvicorn app:app --host 127.0.0.1 --port 8000`
- بعدها عدّل سطر واحد في `main.py`:

```python
CLOUD_API_URL = "https://makkawi.duckdns.org/routers/"
```

التطبيق بيتحقق من الشهادة تلقائياً (certifi موجودة في متطلبات الأندرويد).

---

## 2) تفعيل المصادقة في FastAPI

التطبيق بيرسل بيانات الحساب بطريقتين في نفس الطلب، اختار الأنسب لكودك:

- في جسم الطلب JSON: حقلي `account` و `password`
- وكـ HTTP Basic Auth (نفس القيمتين)

ولازم الـ API يرد بـ **401** أو **403** لو البيانات غلط — التطبيق بيعرض
للمستخدم رسالة "بيانات الحساب غير صحيحة" في الحالة دي.

مثال للتطبيق في FastAPI (بافتراض جدول مستخدمين بكلمات مرور مشفرة bcrypt):

```python
from fastapi import FastAPI, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel

app = FastAPI()

class RouterIn(BaseModel):
    name: str
    ip_address: str
    serial_number: str
    account: str
    password: str

@app.post("/routers/")
def register_router(body: RouterIn):
    user = get_user_by_name(body.account)          # من قاعدة البيانات
    if not user or not bcrypt.verify(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    router = create_router(owner=user, name=body.name,
                           ip=body.ip_address, serial=body.serial_number)
    return {"wireguard_script": generate_wireguard_script(router)}
```

تنبيهات:

- **لا تخزّن كلمات المرور نصاً صريحاً** — استخدم bcrypt
  (`pip install "passlib[bcrypt]"`).
- خزّن الرقم التسلسلي بقيد فريد (unique) حتى ما يتسجّل نفس الراوتر مرتين.
- استحسن تضيف حداً لعدد المحاولات (rate limiting) على المسار دة، مثلاً
  بمكتبة slowapi.

---

## 3) بعد الاتنين ديل

- ارفع إصدار التطبيق في `buildozer.spec` وابنِ APK جديد:
  `buildozer android release`
- ملف `android_manifest_application_args.xml` بيخلي HTTP الداخلي شغال
  (الراوتر 192.168.88.1 ما عندو HTTPS) حتى بعد ما الخادم السحابي يبقى
  HTTPS — ما تشيلو.
