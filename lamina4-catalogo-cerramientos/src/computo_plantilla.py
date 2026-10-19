# -*- coding: utf-8 -*-
"""Lámina 4 - Plantilla en blanco del cómputo de materiales (muros/cubierta + carpintería), A3 vertical,
para completar a mano o en AutoCAD. Mismas columnas que la planilla de referencia del curso."""
import sys, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)
W, H = 297.0, 420.0
doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
for n in ("0-MARCO", "3-TEXTOS", "3-TITULOS", "3-TABLAS"): doc.layers.add(n, color=7)

def pl(pts, layer="3-TABLAS", lw=25, close=False):
    return msp.add_lwpolyline(pts, close=close, dxfattribs={"layer": layer, "lineweight": lw})
def txt(s, x, y, h=2.5, align=TA.LEFT, layer="3-TEXTOS", bold=False):
    t = msp.add_text(s, height=h, dxfattribs={"layer": layer, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "width": 0.9})
    t.set_placement((x, y), align=align); return t
def gris(x0, y0, x1, y1):
    h = msp.add_hatch(color=254, dxfattribs={"layer": "3-TABLAS"}); h.set_solid_fill(color=254, rgb=(232, 232, 232))
    h.paths.add_polyline_path([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], is_closed=True)
def num(v, d=2):
    s = f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def tabla(x0, ytop, titulo, cols, filas, total=None, h=7.0, th=2.8):
    """cols = [(encabezado, ancho, 'l'|'c')]; encabezados de 2 líneas separados por '|'."""
    x1 = x0 + sum(c[1] for c in cols)
    filas = filas + ([total] if total else [])
    hh = 2 * h                                   # alto de la fila de encabezados
    yb = ytop - h - hh - len(filas) * h
    gris(x0, ytop - h - hh, x1, ytop)
    if total: gris(x0, yb, x1, yb + h)
    txt(titulo, (x0 + x1) / 2, ytop - h / 2, 3.0, TA.MIDDLE_CENTER, "3-TABLAS", True)
    pl([(x0, ytop - h), (x1, ytop - h)], lw=18)
    for i in range(len(filas) + 1):
        y = ytop - h - hh - i * h
        pl([(x0, y), (x1, y)], lw=35 if i in (0, len(filas)) or (total and i == len(filas) - 1) else 13)
    xx = x0
    for j, (enc, w, al) in enumerate(cols):
        if j: pl([(xx, ytop - h), (xx, yb)], lw=13)
        ls = enc.split("|")
        for k, l in enumerate(ls):
            txt(l, xx + w / 2, ytop - h - hh / 2 + (len(ls) - 1) * 1.7 - k * 3.4, th, TA.MIDDLE_CENTER, "3-TABLAS", True)
        for i, f in enumerate(filas):
            y = ytop - h - hh - (i + 0.5) * h
            bold = total is not None and i == len(filas) - 1
            if al == "c": txt(f[j], xx + w / 2, y, th, TA.MIDDLE_CENTER, "3-TABLAS", bold)
            else: txt(f[j], xx + 1.5, y, th, TA.MIDDLE_LEFT, "3-TABLAS", bold)
        xx += w
    pl([(x0, ytop), (x1, ytop), (x1, yb), (x0, yb)], lw=50, close=True)
    return yb

# ============================================================== HOJA
txt("CÓMPUTO DE MATERIALES", W / 2, 396, 8.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("LÁMINA 4  -  CATÁLOGO DE CERRAMIENTOS: VIDRIADOS Y OPACOS", W / 2, 385, 3.4, TA.MIDDLE_CENTER, "3-TITULOS")
pl([(15, 379), (W - 15, 379)], "3-TITULOS", 70)

VACIA = lambda n, k: [("",) * k for _ in range(n)]
yb = tabla(15, 370, "CÓMPUTO DE MUROS Y CUBIERTA",
           [("Material", 33, "l"), ("Ancho|del panel", 20, "c"), ("Largo|del panel", 20, "c"), ("Espesor", 18, "c"),
            ("Cantidad|de piezas", 22, "c"), ("m²|necesarios", 24, "c"), ("Metros lineales|necesarios", 32, "c"),
            ("Función", 74, "l"), ("Precio|por m²", 24, "c")],
           VACIA(19, 9), total=("TOTAL",) + ("",) * 8, h=8.0)
yb = tabla(15, yb - 16, "CÓMPUTO DE CARPINTERÍA",
           [("Material", 33, "l"), ("Ancho", 24, "c"), ("Alto", 24, "c"), ("Tipo", 52, "l"),
            ("Cantidad de|carpinterías", 36, "c"), ("m²|necesarios", 34, "c"), ("Precio|por m²", 64, "c")],
           VACIA(11, 7), total=("TOTAL",) + ("",) * 6, h=8.0)
txt("Medidas en metros.  m² = ancho x largo x cantidad  ·  metros lineales = largo x cantidad", 15, yb - 6, 2.6)

# rótulo (formato TP FINAL de la cátedra)
ry0, ry1 = 12, 26
xs = [15, 41, 170, 237, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 20.4, 3.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 19/10/2026", (xs[0] + xs[1]) / 2, 15.2, 1.8, TA.MIDDLE_CENTER)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 22.6, 2.4)
txt("ALUMNA: Candelaria Vitale", xs[1] + 2, 19.0, 2.4)
txt("GRUPO: 13", xs[1] + 2, 15.4, 2.4)
txt("NIVEL:", xs[2] + 2, 22.6, 2.4); txt("OBS:", xs[2] + 2, 19.0, 2.4)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 21.0, 2.6, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 17.0, 2.6, TA.MIDDLE_CENTER)

doc.saveas(f"{OUT}/Lamina4_Computo_Plantilla_A3.dxf")
print("ok")
