# -*- coding: utf-8 -*-
"""Export PNG/ICO from the SVG masters (needs Chromium)."""
import os, re, subprocess, tempfile
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SRC, DST = "out2/logo", "out2/png"
os.makedirs(DST, exist_ok=True)
JOBS = [("qadam-logo", [800, 1600]), ("qadam-logo-dark", [800, 1600]),
        ("qadam-logo-on-green", [800]), ("qadam-logo-mono-ink", [800]),
        ("qadam-logo-mono-white", [800]),
        ("qadam-logo-horizontal", [1200, 2400]), ("qadam-logo-horizontal-dark", [1200]),
        ("qadam-wordmark-ar", [1200]), ("qadam-wordmark-en", [1200]),
        ("qadam-icon", [512, 1024]), ("qadam-app-icon", [180, 512, 1024]),
        ("qadam-favicon", [16, 32, 48, 64]),
        ("qadam-alt-rounded", [800]), ("qadam-alt-ruqaa", [800]), ("qadam-alt-modern", [800])]
for name, widths in JOBS:
    text = open(os.path.join(SRC, name + ".svg"), encoding="utf-8").read()
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', text).groups())
    for w in widths:
        h = max(1, round(w * vh / vw))
        html = (f"<html><head><style>html,body{{margin:0;background:transparent}}"
                f"svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{text}</body></html>")
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html); tmp = f.name
        out = os.path.join(DST, f"{name}-{w}.png" if len(widths) > 1 else f"{name}.png")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--default-background-color=00000000",
                        f"--window-size={w},{h}", f"--screenshot={out}", "file://" + tmp],
                       capture_output=True)
        os.unlink(tmp)
        print(out)
subprocess.run(["convert", f"{DST}/qadam-favicon-16.png", f"{DST}/qadam-favicon-32.png",
                f"{DST}/qadam-favicon-48.png", f"{DST}/qadam-favicon.ico"])
print(f"{DST}/qadam-favicon.ico")
