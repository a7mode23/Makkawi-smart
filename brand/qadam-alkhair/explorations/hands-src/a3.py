# -*- coding: utf-8 -*-
"""Option أ, third round: the heart gets a warm glow, and the name carries the heart
(the dot of «خ» in «الخير» becomes the same gold heart)."""
import glyphs as G
import kit as K
import a2
import hands3 as H
from lock3 import icon_at
from wordmark import HEART

def name_ar(ink, accent, heart_dot=True):
    g, _ = G.shape(K.FONT, "قدم الخير", 100, K.AR_LOC)
    dot = G.take_dot(g, "قدم الخير".index("خ"), "above") if heart_dot else None
    m = f'<path d="{G.path_of(g)}" fill="{ink}"/>'
    if dot:
        m += heart_dot_mark(dot, accent)
    return m, G.bbox_of(g)


def heart_dot_mark(dot, fill, k=1.75):
    """A heart in place of a dot: as wide as k dots, its tip where the dot's bottom was."""
    x0, y0, x1, y1 = dot
    s = (x1 - x0) * k / 44
    return (f'<g transform="translate({(x0 + x1) / 2:.2f} {y1 - 15 * s:.2f}) scale({s:.4f})">'
            f'<path d="{HEART}" fill="{fill}"/></g>')


GLOW = ((38, "#FDF5E4", 1), (27, "#FBE8BF", 1))      # (radius, colour, opacity), outer first


def icon(green=a2.GREEN, gold=a2.GOLD, glow=GLOW, giver=None, **kw):
    """a2.icon with two soft discs of light behind the heart."""
    kw = {**dict(rot=-6, heart_at=(97, 105), heart_s=0.9, wrist="cuff", style="tint", sparkles="pair"), **kw}
    hx, hy = kw["heart_at"]
    disc = "".join(f'<circle cx="{hx}" cy="{hy - 5}" r="{r}" fill="{c}" fill-opacity="{o}"/>' for r, c, o in glow or ())
    return disc + a2.icon(green=green, gold=gold, giver=giver, **kw)


def horizontal(fn, bbox, name=K.C["green"], accent=K.C["gold"], bg=None, H=240, pad=40, heart_dot=True):
    ar, ab = name_ar(name, accent, heart_dot)
    la, lb = K.text("Qadam Alkhair", K.LA_LOC, name)
    ih = H - 2 * pad
    ar_h = ih * 0.36
    s_ar = ar_h / (ab[3] - ab[1]); ar_w = (ab[2] - ab[0]) * s_ar
    s_la = ar_w / (lb[2] - lb[0]); la_h = (lb[3] - lb[1]) * s_la
    gap_t, gap_i = ar_h * 0.24, ih * 0.14
    _, iw = icon_at(fn, bbox, 0, 0, ih)
    W = pad + ar_w + gap_i + iw + pad
    top = (H - (ar_h + gap_t + la_h)) / 2
    a, _ = K.put(ar, ab, pad, top, s_ar)
    l, _ = K.put(la, lb, pad, top + ar_h + gap_t, s_la)
    ic, _ = icon_at(fn, bbox, W - pad - iw, pad, ih)
    return K.svg(W, H, a + l + ic, bg)


def stacked(fn, bbox, name=K.C["green"], accent=K.C["gold"], bg=None, Wd=520, pad=44, heart_dot=True):
    ar, ab = name_ar(name, accent, heart_dot)
    la, lb = K.text("Qadam Alkhair", K.LA_LOC, name)
    ih = Wd * 0.42
    _, iw = icon_at(fn, bbox, 0, 0, ih)
    ic, _ = icon_at(fn, bbox, (Wd - iw) / 2, pad, ih)
    s_ar = (Wd * 0.68) / (ab[2] - ab[0])
    a, abox = K.put(ar, ab, Wd / 2, pad + ih + ih * 0.12, s_ar, "center")
    s_la = (abox[2] - abox[0]) / (lb[2] - lb[0])
    l, lbox = K.put(la, lb, Wd / 2, abox[3] + (abox[3] - abox[1]) * 0.24, s_la, "center")
    return K.svg(Wd, lbox[3] + pad, ic + a + l, bg)
