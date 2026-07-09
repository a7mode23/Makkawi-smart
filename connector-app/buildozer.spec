[app]

# -- identity ---------------------------------------------------------------
title = Makkawi Smart Router Connector
package.name = routerconnector
package.domain = com.makkawismart
version = 1.0.0

# -- sources ----------------------------------------------------------------
source.dir = .
source.include_exts = py,kv,ttf,txt,png,jpg
source.exclude_dirs = __pycache__, bin, .buildozer

# -- runtime requirements -----------------------------------------------------
# requests needs urllib3/charset-normalizer/idna/certifi explicitly on p4a.
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,charset-normalizer,idna,certifi,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

# App icon / splash — drop the images next to this file and uncomment:
#icon.filename = %(source.dir)s/assets/icon.png
#presplash.filename = %(source.dir)s/assets/presplash.png

# -- android ------------------------------------------------------------------
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = False

# The local router (192.168.88.1) speaks plain HTTP, so cleartext traffic
# must stay enabled even after the cloud endpoint moves to HTTPS.
# The attributes are injected into the <application> tag of the manifest.
android.extra_manifest_application_arguments = ./android_manifest_application_args.xml

# Keep the keyboard from resizing the whole UI while typing
android.softinput_mode = below_target

[buildozer]
log_level = 2
warn_on_root = 1

# Build with:
#   pip install buildozer cython
#   buildozer android debug          -> bin/routerconnector-1.0.0-debug.apk
#   buildozer android release        -> unsigned release APK (sign before publishing)
