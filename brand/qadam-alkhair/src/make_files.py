# -*- coding: utf-8 -*-
"""Compose every deliverable of the Qadam Alkhair logo system."""
import os
import build as B
from build import C, MARK_INK, svg, write
from textpath import shape_to_path

AR_TEXT, LA_TEXT = "قدم الخير", "QADAM ALKHAIR"

def mark_variant(uid, style):
    if style == "color":
        return B.mark(uid, None, C["gold"], C["gold"], (C["green_lt"], C["green_dk"]))
    if style == "on_dark":
        return B.mark(uid, C["white"], C["gold_lt"], C["gold_lt"])
    if style == "mono_ink":
        return B.mark(uid, C["ink"], C["ink"], C["ink"])
    if style == "mono_white":
        return B.mark(uid, C["white"], C["white"], C["white"])
    if style == "mono_green":
        return B.mark(uid, C["green"], C["green"], C["green"])
    raise ValueError(style)


def words(size_ar, size_la, tracking=None):
    """Arabic wordmark + Latin line; the Latin is tracked out to the Arabic width."""
    ar = shape_to_path(B.FONT_AR, AR_TEXT, size=size_ar)
    if tracking is not None:
        return ar, shape_to_path(B.FONT_LA, LA_TEXT, size=size_la, tracking=tracking)
    target = ar["bbox"][2] - ar["bbox"][0]
    lo, hi = 0.0, 60.0
    for _ in range(40):                     # solve tracking so both lines share a width
        mid = (lo + hi) / 2
        la = shape_to_path(B.FONT_LA, LA_TEXT, size=size_la, tracking=mid)
        w = la["bbox"][2] - la["bbox"][0]
        lo, hi = (mid, hi) if w < target else (lo, mid)
    return ar, shape_to_path(B.FONT_LA, LA_TEXT, size=size_la, tracking=(lo + hi) / 2)


def put(res, x, y, fill, align="left"):
    x0, _, x1, _ = res["bbox"]
    dx = x - (x0 if align == "left" else x1)
    return f'<g transform="translate({dx:.2f} {y:.2f})"><path d="{res["d"]}" fill="{fill}"/></g>'


def mark_at(uid, style, x, y, h):
    """Place the mark so its INK box sits at (x, y) with height h."""
    s = h / (MARK_INK[3] - MARK_INK[1])
    defs, body = mark_variant(uid, style)
    g = (f'<g transform="translate({x - MARK_INK[0]*s:.2f} {y - MARK_INK[1]*s:.2f}) '
         f'scale({s:.5f})">{body}</g>')
    return defs, g


# ----------------------------------------------------------------- lockups ---
def horizontal(uid, style, ar_fill, la_fill, bg=None, rtl=False):
    ar, la = words(92, 24)
    ar_w = ar["bbox"][2] - ar["bbox"][0]
    la_w = la["bbox"][2] - la["bbox"][0]
    text_w = max(ar_w, la_w)
    mark_h, gap, pad = 140, 44, 32
    mark_w = mark_h * (MARK_INK[2] - MARK_INK[0]) / (MARK_INK[3] - MARK_INK[1])
    W = pad + mark_w + gap + text_w + pad
    H = 230
    ar_base = 124          # baseline of the Arabic line
    la_base = 184          # baseline of the Latin line
    mark_y = (H - mark_h) / 2
    if rtl:
        mx = W - pad - mark_w
        tx = W - pad - mark_w - gap
        align = "right"
    else:
        mx, tx, align = pad, pad + mark_w + gap, "left"
    defs, g = mark_at(uid, style, mx, mark_y, mark_h)
    body = g + put(ar, tx, ar_base, ar_fill, align) + put(la, tx, la_base, la_fill, align)
    return svg(round(W), H, defs, body, bg)


def stacked(uid, style, ar_fill, la_fill, bg=None):
    ar, la = words(80, 21)
    ar_w = ar["bbox"][2] - ar["bbox"][0]
    la_w = la["bbox"][2] - la["bbox"][0]
    mark_h = 160
    mark_w = mark_h * (MARK_INK[2] - MARK_INK[0]) / (MARK_INK[3] - MARK_INK[1])
    W = round(max(mark_w, ar_w, la_w) + 90)
    H = 394
    defs, g = mark_at(uid, style, (W - mark_w) / 2, 40, mark_h)
    ar_base, la_base = 300, 354
    body = (g
            + put(ar, (W - ar_w) / 2, ar_base, ar_fill)
            + put(la, (W - la_w) / 2, la_base, la_fill))
    return svg(W, H, defs, body, bg)


def wordmark_only(uid, ar_fill, la_fill, bg=None):
    ar, la = words(104, 27)
    ar_w = ar["bbox"][2] - ar["bbox"][0]
    la_w = la["bbox"][2] - la["bbox"][0]
    W = round(max(ar_w, la_w) + 60)
    H = 236
    body = (put(ar, (W - ar_w) / 2, 120, ar_fill)
            + put(la, (W - la_w) / 2, 192, la_fill))
    return svg(W, H, "", body, bg)


def icon_tile(uid, radius=112, bg=C["green"], style="on_dark"):
    """App icon: rounded square, mark knocked out in white + gold."""
    defs, g = mark_at(uid, style, 125, 121, 270)
    body = (f'<rect width="512" height="512" rx="{radius}" fill="{bg}"/>' + g)
    extra = (f'<linearGradient id="bg{uid}" x1="0" y1="0" x2="512" y2="512" '
             f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{C["green_lt"]}"/>'
             f'<stop offset="1" stop-color="{C["green_dk"]}"/></linearGradient>')
    body = body.replace(f'fill="{bg}"/>', f'fill="url(#bg{uid})"/>', 1)
    return svg(512, 512, defs + extra, body)


def favicon(uid):
    """Tight-cropped mark for tiny sizes."""
    pad = 6
    s = (64 - 2 * pad) / (MARK_INK[3] - MARK_INK[1])
    defs, body = mark_variant(uid, "color")
    w = (MARK_INK[2] - MARK_INK[0]) * s
    g = (f'<g transform="translate({(64 - w)/2 - MARK_INK[0]*s:.2f} {pad - MARK_INK[1]*s:.2f}) '
         f'scale({s:.5f})">{body}</g>')
    return svg(64, 64, defs, g)


def mark_file(uid, style, bg=None):
    defs, body = mark_variant(uid, style)
    return svg(200, 200, defs, body, bg)


ALTS = {"wheat": B.mark_wheat, "word": B.mark_word, "sprout": B.mark_sprout,
        "heart": B.mark_heart}


def alt_file(uid, kind, bg=None):
    defs, body = ALTS[kind](uid, None, C["gold"], (C["green_lt"], C["green_dk"]))
    return svg(200, 200, defs, body, bg)


FILES = {
    "logo/qadam-mark.svg":                 lambda: mark_file("m1", "color"),
    "logo/qadam-mark-mono-ink.svg":        lambda: mark_file("m2", "mono_ink"),
    "logo/qadam-mark-mono-white.svg":      lambda: mark_file("m3", "mono_white"),
    "logo/qadam-mark-mono-green.svg":      lambda: mark_file("m4", "mono_green"),
    "logo/qadam-mark-on-dark.svg":         lambda: mark_file("m5", "on_dark"),
    "logo/qadam-logo-horizontal.svg":      lambda: horizontal("h1", "color", C["ink"], C["green"]),
    "logo/qadam-logo-horizontal-rtl.svg":  lambda: horizontal("h2", "color", C["ink"], C["green"], rtl=True),
    "logo/qadam-logo-horizontal-dark.svg": lambda: horizontal("h3", "on_dark", C["white"], C["gold_lt"], bg=C["ink"]),
    "logo/qadam-logo-horizontal-mono-white.svg": lambda: horizontal("h4", "mono_white", C["white"], C["white"]),
    "logo/qadam-logo-horizontal-mono-ink.svg":   lambda: horizontal("h5", "mono_ink", C["ink"], C["ink"]),
    "logo/qadam-logo-stacked.svg":         lambda: stacked("s1", "color", C["ink"], C["green"]),
    "logo/qadam-logo-stacked-dark.svg":    lambda: stacked("s2", "on_dark", C["white"], C["gold_lt"], bg=C["ink"]),
    "logo/qadam-wordmark.svg":             lambda: wordmark_only("w1", C["ink"], C["green"]),
    "logo/qadam-app-icon.svg":             lambda: icon_tile("a1"),
    "logo/qadam-favicon.svg":              lambda: favicon("f1"),
    "logo/qadam-alt-wheat.svg":            lambda: alt_file("b1", "wheat"),
    "logo/qadam-alt-word.svg":             lambda: alt_file("c1", "word"),
    "logo/qadam-alt-sprout.svg":           lambda: alt_file("d1", "sprout"),
    "logo/qadam-alt-heart.svg":            lambda: alt_file("e1", "heart"),
}

if __name__ == "__main__":
    for name, fn in FILES.items():
        write(name, fn())
