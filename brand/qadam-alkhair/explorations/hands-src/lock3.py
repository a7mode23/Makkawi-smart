# -*- coding: utf-8 -*-
"""Lockups for any icon function with a measured ink box."""
import kit as K


def icon_at(fn, bbox, x, y, h, **kw):
    x0, y0, x1, y1 = bbox
    s = h / (y1 - y0)
    return (f'<g transform="translate({x - x0 * s:.2f} {y - y0 * s:.2f}) scale({s:.4f})">{fn(**kw)}</g>',
            (x1 - x0) * s)


def horizontal(fn, bbox, name=K.C["green"], bg=None, H=240, pad=36, **kw):
    ar, ab = K.text("قدم الخير", K.AR_LOC, name)
    la, lb = K.text("Qadam Alkhair", K.LA_LOC, name)
    ih = H - 2 * pad
    ar_h = ih * 0.36
    s_ar = ar_h / (ab[3] - ab[1]); ar_w = (ab[2] - ab[0]) * s_ar
    s_la = ar_w / (lb[2] - lb[0]); la_h = (lb[3] - lb[1]) * s_la
    gap_t, gap_i = ar_h * 0.24, ih * 0.14
    _, iw = icon_at(fn, bbox, 0, 0, ih, **kw)
    W = pad + ar_w + gap_i + iw + pad
    top = (H - (ar_h + gap_t + la_h)) / 2
    a, _ = K.put(ar, ab, pad, top, s_ar); l, _ = K.put(la, lb, pad, top + ar_h + gap_t, s_la)
    ic, _ = icon_at(fn, bbox, W - pad - iw, pad, ih, **kw)
    return K.svg(W, H, a + l + ic, bg)


def stacked(fn, bbox, name=K.C["green"], bg=None, Wd=520, pad=44, **kw):
    ar, ab = K.text("قدم الخير", K.AR_LOC, name)
    la, lb = K.text("Qadam Alkhair", K.LA_LOC, name)
    ih = Wd * 0.42
    _, iw = icon_at(fn, bbox, 0, 0, ih, **kw)
    ic, _ = icon_at(fn, bbox, (Wd - iw) / 2, pad, ih, **kw)
    s_ar = (Wd * 0.68) / (ab[2] - ab[0])
    a, abox = K.put(ar, ab, Wd / 2, pad + ih + ih * 0.12, s_ar, "center")
    s_la = (abox[2] - abox[0]) / (lb[2] - lb[0])
    l, lbox = K.put(la, lb, Wd / 2, abox[3] + (abox[3] - abox[1]) * 0.24, s_la, "center")
    return K.svg(Wd, lbox[3] + pad, ic + a + l, bg)


def badge(fn, bbox, bg, shape="circle", S=512, frac=0.64, cap=0.70, **kw):
    x0, y0, x1, y1 = bbox
    h = S * frac
    w = (x1 - x0) * h / (y1 - y0)
    if w > S * cap:
        h *= S * cap / w
        w = S * cap
    g, _ = icon_at(fn, bbox, (S - w) / 2, (S - h) / 2, h, **kw)
    base = (f'<circle cx="{S / 2}" cy="{S / 2}" r="{S / 2}" fill="{bg}"/>' if shape == "circle"
            else f'<rect width="{S}" height="{S}" rx="{S * (0.22 if S > 100 else 0.24):.1f}" fill="{bg}"/>')
    return K.svg(S, S, base + g)


def mark(fn, bbox, S=200, pad=12, **kw):
    x0, y0, x1, y1 = bbox
    h = S - 2 * pad
    w = (x1 - x0) * h / (y1 - y0)
    if w > S - 2 * pad:
        h *= (S - 2 * pad) / w
        w = S - 2 * pad
    g, _ = icon_at(fn, bbox, (S - w) / 2, (S - h) / 2, h, **kw)
    return K.svg(S, S, g)
