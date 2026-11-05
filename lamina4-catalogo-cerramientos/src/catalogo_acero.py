# -*- coding: utf-8 -*-
"""Catálogo de CERRAMIENTOS EN ACERO en el formato de fichas del catálogo de cerramientos (una hoja A3 vertical):
columna OPACO y columna VIDRIADO. Contenido e imágenes tomados de catalogo_cerramientos_acero_A3.pdf.
Todo en un DXF en mm de papel (escala 1:1 de la hoja); del DXF salen el PDF (imágenes insertadas con
pegar_fotos.py) y el DWG (imágenes vinculadas). Letra mínima 2 mm."""
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
FOTOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fotos_acero")
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
CONTENER = {"A-01", "A-02", "A-03", "A-04", "A-05"}
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
FILAS = ("UBICACIÓN", "MEDIDAS", "MATERIAL", "HERRAJES", "COLOR", "OBSERVACIONES")
def ficha(x, yt, w, h, cod, desc, datos):
    rd, rh, lab = 5.5, 5.2, 30.0
    xl, xr, yb = x + lab, x + w, yt - h
    img_t, img_b = yt - rd, yb + len(FILAS) * rh
    pl([(x, yt), (xr, yt), (xr, yb), (x, yb)], "3-TABLAS", 35, True)
    for y in (img_t, img_b): pl([(x, y), (xr, y)], "3-TABLAS", 25)
    for k in range(1, len(FILAS)): pl([(x, img_b - k * rh), (xr, img_b - k * rh)], "3-TABLAS", 13)
    pl([(xl, yt), (xl, img_t)], "3-TABLAS", 13); pl([(xl, img_b), (xl, yb)], "3-TABLAS", 13)
    solido([(x, img_t), (xr, img_t), (xr, yt), (x, yt)], (232, 232, 232), "3-TABLAS")
    txt("DESCRIPCIÓN", x + 1.2, yt - rd / 2, 2.4, TA.MIDDLE_LEFT, "3-TABLAS", True, lab - 1.5)
    txt(desc, xl + (w - lab) / 2, yt - rd / 2, 2.4, TA.MIDDLE_CENTER, "3-TABLAS", True, w - lab - 2)
    for k, (et, val) in enumerate(zip(FILAS, datos)):
        y = img_b - (k + 0.5) * rh
        txt(et, x + 1.2, y, 2.4, TA.MIDDLE_LEFT, "3-TABLAS", True, lab - 1.5)
        txt(val, xl + (w - lab) / 2, y, 2.4, TA.MIDDLE_CENTER, "3-TABLAS", max_ancho=(w - lab - 2) / 1.3)
    foto(cod, x + 0.8, img_b + 0.8, xr - 0.8, img_t - 0.8)

OPACO = [
    ("A-01", "PANEL SANDWICH CERRAMIENTO DE MURO",
     ("cerramiento vertical", "ancho útil 1000 mm · espesor nominal 40 mm", "panel BIG SKIN: chapa + aislación PIR/PUR",
      "tornillos autoperforantes", "gris pizarra", "U = 0,55 W/m²K · peso propio 10,30 kg/m²")),
    ("A-02", "DETALLE DE PANEL",
     ("encuentros / fijación", "según panel", "chapa conformada + EPS + foil",
      "tornillo autoperforante + capeleto", "según panel", "esquema de sellado y fijación del panel")),
]
VIDRIADO = [
    ("A-03", "CARPINTERÍA DE CHAPA GALVANIZADA",
     ("cerramiento vidriado", "según proyecto (módulo a medida)", "chapa galvanizada de 0,5 mm doblada",
      "cámara de aire según diseño", "negro", "chapa galvanizada conformada c/ cámara de aire")),
    ("A-04", "VIDRIO LAMINADO 4+4",
     ("carpintería / paños fijos", "espesor total 8 mm (4+4)", "vidrio laminado: 2 hojas float + PVB",
      "según sistema (presor, perfil, burlete)", "transparente", "mayor seguridad y control de rotura")),
    ("A-05", "DINTEL EXTERIOR",
     ("aberturas (exterior)", "chapa de 0,5 mm doblada a medida", "chapa galvanizada",
      "fijación con tornillos según diseño", "negro", "protección y terminación de la abertura")),
]

# ==================================================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO DE CERRAMIENTOS EN ACERO", W / 2, 401, 7.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("Estructura: perfiles de acero · Cerramientos: panel sandwich y carpinterías de chapa galvanizada · Vidriados: DVH 4+4 laminado",
    W / 2, 393.2, 2.0, TA.MIDDLE_CENTER, "3-TITULOS")
pl([(15, 390), (W - 15, 390)], "3-TITULOS", 70)
pl([(W / 2, 388), (W / 2, 30)], "3-TITULOS", 35)
CWID, YT, YB, GAP = (W - 30) / 2 - 2, 377.0, 30.0, 3.0
for x0, tit, fichas in ((15, "OPACO", OPACO), (W / 2 + 2, "VIDRIADO", VIDRIADO)):
    txt(tit, x0, 382.5, 4.5, TA.LEFT, "3-TITULOS", True)
    pl([(x0, 381.0), (x0 + (22 if tit == "OPACO" else 31), 381.0)], "3-TITULOS", 35)
    hf = (YT - YB - GAP * (len(fichas) - 1)) / len(fichas)
    for k, (cod, desc, datos) in enumerate(fichas):
        ficha(x0, YT - k * (hf + GAP), CWID, hf, cod, desc, datos)

# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 26
xs = [15, 41, 170, 237, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 20.4, 3.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt(f"FECHA: {FECHA}", (xs[0] + xs[1]) / 2, 15.0, 2.0, TA.MIDDLE_CENTER)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 22.6, 2.4)
txt("ALUMNA: Karen Gomez", xs[1] + 2, 19.0, 2.4)
txt("GRUPO: 13", xs[1] + 2, 15.4, 2.4)
txt("NIVEL:", xs[2] + 2, 22.6, 2.4); txt("OBS:", xs[2] + 2, 19.0, 2.4)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 21.0, 2.6, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 17.0, 2.6, TA.MIDDLE_CENTER)

import json
json.dump(RECTS, open(f"{OUT}/fotos_rects.json", "w"))
doc.saveas(f"{OUT}/Catalogo_Cerramientos_Acero_A3.dxf")
print("ok")
