# -*- coding: utf-8 -*-
"""Trace each hand's filled silhouette (everything inside the outline) back into font units."""
import json
import numpy as np
import potrace
from PIL import Image

DIMS = {"palmDownHand": (190, 1560), "palmUpHand": (145, 1410)}   # viewBox x0, -y0 (image is half scale)


def trace(name):
    im = np.asarray(Image.open(f"{name}-flood.png").convert("RGB")).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    outside = (r > 180) & (g < 90) & (b < 90)
    bm = potrace.Bitmap(outside)
    paths = bm.trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2)
    ox, oy = DIMS[name]
    X = lambda p: f"{ox + 2 * p.x:.1f} {oy - 2 * p.y:.1f}"
    d = []
    for c in paths:
        d.append("M" + X(c.start_point))
        for s in c.segments:
            if s.is_corner:
                d.append("L" + X(s.c) + "L" + X(s.end_point))
            else:
                d.append("C" + X(s.c1) + " " + X(s.c2) + " " + X(s.end_point))
        d.append("Z")
    return "".join(d), len(paths)


out = {}
for n in DIMS:
    out[n], k = trace(n)
    print(n, k, "contours", len(out[n]), "chars")
json.dump(out, open("silhouettes.json", "w"))
