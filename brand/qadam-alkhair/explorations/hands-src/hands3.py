# -*- coding: utf-8 -*-
"""Giving and receiving hands, from Noto Emoji (SIL OFL 1.1), with a gold heart between."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

FONT = "emoji/NotoEmoji[wght].ttf"
GREEN, GOLD = "#0F7B5A", "#E3A42B"
HEART = ("M0,15 C-16,4 -22,-5 -22,-13 C-22,-21 -16,-26 -9,-26 C-4.5,-26 -1,-23 0,-19.5 "
         "C1,-23 4.5,-26 9,-26 C16,-26 22,-21 22,-13 C22,-5 16,4 0,15 Z")
_tt = TTFont(FONT)
_cache = {}


def glyph(name, wght=700):
    """-> (path d in font units, flipped to y-down), bbox."""
    key = (name, wght)
    if key not in _cache:
        gs = _tt.getGlyphSet(location={"wght": wght})
        sp = SVGPathPen(gs)
        gs[name].draw(sp)
        bp = BoundsPen(gs)
        gs[name].draw(bp)
        x0, y0, x1, y1 = bp.bounds
        _cache[key] = (sp.getCommands(), (x0, -y1, x1, -y0))
    return _cache[key]


def place(name, x, y, w, fill, mirror=False, wght=700, rot=0):
    """Put a glyph so its ink box is `w` wide with top-left at (x, y)."""
    d, (x0, y0, x1, y1) = glyph(name, wght)
    s = w / (x1 - x0)
    h = (y1 - y0) * s
    cx, cy = x + w / 2, y + h / 2
    m = -1 if mirror else 1
    return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({rot}) scale({m * s:.5f} {s:.5f}) '
            f'translate({-(x0 + x1) / 2:.2f} {-(y0 + y1) / 2:.2f}) scale(1 -1)">'
            f'<path d="{d}" fill="{fill}"/></g>'), h


def heart(x, y, s, fill):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="{HEART}" fill="{fill}"/></g>'


def give_receive_facing(green=GREEN, gold=GOLD, wght=700):
    """أ — the giver (palm down) reaches in from the right, the receiver (palm up) from the left."""
    top, _ = place("palmDownHand", 64, 18, 124, green, mirror=True, wght=wght)
    bot, _ = place("palmUpHand", 12, 108, 124, green, mirror=False, wght=wght)
    return top + bot + heart(100, 98, 0.78, gold)


def give_receive_stacked(green=GREEN, gold=GOLD, wght=700):
    """ب — both reach the same way: the giver above lets the heart fall into the hand below."""
    top, _ = place("palmDownHand", 30, 14, 132, green, wght=wght)
    bot, _ = place("palmUpHand", 38, 112, 132, green, wght=wght)
    return top + bot + heart(128, 96, 0.74, gold)


def single_offer(green=GREEN, gold=GOLD, wght=700):
    """ج — one hand, palm up, offering the heart."""
    h, _ = place("palmUpHand", 20, 92, 160, green, mirror=True, wght=wght)
    return h + heart(92, 70, 1.05, gold)


OPTIONS = [("أ — إيد بتدّي وإيد بتستلم (وش لوش)", give_receive_facing),
           ("ب — الإيد اللي فوق بتنزّل القلب للي تحت", give_receive_stacked),
           ("ج — إيد واحدة بتقدّم القلب", single_offer)]
