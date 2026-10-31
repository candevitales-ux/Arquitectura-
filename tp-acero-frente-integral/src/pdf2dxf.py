# -*- coding: utf-8 -*-
"""Lámina A3 (PDF final) -> DXF 2D, copia exacta de la hoja.

  python3 src/pdf2dxf.py <lamina.pdf> <vec2d.json> <salida.dxf> <factor>

factor = 1  -> milímetros de PAPEL (hoja A3 297 x 420; se plotea 1:1).
factor = 20 -> todo multiplicado por 20: el corte (ESC 1:20) queda en VERDADERA MAGNITUD (1 unidad = 1 mm real);
               se plotea a escala 1:20 sobre A3 y sale idéntico a la hoja.

- Vectores del PDF (corte original de AutoCAD + correcciones + referencias + rótulo) con sus recortes (clip) y con el
  orden de dibujo resuelto: lo que tapa un relleno opaco posterior se recorta (no hay rellenos blancos "tapando").
- Textos como TEXT editables (Arial = Liberation Sans, mismas métricas).
- Los 3 detalles axonométricos (que en el PDF son imagen) se reemplazan por su versión vectorial (caras + aristas visibles)
  exportada por el mismo modelo 3D (build/vec2d.json).
"""
import sys, json, math
import numpy as np
import pymupdf as fitz
import ezdxf
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon, LineString, MultiLineString, box, GeometryCollection
from shapely.ops import unary_union
from shapely import affinity

PDF, VEC, OUT, F = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
K = 25.4 / 72.0          # pt -> mm
HP = 420.0               # alto de la hoja (mm); y del PDF hacia abajo

def T(x, y):             # mm de papel (y abajo) -> coordenadas DXF
    return (x * F, (HP - y) * F)

doc = ezdxf.new("R2000", setup=True)
doc.units = ezdxf.units.MM
doc.header["$INSUNITS"] = 4
doc.header["$MEASUREMENT"] = 1
doc.header["$LTSCALE"] = F
doc.styles.add("ARIAL", font="arial.ttf")
doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
LAY = {"0-MARCO-A3": 8, "1-CORTE-LINEAS": 7, "1-CORTE-RAYADOS": 8, "1-CORTE-RELLENOS": 9, "1-CORTE-ROJO": 1,
       "2-DETALLES-ARISTAS": 7, "2-DETALLES-RELLENOS": 9, "2-DETALLES-RAYADOS": 8,
       "3-TEXTOS": 7, "3-REFERENCIAS": 7, "3-ROTULO": 7}
for n, c in LAY.items(): doc.layers.add(n, color=c)

def lw(w_mm):
    for k in (5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100):
        if w_mm * 100 <= k + 1: return k
    return 100

from ezdxf.colors import DXF_DEFAULT_COLORS, int2rgb
_ACI = [(i, int2rgb(DXF_DEFAULT_COLORS[i])) for i in range(1, 256) if i != 7]
def aci(c):
    """color ACI más cercano (el DWG R2000 no guarda RGB)"""
    return min(_ACI, key=lambda t: 2 * (t[1][0] - c[0]) ** 2 + 4 * (t[1][1] - c[1]) ** 2 + 3 * (t[1][2] - c[2]) ** 2)[0]

def color_attrs(rgb):
    r, g, b = [int(round(c * 255)) for c in rgb]
    if max(r, g, b) < 40: return {"color": 7}                       # negro -> blanco/negro de AutoCAD
    if r > 200 and g < 60 and b < 60: return {"color": 1}           # rojo
    return {"color": aci((r, g, b))}

# ------------------------------------------------------------------ geometría de trazados
def bez(p0, p1, p2, p3):
    L = p0.distance_to(p1) + p1.distance_to(p2) + p2.distance_to(p3)
    n = max(4, min(32, int(L / 1.2)))
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t**3 * p3.x,
                    u**3 * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t**3 * p3.y))
    return out

def subpaths(items, close_last=False):
    """-> lista de (puntos en mm, cerrado)"""
    out, cur = [], None
    def flush(closed=False):
        nonlocal cur
        if cur and len(cur) >= 2: out.append((cur, closed))
        cur = None
    for it in items:
        op = it[0]
        if op == "re":
            flush(); r = it[1]
            out.append(([(r.x0 * K, r.y0 * K), (r.x1 * K, r.y0 * K), (r.x1 * K, r.y1 * K), (r.x0 * K, r.y1 * K)], True)); continue
        if op == "qu":
            flush(); q = it[1]
            out.append(([(p.x * K, p.y * K) for p in (q.ul, q.ur, q.lr, q.ll)], True)); continue
        a = it[1]
        if cur is None or abs(cur[-1][0] - a.x * K) > 1e-4 or abs(cur[-1][1] - a.y * K) > 1e-4:
            flush(); cur = [(a.x * K, a.y * K)]
        if op == "l": cur.append((it[2].x * K, it[2].y * K))
        elif op == "c": cur += [(x * K, y * K) for x, y in bez(it[1], it[2], it[3], it[4])]
    if cur:
        closed = close_last or (len(cur) > 2 and abs(cur[0][0] - cur[-1][0]) < 1e-4 and abs(cur[0][1] - cur[-1][1]) < 1e-4)
        flush(closed)
    return out

def area_geom(sps, even_odd):
    polys = []
    for pts, _ in sps:
        if len(pts) < 3: continue
        g = Polygon(pts)
        if not g.is_valid: g = g.buffer(0)
        if not g.is_empty and g.area > 1e-7: polys.append(g)
    if not polys: return None
    if even_odd:
        g = polys[0]
        for q in polys[1:]: g = g.symmetric_difference(q)
        return g
    if len(polys) == 1: return polys[0]
    # regla nonzero: número de vueltas de cada región según la orientación de los subtrazados
    sign = []
    for pts, _ in sps:
        if len(pts) < 3: continue
        a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        sign.append(1 if a > 0 else -1)
    if len(sign) != len(polys): return unary_union(polys)
    order = sorted(range(len(polys)), key=lambda i: -polys[i].area)
    out = []
    for i in order:
        p = polys[i]; rp = p.representative_point()
        w = sign[i] + sum(sign[j] for j in order if j != i and polys[j].area > p.area and polys[j].contains(rp))
        if w == 0: continue
        inner = [polys[j] for j in order if j != i and polys[j].area < p.area and p.contains(polys[j].representative_point())]
        out.append(p.difference(unary_union(inner)) if inner else p)
        # las regiones internas con vueltas != 0 se agregan cuando les toca
    return unary_union(out) if out else None

def polys_of(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    return [q for q in getattr(g, "geoms", []) for q in polys_of(q)] if hasattr(g, "geoms") else []

def lines_of(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "LineString": return [g]
    if g.geom_type == "LinearRing": return [LineString(g.coords)]
    if hasattr(g, "geoms"): return [l for q in g.geoms for l in lines_of(q)]
    return []

def dashify(line, pattern, phase):
    """corta una LineString en trazos según el patrón (mm)"""
    if not pattern or sum(pattern) <= 0: return [line]
    out, L, s, k, on = [], line.length, -phase, 0, True
    while s < L:
        e = s + pattern[k % len(pattern)]
        if on and e > 0:
            a, b = max(s, 0), min(e, L)
            if b - a > 1e-4:
                from shapely.ops import substring
                out.append(substring(line, a, b))
        s, k, on = e, k + 1, not on
    return out

# ------------------------------------------------------------------ lista de objetos con orden de pintor
OBJ = []           # dict(kind='line'|'fill', geom, layer, attrs, hatch=None)
BB = []            # bounds

def add(kind, geom, layer, attrs, hatch=None):
    if geom is None or geom.is_empty: return
    OBJ.append(dict(kind=kind, geom=geom, layer=layer, attrs=attrs, hatch=hatch)); BB.append(geom.bounds)

def occlude(poly):
    """un relleno opaco tapa todo lo dibujado antes"""
    if not OBJ or poly.area > 40000: return          # el fondo blanco de la hoja no tapa nada
    a = np.array(BB); x0, y0, x1, y1 = poly.bounds
    idx = np.nonzero((a[:, 0] <= x1) & (a[:, 2] >= x0) & (a[:, 1] <= y1) & (a[:, 3] >= y0))[0]
    from shapely.prepared import prep
    pp = prep(poly)
    for i in idx:
        o = OBJ[i]
        if o["geom"].is_empty or not pp.intersects(o["geom"]): continue
        if pp.contains(o["geom"]): o["geom"] = GeometryCollection(); continue
        try: o["geom"] = o["geom"].difference(poly)
        except Exception: o["geom"] = o["geom"].buffer(0).difference(poly) if o["kind"] == "fill" else o["geom"]

# ------------------------------------------------------------------ 0) detalles (vectores 2D del modelo 3D) — en el PDF van debajo de globos y textos: se dibujan primero
HATCH = {"ha": ("ANSI31", 0.25, 0), "hais": ("AR-CONC", 0.03, 0), "h": ("AR-CONC", 0.03, 0), "mort": ("AR-SAND", 0.02, 0),
         "grout": ("AR-SAND", 0.02, 0), "eps": ("ZIGZAG", 0.25, 0), "lana": ("INSUL", 0.12, 0), "tosca": ("GRAVEL", 0.25, 0),
         "tierra": ("EARTH", 0.4, 45)}
for det in json.load(open(VEC)):
    for f in det["faces"]:
        tris = [Polygon([(t[0], t[1]), (t[2], t[3]), (t[4], t[5])]) for t in f["tris"]]
        tris = [q for q in tris if q.is_valid and q.area > 1e-8]
        if not tris: continue
        g = unary_union([q.buffer(0.004, join_style=2) for q in tris]).buffer(-0.004, join_style=2)
        if g.is_empty: continue
        if f.get("glass"): continue                          # vidrio transparente: no tapa
        occlude(g)
        if f.get("cap") and f.get("hatch") in HATCH:
            add("fill", g, "2-DETALLES-RAYADOS", {"color": 8}, hatch=HATCH[f["hatch"]])
    for e in det["edges"]:
        l = LineString([(e[0], e[1]), (e[2], e[3])])
        if l.length > 1e-3: add("line", l, "2-DETALLES-ARISTAS", {"color": 7, "lineweight": 9 if e[4] else 18})

# ------------------------------------------------------------------ rayados con patrón del corte (en el PDF son mosaicos raster)
# mismas coordenadas que src/lamina.py: P = mm del original a 1:10; hoja = (TX, TY) + 0.5·P
TX, TY, KP = 141.5, 6.0, 0.5
Ph = lambda pts: Polygon([(TX + KP * x, TY + KP * y) for x, y in pts])
DX0, DX1, DY0, DY1 = 178.3, 218.4, 263.75, 271.5
dado = Ph([(DX0, DY0), (DX1, DY0), (DX1, DY1), (DX0, DY1)])
add("fill", dado, "1-CORTE-RAYADOS", {"color": 8}, hatch=("ANSI31", 0.75, 0))            # 40 dado H°A°
add("fill", dado, "1-CORTE-RAYADOS", {"color": 8}, hatch=("AR-CONC", 0.03, 0))
for cp in (Ph([(118.7, 264.45), (DX0, 263.9), (DX0, DY1), (118.7, DY1)]), Ph([(DX1, DY0), (278.3, DY0), (278.3, DY1), (DX1, DY1)])):
    add("fill", cp, "1-CORTE-RAYADOS", {"color": 8}, hatch=("AR-CONC", 0.045, 0))        # 4 contrapiso

# ------------------------------------------------------------------ 1) PDF
pdf = fitz.open(PDF); page = pdf[0]
DET_RECTS = []
for im in page.get_image_info(xrefs=True):
    b = [v * K for v in im["bbox"]]
    if im["width"] > 1000 and im["height"] > 1000: DET_RECTS.append(box(*b))     # imágenes de los detalles 3D

def layer_for(rgb, x):
    if rgb and rgb[0] > 0.8 and rgb[1] < 0.3 and rgb[2] < 0.3: return "1-CORTE-ROJO" if x > 140 else "3-TEXTOS"
    return None

clips = []   # (level, geom)
def eff_clip(level):
    g = None
    for L, c in clips:
        if L < level: g = c
    return g

# objetos del PDF en orden; las imágenes de los detalles se intercalan donde aparecen (seqno) -> se usa su posición aprox.
drawings = page.get_drawings(extended=True)
img_strip = None
for im in page.get_image_info(xrefs=True):
    if im["xref"] == 24 or (im["width"] > 2000 and im["height"] < 200): img_strip = im

for d in drawings:
    t, lev = d["type"], d.get("level", 0)
    if t in ("clip", "group"):
        clips = [(L, c) for L, c in clips if L < lev]
        if t == "clip":
            g = area_geom(subpaths(d["items"], True), d.get("even_odd", False)) or Polygon()
            par = eff_clip(lev + 1)
            if par is not None: g = g.intersection(par)
            clips.append((lev, g))
        continue
    clips = [(L, c) for L, c in clips if L < lev]
    clip = eff_clip(lev)
    sps = subpaths(d["items"], bool(d.get("closePath")))
    if not sps: continue
    xmid = (d["rect"].x0 + d["rect"].x1) / 2 * K
    in_corte = xmid > 140 and d["rect"].y1 * K < 380
    # ----- relleno (se descarta el rectángulo negro que es la máscara de la imagen del panel 9, no se ve en la hoja)
    if t == "f" and lev >= 9 and d["rect"].height * K > 50 and 225 < d["rect"].x0 * K < 236: continue
    if "f" in t and d.get("fill") is not None and (d.get("fill_opacity") or 1) > 0:
        g = area_geom(sps, d.get("even_odd", False))
        if g is not None and clip is not None and not clip.contains(g): g = g.intersection(clip)
        if g is not None and not g.is_empty and g.area > 1e-6:
            if (d.get("fill_opacity") or 1) >= 0.999: occlude(g)
            rgb = d["fill"]
            if min(rgb) < 0.985:                                   # los blancos solo tapan
                lay = layer_for(rgb, xmid) or ("1-CORTE-RELLENOS" if in_corte else "3-TEXTOS")
                add("fill", g, lay, color_attrs(rgb))
    # ----- trazo
    if "s" in t and d.get("color") is not None and (d.get("stroke_opacity") or 1) > 0:
        w = (d.get("width") or 0.1) * K
        geoms = []
        for pts, closed in sps:
            if closed and pts[0] != pts[-1]: pts = pts + [pts[0]]
            if len(pts) >= 2: geoms.append(LineString(pts))
        dash = d.get("dashes") or ""
        pat, ph = None, 0
        if dash and "[" in dash and "[]" not in dash.replace(" ", ""):
            inside = dash[dash.index("[") + 1: dash.index("]")].split()
            pat = [float(v) * K for v in inside if v]; ph = float(dash.split("]")[1].strip() or 0) * K
        out = []
        for g in geoms:
            if clip is not None and not clip.contains(g): g = g.intersection(clip)
            for l in lines_of(g):
                out += dashify(l, pat, ph) if pat else [l]
        rgb = d["color"]
        lay = layer_for(rgb, xmid) or ("1-CORTE-LINEAS" if in_corte else "3-TEXTOS")
        for l in out:
            if l.length > 1e-4: add("line", l, lay, dict(color_attrs(rgb), lineweight=lw(w)))

# franja del panel sándwich (9): en el original es una imagen (amarilla arriba y abajo, tramo central no visible)
# -> rellenos lisos del mismo color en los tramos amarillos
if img_strip:
    pix = fitz.Pixmap(pdf, img_strip["xref"])
    A = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3]
    col = A.mean(0)                                   # perfil a lo largo del ancho de la imagen (vertical en la hoja)
    yel = col.mean(1) > 120
    x0, y0, x1, y1 = [v * K for v in img_strip["bbox"]]
    n = len(yel); i = 0; segs = []
    while i < n:
        if yel[i]:
            j = i
            while j < n and yel[j]: j += 1
            # u = i/n -> y = y1 - (y1 - y0)·u  (imagen rotada: el ancho corre de abajo hacia arriba)
            segs.append((box(x0, y1 - (y1 - y0) * j / n, x1, y1 - (y1 - y0) * i / n), col[i:j].mean(0) / 255)); i = j
        else: i += 1
    for g, c in segs:
        add("fill", g, "1-CORTE-RELLENOS", color_attrs(tuple(c)))
        OBJ.insert(0, OBJ.pop()); BB.insert(0, BB.pop())      # debajo de las líneas del corte

# ------------------------------------------------------------------ 3) salida de geometría
def merge_lines(geoms):
    from shapely.ops import linemerge
    m = linemerge(geoms) if len(geoms) > 1 else geoms[0]
    return lines_of(m)

nL = nF = 0
for o in OBJ:
    g = o["geom"]
    if g.is_empty: continue
    if o["kind"] == "line":
        for l in lines_of(g):
            pts = [T(x, y) for x, y in l.coords]
            if len(pts) < 2: continue
            at = {k: v for k, v in o["attrs"].items() if k != "_rgb"}
            if len(pts) == 2: msp.add_line(pts[0], pts[1], dxfattribs={"layer": o["layer"], **at})
            else: msp.add_lwpolyline(pts, dxfattribs={"layer": o["layer"], **at})
            nL += 1
    else:
        for p in polys_of(g.buffer(0) if not g.is_valid else g):
            if p.area < 1e-6: continue
            ext = [T(x, y) for x, y in list(p.exterior.coords)[:-1]]
            holes = [[T(x, y) for x, y in list(r.coords)[:-1]] for r in p.interiors]
            h = msp.add_hatch(dxfattribs={"layer": o["layer"], **{k: v for k, v in o["attrs"].items() if k not in ("lineweight", "_rgb", "true_color")}})
            if o["hatch"]:
                pat, sc, ang = o["hatch"]; h.set_pattern_fill(pat, scale=sc * F, angle=ang)
            else:
                h.set_solid_fill(color=o["attrs"].get("color", 7), rgb=o["attrs"].get("_rgb"))
            h.paths.add_polyline_path(ext, is_closed=True, flags=1)
            for r in holes: h.paths.add_polyline_path(r, is_closed=True)
            nF += 1

# ------------------------------------------------------------------ 4) textos
nT = 0
for b in page.get_text("rawdict" if False else "dict")["blocks"]:
    for ln in b.get("lines", []):
        for s in ln["spans"]:
            txt = s["text"]
            if not txt.strip(): continue
            ox, oy = s["origin"][0] * K, s["origin"][1] * K
            # textos dentro de las imágenes de los detalles no existen (los globos son vectoriales)
            size = s["size"] * K
            bold = bool(s["flags"] & 16) or "Bold" in s["font"]
            c = s["color"]; rgb = ((c >> 16) & 255, (c >> 8) & 255, c & 255)
            lay = "3-TEXTOS"
            if ox > 195 and oy > 205 and oy < 380: lay = "3-REFERENCIAS"
            if oy > 380: lay = "3-ROTULO"
            attrs = {"layer": lay, "height": size * 0.716 * F, "style": "ARIAL-NEGRITA" if bold else "ARIAL"}
            attrs.update({k: v for k, v in color_attrs(tuple(v / 255 for v in rgb)).items() if k != "_rgb"})
            ang = math.degrees(math.atan2(-ln["dir"][1], ln["dir"][0]))
            if abs(ang) > 0.01: attrs["rotation"] = ang
            msp.add_text(txt, dxfattribs=attrs).set_placement(T(ox, oy), align=TextEntityAlignment.LEFT)
            nT += 1

# marco de la hoja A3 (referencia de ploteo; no imprime: capa en color 8, se puede apagar)
msp.add_lwpolyline([T(0, 0), T(297, 0), T(297, 420), T(0, 420)], close=True, dxfattribs={"layer": "0-MARCO-A3", "lineweight": 0})
doc.set_modelspace_vport(height=420 * F * 1.05, center=(148.5 * F, 210 * F))
doc.saveas(OUT)
print(f"{OUT}: {nL} líneas, {nF} rellenos, {nT} textos (factor {F:g})")
