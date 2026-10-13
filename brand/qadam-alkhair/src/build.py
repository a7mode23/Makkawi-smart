# -*- coding: utf-8 -*-
"""Generate the Qadam Alkhair (قدم الخير) logo system as static SVG files."""
import os, math
from textpath import shape_to_path

OUT = os.environ.get("OUT", "out")
FONT_AR = "fonts/Tajawal-ExtraBold.ttf"
FONT_LA = "fonts/Tajawal-Bold.ttf"

C = {
    "green":      "#0F7B5A",
    "green_lt":   "#159A6F",
    "green_dk":   "#0A5440",
    "gold":       "#E3A42B",
    "gold_lt":    "#F6CB6B",
    "ink":        "#12241F",
    "cream":      "#FBF7EF",
    "white":      "#FFFFFF",
}

# ---------------------------------------------------------------- the mark ---
# Built in a 200x200 box. Ring = letter Q / bowl of ق. Leaf = Q tail + growth.
# Two seeds above = the two dots of ق + "seeds of khair".
RING = dict(cx=100, cy=102, r=52, w=21)
LEAF_T = "matrix(0.70711 0.70711 0.70711 -0.70711 124 126)"
LEAF_D = ("M58,0 C45,6.4 27,10 6,10 C-4.2,10 -9.5,5.6 -9.5,0 "
          "C-9.5,-5.6 -4.2,-10 6,-10 C27,-10 45,-6.4 58,0 Z")
SEED_D = ("M0,-13 C4.5,-6.5 8,-3.5 8,1.5 C8,6 4.4,9.5 0,9.5 "
          "C-4.4,9.5 -8,6 -8,1.5 C-8,-3.5 -4.5,-6.5 0,-13 Z")
SEED_S = 0.72          # seeds read as the two dots of ق, not as ears
SEED_X = 12.5          # half the distance between the two dots
SEED_Y = 30
MARK_SHIFT = "translate(-3 11)"


def mark(uid, ring_fill, leaf_fill, seed_fill, gradient=None):
    """Return (defs, body) for the mark, drawn inside a 200x200 user space."""
    defs = []
    if gradient:
        defs.append(
            f'<linearGradient id="g{uid}" x1="24" y1="34" x2="168" y2="172" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{gradient[0]}"/>'
            f'<stop offset="1" stop-color="{gradient[1]}"/></linearGradient>')
        ring_fill = f"url(#g{uid})"
    # mask: notch the ring where the leaf crosses it
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="#000" stroke="#000" '
        f'stroke-width="9" stroke-linejoin="round"/></g></mask>')
    body = (
        f'<g transform="{MARK_SHIFT}">'
        f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="{RING["r"]}" fill="none" '
        f'stroke="{ring_fill}" stroke-width="{RING["w"]}" mask="url(#m{uid})"/>'
        f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="{leaf_fill}"/></g>'
        f'<g transform="translate(84 22) rotate(-14)"><path d="{SEED_D}" fill="{seed_fill}"/></g>'
        f'<g transform="translate(116 22) rotate(14)"><path d="{SEED_D}" fill="{seed_fill}"/></g>'
        f'</g>')
    return "\n".join(defs), body


# ------------------------------------------------------- alternate concepts ---
def mark_wheat(uid, ring_fill, grain_fill, gradient=None):
    """Concept C: Q whose tail is a wheat spike (سنبلة)."""
    defs = []
    if gradient:
        defs.append(
            f'<linearGradient id="g{uid}" x1="24" y1="34" x2="168" y2="172" '
            f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{gradient[0]}"/>'
            f'<stop offset="1" stop-color="{gradient[1]}"/></linearGradient>')
        ring_fill = f"url(#g{uid})"
    grains = []
    grain = "M0,0 C9,-3.4 19,-2.2 24,0 C19,2.2 9,3.4 0,0 Z"
    for i, (t, sc) in enumerate([(9, 1.0), (21.5, 0.92), (33, 0.82)]):
        for sgn in (1, -1):
            grains.append(
                f'<g transform="translate({t} {sgn*3.2}) rotate({sgn*26}) scale({sc})">'
                f'<path d="{grain}" fill="{grain_fill}"/></g>')
    grains.append(f'<g transform="translate(43 0) scale(0.74)">'
                  f'<path d="{grain}" fill="{grain_fill}"/></g>')
    spike = (f'<g transform="{LEAF_T}">'
             f'<path d="M-8,0 L26,0" stroke="{grain_fill}" stroke-width="7.5" '
             f'stroke-linecap="round"/>' + "".join(grains) + '</g>')
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="{LEAF_T}"><path d="M-10,0 L70,0" stroke="#000" stroke-width="34" '
        f'stroke-linecap="round"/></g></mask>')
    body = (f'<g transform="translate(-6 8)">'
            f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="{RING["r"]}" fill="none" '
            f'stroke="{ring_fill}" stroke-width="{RING["w"]}" mask="url(#m{uid})"/>'
            f'{spike}</g>')
    return "\n".join(defs), body


def mark_heart(uid, disc_fill, tail_fill, gradient=None):
    """Concept B: a solid Q whose counter is a heart — العطاء / giving."""
    defs = []
    if gradient:
        defs.append(
            f'<linearGradient id="g{uid}" x1="24" y1="34" x2="168" y2="172" '
            f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{gradient[0]}"/>'
            f'<stop offset="1" stop-color="{gradient[1]}"/></linearGradient>')
        disc_fill = f"url(#g{uid})"
    heart = ("M0,19 C-20,5 -27.5,-7 -27.5,-16.5 C-27.5,-26 -20,-32 -11.5,-32 "
             "C-5.5,-32 -1.3,-28.5 0,-24 C1.3,-28.5 5.5,-32 11.5,-32 "
             "C20,-32 27.5,-26 27.5,-16.5 C27.5,-7 20,5 0,19 Z")
    tail_d = "M-12,0 L54,0"
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="200">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="translate(99 99) scale(0.95)"><path d="{heart}" fill="#000"/></g>'
        f'<g transform="{LEAF_T}"><path d="{tail_d}" stroke="#000" stroke-width="30" '
        f'stroke-linecap="round"/></g></mask>')
    body = (f'<g transform="translate(-4 6)">'
            f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="62.5" fill="{disc_fill}" '
            f'mask="url(#m{uid})"/>'
            f'<g transform="{LEAF_T}"><path d="{tail_d}" stroke="{tail_fill}" stroke-width="20" '
            f'stroke-linecap="round"/></g></g>')
    return "\n".join(defs), body


# ------------------------------------------------------------- the wordmark ---
def text_block(size_ar=100, size_la=30, tracking=7.0):
    ar = shape_to_path(FONT_AR, "قدم الخير", size=size_ar)
    la = shape_to_path(FONT_LA, "QADAM ALKHAIR", size=size_la, tracking=tracking)
    return ar, la


def place(res, x, y, align="left"):
    """Translate a shaped path so its ink box starts at x (or ends at x) on baseline y."""
    x0, y0, x1, y1 = res["bbox"]
    dx = x - x0 if align == "left" else x - x1
    return f'<g transform="translate({dx:.2f} {y:.2f})"><path d="{res["d"]}" fill="%s"/></g>'


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


# ink bounding box of the primary mark inside its 200x200 box
MARK_INK = (34.5, 31.8, 161.5, 178.0)
