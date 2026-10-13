# -*- coding: utf-8 -*-
"""Four developments of the «heart dot» wordmark — each as a complete kit.

a-light   القلب يشعّ        the heart gives off light (three rays)
b-wheat   سنبلة + قلب       the lam of «الخير» grows an ear of wheat
c-cradle  حضن تحت الاسم     a calligraphic stroke holds the name from below
d-kashida مدّ + إشعاع        «الخيـر» stretches open, its heart gives off light
"""
import math, os
import glyphs as G
import wordmark as W
from wordmark import C, HEART, heart, place, svg

F, AR, LA = W.FONT, W.AR_LOC, W.LA_LOC
KINDS = {"a-light": "rays", "b-wheat": "wheat", "c-cradle": "cradle", "d-kashida": "kashida rays"}
TITLES = {"a-light": "القلب يشعّ", "b-wheat": "سنبلة وقلب", "c-cradle": "حضن تحت الاسم",
          "d-kashida": "مدّ وإشعاع"}
GRAIN = "M0,0 C4,-2.6 9.5,-2 12,0 C9.5,2 4,2.6 0,0 Z"


def rays(dot, k, fill, n=3, spread=34, r0=1.25, r1=1.85, w=3.2):
    x0, y0, x1, y1 = dot
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = (x1 - x0) * k / 2
    out = []
    for i in range(n):
        a = math.radians(-90 + (i - (n - 1) / 2) * spread)
        p0 = (cx + math.cos(a) * R * r0, cy + math.sin(a) * R * r0)
        p1 = (cx + math.cos(a) * R * r1, cy + math.sin(a) * R * r1)
        out.append(f'<path d="M{p0[0]:.2f},{p0[1]:.2f} L{p1[0]:.2f},{p1[1]:.2f}" stroke="{fill}" '
                   f'stroke-width="{w}" stroke-linecap="round"/>')
    top = cy - R * r1 - w / 2
    return "".join(out), top


def wheat(g, cluster, fill, scale):
    cs = [c for gl in g if gl["cluster"] == cluster for c in gl["contours"]]
    x0, y0, x1, y1 = max(cs, key=lambda c: c["area"])["bbox"]
    cx, top = (x0 + x1) / 2, y0
    parts = []
    for dy, sc in [(10, 1.0), (4, 0.9), (-2, 0.78)]:
        y = top + dy * scale
        for side, rot in ((1, -58), (-1, -122)):
            parts.append(f'<g transform="translate({cx + side * 1.2 * scale:.2f} {y:.2f}) rotate({rot}) '
                         f'scale({sc * scale:.3f})"><path d="{GRAIN}" fill="{fill}"/></g>')
    parts.append(f'<g transform="translate({cx:.2f} {top - 6 * scale:.2f}) rotate(-90) '
                 f'scale({0.7 * scale:.3f})"><path d="{GRAIN}" fill="{fill}"/></g>')
    return "".join(parts), top - 6 * scale - 12 * 0.7 * scale


def cradle_path(L, R, y, fill, h_ratio=0.055):
    w = R - L
    h = w * h_ratio
    d = (f"M{L:.1f},{y:.1f} "
         f"C{L + w * 0.28:.1f},{y + h * 1.9:.1f} {R - w * 0.34:.1f},{y + h * 2.0:.1f} {R:.1f},{y - h * 1.15:.1f} "
         f"C{R - w * 0.30:.1f},{y + h * 1.25:.1f} {L + w * 0.26:.1f},{y + h * 1.15:.1f} {L:.1f},{y:.1f} Z")
    return f'<path d="{d}" fill="{fill}"/>', y + h * 1.75


def arabic(opt, ink, accent, text=None):
    kind = KINDS[opt]
    text = text or ("قدم الخــير" if "kashida" in kind else "قدم الخير")
    g, _ = G.shape(F, text, 100, AR)
    dot = G.take_dot(g, text.index("خ"), "above")
    m = f'<path d="{G.path_of(g)}" fill="{ink}"/>' + heart(dot, accent, 1.85)
    x0, y0, x1, y1 = G.bbox_of(g)
    y0 = min(y0, dot[1] - (dot[2] - dot[0]) * 0.6)
    if "rays" in kind:
        r, top = rays(dot, 1.85, accent)
        m += r
        y0 = min(y0, top)
    if "wheat" in kind and "ل" in text:
        wh, top = wheat(g, text.index("ل"), accent, 2.1)
        m += wh
        y0 = min(y0, top)
    if "cradle" in kind:
        w = x1 - x0
        c, bottom = cradle_path(x0 - w * 0.01, x1 + w * 0.01, y1 + (y1 - y0) * 0.06, accent)
        m += c
        y1 = bottom
    return m, (x0, y0, x1, y1)


def latin(opt, ink, accent):
    kind = KINDS[opt]
    text = "Qadam Alkhair"
    g, _ = G.shape(F, text, 100, LA)
    dot = G.take_dot(g, text.index("i"), "above")
    m = f'<path d="{G.path_of(g)}" fill="{ink}"/>' + heart(dot, accent, 2.0)
    x0, y0, x1, y1 = G.bbox_of(g)
    if "rays" in kind:
        r, top = rays(dot, 2.0, accent, w=3.6)
        m += r
        y0 = min(y0, top)
    return m, (x0, y0, x1, y1)


# ------------------------------------------------------------------ layouts ---
def stacked(opt, ink, accent, bg=None, Wd=640, pad=48):
    ar, ab = arabic(opt, ink, accent)
    la, lb = latin(opt, ink, accent)
    s_ar = (Wd - 2 * pad) / (ab[2] - ab[0])
    s_la = (ab[2] - ab[0]) * s_ar * 0.62 / (lb[2] - lb[0])
    a, abox = place(ar, ab, Wd / 2, pad, s_ar)
    gap = (abox[3] - abox[1]) * (0.12 if "cradle" in KINDS[opt] else 0.20)
    l, lbox = place(la, lb, Wd / 2, abox[3] + gap, s_la)
    return svg(Wd, lbox[3] + pad, a + l, bg)


def horizontal(opt, ink, accent, bg=None, H=210, pad=44):
    ar, ab = arabic(opt, ink, accent)
    la, lb = latin(opt, ink, accent)
    ar_h = H - 2 * pad
    s_ar = ar_h / (ab[3] - ab[1])
    s_la = ar_h * 0.44 / (lb[3] - lb[1])
    gap = ar_h * 0.34
    la_w, ar_w = (lb[2] - lb[0]) * s_la, (ab[2] - ab[0]) * s_ar
    Wd = pad + la_w + 2 * gap + ar_w + pad
    l, _ = place(la, lb, pad, (H - (lb[3] - lb[1]) * s_la) / 2, s_la, "left")
    a, _ = place(ar, ab, Wd - pad, pad, s_ar, "right")
    xr = pad + la_w + gap
    rule = (f'<rect x="{xr - 1.25:.2f}" y="{H * 0.30:.1f}" width="2.5" height="{H * 0.40:.1f}" '
            f'rx="1.25" fill="{accent}"/>')
    return svg(Wd, H, l + rule + a, bg)


def single(opt, which, ink, accent, Wd=640, pad=40):
    m, b = arabic(opt, ink, accent) if which == "ar" else latin(opt, ink, accent)
    s = (Wd - 2 * pad) / (b[2] - b[0])
    g, box = place(m, b, Wd / 2, pad, s)
    return svg(Wd, box[3] + pad, g)


def icon(opt, fg, accent, bg, shape="circle", S=512):
    kind = KINDS[opt]
    word = {"a-light": "خير", "b-wheat": "الخير", "c-cradle": "خير", "d-kashida": "خــير"}[opt]
    m, b = arabic(opt, fg, accent, text=word)
    frac = 0.66 if opt == "b-wheat" else 0.58
    s = min(S * frac / (b[2] - b[0]), S * 0.56 / (b[3] - b[1]))
    h = (b[3] - b[1]) * s
    g, _ = place(m, b, S / 2, (S - h) / 2, s)
    base = (f'<circle cx="{S / 2}" cy="{S / 2}" r="{S / 2}" fill="{bg}"/>' if shape == "circle"
            else f'<rect width="{S}" height="{S}" rx="{S * 0.22:.0f}" fill="{bg}"/>')
    return svg(S, S, base + g)


def favicon(opt, bg, accent, S=64):
    """Below ~32px the letters close up, so the favicon is the heart (with its rays
    for the options that have them)."""
    rays_on = "rays" in KINDS[opt]
    hs = S * (0.50 if rays_on else 0.62) / 44.0
    cx, cy = S / 2, S / 2 + (S * 0.08 if rays_on else 0)
    m = (f'<g transform="translate({cx} {cy + 5.5 * hs:.2f}) scale({hs:.4f})">'
         f'<path d="{HEART}" fill="{accent}"/></g>')
    if rays_on:
        R = 22 * hs
        for i in range(3):
            a = math.radians(-90 + (i - 1) * 36)
            p0 = (cx + math.cos(a) * R * 1.3, cy + math.sin(a) * R * 1.3)
            p1 = (cx + math.cos(a) * R * 1.85, cy + math.sin(a) * R * 1.85)
            m += (f'<path d="M{p0[0]:.2f},{p0[1]:.2f} L{p1[0]:.2f},{p1[1]:.2f}" stroke="{accent}" '
                  f'stroke-width="{S * 0.06:.2f}" stroke-linecap="round"/>')
    return svg(S, S, f'<rect width="{S}" height="{S}" rx="{S * 0.24:.1f}" fill="{bg}"/>' + m)


def kit(opt):
    g, gd, gr = C["green"], C["cream"], C["green_md"]
    return {
        "logo/qadam-logo.svg": stacked(opt, g, C["gold"]),
        "logo/qadam-logo-dark.svg": stacked(opt, gd, C["gold_lt"], bg=C["ink"]),
        "logo/qadam-logo-on-green.svg": stacked(opt, C["white"], C["gold_lt"], bg=gr),
        "logo/qadam-logo-mono-ink.svg": stacked(opt, C["ink"], C["ink"]),
        "logo/qadam-logo-mono-white.svg": stacked(opt, C["white"], C["white"]),
        "logo/qadam-logo-horizontal.svg": horizontal(opt, g, C["gold"]),
        "logo/qadam-logo-horizontal-dark.svg": horizontal(opt, gd, C["gold_lt"], bg=C["ink"]),
        "logo/qadam-wordmark-ar.svg": single(opt, "ar", g, C["gold"]),
        "logo/qadam-wordmark-en.svg": single(opt, "la", g, C["gold"]),
        "logo/qadam-icon.svg": icon(opt, C["white"], C["gold_lt"], gr, "circle"),
        "logo/qadam-app-icon.svg": icon(opt, C["white"], C["gold_lt"], gr, "square"),
        "logo/qadam-favicon.svg": favicon(opt, gr, C["gold_lt"]),
    }


if __name__ == "__main__":
    out = os.environ.get("OUT", "out3")
    for opt in KINDS:
        for name, content in kit(opt).items():
            p = os.path.join(out, opt, name)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(content)
        print("kit", opt)
