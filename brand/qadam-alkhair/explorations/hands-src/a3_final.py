# -*- coding: utf-8 -*-
"""Option أ, third round — export the set and a one-page sheet."""
import os, sys
import kit as K, lock3 as L, a3, measure as M
from shot import shot

OUT = sys.argv[1] if len(sys.argv) > 1 else "a3out"
os.makedirs(OUT, exist_ok=True)
C = K.C
LIGHT = dict(giver=C["green"])
DARK = dict(green=C["cream"], gold=C["gold_lt"], tint="#1F3B32", bg=C["ink"], giver="#FFFFFF",
            glow=((38, C["gold_lt"], 0.10), (27, C["gold_lt"], 0.20)))
ONGREEN = dict(green="#FFFFFF", gold=C["gold_lt"], tint="#2A8C69", bg=C["step"],
               glow=((38, "#FFFFFF", 0.08), (27, C["gold_lt"], 0.22)))


def fn(kw):
    return lambda **_: a3.icon(**kw)


BB = {k: M.ink_box(a3.icon(**v)) for k, v in (("light", LIGHT), ("dark", DARK), ("green", ONGREEN))}
files = {
    "qadam-logo": (a3.horizontal(fn(LIGHT), BB["light"], bg="#FFFFFF"), 2400),
    "qadam-logo-stacked": (a3.stacked(fn(LIGHT), BB["light"], bg="#FFFFFF"), 1600),
    "qadam-logo-dark": (a3.horizontal(fn(DARK), BB["dark"], name=C["cream"], accent=C["gold_lt"], bg=C["ink"]), 2400),
    "qadam-icon": (L.badge(fn(ONGREEN), BB["green"], C["step"], cap=0.76), 1024),
    "qadam-app-icon": (L.badge(fn(ONGREEN), BB["green"], C["step"], shape="square", S=512, cap=0.76), 1024),
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
