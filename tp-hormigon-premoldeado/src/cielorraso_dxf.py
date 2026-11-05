# -*- coding: utf-8 -*-
"""Cielorraso técnico steel frame -> DXF para AutoCAD.
1) Lámina A3 vertical 2D en mm de papel (1 unidad = 1 mm de hoja; las vistas ya están a 1:15, 1:5 y 1:10),
   capas por elemento con grosor de línea asignado (BYLAYER), rayados AutoCAD en las caras cortadas.
2) Modelo 3D del cielorraso en verdadera magnitud (mm), MESH por material, Z arriba.
uso: python3 src/cielorraso_dxf.py   (tras: node render.js src/cielorraso_bn.html build/cielorraso_bn portrait build/cielorraso_3d.json build/cielorraso_2d.json)"""
import json, subprocess, sys
import ezdxf
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon
from shapely.ops import unary_union

HP = 420.0
P = lambda x, y: (x, HP - y)          # papel SVG (y abajo) -> DXF (y arriba)
D = json.load(open("build/cielorraso_2d.json"))

doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.header["$LWDISPLAY"] = 1
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()

# capa: (color ACI, grosor en 1/100 mm)
LAYERS = {
    "A-LOSA-CORTE": (7, 50), "A-MURO-CORTE": (7, 50), "A-PLACAS-YESO": (7, 35), "A-PERFILES-GALV": (7, 25),
    "A-FIJACIONES": (7, 13), "A-JUNTAS-MASILLA": (7, 13), "A-RAYADOS": (8, 9),
    "T-MARCO-ROTULO": (7, 25), "T-TEXTOS": (7, 18), "T-REFERENCIAS": (7, 13),
}
for n, (c, w) in LAYERS.items():
    l = doc.layers.add(n, color=c); l.dxf.lineweight = w
KEY2LAY = {"insitu": "A-LOSA-CORTE", "mamp": "A-MURO-CORTE", "yeso": "A-PLACAS-YESO", "galv": "A-PERFILES-GALV",
           "steel": "A-FIJACIONES", "neo": "A-FIJACIONES", "masilla": "A-JUNTAS-MASILLA"}
HATCH = {"mamp": ("ANSI31", 0.4, 0), "insitu": ("AR-CONC", 0.06, 0)}

def lw(sw):
    for k in (9, 13, 18, 25, 35, 50, 70):
        if sw * 100 <= k + 2: return k
    return 70

# ------------------------------------------------------------- vistas (aristas visibles + rayados)
for V in D["VEC2D"]:
    for x1, y1, x2, y2, key in V["edges"]:
        if abs(x1 - x2) + abs(y1 - y2) < 0.02: continue
        msp.add_line(P(x1, y1), P(x2, y2), dxfattribs={"layer": KEY2LAY.get(key, "A-FIJACIONES")})
    groups = {}
    for c in V["caps"]:
        if c["key"] in HATCH: groups.setdefault(c["key"], []).extend(Polygon([P(t[0], t[1]), P(t[2], t[3]), P(t[4], t[5])]) for t in c["tris"])
    for key, polys in groups.items():
        U = unary_union([p.buffer(0.01) for p in polys if p.area > 1e-6]).buffer(-0.01)
        pat, sc, ang = HATCH[key]
        for g in getattr(U, "geoms", [U]):
            if g.is_empty or g.area < 0.05: continue
            h = msp.add_hatch(color=256, dxfattribs={"layer": "A-RAYADOS"}); h.set_pattern_fill(pat, color=256, scale=sc, angle=ang)
            h.paths.add_polyline_path(list(g.simplify(0.02).exterior.coords)[:-1], is_closed=True, flags=1)

# ------------------------------------------------------------- anotaciones, globos, referencias, rótulo
ALIGN = {"start": TextEntityAlignment.LEFT, "middle": TextEntityAlignment.CENTER, "end": TextEntityAlignment.RIGHT}
for a in json.loads(D["OVERLAY"]):
    if a["k"] == "t":
        t = msp.add_text(a["s"], height=round(a["size"] * 0.72, 2),
                         dxfattribs={"layer": "T-TEXTOS", "style": "ARIAL-NEGRITA" if a["b"] else "ARIAL"})
        t.set_placement(P(a["x"], a["y"]), align=ALIGN[a["a"]])
    elif a["k"] == "pl":
        lay = "T-REFERENCIAS" if a.get("ref") else "T-MARCO-ROTULO"
        msp.add_lwpolyline([P(*q) for q in a["p"]], close=bool(a.get("c")), dxfattribs={"layer": lay, "lineweight": lw(a["sw"])})
    elif a["k"] == "ci":
        msp.add_circle(P(a["x"], a["y"]), a["r"], dxfattribs={"layer": "T-REFERENCIAS", "lineweight": lw(a["sw"])})
    elif a["k"] == "dot":
        h = msp.add_hatch(color=256, dxfattribs={"layer": "T-REFERENCIAS"}); h.set_solid_fill(color=256)
        h.paths.add_edge_path().add_arc(P(a["x"], a["y"]), a["r"], 0, 360)

doc.set_modelspace_vport(height=430, center=(148.5, 210))
OUT2 = "build/dwg_in/CIELORRASO_STEEL_FRAME_A3_vertical.dxf"
doc.saveas(OUT2); print("ok", OUT2)

# ------------------------------------------------------------- modelo 3D (reutiliza el exportador de las láminas 3D)
OUT3 = "build/dwg_in/CIELORRASO_STEEL_FRAME_modelo_3D.dxf"
subprocess.run([sys.executable, "src/dxf_detalles3d.py", "build/cielorraso_3d.json", OUT3,
                "CIELORRASO TECNICO SUSPENDIDO STEEL FRAME - modelo 3D (mm, verdadera magnitud, Z arriba)"], check=True)
print("ok", OUT3)
