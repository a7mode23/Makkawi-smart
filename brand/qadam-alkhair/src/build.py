# -*- coding: utf-8 -*-
"""Geometry for the Qadam Alkhair (قدم الخير) logo system.

The mark: a ring that reads as the Latin Q and as the cup of the Arabic ق,
holding an open hand that offers a heart — العطاء، وهو الخير.
The gold leaf is the tail of the Q.
"""
import os

OUT = os.environ.get("OUT", "out")
FONT_AR = "fonts/Tajawal-ExtraBold.ttf"
FONT_LA = "fonts/Tajawal-Bold.ttf"

C = {
    "green":    "#0F7B5A",
    "green_lt": "#159A6F",
    "green_dk": "#0A5440",
    "gold":     "#E3A42B",
    "gold_lt":  "#F6CB6B",
    "ink":      "#12241F",
    "cream":    "#FBF7EF",
    "white":    "#FFFFFF",
}

# ---------------------------------------------------------------- geometry ---
RING = dict(cx=100, cy=102, r=52, w=21)
SHIFT = "translate(-2 0)"
LEAF_T = "matrix(0.70711 0.70711 0.70711 -0.70711 124 140)"
LEAF_D = ("M58,0 C45,6.4 27,10 6,10 C-4.2,10 -9.5,5.6 -9.5,0 "
          "C-9.5,-5.6 -4.2,-10 6,-10 C27,-10 45,-6.4 58,0 Z")
LEAFSHAPE = "M0,0 C11,-4 23,-13 26,-27 C12,-26 2,-16 0,-3 Z"
HEART = ("M0,15 C-16,4 -22,-5 -22,-13 C-22,-21 -16,-26 -9,-26 C-4.5,-26 -1,-23 0,-19.5 "
         "C1,-23 4.5,-26 9,-26 C16,-26 22,-21 22,-13 C22,-5 16,4 0,15 Z")
# ink box of the primary mark inside its 200x200 box
INNER = 0.85        # how much of the counter the hand fills
MARK_INK = (27.0, 27.0, 172.9, 172.9)


def _grad(uid, a, b):
    return (f'<linearGradient id="g{uid}" x1="24" y1="40" x2="168" y2="180" '
            f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="1" stop-color="{b}"/></linearGradient>')


def _tail_mask(uid, d=LEAF_D, t=LEAF_T, grow=9):
    return (f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">'
            f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
            f'<g transform="{t}"><path d="{d}" fill="#000" stroke="#000" stroke-width="{grow}" '
            f'stroke-linejoin="round"/></g></mask>')


def _ring(uid, fill, mask=True):
    m = f' mask="url(#m{uid})"' if mask else ""
    return (f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="{RING["r"]}" fill="none" '
            f'stroke="{fill}" stroke-width="{RING["w"]}"{m}/>')


def _tail(fill):
    return f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="{fill}"/></g>'


def _open(uid, ring_fill, gradient):
    defs = []
    if gradient:
        defs.append(_grad(uid, *gradient))
        ring_fill = f"url(#g{uid})"
    return defs, ring_fill


# ------------------------------------------------------------ the mark -------
# ---------------------------------------------------------- primary mark ---
# One solid Q. Its counter is an open hand (negative space) holding a heart;
# the tail cuts into the bowl like a typographic Q. One form, one accent.
import math as _m

Q_C = (98, 96)            # bowl centre
Q_R = 66                  # bowl radius
Q_TAIL = (52, 96, 24)     # tail: from radius, to radius, width
Q_GAP = 5                 # knockout between the tail and the bowl / hand
HAND_AT = (97, 98)
HAND_TILT = -38
HAND_K = 1.0
HEART_S = 0.62
PRIMARY_SHIFT = "translate(-5 -3)"
A45 = 0.70711

# hand in a local frame: palm centre at (0,0), fingers up
_FINGERS = [((-19.5, -15), 30, -8), ((-6.5, -17), 37, -2.5),
            ((6.5, -16.5), 35, 2.5), ((19.5, -13), 26, 8)]
_FINGER_W = 12.6
_THUMB = ((-22, 8), 24, -40)
_THUMB_W = 13.6
_PALM = (-26.5, -22, 53, 50, 19)


def _seg(p1, p2, w, fill):
    return (f'<path d="M{p1[0]:.2f},{p1[1]:.2f} L{p2[0]:.2f},{p2[1]:.2f}" stroke="{fill}" '
            f'stroke-width="{w}" stroke-linecap="round" fill="none"/>')


def _tip(base, length, ang):
    a = _m.radians(ang)
    return (base[0] + length * _m.sin(a), base[1] - length * _m.cos(a))


def hand_shape(fill="#000"):
    x, y, w, h, rx = _PALM
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>']
    parts += [_seg(b, _tip(b, l, a), _FINGER_W, fill) for b, l, a in _FINGERS]
    b, l, a = _THUMB
    parts.append(_seg(b, _tip(b, l, a), _THUMB_W, fill))
    return "".join(parts)


def _heart_in_palm(fill, s=HEART_S):
    return (f'<g transform="translate(0 {3 + 4 * s:.2f}) scale({s})">'
            f'<path d="{HEART}" fill="{fill}"/></g>')


def mark(uid, form_fill, heart_fill, gradient=None, hand=True):
    """Primary mark in a 200x200 box.

    form_fill  colour of the Q (ignored when `gradient` is given)
    heart_fill colour of the heart
    hand=False gives the small-size version: the counter is the heart itself.
    """
    defs = []
    if gradient:
        defs.append(_grad(uid, *gradient))
        form_fill = f"url(#g{uid})"
    cx, cy = Q_C
    t_in, t_out, t_w = Q_TAIL
    e0 = (cx + t_in * A45, cy + t_in * A45)
    e1 = (cx + t_out * A45, cy + t_out * A45)
    T = f'translate({HAND_AT[0]} {HAND_AT[1]}) rotate({HAND_TILT}) scale({HAND_K})'
    if hand:
        counter = f'<g transform="{T}">{hand_shape("#000")}</g>'
        guard = (f'<g transform="{T}" stroke="#000" stroke-width="{2 * Q_GAP / HAND_K:.1f}" '
                 f'stroke-linejoin="round" stroke-linecap="round">{hand_shape("#000")}</g>')
        inner = f'<g transform="{T}">{_heart_in_palm(heart_fill)}</g>'
    else:
        hs = 1.55
        counter = (f'<g transform="translate({cx} {cy + 4}) scale({hs})">'
                   f'<path d="{HEART}" fill="#000"/></g>')
        guard = ""
        inner = ""
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="-60" y="-60" width="320" height="320">'
        f'<rect x="-60" y="-60" width="320" height="320" fill="#fff"/>{counter}'
        + _seg(e0, e1, t_w + 2 * Q_GAP, "#000") + '</mask>')
    defs.append(
        f'<mask id="t{uid}" maskUnits="userSpaceOnUse" x="-60" y="-60" width="320" height="320">'
        f'<rect x="-60" y="-60" width="320" height="320" fill="#fff"/>{guard}</mask>')
    body = (f'<g transform="{PRIMARY_SHIFT}">'
            f'<circle cx="{cx}" cy="{cy}" r="{Q_R}" fill="{form_fill}" mask="url(#m{uid})"/>'
            f'<g mask="url(#t{uid})">{_seg(e0, e1, t_w, form_fill)}</g>{inner}</g>')
    return "\n".join(defs), body


# ------------------------------------------------------- alternate concepts ---
def mark_wheat(uid, ring_fill, grain_fill, gradient=None):
    """Alternate: the tail of the Q is an ear of wheat — رزق."""
    defs, ring_fill = _open(uid, ring_fill, gradient)
    t = "matrix(0.70711 0.70711 0.70711 -0.70711 122 138)"
    defs.append(_tail_mask(uid, d="M-16,0 L74,0", t=t, grow=46))
    grain = "M0,0 C10,-6.5 23,-5 29,0 C23,5 10,6.5 0,0 Z"
    g = []
    for x, sc in [(8, 1.0), (22, 0.94), (35, 0.86), (47, 0.76)]:
        g.append(f'<g transform="translate({x} 4) rotate(30) scale({sc})">'
                 f'<path d="{grain}" fill="{grain_fill}"/></g>')
        g.append(f'<g transform="translate({x} -4) rotate(-30) scale({sc})">'
                 f'<path d="{grain}" fill="{grain_fill}"/></g>')
    g.append(f'<g transform="translate(62 0) scale(0.8)"><path d="{grain}" fill="{grain_fill}"/></g>')
    spike = (f'<g transform="{t}"><path d="M-14,0 L34,0" stroke="{grain_fill}" stroke-width="8" '
             f'stroke-linecap="round"/>{"".join(g)}</g>')
    return "\n".join(defs), f'<g transform="translate(-4 -2)">{_ring(uid, ring_fill)}{spike}</g>'


def mark_word(uid, ring_fill, word_fill, gradient=None):
    """Alternate: the word «خير» sits inside the ring."""
    from textpath import shape_to_path
    defs, ring_fill = _open(uid, ring_fill, gradient)
    defs.append(_tail_mask(uid))
    w = shape_to_path(FONT_AR, "خير", size=100)
    x0, y0, x1, y1 = w["bbox"]
    sc = 62 / (x1 - x0)
    tx = RING["cx"] - (x0 + x1) / 2 * sc
    ty = RING["cy"] - (y0 + y1) / 2 * sc
    body = (f'<g transform="{SHIFT}">{_ring(uid, ring_fill)}'
            f'<g transform="translate({tx:.2f} {ty:.2f}) scale({sc:.4f})">'
            f'<path d="{w["d"]}" fill="{word_fill}"/></g>{_tail(word_fill)}</g>')
    return "\n".join(defs), body


def mark_sprout(uid, ring_fill, leaf_fill, gradient=None):
    """Alternate: a seedling grows out of the Q — النماء."""
    defs, ring_fill = _open(uid, ring_fill, gradient)
    defs.append(_tail_mask(uid))
    body = (f'<g transform="{SHIFT}">{_ring(uid, ring_fill)}'
            f'<path d="M100,60 C100,48 100,42 100,34" stroke="{ring_fill}" stroke-width="8.5" '
            f'stroke-linecap="round" fill="none"/>'
            f'<g transform="translate(99 38) rotate(4) scale(1.28)">'
            f'<path d="{LEAFSHAPE}" fill="{leaf_fill}"/></g>'
            f'<g transform="translate(101 38) rotate(-4) scale(-1.28 1.28)">'
            f'<path d="{LEAFSHAPE}" fill="{leaf_fill}"/></g>{_tail(leaf_fill)}</g>')
    return "\n".join(defs), body


def mark_heart(uid, disc_fill, tail_fill, gradient=None):
    """Alternate: a solid Q whose counter is a heart."""
    defs, disc_fill = _open(uid, disc_fill, gradient)
    tail_d = "M-12,0 L54,0"
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="translate(99 113) scale(1.1)"><path d="{HEART}" fill="#000"/></g>'
        f'<g transform="{LEAF_T}"><path d="{tail_d}" stroke="#000" stroke-width="30" '
        f'stroke-linecap="round"/></g></mask>')
    body = (f'<g transform="{SHIFT}">'
            f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="62.5" fill="{disc_fill}" '
            f'mask="url(#m{uid})"/>'
            f'<g transform="{LEAF_T}"><path d="{tail_d}" stroke="{tail_fill}" stroke-width="20" '
            f'stroke-linecap="round"/></g></g>')
    return "\n".join(defs), body


# ------------------------------------------------------------------ output ---
def svg(w, h, defs, body, bg=None):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img">\n'
            f'<title>قدم الخير — Qadam Alkhair</title>\n'
            f'<defs>\n{defs}\n</defs>\n{bgr}\n{body}\n</svg>\n')


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path, len(content))
