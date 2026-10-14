# -*- coding: utf-8 -*-
"""Qadam Alkhair (قدم الخير) — «خطوات الخير» logo kit.

Two footsteps walking forward — up and to the left, the way Arabic reads —
toward the name. The leading step is gold: the step that brings the good.
"""
import os
import glyphs as G
import foot as F

OUT = os.environ.get("OUT", "kit")
FONT = "fonts/ElMessiri[wght].ttf"
AR_LOC, LA_LOC = {"wght": 700}, {"wght": 600}

C = {
    "green": "#0A5440",     # the name
    "step": "#0F7B5A",      # the back step, green backgrounds
    "gold": "#E3A42B",      # the leading step
    "gold_lt": "#F6CB6B",   # the leading step on dark / green
    "ink": "#12241F",
    "cream": "#FBF7EF",
    "white": "#FFFFFF",
}
ICON_BBOX = (26.97, 10.13, 171.51, 190.63)      # measured in the browser (getBBox)


def icon(x, y, h, back, lead):
    """Place the steps so their ink box starts at (x, y) and is h tall."""
    x0, y0, x1, y1 = ICON_BBOX
    s = h / (y1 - y0)
    g = (f'<g transform="translate({x - x0 * s:.2f} {y - y0 * s:.2f}) scale({s:.4f})">'
         f'{F.pair(back, lead)}</g>')
    return g, (x1 - x0) * s


def text(t, loc, ink):
    g, _ = G.shape(FONT, t, 100, loc)
    return f'<path d="{G.path_of(g)}" fill="{ink}"/>', G.bbox_of(g)


def put(markup, bbox, x, y, s, anchor="left"):
    x0, y0, x1, y1 = bbox
    w = (x1 - x0) * s
    left = {"left": x, "center": x - w / 2, "right": x - w}[anchor]
    return (f'<g transform="translate({left - x0 * s:.2f} {y - y0 * s:.2f}) scale({s:.4f})">{markup}</g>',
            (left, y, left + w, y + (y1 - y0) * s))


def svg(w, h, body, bg=None):
    b = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
            f'height="{h:.0f}" role="img">\n<title>قدم الخير — Qadam Alkhair</title>\n{b}{body}\n</svg>\n')


# ------------------------------------------------------------------ layouts ---
def horizontal(name, back, lead, bg=None, H=240, pad=40):
    """Icon on the right (where Arabic starts), name block to its left."""
    ar, ab = text("قدم الخير", AR_LOC, name)
    la, lb = text("Qadam Alkhair", LA_LOC, name)
    ih = H - 2 * pad
    ar_h = ih * 0.40
    s_ar = ar_h / (ab[3] - ab[1])
    ar_w = (ab[2] - ab[0]) * s_ar
    s_la = ar_w / (lb[2] - lb[0])
    la_h = (lb[3] - lb[1]) * s_la
    gap_t = ar_h * 0.24
    gap_i = ih * 0.16
    _, iw = icon(0, 0, ih, back, lead)
    Wd = pad + ar_w + gap_i + iw + pad
    top = (H - (ar_h + gap_t + la_h)) / 2
    a, _ = put(ar, ab, pad, top, s_ar)
    l, _ = put(la, lb, pad, top + ar_h + gap_t, s_la)
    ic, _ = icon(Wd - pad - iw, pad, ih, back, lead)
    return svg(Wd, H, a + l + ic, bg)


def stacked(name, back, lead, bg=None, Wd=520, pad=44):
    ar, ab = text("قدم الخير", AR_LOC, name)
    la, lb = text("Qadam Alkhair", LA_LOC, name)
    ih = Wd * 0.40
    _, iw = icon(0, 0, ih, back, lead)
    ic, _ = icon((Wd - iw) / 2, pad, ih, back, lead)
    s_ar = (Wd * 0.68) / (ab[2] - ab[0])
    a, abox = put(ar, ab, Wd / 2, pad + ih + ih * 0.12, s_ar, "center")
    s_la = (abox[2] - abox[0]) / (lb[2] - lb[0])
    l, lbox = put(la, lb, Wd / 2, abox[3] + (abox[3] - abox[1]) * 0.24, s_la, "center")
    return svg(Wd, lbox[3] + pad, ic + a + l, bg)


def wordmark(which, ink, Wd=640, pad=40):
    m, b = text("قدم الخير", AR_LOC, ink) if which == "ar" else text("Qadam Alkhair", LA_LOC, ink)
    s = (Wd - 2 * pad) / (b[2] - b[0])
    g, box = put(m, b, Wd / 2, pad, s, "center")
    return svg(Wd, box[3] + pad, g)


def mark(back, lead, S=200, pad=14):
    x0, y0, x1, y1 = ICON_BBOX
    h = S - 2 * pad
    w = (x1 - x0) * h / (y1 - y0)
    g, _ = icon((S - w) / 2, pad, h, back, lead)
    return svg(S, S, g)


def badge(back, lead, bg, shape="circle", S=512, frac=0.62):
    x0, y0, x1, y1 = ICON_BBOX
    h = S * frac
    w = (x1 - x0) * h / (y1 - y0)
    g, _ = icon((S - w) / 2, (S - h) / 2, h, back, lead)
    base = (f'<circle cx="{S / 2}" cy="{S / 2}" r="{S / 2}" fill="{bg}"/>' if shape == "circle"
            else f'<rect width="{S}" height="{S}" rx="{S * (0.22 if S > 100 else 0.24):.1f}" fill="{bg}"/>')
    return svg(S, S, base + g)


FILES = {
    "logo/qadam-logo.svg":                 lambda: horizontal(C["green"], C["step"], C["gold"]),
    "logo/qadam-logo-stacked.svg":         lambda: stacked(C["green"], C["step"], C["gold"]),
    "logo/qadam-logo-dark.svg":            lambda: horizontal(C["cream"], C["cream"], C["gold_lt"], bg=C["ink"]),
    "logo/qadam-logo-stacked-dark.svg":    lambda: stacked(C["cream"], C["cream"], C["gold_lt"], bg=C["ink"]),
    "logo/qadam-logo-on-green.svg":        lambda: horizontal(C["white"], C["white"], C["gold_lt"], bg=C["step"]),
    "logo/qadam-logo-mono-ink.svg":        lambda: horizontal(C["ink"], C["ink"], C["ink"]),
    "logo/qadam-logo-mono-white.svg":      lambda: horizontal(C["white"], C["white"], C["white"]),
    "logo/qadam-wordmark-ar.svg":          lambda: wordmark("ar", C["green"]),
    "logo/qadam-wordmark-en.svg":          lambda: wordmark("la", C["green"]),
    "logo/qadam-mark.svg":                 lambda: mark(C["step"], C["gold"]),
    "logo/qadam-icon.svg":                 lambda: badge(C["white"], C["gold_lt"], C["step"], "circle"),
    "logo/qadam-app-icon.svg":             lambda: badge(C["white"], C["gold_lt"], C["step"], "square"),
    "logo/qadam-favicon.svg":              lambda: badge(C["white"], C["gold_lt"], C["step"], "square", S=64, frac=0.80),
}

if __name__ == "__main__":
    for name, fn in FILES.items():
        p = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(fn())
        print("wrote", p)
