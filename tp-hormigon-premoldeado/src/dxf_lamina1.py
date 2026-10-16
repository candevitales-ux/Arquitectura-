# -*- coding: utf-8 -*-
"""Exporta el corte integral (Lámina 1) a DXF en escala real (1 unidad = 1 mm),
sin interrupciones, con capas por material, rayados AutoCAD, cotas asociativas
editables, niveles, referencias y planilla de referencias. Luego se convierte a DWG."""
import json, ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment

D = json.load(open("build/lamina1_dx.json"))
doc = ezdxf.new("R2018", setup=True)
doc.units = ezdxf.units.MM
msp = doc.modelspace()
doc.styles.add("ARIAL", font="arial.ttf")
for name in ("HIDDEN", "DASHDOT"):
    if name not in doc.linetypes:
        pass

# ---------------------------------------------------------------- capas
LAYERS = {
    # nombre: (color ACI, tipo de línea)
    "A-HORMIGON-PREMOLDEADO": (8, "CONTINUOUS"),
    "A-HORMIGON-INSITU": (33, "CONTINUOUS"),
    "A-HORMIGON-SIMPLE": (9, "CONTINUOUS"),
    "A-MORTERO-CARPETAS": (252, "CONTINUOUS"),
    "A-GROUT": (251, "CONTINUOUS"),
    "A-TERRENO": (32, "CONTINUOUS"),
    "A-TOSCA": (42, "CONTINUOUS"),
    "A-AISLACION-EPS": (50, "CONTINUOUS"),
    "A-AISLACION-LANA": (40, "CONTINUOUS"),
    "A-SOLADOS": (31, "CONTINUOUS"),
    "A-VIDRIO": (4, "CONTINUOUS"),
    "A-ALUMINIO": (253, "CONTINUOUS"),
    "A-ACERO": (250, "CONTINUOUS"),
    "A-NEOPRENO-SELLADORES": (7, "CONTINUOUS"),
    "A-BARRERAS-MEMBRANAS": (7, "CONTINUOUS"),
    "A-SELLADOR-INTUMESCENTE": (1, "CONTINUOUS"),
    "A-YESO-CIELORRASO": (254, "CONTINUOUS"),
    "A-ARMADURAS": (14, "CONTINUOUS"),
    "A-VISTA": (8, "CONTINUOUS"),
    "A-PROYECCION-OCULTO": (8, "DASHED"),
    "A-CONTORNOS": (7, "CONTINUOUS"),
    "A-RAYADOS": (8, "CONTINUOUS"),
    "X-EJES": (1, "DASHDOT"),
    "X-COTAS": (3, "CONTINUOUS"),
    "X-NIVELES": (7, "CONTINUOUS"),
    "X-REFERENCIAS": (1, "CONTINUOUS"),
    "X-TEXTOS": (7, "CONTINUOUS"),
    "X-ROTULO": (7, "CONTINUOUS"),
}
for n, (c, lt) in LAYERS.items():
    doc.layers.add(n, color=c, linetype=lt)

# relleno -> (capa, patrón, escala, ángulo)   escala pensada para impresión a 1:20
FILL = {
    "url(#pHA)": ("A-HORMIGON-PREMOLDEADO", "ANSI31", 8, 0),
    "url(#pHAis)": ("A-HORMIGON-INSITU", "AR-CONC", 1.2, 0),
    "url(#pH)": ("A-HORMIGON-SIMPLE", "AR-CONC", 0.8, 0),
    "url(#pMort)": ("A-MORTERO-CARPETAS", "AR-SAND", 0.6, 0),
    "url(#pHid)": ("A-MORTERO-CARPETAS", "AR-SAND", 0.4, 0),
    "url(#pGrout)": ("A-GROUT", "AR-SAND", 0.4, 0),
    "url(#pTierra)": ("A-TERRENO", "EARTH", 12, 45),
    "url(#pTosca)": ("A-TOSCA", "GRAVEL", 8, 0),
    "url(#pEPS)": ("A-AISLACION-EPS", "ZIGZAG", 6, 0),
    "url(#pEPSv)": ("A-AISLACION-EPS", "ZIGZAG", 6, 90),
    "url(#pLana)": ("A-AISLACION-LANA", "INSUL", 3, 0),
    "url(#pLanaV)": ("A-AISLACION-LANA", "INSUL", 3, 90),
    "url(#pPorc)": ("A-SOLADOS", "SOLID", 1, 0),
}
SOLID = {  # color de relleno -> (capa, rgb)
    "#9aa3ab": ("A-ALUMINIO", (154, 163, 171)), "#b9c0c6": ("A-ALUMINIO", (185, 192, 198)),
    "#bfe3f0": ("A-VIDRIO", (191, 227, 240)), "#6f8796": ("A-VIDRIO", (111, 135, 150)),
    "#3b3b3b": ("A-ACERO", (59, 59, 59)), "#333": ("A-ACERO", (51, 51, 51)),
    "#111": ("A-NEOPRENO-SELLADORES", (17, 17, 17)), "#222": ("A-NEOPRENO-SELLADORES", (34, 34, 34)),
    "#000": ("A-BARRERAS-MEMBRANAS", (0, 0, 0)), "#8d8d8d": ("A-MORTERO-CARPETAS", (141, 141, 141)),
    "#c0392b": ("A-SELLADOR-INTUMESCENTE", (192, 57, 43)), "#f2f2f2": ("A-YESO-CIELORRASO", None),
    "#eceeef": ("A-VISTA", None), "#e3e6e8": ("A-VISTA", None), "#e3e7ea": ("A-VISTA", None), "#e9ecee": ("A-VISTA", None),
    "#fff": ("A-CONTORNOS", None), "#f6f7f8": ("A-CONTORNOS", None), "none": ("A-CONTORNOS", None),
}

def lw(sw):
    v = sw * 1.0   # mm de papel
    for k in (13, 18, 20, 25, 30, 35, 40, 50):
        if v * 100 <= k + 2: return k
    return 50

def hatch(pts, fill, hidden=False):
    if fill in FILL:
        layer, pat, sc, ang = FILL[fill]
        h = msp.add_hatch(color=256, dxfattribs={"layer": layer})
        if pat == "SOLID": h.set_solid_fill(color=256, rgb=(205, 187, 156))
        else: h.set_pattern_fill(pat, color=256, scale=sc, angle=ang)
        if hidden: h.transparency = 0.5
        h.paths.add_polyline_path(pts, is_closed=True)
        return layer
    if fill in SOLID:
        layer, rgb = SOLID[fill]
        if rgb:
            h = msp.add_hatch(color=256, dxfattribs={"layer": layer})
            h.set_solid_fill(color=256, rgb=rgb)
            h.paths.add_polyline_path(pts, is_closed=True)
        return layer
    return "A-CONTORNOS"

for e in D["DX"]:
    hidden = "dasharray" in (e.get("extra") or "")
    red = e.get("stroke") == "#7a1f1f"
    if e["t"] == "poly":
        pts = [tuple(p) for p in e["pts"]]
        layer = hatch(pts, e["fill"], hidden)
        if e["stroke"] != "none" and e["sw"] > 0:
            ol = "A-PROYECCION-OCULTO" if hidden else ("A-ARMADURAS" if red else ("A-VISTA" if e["stroke"] == "#444" else "A-CONTORNOS"))
            msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": ol, "lineweight": lw(e["sw"])})
    elif e["t"] == "pline":
        ol = "A-ARMADURAS" if red else ("A-PROYECCION-OCULTO" if hidden else "A-CONTORNOS")
        msp.add_lwpolyline([tuple(p) for p in e["pts"]], dxfattribs={"layer": ol, "lineweight": lw(e["sw"])})
    elif e["t"] == "circ":
        layer = "A-ARMADURAS"
        msp.add_circle(e["c"], e["r"], dxfattribs={"layer": layer})
        if e["fill"] not in ("#fff", "none"):
            h = msp.add_hatch(color=256, dxfattribs={"layer": layer}); h.set_solid_fill(color=256)
            h.paths.add_edge_path().add_arc(e["c"], e["r"], 0, 360)

# ---------------------------------------------------------------- anotaciones (texto en mm reales para ploteo 1:20)
K = 20.0
def text(s, p, h, layer="X-TEXTOS", align=TextEntityAlignment.LEFT, rot=0):
    t = msp.add_text(s, height=h, rotation=rot, dxfattribs={"layer": layer, "style": "ARIAL"})
    t.set_placement(p, align=align)
    return t

# eje de columna
msp.add_line((100, -2300), (100, 10150), dxfattribs={"layer": "X-EJES", "ltscale": 20})
msp.add_circle((100, 10220), 70, dxfattribs={"layer": "X-EJES"})
text("C", (100, 10220), 70, "X-EJES", TextEntityAlignment.MIDDLE_CENTER)

# niveles
for e in D["DX"]:
    if e["t"] != "nivel": continue
    x, y = e["x"], e["y"]
    msp.add_lwpolyline([(x, y), (x - 26, y + 42), (x + 26, y + 42)], close=True, dxfattribs={"layer": "X-NIVELES"})
    h = msp.add_hatch(color=256, dxfattribs={"layer": "X-NIVELES"}); h.set_solid_fill(color=256)
    h.paths.add_polyline_path([(x, y), (x - 26, y + 42), (x + 26, y + 42)], is_closed=True)
    msp.add_line((x - 80, y), (x + 80, y), dxfattribs={"layer": "X-NIVELES"})
    al = TextEntityAlignment.LEFT if e["side"] == "r" else TextEntityAlignment.RIGHT
    dx = 36 if e["side"] == "r" else -36
    if e["txt"]: text(e["txt"], (x + dx, y + 52), 42, "X-NIVELES", al)
    if e["sub"]: text(e["sub"], (x + dx, y - 50), 30, "X-NIVELES", al)

# cotas (dimensiones asociativas editables)
ds = doc.dimstyles.new("CORTE_1-20")
ds.dxf.dimtxt = 1.7; ds.dxf.dimscale = K; ds.dxf.dimasz = 1.2; ds.dxf.dimblk = "ARCHTICK"
ds.dxf.dimexo = 0.6; ds.dxf.dimexe = 0.8; ds.dxf.dimgap = 0.5; ds.dxf.dimtad = 1; ds.dxf.dimdec = 0
ds.dxf.dimtxsty = "ARIAL"; ds.dxf.dimclrd = 3; ds.dxf.dimclre = 3
for e in D["DX"]:
    if e["t"] != "cota": continue
    (ax, ay), (bx, by) = e["a"], e["b"]
    if e["v"]:
        d = msp.add_linear_dim(base=(ax, (ay + by) / 2), p1=(ax, ay), p2=(bx, by), angle=90, dimstyle="CORTE_1-20",
                               dxfattribs={"layer": "X-COTAS"})
    else:
        d = msp.add_linear_dim(base=((ax + bx) / 2, ay), p1=(ax, ay), p2=(bx, by), angle=0, dimstyle="CORTE_1-20",
                               dxfattribs={"layer": "X-COTAS"})
    if e["txt"] is not None:
        d.dimension.dxf.text = e["txt"] if e["txt"] else "<>"
    d.render()

# referencias numeradas (globos)
for e in D["DX"]:
    if e["t"] != "ref": continue
    (ax, ay), (bx, by) = e["a"], e["b"]
    r = 35
    vx, vy = ax - bx, ay - by; L = max((vx ** 2 + vy ** 2) ** .5, 1)
    msp.add_line((ax, ay), (bx + vx / L * r, by + vy / L * r), dxfattribs={"layer": "X-REFERENCIAS"})
    msp.add_circle((ax, ay), 7, dxfattribs={"layer": "X-REFERENCIAS"})
    msp.add_circle((bx, by), r, dxfattribs={"layer": "X-REFERENCIAS"})
    text(str(e["n"]), (bx, by), 34, "X-REFERENCIAS", TextEntityAlignment.MIDDLE_CENTER)

for e in D["DX"]:
    if e["t"] == "text":
        text(e["s"], tuple(e["p"]), e["h"])

# títulos
text("CORTE INTEGRAL - FACHADA VIDRIADA - HORMIGON PREMOLDEADO DE GRANDES LUCES   ESC. 1:20", (-1100, 10500), 80, "X-TEXTOS")
text("Dibujo en verdadera magnitud (1 unidad = 1 mm). Plotear a 1:20. En la lamina PDF las alturas de vidrio se interrumpen para entrar en A3.",
     (-1100, 10380), 35, "X-TEXTOS")

# planilla de referencias (MTEXT por grupos) a la derecha del corte
x0, y = 3300, 10000
for item in D["LEG"]:
    if item[1] is None:
        y -= 60
        m = msp.add_mtext(r"\L" + item[0], dxfattribs={"layer": "X-ROTULO", "char_height": 42, "style": "ARIAL", "width": 2600})
        m.set_location((x0, y)); y -= 90
        continue
    n, t = item
    m = msp.add_mtext(f"{n}.  {t}", dxfattribs={"layer": "X-ROTULO", "char_height": 32, "style": "ARIAL", "width": 2600})
    m.set_location((x0, y))
    lines = 1 + len(t) // 95
    y -= 52 * lines + 8
y -= 120
m = msp.add_mtext(r"\LNOTAS DEL SISTEMA\l" + r"\P" + r"\P".join(D["NOTAS"]), dxfattribs={"layer": "X-ROTULO", "char_height": 32, "style": "ARIAL", "width": 2700})
m.set_location((x0, y))
y -= 60 * (len(D["NOTAS"]) + 2)
# rótulo
ry = min(y - 150, -1500)
msp.add_lwpolyline([(x0 - 50, ry), (x0 + 2750, ry), (x0 + 2750, ry - 900), (x0 - 50, ry - 900)], close=True, dxfattribs={"layer": "X-ROTULO"})
rot = [("LAMINA 2 - CORTE INTEGRAL", 70), ("Sistema de hormigon premoldeado de grandes luces - Cerramiento vidriado (muro cortina stick)", 36),
       ("MATERIA: Construcciones II", 36), ("CATEDRA: Arq. ____________", 36), ("ALUMNO/A: ____________________", 36),
       ("GRUPO: ____", 36), ("ESCALA: 1:20", 36), ("HOJA: 1 de 2 - A3", 36)]
yy = ry - 120
for s, h in rot:
    text(s, (x0, yy), h, "X-ROTULO"); yy -= h * 2.4

doc.saveas("build/dwg_in/Lamina1_Corte_Integral_1-20.dxf")
print("dxf ok")
