# -*- coding: utf-8 -*-
"""How big a circle fits between the two hands (with no overlap), for a given spread."""
import os, subprocess, tempfile
import numpy as np
from PIL import Image
import a2

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
PX = 2


def hands(spread=0.0, lift=0.0, rot=-6):
    """Giver moves up-right and receiver down-left by `spread`; both move up by `lift`."""
    top = a2.place("palmDownHand", 64 + spread, 18 - spread - lift, 124, "#000", mirror=True, rot=rot, sw=40, wrist="cuff", style="tint", tint="#000", bg="#000")
    bot = a2.place("palmUpHand", 12 - spread, 108 + spread - lift, 124, "#000", sw=40, wrist="cuff", style="tint", tint="#000", bg="#000")
    return top + bot


def mask(markup, lo=-40, size=280):
    W = size * PX
    html = (f'<html><body style="margin:0;background:#fff"><svg xmlns="http://www.w3.org/2000/svg" viewBox="{lo} {lo} {size} {size}" '
            f'width="{W}" height="{W}">{markup}</svg></body></html>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    png = f.name + ".png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{W}",
                    f"--screenshot={png}", "file://" + f.name], capture_output=True)
    a = np.asarray(Image.open(png).convert("L")) < 128
    os.unlink(f.name); os.unlink(png)
    return a


def best_circle(spread=0.0, lift=0.0, lo=-40, size=280, near=(97, 100), search=25, rot=-6):
    """Centre (near `near`) of the largest circle touching no hand, and its radius."""
    m = mask(hands(spread, lift, rot), lo, size)
    edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    ey, ex = np.nonzero(edge)
    pts = np.stack([lo + ex / PX, lo + ey / PX], 1)
    cx, cy = near
    gx, gy = np.meshgrid(np.arange(cx - search, cx + search + 0.1, 0.5), np.arange(cy - search, cy + search + 0.1, 0.5))
    cand = np.stack([gx.ravel(), gy.ravel()], 1)
    best = np.full(len(cand), np.inf)
    for i in range(0, len(pts), 4000):
        d = np.sqrt(((cand[:, None, :] - pts[None, i:i + 4000, :]) ** 2).sum(-1)).min(1)
        best = np.minimum(best, d)
    # a candidate inside a hand is no good
    inside = m[((cand[:, 1] - lo) * PX).astype(int).clip(0, m.shape[0] - 1), ((cand[:, 0] - lo) * PX).astype(int).clip(0, m.shape[1] - 1)]
    best[inside] = 0
    k = int(np.argmax(best))
    return float(cand[k, 0]), float(cand[k, 1]), float(best[k])


if __name__ == "__main__":
    for spread in (0, 4, 8, 12):
        print(spread, [round(v, 1) for v in best_circle(spread)])
