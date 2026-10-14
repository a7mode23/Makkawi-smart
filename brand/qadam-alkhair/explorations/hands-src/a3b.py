# -*- coding: utf-8 -*-
"""Round 3, fixed: the light, the heart and the sparkles sit in the clear space between
the hands — nothing touches a hand."""
import math
import a2, hands3 as H
import clear

GOLD, GLOW_O, GLOW_I = a2.GOLD, "#FDF5E4", "#FBE8BF"


def icon(spread=8, gap=6, band=10, heart_s=0.82, spark_r=4.6, spark_at="level", two=True,
         green=a2.GREEN, gold=GOLD, glow=(GLOW_O, GLOW_I), giver=None, bg="#FFFFFF", tint="#E3F1EA",
         glow_op=(1, 1), _cache={}):
    key = spread
    if key not in _cache:
        _cache[key] = clear.best_circle(spread, near=(105, 105), search=18)
    cx, cy, R = _cache[key]
    kw = dict(sw=40, wrist="cuff", style="tint", tint=tint, bg=bg)
    top = a2.place("palmDownHand", 64 + spread, 18 - spread, 124, giver or green, mirror=True, rot=-6, **kw)
    bot = a2.place("palmUpHand", 12 - spread, 108 + spread, 124, green, **kw)
    ro = R - gap
    ri = ro - band if two else ro
    g = ""
    if glow:
        g += f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{ro:.2f}" fill="{glow[0]}" fill-opacity="{glow_op[0]}"/>'
        if two:
            g += f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{ri:.2f}" fill="{glow[1]}" fill-opacity="{glow_op[1]}"/>'
    # heart: centre its ink box on the light
    g += H.heart(round(cx, 2), round(cy + 5.5 * heart_s, 2), heart_s, gold)
    if spark_r:
        rs = (ri + ro) / 2 if two else ro - spark_r - 1.5
        angs = {"level": (0, 180), "high": (-38, 218)}[spark_at]
        for a in angs:
            t = math.radians(a)
            g += a2.sparkle(round(cx + rs * math.cos(t), 2), round(cy + rs * math.sin(t), 2), spark_r, gold)
    return top + bot + g, (cx, cy, R)
