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
RING = dict(cx=100, cy=112, r=52, w=21)
SHIFT = "translate(-2 0)"
LEAF_T = "matrix(0.70711 0.70711 0.70711 -0.70711 124 140)"
LEAF_D = ("M58,0 C45,6.4 27,10 6,10 C-4.2,10 -9.5,5.6 -9.5,0 "
          "C-9.5,-5.6 -4.2,-10 6,-10 C27,-10 45,-6.4 58,0 Z")
LEAFSHAPE = "M0,0 C11,-4 23,-13 26,-27 C12,-26 2,-16 0,-3 Z"
HEART = ("M0,15 C-16,4 -22,-5 -22,-13 C-22,-21 -16,-26 -9,-26 C-4.5,-26 -1,-23 0,-19.5 "
         "C1,-23 4.5,-26 9,-26 C16,-26 22,-21 22,-13 C22,-5 16,4 0,15 Z")
# ink box of the primary mark inside its 200x200 box
INNER = 0.85        # how much of the counter the hand fills
MARK_INK = (35.5, 49.5, 163.0, 181.0)


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
def _cap(x1, y1, x2, y2, w, fill):
    return (f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{fill}" stroke-width="{w}" '
            f'stroke-linecap="round" fill="none"/>')


def mark(uid, ring_fill, hand_fill, heart_fill=None, gradient=None, hand=True):
    """Primary: an open hand carrying a heart in its palm, inside the Q.

    The heart is knocked out of the hand, so it reads on any background and in
    one colour. `hand=False` gives the simplified small-size mark (heart only).
    """
    defs, ring_fill = _open(uid, ring_fill, gradient)
    defs.append(_tail_mask(uid))
    heart_at = ('<g transform="translate(48 57) scale({s})">'
                '<path d="' + HEART + '" fill="{f}"/></g>')
    if hand:
        fingers = "".join(_cap(x, 52, x, top, 13, hand_fill) for x, top in
                          [(26, 16), (41, 6), (56, 11), (71, 24)])
        palm = f'<rect x="19" y="34" width="59" height="46" rx="20" fill="{hand_fill}"/>'
        thumb = _cap(26, 56, 6, 44, 13, hand_fill)
        defs.append(
            f'<mask id="p{uid}" maskUnits="userSpaceOnUse" x="-40" y="-40" width="280" height="280">'
            f'<rect x="-40" y="-40" width="280" height="280" fill="#fff"/>'
            + heart_at.format(s=0.70, f="#000") + '</mask>')
        inner = f'<g mask="url(#p{uid})">{fingers}{thumb}{palm}</g>'
        if heart_fill:
            inner += heart_at.format(s=0.58, f=heart_fill)
        g = (f'<g transform="translate(98 112) rotate(-15) scale(0.70) translate(-48 -46)">'
             f'{inner}</g>')
    else:
        g = (f'<g transform="translate(98 112) scale(1.25) translate(-48 -57)">'
             + heart_at.format(s=1.0, f=hand_fill) + '</g>')
    return "\n".join(defs), f'<g transform="{SHIFT}">{_ring(uid, ring_fill)}{g}{_tail(hand_fill)}</g>'


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
