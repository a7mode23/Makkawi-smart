# -*- coding: utf-8 -*-
"""Measure the true ink box (strokes included) of icon markup drawn in a 200x200 space."""
import os, subprocess, tempfile
import numpy as np
from PIL import Image

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"


def ink_box(markup, lo=-40, size=280, px=4):
    W = size * px
    html = (f'<html><head><style>html,body{{margin:0;background:transparent}}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{lo} {lo} {size} {size}" width="{W}" height="{W}">'
            f'{markup}</svg></body></html>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    png = f.name + ".png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000", f"--window-size={W},{W}", f"--screenshot={png}",
                    "file://" + f.name], capture_output=True)
    a = np.asarray(Image.open(png).convert("RGBA"))[..., 3]
    os.unlink(f.name); os.unlink(png)
    ys, xs = np.nonzero(a > 8)
    return (lo + xs.min() / px, lo + ys.min() / px, lo + (xs.max() + 1) / px, lo + (ys.max() + 1) / px)


if __name__ == "__main__":
    import a2
    print(ink_box(a2.icon(wrist="cuff", rot=-6, heart_at=(98, 102))))
