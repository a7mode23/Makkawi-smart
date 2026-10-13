# -*- coding: utf-8 -*-
"""Shape text and expose every glyph contour, so a single dot can be swapped."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

_cache = {}


def _font(path, loc):
    key = (path, tuple(sorted((loc or {}).items())))
    if key not in _cache:
        tt = TTFont(path)
        gs = tt.getGlyphSet(location=loc) if loc else tt.getGlyphSet()
        _cache[key] = (tt, gs)
    return _cache[key]


def _split(rec):
    contours, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op in ("closePath", "endPath"):
            contours.append(cur)
            cur = []
    if cur:
        contours.append(cur)
    return contours


def _replay(ops, pen):
    for op, args in ops:
        getattr(pen, op)(*args)


def shape(path, text, size=100, loc=None, tracking=0.0):
    """-> list of glyphs: {cluster, name, contours:[{d, bbox, area}]}, plus advance."""
    blob = hb.Blob.from_file_path(path)
    face = hb.Face(blob)
    font = hb.Font(face)
    upem = face.upem
    font.scale = (upem, upem)
    if loc:
        font.set_variations(loc)
    buf = hb.Buffer()
    buf.add_codepoints([ord(c) for c in text])
    buf.guess_segment_properties()
    hb.shape(font, buf)
    tt, gs = _font(path, loc)
    order = tt.getGlyphOrder()
    s = size / upem
    x = 0.0
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        rec = DecomposingRecordingPen(gs)
        t = Transform(s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s)
        gs[name].draw(TransformPen(rec, t))
        cs = []
        for ops in _split(rec):
            sp = SVGPathPen(None, ntos=lambda v: f"{v:.2f}")
            _replay(ops, sp)
            bp = BoundsPen(None)
            _replay(ops, bp)
            if bp.bounds is None:
                continue
            x0, y0, x1, y1 = bp.bounds
            cs.append({"d": sp.getCommands(), "bbox": bp.bounds, "area": (x1 - x0) * (y1 - y0)})
        out.append({"cluster": info.cluster, "name": name, "contours": cs})
        x += pos.x_advance + tracking / s
    return out, x * s


def bbox_of(glyphs):
    xs0, ys0, xs1, ys1 = [], [], [], []
    for g in glyphs:
        for c in g["contours"]:
            a, b, cc, d = c["bbox"]
            xs0.append(a); ys0.append(b); xs1.append(cc); ys1.append(d)
    return min(xs0), min(ys0), max(xs1), max(ys1)


def take_dot(glyphs, cluster, where="above", tol=2.0):
    """Remove the dot of the letter at `cluster` (the contour that sits clear of
    all the others, above or below them); return its bbox."""
    cand = [(g, c) for g in glyphs if g["cluster"] == cluster for c in g["contours"]]
    if len(cand) < 2:
        return None
    if where == "above":
        g, c = min(cand, key=lambda gc: gc[1]["bbox"][1])
        others = [o for _, o in cand if o is not c]
        if c["bbox"][3] > min(o["bbox"][1] for o in others) + tol:
            return None
    else:
        g, c = max(cand, key=lambda gc: gc[1]["bbox"][3])
        others = [o for _, o in cand if o is not c]
        if c["bbox"][1] < max(o["bbox"][3] for o in others) - tol:
            return None
    g["contours"].remove(c)
    return c["bbox"]


def path_of(glyphs):
    return " ".join(c["d"] for g in glyphs for c in g["contours"])
