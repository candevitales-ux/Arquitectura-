# -*- coding: utf-8 -*-
"""Lámina A3 vertical completa en un único DXF/DWG 2D, en milímetros de papel (escala 1:1 de la hoja):
marco A3 297x420, corte integral 1:20 (geometría real escalada y recortada en bandas), referencias, rótulo y
las 3 axonometrías como dibujo 2D (rellenos ordenados + aristas visibles)."""
import json, re, math, xml.etree.ElementTree as ET
import ezdxf
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union

HPAGE = 420.0
def P(x, y): return (x, HPAGE - y)              # coord. SVG (y abajo) -> DXF (y arriba)

doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
LAY = {"0-MARCO-A3": 7, "1-CORTE-CONTORNOS": 7, "1-CORTE-RAYADOS": 8, "1-CORTE-RELLENOS": 9, "1-CORTE-ARMADURAS": 14,
       "1-CORTE-OCULTO": 8, "1-CORTE-VISTA": 8, "2-AXO-RELLENOS": 9, "2-AXO-RAYADOS": 8, "2-AXO-ARISTAS": 7,
       "3-TEXTOS": 7, "3-REFERENCIAS": 1, "3-COTAS-NIVELES": 7, "3-EJES": 1}
for n, c in LAY.items(): doc.layers.add(n, color=c)

def rgb(h):
    h = h.strip().lstrip("#"); h = "".join(c * 2 for c in h) if len(h) == 3 else h
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lw(sw):
    for k in (9, 13, 18, 25, 35, 50):
        if sw * 100 <= k + 2: return k
    return 50

# =============================================================== CORTE (geometría real -> papel, por bandas)
S, PX0, XR0, XMAX = 20.0, 9.0, -600.0, 1700.0
BANDS = [(7600, 9540, 10.0), (3200, 5000, 111.0), (-2180, 1500, 205.0)]
FILL = {"url(#pHA)": ("ANSI31", 0.4, 0), "url(#pHAis)": ("AR-CONC", 0.06, 0), "url(#pH)": ("AR-CONC", 0.04, 0),
        "url(#pMort)": ("AR-SAND", 0.03, 0), "url(#pHid)": ("AR-SAND", 0.02, 0), "url(#pGrout)": ("AR-SAND", 0.02, 0),
        "url(#pTierra)": ("EARTH", 0.6, 45), "url(#pTosca)": ("GRAVEL", 0.4, 0), "url(#pEPS)": ("ZIGZAG", 0.3, 0),
        "url(#pEPSv)": ("ZIGZAG", 0.3, 90), "url(#pLana)": ("INSUL", 0.15, 0), "url(#pLanaV)": ("INSUL", 0.15, 90)}
BG = {"url(#pHA)": "#d3d6d9", "url(#pHAis)": "#dedad2", "url(#pH)": "#e6e4df", "url(#pMort)": "#e9e9e9", "url(#pHid)": "#c9dbe6",
      "url(#pGrout)": "#bdbdbd", "url(#pTierra)": "#ece3d2", "url(#pTosca)": "#efe4c8", "url(#pEPS)": "#fff5bf", "url(#pEPSv)": "#fff5bf",
      "url(#pLana)": "#fbe2a8", "url(#pLanaV)": "#fbe2a8", "url(#pPorc)": "#cdbb9c"}

def add_fill(polys, fill, layer_fill, layer_hatch, pat_scale_mult=1.0):
    """polys: lista de shapely Polygons ya en coordenadas DXF"""
    for g in polys:
        if g.is_empty or g.area < 1e-4: continue
        ext = list(g.exterior.coords)[:-1]
        col = BG.get(fill, fill if fill.startswith("#") else None)
        if col and col.lower() not in ("#fff", "#ffffff", "none"):
            h = msp.add_hatch(color=256, dxfattribs={"layer": layer_fill}); h.set_solid_fill(color=256, rgb=rgb(col))
            h.paths.add_polyline_path(ext, is_closed=True, flags=1)
            for hole in g.interiors: h.paths.add_polyline_path(list(hole.coords)[:-1], is_closed=True)
        if fill in FILL:
            pat, sc, ang = FILL[fill]
            h = msp.add_hatch(color=256, dxfattribs={"layer": layer_hatch}); h.set_pattern_fill(pat, color=8, scale=sc * pat_scale_mult, angle=ang)
            h.paths.add_polyline_path(ext, is_closed=True, flags=1)
            for hole in g.interiors: h.paths.add_polyline_path(list(hole.coords)[:-1], is_closed=True)

D = json.load(open("build/final_dx.json"))
for lo, hi, top in BANDS:
    W = box(XR0, lo, XMAX, hi)
    dy = top - (1000.0 - hi / S)
    T = lambda x, y: P(PX0 + (x - XR0) / S, 1000.0 - y / S + dy)
    for e in D["DX"]:
        dash = "dasharray" in (e.get("extra") or "")
        if e["t"] == "poly":
            G = Polygon(e["pts"]).buffer(0)
            if G.is_empty or not G.intersects(W): continue
            G = G.intersection(W)
            polys = [g for g in getattr(G, "geoms", [G]) if g.geom_type == "Polygon"]
            polys = [Polygon([T(x, y) for x, y in g.exterior.coords], [[T(x, y) for x, y in r.coords] for r in g.interiors]) for g in polys]
            if e["fill"] not in ("none",):
                add_fill(polys, e["fill"], "1-CORTE-RELLENOS", "1-CORTE-RAYADOS")
            if e["stroke"] != "none" and e["sw"] > 0:
                lay = "1-CORTE-OCULTO" if dash else ("1-CORTE-ARMADURAS" if e["stroke"] == "#7a1f1f" else ("1-CORTE-VISTA" if e["stroke"] == "#444" else "1-CORTE-CONTORNOS"))
                for g in polys:
                    pl = msp.add_lwpolyline(list(g.exterior.coords)[:-1], close=True, dxfattribs={"layer": lay, "lineweight": lw(e["sw"])})
                    if dash: pl.dxf.linetype = "DASHED"; pl.dxf.ltscale = 0.08
        elif e["t"] == "pline":
            G = LineString(e["pts"]).intersection(W)
            for g in getattr(G, "geoms", [G]):
                if g.is_empty or g.geom_type != "LineString": continue
                lay = "1-CORTE-ARMADURAS" if e["stroke"] == "#7a1f1f" else ("1-CORTE-OCULTO" if dash else "1-CORTE-CONTORNOS")
                pl = msp.add_lwpolyline([T(x, y) for x, y in g.coords], dxfattribs={"layer": lay, "lineweight": lw(e["sw"])})
                if e["stroke"] not in ("#000", "#7a1f1f"): pl.rgb = rgb(e["stroke"])
                if dash: pl.dxf.linetype = "DASHED"; pl.dxf.ltscale = 0.08
        elif e["t"] == "circ":
            (cx, cy), r = e["c"], e["r"] / S
            if not (XR0 < cx < XMAX and lo < cy < hi): continue
            c = T(cx, cy)
            if e["fill"] not in ("none", "#fff"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": "1-CORTE-ARMADURAS"}); h.set_solid_fill(color=256, rgb=rgb(e["fill"]))
                h.paths.add_edge_path().add_arc(c, r, 0, 360)
            else:
                msp.add_circle(c, r, dxfattribs={"layer": "1-CORTE-CONTORNOS"})

# =============================================================== AXONOMETRÍAS (2D)
AXO_PAT = {"ha": ("ANSI31", 0.3), "hais": ("AR-CONC", 0.04), "h": ("AR-CONC", 0.03), "mort": ("AR-SAND", 0.02), "grout": ("AR-SAND", 0.015),
           "tosca": ("GRAVEL", 0.3), "tierra": ("EARTH", 0.4), "eps": ("ZIGZAG", 0.25), "lana": ("INSUL", 0.12)}
V = json.load(open("build/final_2d.json"))
for det in V["VEC2D"]:
    for f in det["faces"]:
        polys = unary_union([Polygon([(t[0], t[1]), (t[2], t[3]), (t[4], t[5])]).buffer(0.002) for t in f["tris"]])
        polys = [g for g in getattr(polys, "geoms", [polys]) if g.geom_type == "Polygon" and g.area > 1e-4]
        col = rgb(f["color"]); sh = f.get("shade", 1) or 1
        col = tuple(max(0, min(255, int(c * (sh if not f["cap"] else 1)))) for c in col)
        for g in polys:
            ext = [P(x, y) for x, y in list(g.exterior.coords)[:-1]]
            if not f["glass"]:   # sin pintar: máscara (wipeout) del color del fondo para ocultar lo que queda detrás
                msp.add_wipeout(ext, dxfattribs={"layer": "2-AXO-RELLENOS"})
            if f["cap"] and f.get("hatch") in AXO_PAT:
                pat, sc = AXO_PAT[f["hatch"]]
                h2 = msp.add_hatch(color=256, dxfattribs={"layer": "2-AXO-RAYADOS"}); h2.set_pattern_fill(pat, color=8, scale=sc)
                h2.paths.add_polyline_path(ext, is_closed=True, flags=1)
    for x0, y0, x1, y1, gl in det["edges"]:
        msp.add_line(P(x0, y0), P(x1, y1), dxfattribs={"layer": "2-AXO-ARISTAS", "lineweight": 13 if gl else 25})

# =============================================================== ANOTACIONES (SVG en mm de papel)
def num(v): return float(v) if v not in (None, "") else 0.0
def svg_elements(xml):
    xml = re.sub(r'(<[^>]*?\sfill="[^"]*")([^>]*?)\sfill="[^"]*"', r'\1\2', xml)
    root = ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">{xml}</svg>')
    for el in root:
        tag = el.tag.split("}")[1]
        if tag in ("defs", "g"): continue
        yield tag, el
def layer_for(color):
    c = (color or "#000").lower()
    return "3-REFERENCIAS" if c in ("#c0392b",) else ("3-EJES" if c == "#b03030" else "3-TEXTOS")
def draw_svg(xml, skip_rects=True):
    for tag, el in svg_elements(xml):
        a = el.attrib
        stroke = a.get("stroke", "none"); fill = a.get("fill", "#000")
        dash = "stroke-dasharray" in a
        if tag == "text":
            txt = "".join(el.itertext())
            size = num(a.get("font-size", 2)); bold = a.get("font-weight") == "bold"
            x, y = num(a.get("x")), num(a.get("y")); rot = 0
            m = re.search(r"rotate\(([-\d.]+)", a.get("transform", ""))
            if m: rot = -float(m.group(1))
            t = msp.add_text(txt, height=size * 0.72, rotation=rot, dxfattribs={"layer": layer_for(fill), "style": "ARIAL-NEGRITA" if bold else "ARIAL"})
            if fill not in ("#000", "#000000"): t.rgb = rgb(fill)
            al = {"middle": TextEntityAlignment.CENTER, "end": TextEntityAlignment.RIGHT}.get(a.get("text-anchor"), TextEntityAlignment.LEFT)
            t.set_placement(P(x, y), align=al)
        elif tag == "line":
            l = msp.add_line(P(num(a["x1"]), num(a["y1"])), P(num(a["x2"]), num(a["y2"])), dxfattribs={"layer": layer_for(stroke), "lineweight": lw(num(a.get("stroke-width", 0.15)))})
            if stroke not in ("#000",): l.rgb = rgb(stroke)
            if dash: l.dxf.linetype = "DASHDOT" if stroke == "#b03030" else "DASHED"; l.dxf.ltscale = 0.12
        elif tag == "polyline":
            pts = [tuple(map(float, q.split(","))) for q in a["points"].split()]
            pl = msp.add_lwpolyline([P(*q) for q in pts], dxfattribs={"layer": layer_for(stroke), "lineweight": lw(num(a.get("stroke-width", 0.15)))})
            if stroke not in ("#000",): pl.rgb = rgb(stroke)
        elif tag == "circle":
            c = P(num(a["cx"]), num(a["cy"])); r = num(a["r"])
            if fill not in ("none", "#fff"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": layer_for(fill)}); h.set_solid_fill(color=256, rgb=rgb(fill))
                h.paths.add_edge_path().add_arc(c, r, 0, 360)
            if stroke not in ("none",):
                ci = msp.add_circle(c, r, dxfattribs={"layer": layer_for(stroke)}); ci.rgb = rgb(stroke)
        elif tag == "path":
            m = re.match(r"M([-\d.]+),([-\d.]+) l([-\d.]+),([-\d.]+) h([-\d.]+) z", a.get("d", ""))
            if m:
                x, y, dx, dy, hh = map(float, m.groups())
                pts = [P(x, y), P(x + dx, y + dy), P(x + dx + hh, y + dy)]
                h = msp.add_hatch(color=7, dxfattribs={"layer": "3-COTAS-NIVELES"}); h.set_solid_fill(color=7)
                h.paths.add_polyline_path(pts, is_closed=True)
        elif tag == "rect":
            x, y, w, hgt = (num(a.get(k)) for k in ("x", "y", "width", "height"))
            if skip_rects and w > 10: continue
            pts = [P(x, y), P(x + w, y), P(x + w, y + hgt), P(x, y + hgt)]
            if fill not in ("none", "#fff"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": "3-TEXTOS"}); h.set_solid_fill(color=256, rgb=rgb(fill)); h.paths.add_polyline_path(pts, is_closed=True)
            msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "3-TEXTOS", "lineweight": 13})

svgpart = open("build/final_corte.svgpart").read()
svgpart = svgpart[svgpart.index("</defs>") + 7:]
draw_svg(svgpart)
draw_svg(V["OVERLAY"])

# =============================================================== MARCO A3
msp.add_lwpolyline([(0, 0), (297, 0), (297, 420), (0, 420)], close=True, dxfattribs={"layer": "0-MARCO-A3", "lineweight": 13})
msp.add_lwpolyline([P(4, 4), P(293, 4), P(293, 416), P(4, 416)], close=True, dxfattribs={"layer": "0-MARCO-A3", "lineweight": 50})
doc.header["$EXTMIN"] = (0, 0, 0); doc.header["$EXTMAX"] = (297, 420, 0)
doc.set_modelspace_vport(height=430, center=(148.5, 210))
doc.saveas("build/dwg_lamina_in/Lamina_A3_vertical_Corte_y_Nudos_2D.dxf")
print("ok")
