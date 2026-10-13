# -*- coding: utf-8 -*-
"""«قدم الخير» — footprint icons, each with one khair cue."""
import math

GOLD, GOLD_LT, GREEN, GREEN_DK = "#E3A42B", "#F6CB6B", "#0F7B5A", "#0A5440"
HEART = ("M0,15 C-16,4 -22,-5 -22,-13 C-22,-21 -16,-26 -9,-26 C-4.5,-26 -1,-23 0,-19.5 "
         "C1,-23 4.5,-26 9,-26 C16,-26 22,-21 22,-13 C22,-5 16,4 0,15 Z")

# a right footprint in a local box ~ (-40..40, -70..70), toes up; big toe on the left
TOES = [(-21, -52, 11.5, 13.5), (-3, -60, 8.6, 9.8), (11, -57, 7.6, 8.6), (23, -50, 6.6, 7.6), (32, -40, 5.6, 6.6)]
SOLE = ("M-24,-30 C-27,-44 -4,-48 14,-42 C28,-37 36,-26 34,-8 "
        "C32,10 22,22 20,38 C18,56 12,68 -2,68 C-18,68 -22,54 -20,38 "
        "C-18,22 -13,10 -16,-4 C-18,-14 -22,-22 -24,-30 Z")


def toes(fill, shape="oval"):
    out = []
    for x, y, rx, ry in TOES:
        if shape == "heart":
            s = rx / 22 * 1.05
            out.append(f'<g transform="translate({x} {y + 5.5 * s:.2f}) scale({s:.3f})"><path d="{HEART}" fill="{fill}"/></g>')
        else:
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}"/>')
    return "".join(out)


def foot(x, y, s=1.0, rot=0, sole_fill=GREEN, toe_fill=GREEN, mirror=False, sole=None, toe_shape="oval"):
    m = " scale(-1 1)" if mirror else ""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s}){m}">'
            f'<path d="{sole or SOLE}" fill="{sole_fill}"/>{toes(toe_fill, toe_shape)}</g>')


# ------------------------------------------------------------------- icons ---
def heart_step(green=GREEN, gold=GOLD):
    """أ — قدم القلب: the sole is a heart; five toes above it make it a footprint."""
    t = ""
    for x, y, rx, ry in [(-27, -56, 10.5, 12.5), (-8, -64, 8.2, 9.4), (8, -62, 7.4, 8.4),
                         (21, -56, 6.4, 7.4), (31, -46, 5.4, 6.4)]:
        t += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{green}"/>'
    return (f'<g transform="translate(98 116) rotate(-8)">'
            f'<g transform="translate(2 22) scale(2.0)"><path d="{HEART}" fill="{gold}"/></g>{t}</g>')


def leaf_step(green=GREEN, gold=GOLD):
    """ب — قدم الورقة: the sole is a green leaf with its vein; the toes are gold seeds."""
    vein = ('<path d="M3,60 C0,30 2,0 8,-32" stroke="#FFFFFF" stroke-width="2.6" '
            'fill="none" stroke-linecap="round"/>'
            '<path d="M3,32 Q-6,26 -12,18 M4,10 Q13,4 20,-4 M5,-10 Q-3,-16 -9,-24" stroke="#FFFFFF" '
            'stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    return (f'<g transform="translate(100 104) rotate(-10) scale(1.15)">'
            f'<path d="{SOLE}" fill="{green}"/>{vein}{toes(gold)}</g>')


def steps(green=GREEN, gold=GOLD):
    """ج — خطوات الخير: two steps forward, the leading one in gold."""
    return (foot(76, 128, 0.78, -14, green, green, mirror=True)
            + foot(128, 76, 0.78, 14 - 4, gold, gold))


def blessed_step(green=GREEN, gold=GOLD):
    """د — قدم البركة: a footprint with a sparkle of blessing by its toes."""
    def spark(x, y, r):
        k = r * 0.28
        return (f'<path d="M{x},{y - r} C{x + k * 0.6},{y - k} {x + k},{y - k * 0.6} {x + r},{y} '
                f'C{x + k},{y + k * 0.6} {x + k * 0.6},{y + k} {x},{y + r} '
                f'C{x - k * 0.6},{y + k} {x - k},{y + k * 0.6} {x - r},{y} '
                f'C{x - k},{y - k * 0.6} {x - k * 0.6},{y - k} {x},{y - r} Z" fill="{gold}"/>')
    return (foot(92, 108, 1.1, -8, green, green)
            + spark(150, 46, 20) + spark(166, 86, 10) + spark(130, 20, 8))


FEET = [("أ — قدم القلب", heart_step), ("ب — قدم الورقة", leaf_step),
        ("ج — خطوات الخير", steps), ("د — قدم البركة", blessed_step)]


def steps_left(green=GREEN, gold=GOLD):
    """ج — mirrored: the steps walk up and to the left, into an Arabic name."""
    return f'<g transform="translate(200 0) scale(-1 1)">{steps(green, gold)}</g>'
