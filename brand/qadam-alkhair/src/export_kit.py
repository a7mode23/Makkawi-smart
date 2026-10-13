# -*- coding: utf-8 -*-
"""Export PNG/ICO from kit/logo into kit/png (needs Chromium)."""
import os, re, subprocess, sys, tempfile
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
ROOT = sys.argv[1] if len(sys.argv) > 1 else "kit"
SRC, DST = os.path.join(ROOT, "logo"), os.path.join(ROOT, "png")
JOBS = [("qadam-logo", [1200, 2400]), ("qadam-logo-stacked", [800, 1600]),
        ("qadam-logo-dark", [1200]), ("qadam-logo-stacked-dark", [800]),
        ("qadam-logo-on-green", [1200]), ("qadam-logo-mono-ink", [1200]), ("qadam-logo-mono-white", [1200]),
        ("qadam-wordmark-ar", [1200]), ("qadam-wordmark-en", [1200]),
        ("qadam-mark", [512, 1024]), ("qadam-icon", [512, 1024]), ("qadam-app-icon", [180, 512, 1024]),
        ("qadam-favicon", [16, 32, 48, 64])]
os.makedirs(DST, exist_ok=True)


def shot(svg_text, w, out):
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text).groups())
    h = max(1, round(w * vh / vw))
    html = (f"<html><head><style>html,body{{margin:0;background:transparent}}"
            f"svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg_text}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp = f.name
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={out}", "file://" + tmp], capture_output=True)
    os.unlink(tmp)


for name, widths in JOBS:
    text = open(os.path.join(SRC, name + ".svg"), encoding="utf-8").read()
    for w in widths:
        shot(text, w, os.path.join(DST, f"{name}-{w}.png" if len(widths) > 1 else f"{name}.png"))
subprocess.run(["convert"] + [os.path.join(DST, f"qadam-favicon-{s}.png") for s in (16, 32, 48)]
               + [os.path.join(DST, "qadam-favicon.ico")])
print(len(os.listdir(DST)), "files in", DST)
