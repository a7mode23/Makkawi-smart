# -*- coding: utf-8 -*-
"""A refined footprint, drawn once and reused: single, pair, rising steps."""
import math

GREEN, GOLD = "#0F7B5A", "#E3A42B"

# right foot, toes up, big toe on the inner (left) side; local box ~ (-34..38, -78..78)
SOLE = ("M-21,-38 C-17,-50 2,-52 17,-47 C31,-42 38,-30 37,-12 "
        "C36,6 28,20 25,36 C22,54 17,74 2,77 C-13,80 -21,66 -20,50 "
        "C-19,36 -10,24 -11,8 C-12,-6 -24,-22 -21,-38 Z")
# toes follow an arc above the ball; ovals tilted to fan out
TOES = [(-17.5, -64.0, 10.6, 12.8, -14), (2.0, -70.5, 8.1, 9.9, -4), (16.5, -67.0, 7.0, 8.6, 6),
        (27.8, -58.5, 6.0, 7.3, 15), (35.8, -46.5, 5.0, 6.1, 25)]


def foot(fill, toe_fill=None, x=0, y=0, s=1.0, rot=0, mirror=False):
    toe_fill = toe_fill or fill
    m = " scale(-1 1)" if mirror else ""
    toes = "".join(f'<ellipse cx="{tx}" cy="{ty}" rx="{rx}" ry="{ry}" transform="rotate({a} {tx} {ty})" '
                   f'fill="{toe_fill}"/>' for tx, ty, rx, ry, a in TOES)
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s}){m}">'
            f'<path d="{SOLE}" fill="{fill}"/>{toes}</g>')


def single(green=GREEN, gold=GOLD):
    """أ — قدم واحدة: green sole, golden toes — the step leaves gold behind."""
    return foot(green, gold, 100, 104, 1.12, -10)


def pair(green=GREEN, gold=GOLD):
    """ب — قدمان: left foot behind in green, right foot ahead in gold; walking up-left."""
    back = foot(green, green, 128, 128, 0.74, 12, mirror=False)
    lead = foot(gold, gold, 74, 74, 0.74, -16, mirror=True)
    return back + lead


def rising(green=GREEN, gold=GOLD, start=(124, 166), step=70, lateral=14, sc=0.40):
    """ج — ثلاث خطوات: a short path that climbs up and to the left; the last step is gold."""
    d = (-0.55, -0.835)                      # walking direction (up-left)
    p = (-d[1], d[0])                        # the walker's right-hand side
    rot = math.degrees(math.atan2(d[0], -d[1]))
    out = []
    for i in range(3):
        side = 1 if i % 2 == 0 else -1       # right, left, right
        cx = start[0] + i * step * d[0] + side * lateral * p[0]
        cy = start[1] + i * step * d[1] + side * lateral * p[1]
        fill = gold if i == 2 else green
        out.append(foot(fill, fill, round(cx, 1), round(cy, 1), sc, round(rot, 1), mirror=(side < 0)))
    return "".join(out)


OPTIONS = [("أ — قدم واحدة", single), ("ب — قدمان", pair), ("ج — ثلاث خطوات", rising)]
