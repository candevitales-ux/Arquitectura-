# -*- coding: utf-8 -*-
"""Lámina 3 a DXF: cada detalle es la misma geometría del corte (mm reales) recortada a su ventana,
con capas por material, rayados, globos de referencia y planilla. Plotear a 1:5."""
import json, ezdxf
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon, LineString, box

D = json.load(open("build/lamina3_dx.json"))
doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf")
msp = doc.modelspace()
LAY = {"A-HORMIGON-PREMOLDEADO": 8, "A-HORMIGON-INSITU": 33, "A-HORMIGON-SIMPLE": 9, "A-MORTERO-CARPETAS": 252, "A-AISLACION": 40,
       "A-SOLADOS": 31, "A-VIDRIO": 4, "A-ALUMINIO": 253, "A-ACERO": 250, "A-NEOPRENO-SELLADORES": 7, "A-SELLADOR-INTUMESCENTE": 1,
       "A-YESO": 254, "A-ARMADURAS": 14, "A-VISTA": 8, "A-OCULTO": 8, "A-CONTORNOS": 7, "X-REFERENCIAS": 1, "X-TEXTOS": 7, "X-MARCO": 8}
for n, c in LAY.items():
    doc.layers.add(n, color=c, linetype="DASHED" if n in ("A-OCULTO", "X-MARCO") else "CONTINUOUS")
PAT = {"url(#pHA)": ("A-HORMIGON-PREMOLDEADO", "ANSI31", 2), "url(#pHAis)": ("A-HORMIGON-INSITU", "AR-CONC", 0.3),
       "url(#pH)": ("A-HORMIGON-SIMPLE", "AR-CONC", 0.2), "url(#pMort)": ("A-MORTERO-CARPETAS", "AR-SAND", 0.15),
       "url(#pEPSv)": ("A-AISLACION", "ZIGZAG", 1.5), "url(#pLana)": ("A-AISLACION", "INSUL", 0.8), "url(#pLanaV)": ("A-AISLACION", "INSUL", 0.8)}
def solid_layer(c):
    c = c.lower()
    if c in ("#bfe3f0", "#e8f3f7", "#6f8796"): return "A-VIDRIO"
    if c in ("#9aa3ab", "#c3c9ce", "#e9e2c3"): return "A-ALUMINIO"
    if c in ("#4a4f55", "#8d959c", "#b4bac0"): return "A-ACERO"
    if c in ("#151515", "#222", "#262626", "#555", "#333", "#3c4650"): return "A-NEOPRENO-SELLADORES"
    if c == "#c0392b": return "A-SELLADOR-INTUMESCENTE"
    if c == "url(#pporc)": return "A-SOLADOS"
    if c in ("#8e2a1a",): return "A-ARMADURAS"
    if c in ("#f2f2f2",): return "A-YESO"
    return None
def rgb(h):
    h = h.lstrip("#"); h = "".join(ch * 2 for ch in h) if len(h) == 3 else h
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

OFF = {"D1": (0, 0), "D3": (1500, 0), "D2": (3000, 0)}
for det in D["DET"]:
    x0, y0, x1, y1 = det["win"]; W = box(x0, y0, x1, y1)
    ox, oy = OFF[det["id"]][0] - x0, OFF[det["id"]][1] - y0
    T = lambda p: (p[0] + ox, p[1] + oy)
    for e in D["E"]:
        dash = e.get("dash")
        if e["t"] == "poly":
            P = Polygon(e["pts"]).buffer(0)
            if P.is_empty or not P.intersects(W): continue
            G = P.intersection(W)
            geoms = getattr(G, "geoms", [G])
            for g in geoms:
                if g.geom_type != "Polygon" or g.area < 1: continue
                pts = [T(p) for p in list(g.exterior.coords)[:-1]]
                fill = e["fill"]
                lay = None
                if fill in PAT:
                    lay, pat, sc = PAT[fill]
                    h = msp.add_hatch(color=256, dxfattribs={"layer": lay}); h.set_pattern_fill(pat, color=256, scale=sc)
                    h.paths.add_polyline_path(pts, is_closed=True)
                elif fill not in ("none", "#fff", "#f7f8f9", "#eceeef", "#e3e6e8", "#e3e7ea", "#e9ecee"):
                    lay = solid_layer(fill) or "A-CONTORNOS"
                    h = msp.add_hatch(color=256, dxfattribs={"layer": lay}); h.set_solid_fill(color=256, rgb=rgb(fill) if not fill.startswith("url") else (205, 187, 156))
                    h.paths.add_polyline_path(pts, is_closed=True)
                if e["stroke"] != "none" and e["sw"] > 0:
                    ol = "A-OCULTO" if dash else ("A-VISTA" if e["stroke"] in ("#555", "#777") else (lay or "A-CONTORNOS"))
                    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": ol, "lineweight": 50 if e["sw"] >= 0.45 else 25 if e["sw"] >= 0.25 else 13})
        elif e["t"] == "pline":
            Ls = LineString(e["pts"]).intersection(W)
            for g in getattr(Ls, "geoms", [Ls]):
                if g.is_empty or g.geom_type != "LineString": continue
                lay = "A-ARMADURAS" if e["stroke"] == "#8e2a1a" else ("A-OCULTO" if dash else "A-CONTORNOS")
                msp.add_lwpolyline([T(p) for p in g.coords], dxfattribs={"layer": lay, "lineweight": 35 if e["sw"] >= 0.35 else 18})
        elif e["t"] == "circ":
            (cx, cy), r = e["c"], e["r"]
            if not (x0 < cx < x1 and y0 < cy < y1): continue
            lay = "A-ARMADURAS" if e["fill"] in ("#8e2a1a", "#000") else (solid_layer(e["fill"]) or "A-CONTORNOS")
            msp.add_circle(T((cx, cy)), r, dxfattribs={"layer": lay})
            if e["fill"] not in ("none", "#fff"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": lay}); h.set_solid_fill(color=256)
                h.paths.add_edge_path().add_arc(T((cx, cy)), r, 0, 360)
    # marco, título y referencias (texto para ploteo a 1:5: 1 mm papel = 5 unidades)
    msp.add_lwpolyline([T((x0, y0)), T((x1, y0)), T((x1, y1)), T((x0, y1))], close=True, dxfattribs={"layer": "X-MARCO"})
    t = msp.add_text(det["t"] + "  -  CORTE ESC. 1:5", height=14, dxfattribs={"layer": "X-TEXTOS", "style": "ARIAL"})
    t.set_placement(T((x0, y1 + 40)))
    refs = D["REFS"][det["id"]]
    xm = (x0 + x1) / 2
    left = sorted([r for r in refs if r[2][0] < xm], key=lambda r: -r[2][1]); right = sorted([r for r in refs if r[2][0] >= xm], key=lambda r: -r[2][1])
    for side, lst in ((-1, left), (1, right)):
        bx = (x0 - 60) if side < 0 else (x1 + 60)
        n = len(lst); ys = [y1 - 30 - k * ((y1 - y0 - 60) / max(n - 1, 1)) for k in range(n)]
        for (num, txt, (ax, ay)), by in zip(lst, ys):
            msp.add_line(T((ax, ay)), T((bx - side * 10, by)), dxfattribs={"layer": "X-REFERENCIAS"})
            msp.add_circle(T((bx, by)), 10, dxfattribs={"layer": "X-REFERENCIAS"})
            tt = msp.add_text(str(num), height=9, dxfattribs={"layer": "X-REFERENCIAS", "style": "ARIAL"})
            tt.set_placement(T((bx, by)), align=TextEntityAlignment.MIDDLE_CENTER)
    m = msp.add_mtext(r"\P".join(f"{n}. {t}" for n, t, _ in refs), dxfattribs={"layer": "X-TEXTOS", "char_height": 9, "style": "ARIAL", "width": x1 - x0})
    m.set_location(T((x0, y0 - 60)))
t = msp.add_text("LAMINA 3 - DETALLES DE UNIONES EN CORTE (ventanas del corte integral, mm reales, plotear a 1:5)", height=25, dxfattribs={"layer": "X-TEXTOS", "style": "ARIAL"})
t.set_placement((0, 1400))
doc.saveas("build/dwg_in/Lamina3_Detalles_Uniones_Corte_1-5.dxf")
print("ok")
