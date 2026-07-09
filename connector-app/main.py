# -*- coding: utf-8 -*-
"""
=============================================================================
 Makkawi Smart Router Connector
 -----------------------------------------------------------------------------
 A zero-config mobile bridge between a local offline MikroTik router
 (RouterOS v7, reachable on http://192.168.88.1) and the Makkawi Smart
 Cloud Platform (FastAPI backend).

 Author  : Makkawi Smart — Atbara Market
 Stack   : Python 3.9+ / Kivy 2.x / KivyMD 1.2.0 / requests
 UI      : Arabic (RTL), iOS-inspired clean cards, palette:
           Primary #1d4ed8 | Background #f8fafc | Text #0f172a | Cards #ffffff

 INSTALL (desktop testing):
     pip install kivy kivymd==1.2.0 requests arabic-reshaper python-bidi

 ANDROID (buildozer.spec essentials):
     requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,
                    charset-normalizer,idna,certifi,arabic-reshaper,python-bidi
     android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
     # python-for-android debug builds allow cleartext HTTP by default.
     # For release builds make sure usesCleartextTraffic is enabled since the
     # router (192.168.88.1) and the cloud endpoint use plain HTTP.

 ARABIC FONT:
     Drop "Cairo-Regular.ttf" next to this file (or in ./assets/fonts/) for
     the best look. If absent, the app falls back to a system font that
     contains Arabic glyphs (Android Noto Naskh, Windows Tahoma, ...).
=============================================================================
"""

import os
import socket
import textwrap
import threading

import requests

from kivy.clock import Clock, mainthread
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.utils import get_color_from_hex, platform

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

# ---------------------------------------------------------------------------
# Optional Arabic shaping (strongly recommended). The app degrades gracefully
# if the libraries are missing, but Arabic will render disconnected.
# ---------------------------------------------------------------------------
try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    # Keep isolated letters at their base codepoints: several fonts
    # (Cairo included) ship contextual forms but not the legacy
    # "isolated" presentation-form codepoints.
    _RESHAPER = arabic_reshaper.ArabicReshaper(
        configuration={"use_unshaped_instead_of_isolated": True})
    _ARABIC_SHAPING = True
except ImportError:  # pragma: no cover
    _ARABIC_SHAPING = False


# ===========================================================================
# 1. CONFIGURATION
# ===========================================================================

ROUTER_HOST = "192.168.88.1"
ROUTER_REST_BASE = f"http://{ROUTER_HOST}/rest"
ROUTER_TIMEOUT = 8          # seconds per local REST call
ROUTER_PROBE_TIMEOUT = 2.5  # seconds for the live TCP reachability probe
ROUTER_PROBE_PORTS = (80, 443)
STATUS_POLL_INTERVAL = 6    # seconds between automatic connectivity checks

CLOUD_API_URL = "http://167.233.202.51:8000/routers/"
CLOUD_TIMEOUT = 20          # seconds

PROVISION_SCRIPT_NAME = "makkawi-cloud-provision"
PROVISION_SCRIPT_POLICY = (
    "ftp,reboot,read,write,policy,test,password,sensitive,romon"
)

# Colors (design system)
C_PRIMARY = "#1d4ed8"
C_BG = "#f8fafc"
C_TEXT = "#0f172a"
C_MUTED = "#64748b"
C_STEP = "#334155"
C_IDLE = "#94a3b8"
C_GREEN = "#16a34a"
C_RED = "#dc2626"
C_AMBER = "#d97706"

# ===========================================================================
# 2. ARABIC TEXT LAYER
# ===========================================================================

TEXTS = {
    "app_title": "Makkawi Smart Router Connector",
    "app_subtitle": "الربط الذكي بين راوتر المكروتك ومنصة مكاوي سمارت السحابية",

    "status_checking": "جارٍ فحص الاتصال بجهاز المكروتك...",
    "status_connected": "متصل بجهاز المكروتك المحلي",
    "status_disconnected": "غير متصل بشبكة واي فاي المكروتك",

    "cloud_section": "حساب المنصة السحابية",
    "cloud_user_hint": "اسم مستخدم حساب مكاوي (مثال: user@mk.com)",
    "alias_hint": "اسم الراوتر / اللقب (مثال: راوتر المنزل)",

    "router_section": "بيانات دخول الراوتر المحلي",
    "mik_user_hint": "اسم مستخدم المكروتك (الافتراضي: admin)",
    "mik_pass_hint": "كلمة مرور المكروتك (راجع ملصق الراوتر)",

    "steps_title": "خطوات التفعيل",
    "step_serial": "جلب الرقم التسلسلي للراوتر",
    "step_cloud": "تسجيل الجهاز في منصة مكاوي سمارت",
    "step_inject": "حقن إعدادات WireGuard في الراوتر",
    "serial_prefix": "الرقم التسلسلي",

    "activate_btn": "تفعيل وربط الراوتر",
    "footer": "Makkawi Smart — سوق عطبرة © 2026",

    "dlg_ok": "حسناً",
    "dlg_cancel": "إلغاء",
    "dlg_retry": "إعادة المحاولة",

    "success_title": "تم الربط بنجاح",
    "success_msg": (
        "تهانينا! تم ربط الراوتر الخاص بك بنجاح بمنصة مكاوي سمارت "
        "للتحكم السحابي المركزي. سيقوم الراوتر بإعادة التشغيل خلال لحظات."
    ),

    "err_title": "حدث خطأ",
    "auth_title": "كلمة المرور مطلوبة",
    "auth_msg": (
        "بيانات دخول المكروتك غير صحيحة. أدخل كلمة المرور المدونة على "
        "ملصق الراوتر ثم أعد المحاولة."
    ),
    "err_missing_fields": (
        "يرجى تعبئة اسم مستخدم حساب مكاوي واسم الراوتر قبل المتابعة."
    ),
    "err_not_connected": (
        "لم يتم العثور على راوتر مكروتك. يرجى الاتصال بشبكة الواي فاي "
        "الخاصة بالراوتر أولاً ثم إعادة المحاولة."
    ),
    "err_router_unreachable": (
        "تعذر الوصول إلى الراوتر على العنوان 192.168.88.1. تأكد من اتصال "
        "هاتفك بشبكة واي فاي المكروتك ثم أعد المحاولة."
    ),
    "err_cloud_unreachable": (
        "تعذر الوصول إلى خادم مكاوي سمارت السحابي. تأكد من توفر اتصال "
        "بالإنترنت وحاول مرة أخرى لاحقاً."
    ),
    "err_cloud_response": (
        "استجاب الخادم السحابي بخطأ غير متوقع. يرجى المحاولة لاحقاً أو "
        "التواصل مع الدعم الفني لمنصة مكاوي سمارت."
    ),
    "err_no_script": (
        "لم يستلم التطبيق سكربت التهيئة من الخادم السحابي. يرجى التواصل "
        "مع الدعم الفني لمنصة مكاوي سمارت."
    ),
    "err_inject": (
        "فشل تنفيذ إعدادات WireGuard على الراوتر. تحقق من أن إصدار "
        "RouterOS هو v7 وأن المستخدم يملك الصلاحيات الكاملة."
    ),
}


def _contains_arabic(text):
    return any("؀" <= ch <= "ۿ" for ch in text)


def ar(text):
    """Reshape + reorder Arabic text so Kivy renders it correctly (RTL)."""
    if _ARABIC_SHAPING and text and _contains_arabic(text):
        try:
            return get_display(_RESHAPER.reshape(text))
        except Exception:
            return text
    return text


def ar_wrap(text, width=38):
    """
    Bidi-safe wrapping for long paragraphs (dialog bodies).

    Kivy wraps text AFTER the bidi reordering, which flips the visual
    order of the lines. Pre-wrapping the logical string and running the
    reshaper/bidi pass per line keeps the lines in reading order.
    """
    if not (_ARABIC_SHAPING and text and _contains_arabic(text)):
        return text
    lines = textwrap.wrap(text, width=width)
    return "\n".join(ar(line) for line in lines)


# ===========================================================================
# 3. FONT DISCOVERY (Arabic-capable)
# ===========================================================================

FONT_CANDIDATES = [
    # Bundled with the app (preferred — Cairo, brand font)
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cairo-Regular.ttf"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts", "Cairo-Regular.ttf"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Cairo-Regular.ttf"),
    # Android system fonts
    "/system/fonts/NotoNaskhArabic-Regular.ttf",
    "/system/fonts/NotoSansArabic-Regular.ttf",
    "/system/fonts/NotoKufiArabic-Regular.ttf",
    # Windows
    "C:/Windows/Fonts/tahoma.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    # Linux desktop
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/truetype/kacst/KacstOne.ttf",
]


def find_arabic_font():
    """Return (regular, bold) paths of the first available Arabic font."""
    for path in FONT_CANDIDATES:
        if path and os.path.exists(path):
            bold = path.replace("-Regular", "-Bold")
            return path, (bold if os.path.exists(bold) else path)
    return None, None


# ===========================================================================
# 4. MIKROTIK ROUTEROS v7 REST CLIENT
# ===========================================================================

class MikrotikError(Exception):
    """Generic RouterOS REST error."""


class MikrotikAuthError(MikrotikError):
    """401 — credentials rejected."""


class MikrotikUnreachable(MikrotikError):
    """Network-level failure (timeout / refused / no route)."""


# Session for LAN traffic to the router: trust_env=False bypasses any
# system/Wi-Fi HTTP proxy, which must never sit between us and 192.168.88.1
# (a proxy or captive portal would also fake the reachability probe).
_LOCAL_HTTP = requests.Session()
_LOCAL_HTTP.trust_env = False


class MikrotikClient:
    """Thin wrapper around the RouterOS v7 REST API (http://host/rest)."""

    def __init__(self, host=ROUTER_HOST, username="admin", password="",
                 timeout=ROUTER_TIMEOUT):
        self.base = f"http://{host}/rest"
        self.auth = (username, password)
        self.timeout = timeout

    # -- low level ----------------------------------------------------------
    def _request(self, method, path, json_body=None):
        url = self.base + path
        try:
            resp = _LOCAL_HTTP.request(
                method, url, auth=self.auth, json=json_body,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as exc:
            raise MikrotikUnreachable(str(exc))

        if resp.status_code == 401:
            raise MikrotikAuthError("Unauthorized (401)")
        if resp.status_code >= 400:
            raise MikrotikError(
                f"HTTP {resp.status_code}: {resp.text[:200]}"
            )
        if not resp.text or not resp.text.strip():
            return None
        try:
            return resp.json()
        except ValueError:
            return None

    # -- Step A: unique hardware serial --------------------------------------
    def get_serial(self):
        """Return the routerboard serial-number (fallback: license IDs on CHR)."""
        data = self._request("GET", "/system/routerboard") or {}
        serial = data.get("serial-number")
        if not serial:
            lic = self._request("GET", "/system/license") or {}
            serial = lic.get("system-id") or lic.get("software-id")
        if not serial:
            raise MikrotikError("serial-number not found on device")
        return str(serial).strip()

    # -- Step C: inject + execute the WireGuard provisioning script ----------
    def inject_and_run_script(self, source, name=PROVISION_SCRIPT_NAME):
        """
        1) Remove any stale copy of the provisioning script.
        2) Create it via PUT /rest/system/script.
        3) Execute it via POST /rest/system/script/run.
        """
        # 1) cleanup stale copies (best effort)
        try:
            existing = self._request(
                "GET", f"/system/script?name={name}"
            ) or []
            for item in existing:
                sid = item.get(".id")
                if sid:
                    self._request("DELETE", f"/system/script/{sid}")
        except MikrotikError:
            pass

        # 2) create the script with full policy so WireGuard/IP/peer
        #    commands and a final reboot are all permitted
        created = self._request("PUT", "/system/script", json_body={
            "name": name,
            "source": source,
            "policy": PROVISION_SCRIPT_POLICY,
        })
        sid = (created or {}).get(".id")

        # 3) run it (prefer .id, fall back to name)
        try:
            body = {".id": sid} if sid else {"number": name}
            self._request("POST", "/system/script/run", json_body=body)
        except MikrotikUnreachable:
            # A provisioning script that ends with /system reboot will drop
            # the connection mid-request — that is a SUCCESS signal here.
            pass
        except MikrotikError:
            self._request("POST", "/system/script/run",
                          json_body={"number": name})


def probe_router(host=ROUTER_HOST, ports=ROUTER_PROBE_PORTS,
                 timeout=ROUTER_PROBE_TIMEOUT):
    """
    Fast reachability check against the default MikroTik gateway.

    An unauthenticated GET to /rest answers with 401 on RouterOS v7 —
    any HTTP status code therefore proves a live web server at the
    gateway, which is a much stronger signal than a bare TCP handshake.
    """
    try:
        _LOCAL_HTTP.get(f"http://{host}/rest/system/identity",
                        timeout=timeout)
        return True  # any HTTP response (200/401/404) => device is alive
    except requests.exceptions.RequestException:
        pass
    # Fallback: raw TCP probe (covers routers with www service on 443 only)
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            continue
    return False


def get_local_ip():
    """Best-effort discovery of the phone's IP on the router's LAN."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect((ROUTER_HOST, 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return ROUTER_HOST  # sensible placeholder


# ===========================================================================
# 5. MAKKAWI SMART CLOUD CLIENT
# ===========================================================================

class CloudError(Exception):
    """Cloud responded with an unexpected error."""


class CloudUnreachable(CloudError):
    """Cloud server timed out or is offline."""


class CloudScriptMissing(CloudError):
    """Cloud registered the router but returned no provisioning script."""


_SCRIPT_KEYS = (
    "wireguard_script", "provisioning_script", "wg_script",
    "provision_script", "script", "config", "provision",
)


def _extract_script(data):
    """Recursively locate the WireGuard provisioning script in the response."""
    if isinstance(data, str):
        low = data.lower()
        if "wireguard" in low or "/interface" in low:
            return data
        return None
    if isinstance(data, dict):
        for key in _SCRIPT_KEYS:
            val = data.get(key)
            if isinstance(val, str) and val.strip():
                return val
        for val in data.values():
            found = _extract_script(val)
            if found:
                return found
    if isinstance(data, list):
        for val in data:
            found = _extract_script(val)
            if found:
                return found
    return None


def register_router_on_cloud(account, alias, ip_address, serial):
    """
    Step B — POST the router to the Makkawi Smart Cloud API and return the
    generated WireGuard provisioning script.

    NOTE: field names below match a typical FastAPI /routers/ schema —
    adjust "account" / "serial_number" here if the backend schema differs.
    """
    payload = {
        "name": alias,
        "ip_address": ip_address,
        "serial_number": serial,
        "account": account,
    }
    try:
        resp = requests.post(CLOUD_API_URL, json=payload,
                             timeout=CLOUD_TIMEOUT)
    except requests.exceptions.RequestException as exc:
        raise CloudUnreachable(str(exc))

    if resp.status_code >= 400:
        raise CloudError(f"HTTP {resp.status_code}: {resp.text[:200]}")

    try:
        data = resp.json()
    except ValueError:
        data = resp.text

    script = _extract_script(data)
    if not script:
        raise CloudScriptMissing("No provisioning script in cloud response")
    return script


# ===========================================================================
# 6. USER INTERFACE (KV)
# ===========================================================================

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<SectionTitle@MDBoxLayout>:
    icon: ""
    title: ""
    adaptive_height: True
    spacing: dp(8)
    MDLabel:
        text: root.title
        adaptive_height: True
        halign: "right"
        bold: True
        font_style: "Subtitle1"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#0f172a")
        pos_hint: {"center_y": .5}
    MDIcon:
        icon: root.icon
        size_hint: None, None
        size: dp(26), dp(26)
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#1d4ed8")
        pos_hint: {"center_y": .5}

<StepRow@MDBoxLayout>:
    step_icon: "checkbox-blank-circle-outline"
    step_color: get_color_from_hex("#94a3b8")
    step_text: ""
    icon_ref: icon_ref
    label_ref: label_ref
    adaptive_height: True
    spacing: dp(10)
    MDLabel:
        id: label_ref
        text: root.step_text
        adaptive_height: True
        halign: "right"
        font_style: "Body2"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#334155")
        pos_hint: {"center_y": .5}
    MDIcon:
        id: icon_ref
        icon: root.step_icon
        size_hint: None, None
        size: dp(24), dp(24)
        theme_text_color: "Custom"
        text_color: root.step_color
        pos_hint: {"center_y": .5}

MDScreen:
    md_bg_color: get_color_from_hex("#f8fafc")

    ScrollView:
        do_scroll_x: False
        bar_width: dp(3)

        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            padding: dp(18), dp(26), dp(18), dp(22)
            spacing: dp(14)

            # ---------------- HEADER ----------------
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: dp(2)
                MDIcon:
                    icon: "router-wireless"
                    size_hint: None, None
                    size: dp(52), dp(52)
                    font_size: dp(52)
                    pos_hint: {"center_x": .5}
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#1d4ed8")
                MDLabel:
                    text: app.tr('app_title')
                    adaptive_height: True
                    halign: "center"
                    bold: True
                    font_style: "H5"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#0f172a")
                MDLabel:
                    text: app.tr('app_subtitle')
                    adaptive_height: True
                    halign: "center"
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#64748b")

            # ---------------- LIVE STATUS CARD ----------------
            MDCard:
                orientation: "horizontal"
                adaptive_height: True
                padding: dp(14), dp(10), dp(14), dp(10)
                spacing: dp(10)
                radius: [dp(18)]
                md_bg_color: get_color_from_hex("#ffffff")
                elevation: 1

                MDIconButton:
                    icon: "refresh"
                    theme_icon_color: "Custom"
                    icon_color: get_color_from_hex("#64748b")
                    pos_hint: {"center_y": .5}
                    on_release: app.manual_refresh()

                MDLabel:
                    text: app.status_text
                    adaptive_height: True
                    halign: "right"
                    bold: True
                    font_style: "Body1"
                    theme_text_color: "Custom"
                    text_color: app.status_color
                    pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "circle"
                    size_hint: None, None
                    size: dp(18), dp(18)
                    font_size: dp(18)
                    theme_text_color: "Custom"
                    text_color: app.status_color
                    pos_hint: {"center_y": .5}

            # ---------------- CLOUD ACCOUNT CARD ----------------
            MDCard:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(16), dp(16), dp(16), dp(18)
                spacing: dp(6)
                radius: [dp(18)]
                md_bg_color: get_color_from_hex("#ffffff")
                elevation: 1

                SectionTitle:
                    icon: "cloud-outline"
                    title: app.tr('cloud_section')

                MDTextField:
                    id: cloud_user
                    hint_text: app.tr('cloud_user_hint')
                    mode: "rectangle"
                    halign: "right"
                    write_tab: False

                MDTextField:
                    id: alias
                    hint_text: app.tr('alias_hint')
                    mode: "rectangle"
                    halign: "right"
                    write_tab: False

            # ---------------- ROUTER CREDENTIALS CARD ----------------
            MDCard:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(16), dp(16), dp(16), dp(18)
                spacing: dp(6)
                radius: [dp(18)]
                md_bg_color: get_color_from_hex("#ffffff")
                elevation: 1

                SectionTitle:
                    icon: "shield-key-outline"
                    title: app.tr('router_section')

                MDTextField:
                    id: mik_user
                    text: "admin"
                    hint_text: app.tr('mik_user_hint')
                    mode: "rectangle"
                    halign: "right"
                    write_tab: False

                MDTextField:
                    id: mik_pass
                    hint_text: app.tr('mik_pass_hint')
                    mode: "rectangle"
                    halign: "right"
                    password: True
                    write_tab: False

            # ---------------- ACTIVATION STEPS CARD ----------------
            MDCard:
                orientation: "vertical"
                adaptive_height: True
                padding: dp(16), dp(16), dp(16), dp(18)
                spacing: dp(12)
                radius: [dp(18)]
                md_bg_color: get_color_from_hex("#ffffff")
                elevation: 1

                SectionTitle:
                    icon: "progress-check"
                    title: app.tr('steps_title')

                StepRow:
                    id: step_serial
                    step_text: app.tr('step_serial')

                StepRow:
                    id: step_cloud
                    step_text: app.tr('step_cloud')

                StepRow:
                    id: step_inject
                    step_text: app.tr('step_inject')

            # ---------------- ACTIVATE BUTTON ----------------
            MDRaisedButton:
                text: app.tr('activate_btn')
                md_bg_color: get_color_from_hex("#1d4ed8")
                text_color: 1, 1, 1, 1
                font_size: dp(17)
                size_hint_x: 1
                size_hint_y: None
                height: dp(52)
                elevation: 0
                disabled: app.busy
                on_release: app.start_activation()

            # ---------------- FOOTER ----------------
            MDLabel:
                text: app.tr('footer')
                adaptive_height: True
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#94a3b8")
'''


# ===========================================================================
# 7. APPLICATION
# ===========================================================================

STEP_STATES = {
    "idle":    ("checkbox-blank-circle-outline", C_IDLE),
    "running": ("progress-clock",                C_AMBER),
    "done":    ("check-circle",                  C_GREEN),
    "error":   ("close-circle",                  C_RED),
}


class MakkawiConnectorApp(MDApp):
    status_text = StringProperty("")
    status_color = ColorProperty(get_color_from_hex(C_AMBER))
    busy = BooleanProperty(False)
    router_connected = BooleanProperty(False)

    _dialog = None
    _probing = False

    # -- boot ----------------------------------------------------------------
    def build(self):
        self.title = TEXTS["app_title"]
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Window.clearcolor = get_color_from_hex(C_BG)

        font, font_bold = find_arabic_font()
        if font:
            # Re-register every font family KivyMD's typography uses
            # (Roboto, RobotoMedium, RobotoLight, ...) so labels, text
            # fields, buttons AND dialog titles all render Arabic glyphs.
            families = {style[0] for style in
                        self.theme_cls.font_styles.values()}
            families.add("Roboto")
            families.discard("Icons")  # never override the icon font
            for family in families:
                LabelBase.register(name=family, fn_regular=font,
                                   fn_bold=font_bold)

        self.status_text = self.tr("status_checking")
        return Builder.load_string(KV)

    def on_start(self):
        self._poll_event = Clock.schedule_interval(
            lambda dt: self.refresh_status(), STATUS_POLL_INTERVAL
        )
        self.refresh_status()

    def tr(self, key):
        return ar(TEXTS.get(key, key))

    # -- live connectivity status --------------------------------------------
    def manual_refresh(self):
        self.status_text = self.tr("status_checking")
        self.status_color = get_color_from_hex(C_AMBER)
        self.refresh_status()

    def refresh_status(self):
        if self._probing:
            return
        self._probing = True
        threading.Thread(target=self._probe_worker, daemon=True).start()

    def _probe_worker(self):
        alive = probe_router()
        self._apply_status(alive)

    @mainthread
    def _apply_status(self, alive):
        self._probing = False
        self.router_connected = alive
        if alive:
            self.status_text = self.tr("status_connected")
            self.status_color = get_color_from_hex(C_GREEN)
        else:
            self.status_text = self.tr("status_disconnected")
            self.status_color = get_color_from_hex(C_RED)

    # -- step indicators ------------------------------------------------------
    @mainthread
    def set_step(self, step_id, state, extra_text=None):
        row = self.root.ids[step_id]
        icon, color = STEP_STATES[state]
        row.step_icon = icon
        row.step_color = get_color_from_hex(color)
        if extra_text is not None:
            row.label_ref.text = extra_text

    @mainthread
    def reset_steps(self):
        for sid, key in (("step_serial", "step_serial"),
                         ("step_cloud", "step_cloud"),
                         ("step_inject", "step_inject")):
            self.set_step(sid, "idle", extra_text=self.tr(key))

    # -- dialogs ---------------------------------------------------------------
    @mainthread
    def show_dialog(self, title, message, retry=False):
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None

        buttons = [
            MDRaisedButton(
                text=self.tr("dlg_ok"),
                md_bg_color=get_color_from_hex(C_PRIMARY),
                on_release=lambda *_: self._dismiss_dialog(),
            )
        ]
        if retry:
            buttons.insert(0, MDFlatButton(
                text=self.tr("dlg_retry"),
                theme_text_color="Custom",
                text_color=get_color_from_hex(C_PRIMARY),
                on_release=lambda *_: self._retry_from_dialog(),
            ))

        self._dialog = MDDialog(
            title=self.tr(title) if title in TEXTS else title,
            text=ar_wrap(TEXTS.get(message, message)),
            radius=[dp(20), dp(20), dp(20), dp(20)],
            buttons=buttons,
        )
        # RTL: align the dialog title and body to the right
        try:
            self._dialog.ids.title.halign = "right"
            self._dialog.ids.text.halign = "right"
        except (AttributeError, KeyError):
            pass
        self._dialog.open()

    def _dismiss_dialog(self):
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None

    def _retry_from_dialog(self):
        self._dismiss_dialog()
        self.start_activation()

    # -- main activation flow ---------------------------------------------------
    def start_activation(self):
        if self.busy:
            return

        ids = self.root.ids
        account = ids.cloud_user.text.strip()
        alias = ids.alias.text.strip()
        mik_user = ids.mik_user.text.strip() or "admin"
        mik_pass = ids.mik_pass.text

        if not account or not alias:
            self.show_dialog("err_title", "err_missing_fields")
            return
        if not self.router_connected:
            self.show_dialog("err_title", "err_not_connected")
            return

        self.busy = True
        self.reset_steps()
        threading.Thread(
            target=self._activation_worker,
            args=(account, alias, mik_user, mik_pass),
            daemon=True,
        ).start()

    def _activation_worker(self, account, alias, mik_user, mik_pass):
        client = MikrotikClient(username=mik_user, password=mik_pass)

        # ---- Step A: hardware serial ------------------------------------
        self.set_step("step_serial", "running")
        try:
            serial = client.get_serial()
        except MikrotikAuthError:
            self.set_step("step_serial", "error")
            self._finish(dialog=("auth_title", "auth_msg", True))
            return
        except MikrotikUnreachable:
            self.set_step("step_serial", "error")
            self._finish(dialog=("err_title", "err_router_unreachable", True))
            return
        except MikrotikError:
            self.set_step("step_serial", "error")
            self._finish(dialog=("err_title", "err_inject", False))
            return
        self.set_step(
            "step_serial", "done",
            extra_text=ar(f"{TEXTS['serial_prefix']}: {serial}"),
        )

        # ---- Step B: cloud registration ----------------------------------
        self.set_step("step_cloud", "running")
        try:
            script = register_router_on_cloud(
                account, alias, get_local_ip(), serial,
            )
        except CloudUnreachable:
            self.set_step("step_cloud", "error")
            self._finish(dialog=("err_title", "err_cloud_unreachable", True))
            return
        except CloudScriptMissing:
            self.set_step("step_cloud", "error")
            self._finish(dialog=("err_title", "err_no_script", False))
            return
        except CloudError:
            self.set_step("step_cloud", "error")
            self._finish(dialog=("err_title", "err_cloud_response", True))
            return
        self.set_step("step_cloud", "done")

        # ---- Step C: inject + run the WireGuard script --------------------
        self.set_step("step_inject", "running")
        try:
            client.inject_and_run_script(script)
        except MikrotikAuthError:
            self.set_step("step_inject", "error")
            self._finish(dialog=("auth_title", "auth_msg", True))
            return
        except MikrotikError:
            self.set_step("step_inject", "error")
            self._finish(dialog=("err_title", "err_inject", True))
            return
        self.set_step("step_inject", "done")

        self._finish(dialog=("success_title", "success_msg", False))

    @mainthread
    def _finish(self, dialog=None):
        self.busy = False
        if dialog:
            title, message, retry = dialog
            self.show_dialog(title, message, retry=retry)


if __name__ == "__main__":
    MakkawiConnectorApp().run()
