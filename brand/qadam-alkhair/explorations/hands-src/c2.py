# -*- coding: utf-8 -*-
"""Option ج developed: one hand offering a glowing heart."""
import math
import a2, hands3 as H, clear

GREEN, GOLD = a2.GREEN, a2.GOLD


def hand(x, y, w, green, rot, bg="#FFFFFF", tint="#E3F1EA"):
    return a2.place("palmUpHand", x, y, w, green, mirror=True, rot=rot, sw=40, wrist="cuff", style="tint", tint=tint, bg=bg)


def icon(green=GREEN, gold=GOLD, bg="#FFFFFF", tint="#E3F1EA", glow=("#FDF5E4", "#FBE8BF"), glow_op=(1, 1),
         rot=0, hand_at=(20, 104, 164), heart=(90, 62), heart_s=0.95, gap=7, band=11, spark_r=5.4, _cache={}):
    x, y, w = hand_at
    hx, hy = heart
    key = (hand_at, rot, heart)
    if key not in _cache:
        black = hand(x, y, w, "#000", rot, bg="#000", tint="#000")
        _cache[key] = clear.min_dist(black, (hx, hy))
    ro = min(_cache[key] - gap, 42)
    ri = ro - band
    g = ""
    if glow:
        g += f'<circle cx="{hx}" cy="{hy}" r="{ro:.2f}" fill="{glow[0]}" fill-opacity="{glow_op[0]}"/>'
        g += f'<circle cx="{hx}" cy="{hy}" r="{ri:.2f}" fill="{glow[1]}" fill-opacity="{glow_op[1]}"/>'
    g += H.heart(hx, round(hy + 5.5 * heart_s, 2), heart_s, gold)
    rs = (ri + ro) / 2
    for a in (0, 180):
        t = math.radians(a)
        g += a2.sparkle(round(hx + rs * math.cos(t), 2), round(hy + rs * math.sin(t), 2), spark_r, gold)
    return g + hand(x, y, w, green, rot, bg, tint), ro
