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
RING = dict(cx=100, cy=116, r=52, w=21)
LEAF_T = "matrix(0.70711 0.70711 0.70711 -0.70711 124 140)"
LEAFSHAPE = "M0,0 C11,-4 23,-13 26,-27 C12,-26 2,-16 0,-3 Z"   # leaf, tip up-right
LEAF_D = ("M58,0 C45,6.4 27,10 6,10 C-4.2,10 -9.5,5.6 -9.5,0 "
          "C-9.5,-5.6 -4.2,-10 6,-10 C27,-10 45,-6.4 58,0 Z")
SEED_D = ("M0,-13 C4.5,-6.5 8,-3.5 8,1.5 C8,6 4.4,9.5 0,9.5 "
          "C-4.4,9.5 -8,6 -8,1.5 C-8,-3.5 -4.5,-6.5 0,-13 Z")
SEED_S = 0.72          # seeds read as the two dots of ق, not as ears
SEED_X = 12.5          # half the distance between the two dots
SEED_Y = 30
MARK_SHIFT = "translate(-2 0)"


def mark(uid, ring_fill, leaf_fill, seed_fill, gradient=None):
    """The mark, in a 200x200 box.

    Ring   = the bowl of Q and of ق.
    Sprout = two leaves on a stem growing out of the ring; they also sit where
             the two dots of ق sit, so the letter still reads.
    Leaf tail = the tail of Q and a leaf at once — the khair cue.
    """
    defs = []
    if gradient:
        defs.append(
            f'<linearGradient id="g{uid}" x1="24" y1="34" x2="168" y2="180" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{gradient[0]}"/>'
            f'<stop offset="1" stop-color="{gradient[1]}"/></linearGradient>')
        ring_fill = f"url(#g{uid})"
    stem_fill = ring_fill
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="#000" stroke="#000" '
        f'stroke-width="9" stroke-linejoin="round"/></g></mask>')
    body = (
        f'<g transform="{MARK_SHIFT}">'
        f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="{RING["r"]}" fill="none" '
        f'stroke="{ring_fill}" stroke-width="{RING["w"]}" mask="url(#m{uid})"/>'
        f'<path d="M100,60 C100,48 100,42 100,34" stroke="{stem_fill}" stroke-width="8.5" '
        f'stroke-linecap="round" fill="none"/>'
        f'<g transform="translate(99 38) rotate(4) scale(1.28)">'
        f'<path d="{LEAFSHAPE}" fill="{leaf_fill}"/></g>'
        f'<g transform="translate(101 38) rotate(-4) scale(-1.28 1.28)">'
        f'<path d="{LEAFSHAPE}" fill="{leaf_fill}"/></g>'
        f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="{leaf_fill}"/></g>'
        f'</g>')
    return "\n".join(defs), body


# ------------------------------------------------------- alternate concepts ---
def mark_wheat(uid, ring_fill, grain_fill, gradient=None):
    """Alternate: a wheat ear rises out of the Q — رزق وخير."""
    defs = []
    if gradient:
        defs.append(
            f'<linearGradient id="g{uid}" x1="24" y1="34" x2="168" y2="180" '
            f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{gradient[0]}"/>'
            f'<stop offset="1" stop-color="{gradient[1]}"/></linearGradient>')
        ring_fill = f"url(#g{uid})"
    grain = "M0,0 C9,-5.5 20,-4 25,0 C20,4 9,5.5 0,0 Z"
    ears = []
    for y, sc in [(60, 1.0), (47, 0.9), (35, 0.78)]:
        ears.append(f'<g transform="translate(102 {y}) rotate(-52) scale({sc})">'
                    f'<path d="{grain}" fill="{grain_fill}"/></g>')
        ears.append(f'<g transform="translate(98 {y}) rotate(-128) scale({sc})">'
                    f'<path d="{grain}" fill="{grain_fill}"/></g>')
    ears.append(f'<g transform="translate(100 28) rotate(-90) scale(0.72)">'
                f'<path d="{grain}" fill="{grain_fill}"/></g>')
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="#000" stroke="#000" '
        f'stroke-width="9" stroke-linejoin="round"/></g></mask>')
    body = (f'<g transform="{MARK_SHIFT}">'
            f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="{RING["r"]}" fill="none" '
            f'stroke="{ring_fill}" stroke-width="{RING["w"]}" mask="url(#m{uid})"/>'
            f'<path d="M100,66 L100,32" stroke="{ring_fill}" stroke-width="8" '
            f'stroke-linecap="round"/>{"".join(ears)}'
            f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="{grain_fill}"/></g></g>')
    return "\n".join(defs), body


def mark_hand(uid, ring_fill, hand_fill, leaf_fill, gradient=None):
    """Alternate: an open hand offering a seedling — قدّم الخير حرفياً."""
    defs = []
    if gradient:
        defs.append(
            f'<linearGradient id="g{uid}" x1="24" y1="34" x2="168" y2="180" '
            f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{gradient[0]}"/>'
            f'<stop offset="1" stop-color="{gradient[1]}"/></linearGradient>')
        ring_fill = f"url(#g{uid})"
    fingers = "".join(
        f'<path d="M{x},{y} L{x},{y-l}" stroke="{hand_fill}" stroke-width="9.5" '
        f'stroke-linecap="round"/>'
        for x, y, l in [(80, 130, 18), (91, 130, 25), (102, 130, 25), (113, 130, 18)])
    palm = (f'<path d="M74,126 C74,144 86,154 100,154 C114,154 126,144 126,126 Z" fill="{hand_fill}"/>'
            f'<rect x="74" y="118" width="52" height="14" rx="7" fill="{hand_fill}"/>'
            f'<path d="M74,128 C64,126 60,118 64,112" fill="none" stroke="{hand_fill}" '
            f'stroke-width="10" stroke-linecap="round"/>')
    sprout = (f'<path d="M100,118 L100,98" stroke="{leaf_fill}" stroke-width="6" stroke-linecap="round"/>'
              f'<g transform="translate(99 100) rotate(4) scale(0.8)">'
              f'<path d="{LEAFSHAPE}" fill="{leaf_fill}"/></g>'
              f'<g transform="translate(101 100) rotate(-4) scale(-0.8 0.8)">'
              f'<path d="{LEAFSHAPE}" fill="{leaf_fill}"/></g>')
    dots = "".join(f'<g transform="translate({100 + s*12.5} 44) rotate({s*10}) scale(0.72)">'
                   f'<path d="{SEED_D}" fill="{hand_fill}"/></g>' for s in (-1, 1))
    defs.append(
        f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="240" height="240">'
        f'<rect x="-20" y="-20" width="240" height="240" fill="#fff"/>'
        f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="#000" stroke="#000" '
        f'stroke-width="9" stroke-linejoin="round"/></g></mask>')
    body = (f'<g transform="{MARK_SHIFT}">'
            f'<circle cx="{RING["cx"]}" cy="{RING["cy"]}" r="{RING["r"]}" fill="none" '
            f'stroke="{ring_fill}" stroke-width="{RING["w"]}" mask="url(#m{uid})"/>'
            f'{dots}{palm}{fingers}{sprout}'
            f'<g transform="{LEAF_T}"><path d="{LEAF_D}" fill="{hand_fill}"/></g></g>')
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
        f'<g transform="translate(99 113) scale(0.95)"><path d="{heart}" fill="#000"/></g>'
        f'<g transform="{LEAF_T}"><path d="{tail_d}" stroke="#000" stroke-width="30" '
        f'stroke-linecap="round"/></g></mask>')
    body = (f'<g transform="translate(-2 0)">'
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
MARK_INK = (35.5, 7.0, 163.0, 178.5)
