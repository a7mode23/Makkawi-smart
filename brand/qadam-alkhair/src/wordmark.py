# -*- coding: utf-8 -*-
"""Qadam Alkhair (قدم الخير) — wordmark logo system.

One idea: the dot of «khair» is a heart, in both scripts — the dot of خ in
«الخير» and the dot of i in «Alkhair». Everything else stays plain type.
"""
import os
import glyphs as G

HEART = ("M0,15 C-16,4 -22,-5 -22,-13 C-22,-21 -16,-26 -9,-26 C-4.5,-26 -1,-23 0,-19.5 C1,-23 4.5,-26 9,-26 C16,-26 22,-21 22,-13 C22,-5 16,4 0,15 Z")

OUT = os.environ.get("OUT", "out2")
FONT = "fonts/ElMessiri[wght].ttf"
AR_LOC = {"wght": 700}
LA_LOC = {"wght": 600}
AR_TEXT, LA_TEXT = "قدم الخير", "Qadam Alkhair"

C = {
    "green":    "#0A5440",   # ink of the name
    "green_md": "#0F7B5A",
    "green_lt": "#159A6F",
    "gold":     "#E3A42B",   # the heart — the only accent
    "gold_lt":  "#F6CB6B",
    "ink":      "#12241F",
    "cream":    "#FBF7EF",
    "white":    "#FFFFFF",
}

HEART_W = 44.0


def heart(bbox, fill, k):
    x0, y0, x1, y1 = bbox
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = (x1 - x0) * k / HEART_W
    return (f'<g transform="translate({cx:.2f} {cy + 5.5 * s:.2f}) scale({s:.4f})">'
            f'<path d="{HEART}" fill="{fill}"/></g>')


def word(text, loc, dot_index, ink, accent, k, font=FONT, where="above"):
    g, _ = G.shape(font, text, 100, loc)
    dot = G.take_dot(g, dot_index, where) if dot_index is not None else None
    m = f'<path d="{G.path_of(g)}" fill="{ink}"/>'
    if dot:
        m += heart(dot, accent, k)
    return m, G.bbox_of(g)


def arabic(ink, accent, font=FONT, loc=AR_LOC, k=None):
    k = k or (1.25 if "Ruqaa" in font else 1.85)
    return word(AR_TEXT, loc, AR_TEXT.index("خ"), ink, accent, k, font)


def latin(ink, accent, font=FONT, loc=LA_LOC, k=2.0):
    return word(LA_TEXT, loc, LA_TEXT.index("i"), ink, accent, k, font)


def place(markup, bbox, x, y, scale, anchor="center"):
    """Put a block so that (anchor point of its bbox) lands on (x, y-top)."""
    x0, y0, x1, y1 = bbox
    w = (x1 - x0) * scale
    if anchor == "center":
        left = x - w / 2
    elif anchor == "right":
        left = x - w
    else:
        left = x
    tx = left - x0 * scale
    ty = y - y0 * scale
    box = (left, y, left + w, y + (y1 - y0) * scale)
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.4f})">{markup}</g>', box


def svg(w, h, body, bg=None, title="قدم الخير — Qadam Alkhair"):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img">\n<title>{title}</title>\n{b}{body}\n</svg>\n')


# ------------------------------------------------------------------ layouts ---
def stacked(ink, accent, bg=None, la_ink=None, font=FONT, ar_loc=AR_LOC, la_font=None,
            la_loc=LA_LOC, W=640, pad=48, la_ratio=0.62, gap=0.20):
    ar, ab = arabic(ink, accent, font, ar_loc)
    la, lb = latin(la_ink or ink, accent, la_font or font, la_loc)
    s_ar = (W - 2 * pad) / (ab[2] - ab[0])
    s_la = (ab[2] - ab[0]) * s_ar * la_ratio / (lb[2] - lb[0])
    a, abox = place(ar, ab, W / 2, pad, s_ar)
    l, lbox = place(la, lb, W / 2, abox[3] + (abox[3] - abox[1]) * gap, s_la)
    return svg(W, lbox[3] + pad, a + l, bg)


def horizontal(ink, accent, bg=None, rule=None, H=200, pad=44):
    ar, ab = arabic(ink, accent)
    la, lb = latin(ink, accent)
    ar_h = H - 2 * pad
    s_ar = ar_h / (ab[3] - ab[1])
    # Latin cap height ~ 46% of the Arabic block
    s_la = ar_h * 0.46 / (lb[3] - lb[1])
    gap = ar_h * 0.36
    la_w = (lb[2] - lb[0]) * s_la
    ar_w = (ab[2] - ab[0]) * s_ar
    W = pad + la_w + gap * 2 + ar_w + pad
    l, lbox = place(la, lb, pad, (H - (lb[3] - lb[1]) * s_la) / 2 - 2, s_la, "left")
    a, abox = place(ar, ab, W - pad, pad, s_ar, "right")
    xr = pad + la_w + gap
    r = (f'<rect x="{xr - 1.25:.2f}" y="{H * 0.30:.1f}" width="2.5" height="{H * 0.40:.1f}" '
         f'rx="1.25" fill="{rule or accent}"/>')
    return svg(W, H, l + r + a, bg)


def single(which, ink, accent, bg=None, W=640, pad=40):
    m, b = (arabic if which == "ar" else latin)(ink, accent)
    s = (W - 2 * pad) / (b[2] - b[0])
    g, box = place(m, b, W / 2, pad, s)
    return svg(W, box[3] + pad, g, bg)


def khair_icon(fg, accent, bg, shape="circle", S=512, frac=0.60, font=FONT, loc=AR_LOC):
    """Avatar / app icon: the word «خير» with its heart dot."""
    m, b = word("خير", loc, 0, fg, accent, 1.9, font)
    s = S * frac / (b[2] - b[0])
    h = (b[3] - b[1]) * s
    g, _ = place(m, b, S / 2, (S - h) / 2 + S * 0.01, s)
    if shape == "circle":
        base = f'<circle cx="{S / 2}" cy="{S / 2}" r="{S / 2}" fill="{bg}"/>'
    else:
        base = f'<rect width="{S}" height="{S}" rx="{S * 0.22:.0f}" fill="{bg}"/>'
    return svg(S, S, base + g)


def favicon(bg, accent, S=64):
    """Below ~32px the letters close up: the favicon is the heart alone."""
    s = S * 0.62 / HEART_W
    return svg(S, S, f'<rect width="{S}" height="{S}" rx="{S * 0.24:.1f}" fill="{bg}"/>'
                     f'<g transform="translate({S / 2} {S / 2 + 5.5 * s:.2f}) scale({s:.4f})">'
                     f'<path d="{HEART}" fill="{accent}"/></g>')


def write(name, content):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)
    print("wrote", p)


if __name__ == "__main__":
    F = "fonts/"
    files = {
        "logo/qadam-logo.svg": stacked(C["green"], C["gold"]),
        "logo/qadam-logo-dark.svg": stacked(C["cream"], C["gold_lt"], bg=C["ink"]),
        "logo/qadam-logo-on-green.svg": stacked(C["white"], C["gold_lt"], bg=C["green_md"]),
        "logo/qadam-logo-mono-ink.svg": stacked(C["ink"], C["ink"]),
        "logo/qadam-logo-mono-white.svg": stacked(C["white"], C["white"]),
        "logo/qadam-logo-horizontal.svg": horizontal(C["green"], C["gold"]),
        "logo/qadam-logo-horizontal-dark.svg": horizontal(C["cream"], C["gold_lt"], bg=C["ink"]),
        "logo/qadam-wordmark-ar.svg": single("ar", C["green"], C["gold"]),
        "logo/qadam-wordmark-en.svg": single("la", C["green"], C["gold"]),
        "logo/qadam-icon.svg": khair_icon(C["white"], C["gold_lt"], C["green_md"], "circle"),
        "logo/qadam-app-icon.svg": khair_icon(C["white"], C["gold_lt"], C["green_md"], "square"),
        "logo/qadam-favicon.svg": favicon(C["green_md"], C["gold_lt"]),
        "logo/qadam-alt-rounded.svg": stacked(C["green"], C["gold"], font=F + "BalooBhaijaan2[wght].ttf",
                                              ar_loc={"wght": 700}, la_loc={"wght": 600}),
        "logo/qadam-alt-ruqaa.svg": stacked(C["green"], C["gold"], font=F + "ArefRuqaa-Bold.ttf",
                                            ar_loc=None, la_font=FONT, la_loc=LA_LOC),
        "logo/qadam-alt-modern.svg": stacked(C["green"], C["gold"], font=F + "ReadexPro[HEXP,wght].ttf",
                                             ar_loc={"wght": 600}, la_loc={"wght": 500}),
    }
    for n, c in files.items():
        write(n, c)
