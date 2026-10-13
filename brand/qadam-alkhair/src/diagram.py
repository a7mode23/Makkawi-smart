# -*- coding: utf-8 -*-
"""Annotated construction diagram: what each part of the mark means."""
import build as B
from build import C, MARK_INK
from textpath import shape_to_path

W, H = 840, 430
S = 250 / (MARK_INK[3] - MARK_INK[1])          # mark height 250
MX, MY = 70, 90
LABEL_RIGHT = W - 40

def to_canvas(x, y):
    return MX + (x - MARK_INK[0]) * S, MY + (y - MARK_INK[1]) * S

ITEMS = [
    ((139.7, 46.3),  "حرف Q · كتلة واحدة", 86),
    ((112.5, 79.0),  "جوف الحرف كفّ مفتوحة", 176),
    ((95.4, 99.3),   "قلب في الراحة · الخير", 266),
    ((146.0, 146.0), "ذيل Q يقطع الحرف", 356),
]

defs, body = B.mark("d1", None, C["gold"],
                    gradient=(C["green_lt"], C["green_dk"]))
parts = [f'<g transform="translate({MX - MARK_INK[0]*S:.2f} {MY - MARK_INK[1]*S:.2f}) '
         f'scale({S:.5f})">{body}</g>']

for (mx, my), text, ly in ITEMS:
    px, py = to_canvas(mx, my)
    lab = shape_to_path(B.FONT_LA.replace("Bold", "Bold"), "x", size=1)  # placeholder, replaced below
    lab = shape_to_path(B.FONT_AR.replace("ExtraBold", "Bold"), text, size=19)
    x0, _, x1, _ = lab["bbox"]
    left = LABEL_RIGHT - (x1 - x0) - 18
    parts.append(
        f'<path d="M{px:.1f},{py:.1f} L{left-46:.1f},{py:.1f} L{left-18:.1f},{ly:.1f} '
        f'L{left-6:.1f},{ly:.1f}" fill="none" stroke="currentColor" stroke-width="1.6" '
        f'stroke-opacity="0.38" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="currentColor" fill-opacity="0.38"/>'
        f'<g transform="translate({LABEL_RIGHT - x1:.2f} {ly + 7:.2f})">'
        f'<path d="{lab["d"]}" fill="currentColor"/></g>')

svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
       'role="img" aria-label="شرح عناصر شعار قدم الخير">\n<title>قدم الخير — بناء العلامة</title>\n'
       '<defs>\n%s\n</defs>\n%s\n</svg>\n') % (W, H, W, H, defs, "\n".join(parts))
open("out/logo/qadam-concept-diagram.svg", "w", encoding="utf-8").write(svg)
print("ok", len(svg))
