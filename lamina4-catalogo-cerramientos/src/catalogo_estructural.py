# -*- coding: utf-8 -*-
"""Catálogo ESTRUCTURAL DE HORMIGÓN en formato fichas (mismo formato que el catálogo de cerramientos), una hoja A3
vertical. Contenido e imágenes tomados del catálogo estructural del grupo (CATALOGO_ESTRUCTURAL.pdf): panel Pi,
viga doble T, viga L, columna premoldeada, ménsula, apoyos y fundación. Todo en un DXF en mm de papel (escala 1:1
de la hoja); del DXF salen el PDF (fotos insertadas con pegar_fotos.py) y el DWG (fotos vinculadas). Letra mínima 2 mm."""
import math, sys, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA
from ezdxf.math import Matrix44
from ezdxf import bbox as _bbox
from shapely.geometry import LineString
from PIL import ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)
W, H = 297.0, 420.0
FECHA = "05/11/2026"
FOTOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fotos_estructural")
RECTS = {}   # código -> recuadro (x0, y0, x1, y1) de la foto en mm de papel, para el PDF
T_MIN = 2.0

doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
for n, c in {"0-MARCO": 7, "1-DIBUJO": 7, "1-RELLENOS": 9, "1-RAYADOS": 8, "3-TEXTOS": 7, "3-TITULOS": 7,
             "3-TABLAS": 7}.items():
    doc.layers.add(n, color=c)

def pl(pts, layer="1-DIBUJO", lw=18, close=False):
    return msp.add_lwpolyline(pts, close=close, dxfattribs={"layer": layer, "lineweight": lw})

def solido(pts, rgb, layer="1-RELLENOS"):
    h = msp.add_hatch(color=9, dxfattribs={"layer": layer}); h.set_solid_fill(color=9, rgb=rgb)
    h.paths.add_polyline_path(pts, is_closed=True)
    return h

PATRONES = {}   # handle -> (patrón, escala en la hoja) para rehacer el rayado después de reducir el dibujo
def rayado(pts, pat, esc, ang=0):
    h = msp.add_hatch(color=8, dxfattribs={"layer": "1-RAYADOS"}); h.set_pattern_fill(pat, color=8, scale=esc, angle=ang)
    h.paths.add_polyline_path(pts, is_closed=True)
    PATRONES[h.dxf.handle] = (pat, esc, ang)

_FUENTE = {b: ImageFont.truetype(f"/usr/share/fonts/truetype/liberation/LiberationSans-{'Bold' if b else 'Regular'}.ttf", 100) for b in (0, 1)}
def ancho(s, h, bold=False):
    """Ancho aproximado del texto en mm (Arial ~ Liberation Sans, factor de ancho 0,9)."""
    return _FUENTE[bool(bold)].getlength(s) / 100 * h * 0.9

def txt(s, x, y, h=2.0, align=TA.LEFT, layer="3-TEXTOS", bold=False, max_ancho=None):
    assert h >= T_MIN - 1e-9, s
    if max_ancho: assert ancho(s, h, bold) <= max_ancho, f"no entra: {s!r} ({ancho(s, h, bold):.1f} > {max_ancho:.1f} mm)"
    t = msp.add_text(s, height=h, dxfattribs={"layer": layer, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "width": 0.9})
    t.set_placement((x, y), align=align)
    return t

# ------------------------------------------------------------------ fotos
CONTENER = {"E-04", "E-06", "E-09"}
def foto(cod, x0, y0, x1, y1):
    """Recorta la foto al recuadro (cubre todo, centrada), la guarda en OUT/fotos y la inserta como IMAGE."""
    from PIL import Image
    im = Image.open(os.path.join(FOTOS_DIR, f"{cod}.jpg")).convert("RGB")
    r = (x1 - x0) / (y1 - y0); w, h = im.size
    if cod in CONTENER:                    # dibujos técnicos: se muestran completos, con fondo blanco
        nw, nh = (int(h * r), h) if w / h < r else (w, int(w / r))
        fondo = Image.new("RGB", (nw, nh), "white"); fondo.paste(im, ((nw - w) // 2, (nh - h) // 2)); im = fondo
    elif w / h > r: nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    os.makedirs(f"{OUT}/fotos", exist_ok=True)
    dst = f"{OUT}/fotos/{cod}.jpg"; im.save(dst, quality=90)
    idef = doc.add_image_def(filename=f"fotos/{cod}.jpg", size_in_pixel=im.size)
    msp.add_image(idef, insert=(x0, y0), size_in_units=(x1 - x0, y1 - y0), dxfattribs={"layer": "1-DIBUJO"})
    pl([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "3-TABLAS", 13, True)
    RECTS[cod] = (x0, y0, x1, y1)

# ------------------------------------------------------------------ ficha
CW, CH = 86.0, 116.0
NR, RH = 5, 4.6                        # renglones de texto debajo de la imagen
def renglones(texto, h, maxw):
    """Corta el texto en renglones que entran en maxw (mm)."""
    out, cur = [], ""
    for w in texto.split():
        t = (cur + " " + w).strip()
        if ancho(t, h) * 1.45 <= maxw: cur = t     # margen: el texto renderizado sale bastante más ancho que la medida
        else: out.append(cur); cur = w
    return out + [cur]

def ficha(x, yt, cod, titulo, texto):
    rd, lab = 4.8, 27.0
    xl, xr = x + lab, x + CW
    yb = yt - CH
    img_t, img_b = yt - rd, yb + NR * RH
    pl([(x, yt), (xr, yt), (xr, yb), (x, yb)], "3-TABLAS", 35, True)
    for y in (img_t, img_b): pl([(x, y), (xr, y)], "3-TABLAS", 25)
    for i in range(1, NR): pl([(x, img_b - i * RH), (xr, img_b - i * RH)], "3-TABLAS", 13)
    pl([(xl, yt), (xl, img_t)], "3-TABLAS", 13)
    solido([(x, yt - rd), (xr, yt - rd), (xr, yt), (x, yt)], (232, 232, 232), "3-TABLAS")
    txt("DESCRIPCIÓN", x + 1, yt - rd / 2, 2.2, TA.MIDDLE_LEFT, "3-TABLAS", True, lab - 1.5)
    txt(titulo, xl + (CW - lab) / 2, yt - rd / 2, 2.2, TA.MIDDLE_CENTER, "3-TABLAS", True, CW - lab - 1.2)
    lin = renglones(texto, 2.4, CW - 3)
    assert len(lin) <= NR, (cod, lin)
    for i, l in enumerate(lin):
        txt(l, x + 1.5, img_b - (i + 0.5) * RH, 2.4, TA.MIDDLE_LEFT, "3-TABLAS")
    foto(cod, x + 0.8, img_b + 0.8, xr - 0.8, img_t - 0.8)

# títulos y textos del catálogo estructural del grupo (PDF 2), con ortografía corregida
ELEMENTOS = [
    ("E-01", "PANEL PI", "Panel Pi: elemento prefabricado de 2,50 m x 10 m utilizado habitualmente para cubiertas y techos de grandes luces."),
    ("E-02", "VIGA DOBLE “T” TENSAR", "Viga tensar doble “T”: viga de alta resistencia pretensada de 0,70 m x 12 m ubicada generalmente en entrepisos y techos."),
    ("E-03", "VIGA “L”", "Viga “L”: viga con sección en forma de L, es utilizada para los apoyos de losas, paneles, viguetas; generalmente se apoya en las ménsulas de las columnas."),
    ("E-04", "COLUMNA PREMOLDEADA", "Columna premoldeada: esta columna premoldeada de hormigón está destinada a soportar y transportar todo el peso de la estructura hacia la cimentación."),
    ("E-05", "MÉNSULA", "Ménsula: la ménsula es una saliente de la columna que está destinada a soportar y recibir las cargas de las vigas."),
    ("E-06", "APOYO DE VIGA DOBLE “T”", "Ménsula: otra imagen de la ménsula donde se observa su vinculación con una viga doble T, con sus pernos de anclaje y el neopreno, que ayudan a que la viga no se caiga."),
    ("E-07", "APOYO DE VIGA “L” A COLUMNA", "Apoyo de viga “L” a columna: en esta imagen se observa cómo está colocada la viga L, ya que se requiere un correcto montaje y diseño de la transferencia de cargas."),
    ("E-08", "APOYO DEL PANEL PI", "Apoyo de panel Pi a columna: se observa con detalle cómo se vincula en la cubierta el panel Pi de marca Astori a la ménsula de la columna premoldeada."),
    ("E-09", "FUNDACIÓN", "Fundación: soporta las cargas estructurales de grandes luces, además de estar diseñada para encastrarse a la columna y asegurar su estabilidad."),
]

# ==================================================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO ESTRUCTURAL DE HORMIGÓN", W / 2, 401, 7.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("Elementos premoldeados de hormigón para grandes luces: panel Pi · vigas doble T y L · columnas c/ ménsula · apoyos · fundación",
    W / 2, 393.2, 2.0, TA.MIDDLE_CENTER, "3-TITULOS")
pl([(15, 390), (W - 15, 390)], "3-TITULOS", 70)
for i, (cod, desc, datos) in enumerate(ELEMENTOS):
    col, fila = i % 3, i // 3
    ficha(15 + col * (CW + 4.5), 386 - fila * (CH + 4.0), cod, desc, datos)

# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 26
xs = [15, 41, 170, 237, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 20.4, 3.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt(f"FECHA: {FECHA}", (xs[0] + xs[1]) / 2, 15.0, 2.0, TA.MIDDLE_CENTER)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 22.6, 2.4)
txt("ALUMNA: Azcona Karina", xs[1] + 2, 19.0, 2.4)
txt("GRUPO: 13", xs[1] + 2, 15.4, 2.4)
txt("NIVEL:", xs[2] + 2, 22.6, 2.4); txt("OBS:", xs[2] + 2, 19.0, 2.4)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 21.0, 2.6, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 17.0, 2.6, TA.MIDDLE_CENTER)

import json
json.dump(RECTS, open(f"{OUT}/fotos_rects.json", "w"))
doc.saveas(f"{OUT}/Catalogo_Estructural_Hormigon_A3.dxf")
print("ok")
