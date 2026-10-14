# -*- coding: utf-8 -*-
"""Option أ exactly as approved: export horizontal, stacked and round icon."""
import os, re, subprocess, tempfile
import kit as K, lock3 as L, hands3 as H

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
BBOX = (12.00, 18.00, 188.00, 181.60)
OUT = "a1"
os.makedirs(OUT, exist_ok=True)


def shot(svg_text, w, out):
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text).groups())
    h = max(1, round(w * vh / vw))
    html = (f"<html><head><style>html,body{{margin:0;background:transparent}}"
            f"svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg_text}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={out}", "file://" + f.name], capture_output=True)
    os.unlink(f.name)


fn = H.give_receive_facing
files = {
    "qadam-a-logo": (L.horizontal(fn, BBOX, bg="#FFFFFF", H=240, pad=40), 2400),
    "qadam-a-stacked": (L.stacked(fn, BBOX, bg="#FFFFFF"), 1600),
    "qadam-a-icon": (L.badge(fn, BBOX, K.C["step"], green="#FFFFFF", gold=K.C["gold_lt"]), 1024),
}
for name, (svg, w) in files.items():
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg)
    shot(svg, w, f"{OUT}/{name}.png")
print(os.listdir(OUT))
