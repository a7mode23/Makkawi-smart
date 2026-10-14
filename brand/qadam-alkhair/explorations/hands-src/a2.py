# -*- coding: utf-8 -*-
"""Option أ developed: heavier line to match the name, sleeve cuffs, sparkles round the heart."""
import json
import hands3 as H

SIL = json.load(open("silhouettes.json"))
LINES = {"palmDownHand": slice(1, None), "palmUpHand": slice(2, None)}   # finger-line contours

GREEN, DARK, GOLD = "#0F7B5A", "#0A5440", "#E3A42B"
# Per glyph, in its own font units (y up). Both glyphs have the wrist on the left.
WRIST = {"palmDownHand": (250, 678, 1348), "palmUpHand": (205, 50, 807)}      # x, y bottom, y top


def place(name, x, y, w, fill, mirror=False, rot=0, sw=0, wrist="box", bg="#FFFFFF", style="line",
          tint="#E3F1EA", sw_lines=None, sleeve=None):
    """Like hands3.place, plus a stroke `sw` (font units), a wrist treatment
    (box = as drawn, cuff = outlined shirt cuff, solid = filled cuff) and a style:
    line = outline only, tint = outline over a light fill, solid = filled hand with white finger lines."""
    d, (x0, y0, x1, y1) = H.glyph(name)
    parts = ["M" + p for p in d.split("M") if p]
    s = w / (x1 - x0)
    h = (y1 - y0) * s
    cx, cy = x + w / 2, y + h / 2
    m = -1 if mirror else 1
    st = f' stroke="{fill}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
    t = 120 + sw                                  # drawn line thickness
    if style == "solid":
        fl = "".join(parts[LINES[name]])
        body = (f'<path d="{SIL[name]}" fill="{fill}"{st}/>'
                f'<path d="{fl}" fill="{bg}" stroke="{bg}" stroke-width="{sw * 0.5:.0f}" stroke-linejoin="round"/>')
    else:
        if sw_lines is None:
            body = f'<path d="{d}" fill="{fill}"{st}/>'
        else:                                       # bold outline, finer finger lines
            n = LINES[name].start
            outline, fl = "".join(parts[:n]), "".join(parts[n:])
            body = (f'<path d="{outline}" fill="{fill}"{st}/>'
                    f'<path d="{fl}" fill="{fill}" stroke="{fill}" stroke-width="{sw_lines}" stroke-linejoin="round"/>')
        if style == "tint":
            body = f'<path d="{SIL[name]}" fill="{tint}"/>' + body
    wx, wb, wt = WRIST[name]
    if wrist in ("cuff", "solid"):
        cx0, cx1 = wx - 200, wx + 120 + t * 0.6
        cy0, cy1 = wb - 90, wt + 90
        f = sleeve or {"cuff": tint if style == "tint" else bg, "solid": fill}[wrist]
        body += (f'<rect x="{cx0:.0f}" y="{cy0:.0f}" width="{cx1 - cx0:.0f}" height="{cy1 - cy0:.0f}" rx="110" '
                 f'fill="{f}" stroke="{sleeve or fill}" stroke-width="{t:.0f}"/>')
    return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({rot}) scale({m * s:.5f} {s:.5f}) '
            f'translate({-(x0 + x1) / 2:.2f} {-(y0 + y1) / 2:.2f}) scale(1 -1)">{body}</g>')


def sparkle(x, y, r, fill):
    k = r * 0.16
    return (f'<path d="M{x},{y - r} C{x + k},{y - k} {x + k},{y - k} {x + r},{y} '
            f'C{x + k},{y + k} {x + k},{y + k} {x},{y + r} C{x - k},{y + k} {x - k},{y + k} {x - r},{y} '
            f'C{x - k},{y - k} {x - k},{y - k} {x},{y - r}Z" fill="{fill}"/>')


SPARKS = {
    "diag":  [(-25, -13, 7.5), (25, 15, 5.2)],                     # what was sent
    "pair":  [(-28, -5, 6.4), (28, -5, 6.4)],                      # level pair, same size
    "trio":  [(-28, -2, 6.0), (0, -34, 4.6), (28, -2, 6.0)],       # left, above, right
    "cluster": [(-27, -16, 7.0), (-36, -2, 3.8), (-17, -29, 3.6)],  # one sparkle-group, upper left
    "sym":   [(-26, -11, 6.0), (26, 11, 6.0)],                     # diagonal, same size
}


def icon(green=GREEN, gold=GOLD, wrist="box", bg="#FFFFFF", sw=40, rot=0, sparkles="diag", style="line",
         tint="#E3F1EA", giver=None, heart_at=(100, 98), heart_s=0.78):
    kw = dict(sw=sw, wrist=wrist, bg=bg, style=style, tint=tint)
    top = place("palmDownHand", 64, 18, 124, giver or green, mirror=True, rot=rot, **kw)
    bot = place("palmUpHand", 12, 108, 124, green, **kw)
    hx, hy = heart_at
    g = top + bot + H.heart(hx, hy, heart_s, gold)
    for dx, dy, r in SPARKS.get(sparkles or "", []):
        g += sparkle(hx + dx, hy + dy, r, gold)
    return g
