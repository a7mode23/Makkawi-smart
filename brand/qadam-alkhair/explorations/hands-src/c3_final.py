# -*- coding: utf-8 -*-
"""Option ج, round 2 — export the set and a one-page sheet."""
import os, sys
import kit as K, lock3 as L, a3, c3, measure as M
from shot import shot

OUT = sys.argv[1] if len(sys.argv) > 1 else "c5out"
os.makedirs(OUT, exist_ok=True)
C = K.C
SHAPE = dict(sw_lines=0, shine="#FFFFFF")
LIGHT = dict(SHAPE, sleeve=c3.DARK)
DARK = dict(SHAPE, green=C["cream"], gold=C["gold_lt"], tint="#1F3B32", bg=C["ink"], sleeve=C["cream"],
            glow=(C["gold_lt"], C["gold_lt"]), glow_op=(0.12, 0.26))
ONGREEN = dict(SHAPE, green="#FFFFFF", gold=C["gold_lt"], tint="#2A8C69", bg=C["step"], sleeve="#FFFFFF",
               glow=("#FFFFFF", C["gold_lt"]), glow_op=(0.08, 0.22))


def fn(kw):
    return lambda **_: c3.icon(**kw)[0]


BB = {k: M.ink_box(fn(v)()) for k, v in (("light", LIGHT), ("dark", DARK), ("green", ONGREEN))}
files = {
    "qadam-logo": (a3.horizontal(fn(LIGHT), BB["light"], bg="#FFFFFF"), 2400),
    "qadam-logo-stacked": (a3.stacked(fn(LIGHT), BB["light"], bg="#FFFFFF"), 1600),
    "qadam-logo-dark": (a3.horizontal(fn(DARK), BB["dark"], name=C["cream"], accent=C["gold_lt"], bg=C["ink"]), 2400),
    "qadam-icon": (L.badge(fn(ONGREEN), BB["green"], C["step"], frac=0.70, cap=0.76), 1024),
    "qadam-app-icon": (L.badge(fn(ONGREEN), BB["green"], C["step"], shape="square", S=512, frac=0.70, cap=0.76), 1024),
}
for name, (svg, w) in files.items():
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg)
    shot(svg, w, f"{OUT}/{name}.png")

sheet = f"""<html><head><meta charset=utf-8><style>
body{{margin:0;background:#FBF7EF;padding:28px;width:1144px;display:grid;gap:22px}}
.card{{background:#fff;border-radius:22px;padding:22px 30px;display:flex;align-items:center;justify-content:center}}
.dark{{background:{C["ink"]}}} .row{{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:22px}}
img{{width:100%;display:block}} .ic img{{width:80%}}
</style></head><body>
<div class=card><img src="qadam-logo.png"></div>
<div class=row><div class=card><img src="qadam-logo-stacked.png"></div>
<div class="card ic"><img src="qadam-icon.png"></div><div class="card ic"><img src="qadam-app-icon.png"></div></div>
<div class="card dark"><img src="qadam-logo-dark.png"></div>
</body></html>"""
open(f"{OUT}/sheet.html", "w", encoding="utf-8").write(sheet)
print(BB)
