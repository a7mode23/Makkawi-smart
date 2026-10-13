# -*- coding: utf-8 -*-
"""Export PNG/ICO for every kit under ROOT/<option>/logo -> ROOT/<option>/png (needs Chromium)."""
import os, re, subprocess, sys, tempfile
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
ROOT = sys.argv[1] if len(sys.argv) > 1 else "out3"
JOBS = [("qadam-logo", [800, 1600]), ("qadam-logo-dark", [800]), ("qadam-logo-on-green", [800]),
        ("qadam-logo-mono-ink", [800]), ("qadam-logo-mono-white", [800]),
        ("qadam-logo-horizontal", [1200]), ("qadam-logo-horizontal-dark", [1200]),
        ("qadam-wordmark-ar", [1200]), ("qadam-wordmark-en", [1200]),
        ("qadam-icon", [512]), ("qadam-app-icon", [180, 512]), ("qadam-favicon", [16, 32, 48])]


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
                    f"--window-size={w},{h}", f"--screenshot={out}", "file://" + tmp],
                   capture_output=True)
    os.unlink(tmp)


for opt in sorted(os.listdir(ROOT)):
    src, dst = os.path.join(ROOT, opt, "logo"), os.path.join(ROOT, opt, "png")
    if not os.path.isdir(src):
        continue
    os.makedirs(dst, exist_ok=True)
    for name, widths in JOBS:
        p = os.path.join(src, name + ".svg")
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8").read()
        for w in widths:
            out = os.path.join(dst, f"{name}-{w}.png" if len(widths) > 1 else f"{name}.png")
            shot(text, w, out)
    subprocess.run(["convert"] + [os.path.join(dst, f"qadam-favicon-{s}.png") for s in (16, 32, 48)]
                   + [os.path.join(dst, "qadam-favicon.ico")])
    print(opt, len(os.listdir(dst)), "files")
