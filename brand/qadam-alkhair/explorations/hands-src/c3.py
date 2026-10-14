# -*- coding: utf-8 -*-
"""Option ج, round 2: finer finger lines inside a bold outline, a filled sleeve, a shine on the heart."""
import math
import a2, hands3 as H, clear

GREEN, DARK, GOLD = a2.GREEN, "#0A5440", a2.GOLD
SHINE = "M-14.5,-20.5 C-17.5,-18.5 -18.6,-15.2 -17.6,-11.6"


def hand(x, y, w, green, rot, bg="#FFFFFF", tint="#E3F1EA", sw_lines=None, sleeve=None):
    return a2.place("palmUpHand", x, y, w, green, mirror=True, rot=rot, sw=40, wrist="cuff", style="tint",
                    tint=tint, bg=bg, sw_lines=sw_lines, sleeve=sleeve)


def heart(x, y, s, fill, shine=None):
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="{H.HEART}" fill="{fill}"/>'
    if shine:
        g += f'<path d="{SHINE}" fill="none" stroke="{shine}" stroke-width="3.4" stroke-linecap="round" opacity="0.9"/>'
    return g + "</g>"


def icon(green=GREEN, gold=GOLD, bg="#FFFFFF", tint="#E3F1EA", glow=("#FDF5E4", "#FBE8BF"), glow_op=(1, 1),
         rot=-14, hand_at=(20, 104, 164), heart_at=(70, 74), heart_s=0.86, gap=7, band=10, spark_r=5,
         sw_lines=None, sleeve=None, shine=None, _cache={}):
    x, y, w = hand_at
    hx, hy = heart_at
    key = (hand_at, rot, heart_at)
    if key not in _cache:
        black = hand(x, y, w, "#000", rot, bg="#000", tint="#000")
        _cache[key] = clear.min_dist(black, (hx, hy))
    ro = min(_cache[key] - gap, 42)
    ri = ro - band
    g = ""
    if glow:
        g += f'<circle cx="{hx}" cy="{hy}" r="{ro:.2f}" fill="{glow[0]}" fill-opacity="{glow_op[0]}"/>'
        g += f'<circle cx="{hx}" cy="{hy}" r="{ri:.2f}" fill="{glow[1]}" fill-opacity="{glow_op[1]}"/>'
    g += heart(hx, round(hy + 5.5 * heart_s, 2), heart_s, gold, shine)
    rs = (ri + ro) / 2
    for a in (0, 180):
        t = math.radians(a)
        g += a2.sparkle(round(hx + rs * math.cos(t), 2), round(hy + rs * math.sin(t), 2), spark_r, gold)
    return g + hand(x, y, w, green, rot, bg, tint, sw_lines, sleeve), ro
