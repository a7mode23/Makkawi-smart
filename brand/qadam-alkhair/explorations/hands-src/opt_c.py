# -*- coding: utf-8 -*-
"""Option ج as first shown: one hand, palm up, offering the heart — horizontal, stacked, icon."""
import os
import kit as K, lock3 as L, hands3 as H
from shot import shot

BBOX = (20.00, 42.70, 180.00, 186.98)
OUT = "c1"
os.makedirs(OUT, exist_ok=True)
fn = H.single_offer
files = {
    "qadam-c-logo": (L.horizontal(fn, BBOX, bg="#FFFFFF", H=240, pad=40), 2400),
    "qadam-c-stacked": (L.stacked(fn, BBOX, bg="#FFFFFF"), 1600),
    "qadam-c-icon": (L.badge(fn, BBOX, K.C["step"], green="#FFFFFF", gold=K.C["gold_lt"]), 1024),
}
for name, (svg, w) in files.items():
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg)
    shot(svg, w, f"{OUT}/{name}.png")
print(sorted(os.listdir(OUT)))
