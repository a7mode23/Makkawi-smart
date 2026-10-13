# -*- coding: utf-8 -*-
import os, re, subprocess, tempfile
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SRC, DST = "out/logo", "out/png"
os.makedirs(DST, exist_ok=True)

JOBS = [("qadam-mark", [512, 1024]), ("qadam-mark-mono-ink", [512]),
        ("qadam-mark-mono-white", [512]), ("qadam-mark-mono-green", [512]),
        ("qadam-logo-horizontal", [1200, 2400]), ("qadam-logo-horizontal-rtl", [1200]),
        ("qadam-logo-horizontal-dark", [1200, 2400]),
        ("qadam-logo-horizontal-mono-white", [1200]),
        ("qadam-logo-stacked", [900, 1800]), ("qadam-logo-stacked-dark", [900]),
        ("qadam-wordmark", [1600]), ("qadam-app-icon", [512, 1024]),
        ("qadam-favicon", [16, 32, 48, 64, 180, 512]),
        ("qadam-alt-heart", [512]), ("qadam-alt-wheat", [512]),
        ("qadam-alt-hand", [512])]

def viewbox(svg_text):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    return float(m.group(1)), float(m.group(2))

for name, widths in JOBS:
    path = os.path.join(SRC, name + ".svg")
    svg_text = open(path, encoding="utf-8").read()
    vw, vh = viewbox(svg_text)
    for w in widths:
        h = max(1, round(w * vh / vw))
        html = (f'<html><head><meta charset=utf-8><style>html,body{{margin:0;padding:0;'
                f'background:transparent}}svg{{display:block;width:{w}px;height:{h}px}}</style>'
                f'</head><body>{svg_text}</body></html>')
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html); tmp = f.name
        suffix = f"-{w}" if len(widths) > 1 or name.startswith("qadam-favicon") else ""
        out = os.path.join(DST, f"{name}{suffix}.png")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                        "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--default-background-color=00000000",
                        f"--window-size={w},{h}", f"--screenshot={out}", "file://" + tmp],
                       capture_output=True)
        os.unlink(tmp)
        print(out, os.path.getsize(out))
