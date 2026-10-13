import sys, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen

def shape_to_path(font_path, text, size=100, variations=None, tracking=0, rtl=None):
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    hbfont = hb.Font(face)
    upem = face.upem
    hbfont.scale = (upem, upem)
    if variations:
        hbfont.set_variations(variations)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    if rtl:
        buf.direction = "rtl"
    hb.shape(hbfont, buf)
    infos, poss = buf.glyph_infos, buf.glyph_positions

    tt = TTFont(font_path)
    loc = variations or {}
    try:
        gs = tt.getGlyphSet(location=loc) if loc else tt.getGlyphSet()
    except TypeError:
        gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()

    scale = size / upem
    x = y = 0.0
    paths = []
    bounds = BoundsPen(gs)
    for info, pos in zip(infos, poss):
        gname = order[info.codepoint]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        t = Transform(scale, 0, 0, -scale, (x + pos.x_offset) * scale, (y + pos.y_offset) * -scale)
        tpen = TransformPen(pen, t)
        gs[gname].draw(tpen)
        gs[gname].draw(TransformPen(bounds, t))
        d = pen.getCommands()
        if d:
            paths.append(d)
        x += pos.x_advance + (tracking / scale if scale else 0)
        y += pos.y_advance
    return {"d": " ".join(paths), "advance": x * scale, "bbox": bounds.bounds}

if __name__ == "__main__":
    cfg = json.loads(sys.argv[1])
    print(json.dumps(shape_to_path(**cfg)))
