# -*- coding: utf-8 -*-
"""Lámina 4 - Catálogo de cerramientos en formato FICHAS CON FOTOS (estilo catálogo de productos), una hoja A3 vertical:
columna OPACO (panel liso de H°A con alma de EPS, vertical, Astori) y columna VIDRIADO (muro cortina stick),
sobre la estructura común (columnas, VL, viga L de borde, losa SHAP, fundación).
Cada ficha: descripción, denominación, foto real de referencia del componente (Wikimedia Commons, ver
fotos/CREDITOS_FOTOS.txt; con --dibujos se usan los dibujos 3D), ubicación, medidas, material, herrajes, color y
observaciones. Todo en un DXF en mm de papel (escala 1:1 de la hoja); del DXF salen el PDF y el DWG.
Letra mínima 2 mm."""
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
FOTOS = "--dibujos" not in sys.argv
FOTOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fotos")
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

# ------------------------------------------------------------------ dibujo 3D (perspectiva caballera)
KX, KY = math.cos(math.radians(30)) * 0.6, math.sin(math.radians(30)) * 0.6
def P(u, v, w): return (u + w * KX, v + w * KY)

def ccw(poly):
    a = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    return poly if a > 0 else list(reversed(poly))

def prisma(perfil, w0, w1, rgb, huecos=(), pat=None, lw=18):
    """Extrusión del perfil (plano u-v) entre w0 y w1: caras laterales visibles + tapa frontal (w0)."""
    perfil = ccw(perfil); n = len(perfil); caras = []
    for i in range(n):
        (ua, va), (ub, vb) = perfil[i], perfil[(i + 1) % n]
        nx, ny = vb - va, -(ub - ua)
        if nx * KX + ny * KY > 1e-9:
            f = [P(ua, va, w0), P(ub, vb, w0), P(ub, vb, w1), P(ua, va, w1)]
            caras.append((((ua + ub) / 2) * KX + ((va + vb) / 2) * KY, f, nx * KX + ny * KY))
    for _, f, luz in sorted(caras, key=lambda c: -c[0]):
        k = 0.86 if luz > 0.4 * math.hypot(KX, KY) else 0.93            # sombreado simple de las caras
        solido(f, tuple(int(c * k) for c in rgb)); pl(f, lw=13, close=True)
    tapa = [P(u, v, w0) for u, v in perfil]
    solido(tapa, rgb)
    if pat: rayado(tapa, *pat)
    pl(tapa, lw=lw, close=True)
    for hu in huecos:
        q = [P(u, v, w0) for u, v in hu]; solido(q, (120, 120, 120)); pl(q, lw=9, close=True)

def caja(u0, u1, v0, v1, w0, w1, rgb, pat=None, lw=18):
    prisma([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], w0, w1, rgb, pat=pat, lw=lw)

def chapa(polilinea, e, w0, w1, rgb, lw=18):
    """Chapa plegada: polilínea con espesor e, extruida."""
    g = LineString(polilinea).buffer(e / 2, cap_style=2, join_style=2)
    prisma(list(g.exterior.coords)[:-1], w0, w1, rgb, lw=lw)

def circulo(cx, cy, r, n=20): return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]

def cil_v(u, w, r, v0, v1, rgb):
    """Cilindro vertical (eje v)."""
    top = [P(u + r * math.cos(t), v1, w + r * math.sin(t)) for t in [2 * math.pi * k / 20 for k in range(20)]]
    a, b = P(u - r, v0, w), P(u + r, v0, w)
    cuerpo = [a, b, (b[0], top[0][1] - (P(u + r, v1, w)[1] - b[1]) + (P(u + r, v1, w)[1] - b[1])), P(u + r, v1, w), P(u - r, v1, w)]
    cuerpo = [a, b, P(u + r, v1, w), P(u - r, v1, w)]
    solido(cuerpo, tuple(int(c * 0.88) for c in rgb)); pl(cuerpo, lw=13, close=True)
    solido(top, rgb); pl(top, lw=13, close=True)

def cil_u(v, w, r, u0, u1, rgb):
    """Cilindro horizontal (eje u) con su extremo u1 visible."""
    cuerpo = [P(u0, v - r, w), P(u1, v - r, w), P(u1, v + r, w), P(u0, v + r, w)]
    solido(cuerpo, tuple(int(c * 0.88) for c in rgb)); pl(cuerpo, lw=13, close=True)
    fin = [P(u1, v + r * math.sin(t), w + r * math.cos(t)) for t in [2 * math.pi * k / 20 for k in range(20)]]
    solido(fin, rgb); pl(fin, lw=13, close=True)

def hex_u(v, w, r, u0, u1, rgb):
    """Cabeza hexagonal / tuerca sobre el eje u."""
    caras = [P(u1, v + r * math.sin(t), w + r * math.cos(t)) for t in [math.pi / 3 * k for k in range(6)]]
    cuerpo = [P(u0, v - r, w), P(u1, v - r, w), P(u1, v + r, w), P(u0, v + r, w)]
    solido(cuerpo, tuple(int(c * 0.85) for c in rgb)); pl(cuerpo, lw=13, close=True)
    solido(caras, rgb); pl(caras, lw=13, close=True)

def colocar(ents, x0, y0, x1, y1, margen=3.0):
    """Reduce el dibujo (en mm reales) para que entre en el recuadro de la ficha y lo centra."""
    ents = [e for e in ents if e.is_alive]
    caja_ = _bbox.extents(ents)
    s = min((x1 - x0 - 2 * margen) / caja_.size.x, (y1 - y0 - 2 * margen) / caja_.size.y)
    M = Matrix44.chain(Matrix44.translate(-caja_.center.x, -caja_.center.y, 0), Matrix44.scale(s, s, 1),
                       Matrix44.translate((x0 + x1) / 2, (y0 + y1) / 2, 0))
    for e in ents:
        e.transform(M)
        if e.dxftype() == "HATCH" and e.dxf.handle in PATRONES:
            pat, esc, ang = PATRONES[e.dxf.handle]
            e.set_pattern_fill(pat, color=8, scale=esc, angle=ang)

# ------------------------------------------------------------------ colores
HA, EPSC, GALV, ALU, VID = (222, 222, 222), (250, 238, 190), (196, 202, 208), (206, 210, 214), (205, 226, 236)
ESM, NEO, SELL, LANA, MEMB = (105, 108, 114), (60, 60, 60), (95, 95, 95), (238, 214, 150), (176, 178, 182)

# ------------------------------------------------------------------ dibujos de cada componente (mm reales)
def d_panel():
    for u0, u1, c, pat in ((0, 50, HA, ("AR-CONC", 0.02)), (50, 150, EPSC, None), (150, 200, HA, ("AR-CONC", 0.02))):
        caja(u0, u1, 0, 1400, 0, 1100, c, pat)
    pl([P(175, 1400, 380), P(175, 1500, 380), P(175, 1500, 520), P(175, 1400, 520)], lw=35)       # gancho de izaje

def d_inserto():
    c = [(0, 0), (40, 0), (40, 25), (29, 25), (29, 22.5), (37.5, 22.5), (37.5, 2.5), (2.5, 2.5), (2.5, 22.5), (11, 22.5), (11, 25), (0, 25)]
    for wa in (40, 230): cil_v(20, wa, 5, -45, 0, GALV)                                            # patas de anclaje
    prisma(c, 0, 300, GALV)
    caja(8, 32, 14, 21, 120, 150, (150, 155, 160))                                                 # cabeza del bulón T
    cil_v(20, 135, 6, 21, 85, (170, 175, 180))
    caja(12, 28, 85, 95, 125, 145, (150, 155, 160))

def d_grapa():
    prisma([(0, 0), (100, 0), (100, 8), (8, 8), (8, 100), (0, 100)], 0, 80, GALV)
    ran = [P(8, 45 + 7 * math.sin(t), 40 + 20 * math.cos(t) * 0 + 0) for t in []]
    for v_ in (50,):
        s_ = [P(8, v_ - 7, 22), P(8, v_ + 7, 22), P(8, v_ + 7, 58), P(8, v_ - 7, 58)]
        solido(s_, (90, 90, 90)); pl(s_, lw=9, close=True)                                          # ranura de regulación
    cil_u(50, 40, 6, -60, 8, (170, 175, 180)); hex_u(50, 40, 10, -75, -60, (150, 155, 160))       # bulón M12 + tuerca
    s2 = [P(40, 8, 15), P(70, 8, 15), P(70, 8, 30), P(40, 8, 30)]
    solido(s2, (90, 90, 90)); pl(s2, lw=9, close=True)

def d_apoyo():
    caja(0, 220, -120, 0, 0, 220, HA, ("AR-CONC", 0.02))                                           # viga de fundación (corte)
    caja(30, 190, 0, 15, 35, 185, NEO)                                                             # neopreno
    cil_v(110, 110, 8, 15, 190, (170, 175, 180))                                                   # pasador

def d_junta():
    for s in (-1, 1):
        a, b = (s * 10, s * 160) if s > 0 else (s * 160, s * 10)
        caja(a, b, 150, 200, 0, 300, HA, ("AR-CONC", 0.02)); caja(a, b, 50, 150, 0, 300, EPSC); caja(a, b, 0, 50, 0, 300, HA, ("AR-CONC", 0.02))
    for y0 in (0, 188):
        caja(-10, 10, y0, y0 + 12, 0, 300, SELL)
    for yc in (24, 176):
        prisma(circulo(0, yc, 11), 0, 300, (235, 235, 235))

def d_cupertina():
    chapa([(-30, -110), (-30, 15), (235, 15), (235, -50), (248, -62)], 1.5, 0, 700, GALV)
    caja(-25, 0, -400, 0, 60, 640, HA)                                                              # coronamiento del panel (ref.)
    cil_v(100, 350, 5, 15, 40, (150, 155, 160))

def d_lana():
    caja(0, 60, 0, 500, 0, 600, LANA)
    for k in range(1, 10):
        pl([P(0, 50 * k, 0), P(30, 50 * k + 12, 0), P(60, 50 * k, 0)], lw=9)
    caja(0, 60, 500, 520, 0, 600, SELL)

def d_membrana():
    caja(0, 900, 0, 4, 0, 700, MEMB)                                                               # paño desplegado
    prisma(circulo(980, 110, 110, 24), 0, 700, MEMB)                                               # rollo
    for r in (80, 50, 20): pl([P(980 + r * math.cos(2 * math.pi * k / 24), 110 + r * math.sin(2 * math.pi * k / 24), 0) for k in range(24)], lw=9, close=True)
    chapa([(-60, 160), (-20, 160), (-20, 20)], 2, 0, 700, GALV)                                     # babeta

def tubo(ancho, alto, L):
    nariz = [(0, 0), (ancho, 0), (ancho, alto), (ancho / 2 + 6, alto), (ancho / 2 + 6, alto + 12), (ancho / 2 - 6, alto + 12), (ancho / 2 - 6, alto), (0, alto)]
    prisma(nariz, 0, L, ALU, huecos=[[(3, 3), (ancho - 3, 3), (ancho - 3, alto - 16), (3, alto - 16)],
                                     [(3, alto - 13), (ancho / 2 - 4, alto - 13), (ancho / 2 - 4, alto - 3), (3, alto - 3)],
                                     [(ancho / 2 + 4, alto - 13), (ancho - 3, alto - 13), (ancho - 3, alto - 3), (ancho / 2 + 4, alto - 3)]])

def d_montante(): tubo(50, 150, 700)
def d_travesano(): tubo(50, 120, 500)

def d_presor():
    caja(0, 50, 0, 6, 0, 450, ALU)                                                                 # presor
    chapa([(-1, 30), (-1, 50), (51, 50), (51, 30)], 2, 0, 450, (225, 228, 232))                    # tapa a presión
    for u0 in (5, 37): caja(u0, u0 + 8, -14, -8, 0, 450, NEO)                                       # burletes EPDM
    cil_v(25, 225, 3, 6, 60, (170, 175, 180))

def d_dvh():
    caja(0, 1500, 0, 2400, 0, 25, VID, ("GLASS", 3.0))
    m = [P(30, 30, 0), P(1470, 30, 0), P(1470, 2370, 0), P(30, 2370, 0)]
    pl(m, lw=13, close=True)                                                                       # separador perimetral
    for k in (0.3, 0.45):
        pl([P(1500 * k, 2400 * 0.82, 0), P(1500 * (k + 0.18), 2400 * 0.95, 0)], lw=9)

def d_spandrel():
    caja(320, 1820, 280, 1180, 160, 170, GALV)                                                     # bandeja galv.
    caja(160, 1660, 140, 1040, 90, 140, LANA)                                                      # lana mineral 50
    caja(0, 1500, 0, 900, 0, 6, ESM)                                                               # vidrio esmaltado

def d_anclaje():
    caja(-60, 260, -120, 0, 0, 240, HA, ("AR-CONC", 0.02))                                         # viga L de borde (trozo)
    c = [(0, 0), (40, 0), (40, -25), (0, -25)]
    caja(40, 200, -6, 0, 60, 200, (150, 155, 160))                                                 # riel embutido (boca)
    prisma([(0, 0), (100, 0), (100, 8), (8, 8), (8, 100), (0, 100)], 90, 170, GALV)                # grapa
    cil_v(70, 130, 6, 8, 40, (170, 175, 180))                                                      # bulón T
    cil_u(50, 130, 6, -70, 8, (170, 175, 180)); hex_u(50, 130, 10, -85, -70, (150, 155, 160))       # bulón M12

def d_dilatacion():
    caja(6, 44, 300, 720, 6, 144, (170, 175, 180))                                                 # manguito
    caja(0, 50, 0, 500, 0, 150, ALU)                                                               # montante inferior
    caja(0, 50, 520, 1000, 0, 150, ALU)                                                            # montante superior

def d_guia():
    caja(-120, 290, -150, 0, 0, 320, HA, ("AR-CONC", 0.02))                                        # viga de fundación (trozo)
    prisma([(0, 0), (156, 0), (156, 80), (153, 80), (153, 3), (3, 3), (3, 80), (0, 80)], 0, 320, ALU)
    cil_v(78, 160, 5, 3, 40, (150, 155, 160)); caja(70, 86, 3, 9, 152, 168, (150, 155, 160))
    caja(3, 153, 22, 300, 30, 290, ALU)                                                            # montante (no apoya)

# ------------------------------------------------------------------ fotos
def foto(cod, x0, y0, x1, y1):
    """Recorta la foto al recuadro (cubre todo, centrada), la guarda en OUT/fotos y la inserta como IMAGE."""
    from PIL import Image
    im = Image.open(os.path.join(FOTOS_DIR, f"{cod}.jpg")).convert("RGB")
    r = (x1 - x0) / (y1 - y0); w, h = im.size
    if w / h > r: nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    os.makedirs(f"{OUT}/fotos", exist_ok=True)
    dst = f"{OUT}/fotos/{cod}.jpg"; im.save(dst, quality=90)
    idef = doc.add_image_def(filename=f"fotos/{cod}.jpg", size_in_pixel=im.size)
    msp.add_image(idef, insert=(x0, y0), size_in_units=(x1 - x0, y1 - y0), dxfattribs={"layer": "1-DIBUJO"})
    pl([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "3-TABLAS", 13, True)
    RECTS[cod] = (x0, y0, x1, y1)

# ------------------------------------------------------------------ ficha
CW, CH = 64.0, 84.0
FILAS = ("UBICACIÓN", "MEDIDAS", "MATERIAL", "HERRAJES", "COLOR", "OBSERVACIONES")
def ficha(x, yt, cod, desc, dibujo, datos):
    rh, rd, lab = 4.4, 4.6, 24.0
    xl, xr = x + lab, x + CW
    yb = yt - CH
    img_t, img_b = yt - rd, yb + len(FILAS) * rh          # sin renglón de denominación: la foto sube
    pl([(x, yt), (xr, yt), (xr, yb), (x, yb)], "3-TABLAS", 35, True)
    for y in (img_t, img_b): pl([(x, y), (xr, y)], "3-TABLAS", 25)
    for i in range(1, len(FILAS)): pl([(x, img_b - i * rh), (xr, img_b - i * rh)], "3-TABLAS", 13)
    pl([(xl, yt), (xl, img_t)], "3-TABLAS", 13); pl([(xl, img_b), (xl, yb)], "3-TABLAS", 13)
    solido([(x, yt - rd), (xr, yt - rd), (xr, yt), (x, yt)], (232, 232, 232), "3-TABLAS")
    txt("DESCRIPCIÓN", x + 1, yt - rd / 2, 2.0, TA.MIDDLE_LEFT, "3-TABLAS", True)
    txt(desc, xl + (CW - lab) / 2, yt - rd / 2, 2.0, TA.MIDDLE_CENTER, "3-TABLAS", True, CW - lab - 1.2)
    for i, (k, val) in enumerate(zip(FILAS, datos)):
        y = img_b - (i + 0.5) * rh
        txt(k, x + 1, y, 2.0, TA.MIDDLE_LEFT, "3-TABLAS", True, lab - 1.5)
        txt(val, xl + (CW - lab) / 2, y, 2.0, TA.MIDDLE_CENTER, "3-TABLAS", max_ancho=CW - lab - 1.2)
    if FOTOS: foto(cod, x + 0.8, img_b + 0.8, xr - 0.8, img_t - 0.8)
    else: n0 = len(msp); dibujo(); colocar(list(msp)[n0:], x, img_b, xr, img_t)

OPACO = [
    ("OP-01", "PANEL PL LISO C/ ALMA EPS", d_panel,
     ("cerramiento opaco vertical", "e 0,20 · ancho 2,50 m", "H°A premoldeado + EPS 10 cm",
      "insertos + gancho de izaje", "gris hormigón visto", "Astori PL-20 · K ≈ 0,33")),
    ("OP-02", "INSERTO / RIEL DE ANCLAJE", d_inserto,
     ("panel y viga L de borde", "canal 40 x 25 mm · L 0,30 m", "acero galvanizado",
      "bulón cabeza T M12", "gris galvanizado", "embutido al hormigonar")),
    ("OP-03", "GRAPA REGULABLE", d_grapa,
     ("unión panel - viga L de borde", "L 100 x 100 x 8 · ranura 14 x 40", "acero galvanizado",
      "bulón M12 inox + arandelas", "gris galvanizado", "igual que el muro cortina")),
    ("OP-04", "APOYO INFERIOR DEL PANEL", d_apoyo,
     ("viga de fundación perimetral", "neopreno 160x150x15 · Ø16", "neopreno dureza 60 + acero",
      "pasador en vaina c/ grout", "negro", "según fabricante")),
    ("OP-05", "JUNTA ENTRE PANELES", d_junta,
     ("juntas verticales", "junta 20 mm · cordón Ø25 mm", "sellador PU / MS + cordón PE",
      "------", "gris (a elección)", "sellado en ambas caras")),
    ("OP-06", "CUPERTINA", d_cupertina,
     ("coronamiento del panel", "chapa N°22 · desarrollo 0,40 m", "chapa galvanizada plegada",
      "tornillo autoperf. c/ arandela", "gris / natural", "goterón ext. e int. · c/ 0,60 m")),
    ("OP-07", "LANA MINERAL CORTAFUEGO", d_lana,
     ("junta panel - losa SHAP", "e 20 mm · 70 kg/m³", "lana de roca", "------",
      "natural", "sellador en ambas caras")),
    ("OP-08", "MEMBRANA + BABETA", d_membrana,
     ("encuentro panel - cubierta", "rollo 1 x 10 m · e 4 mm", "membrana asfáltica c/ aluminio",
      "babeta galv. en buña + sellador", "aluminio", "con media caña de mortero")),
]
VIDRIADO = [
    ("VD-01", "MONTANTE (MULLION)", d_montante,
     ("muro cortina - vertical", "50 x 150 mm · L 4,50 m", "aluminio extruido 6063-T6",
      "grapa regulable + manguito", "anodizado natural", "colgado de cada entrepiso")),
    ("VD-02", "TRAVESAÑO", d_travesano,
     ("muro cortina - horizontal", "50 x 120 mm · L 1,50 m", "aluminio extruido 6063-T6",
      "escuadras al montante", "anodizado natural", "con drenaje y ventilación")),
    ("VD-03", "PRESOR + TAPA + BURLETES", d_presor,
     ("fijación exterior del vidrio", "presor 50x6 · tapa 50x20", "aluminio + burletes EPDM",
      "tornillo inox c/ 0,25 m", "a elección (RAL)", "tapa a presión")),
    ("VD-04", "VIDRIO DVH (VISIÓN)", d_dvh,
     ("paños de visión", "1,50 x 3,60 m · e 24,8 mm", "6 templ. + 12 + 3+3 lam. PVB",
      "calzos de apoyo", "incoloro", "U ≈ 2,8 W/m²K · Rw ≈ 36 dB")),
    ("VD-05", "SPANDREL", d_spandrel,
     ("frente de losas (h 0,90 m)", "1,50 x 0,90 m · vidrio 6 mm", "templado esmaltado + lana",
      "bandeja chapa galvanizada", "gris oscuro (esmalte)", "oculta losa SHAP y vigas")),
    ("VD-06", "ANCLAJE REGULABLE", d_anclaje,
     ("montante - viga L de borde", "L 100 x 100 x 8 · riel 40 x 25", "acero galvanizado",
      "bulón M12 inox + bulón T", "gris galvanizado", "común con el opaco")),
    ("VD-07", "JUNTA DE DILATACIÓN", d_dilatacion,
     ("unión de montantes", "junta 20 mm · manguito 0,40", "aluminio extruido",
      "tornillo en un solo extremo", "anodizado natural", "absorbe dilatación y flechas")),
    ("VD-08", "PERFIL GUÍA DE ARRANQUE", d_guia,
     ("arranque s/ viga de fundación", "U 156 x 80 mm", "aluminio extruido",
      "broca Ø9,5 x 80 + tuerca", "anodizado natural", "deslizante (no apoya)")),
]

# ==================================================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO DE CERRAMIENTOS", W / 2, 401, 7.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("Estructura común a ambos: columnas H°A 40x40 · vigas VL doble T 40x70 · viga L de borde · losa hueca SHAP h 16 · bases c/ cuello + viga de fundación",
    W / 2, 393.2, 2.0, TA.MIDDLE_CENTER, "3-TITULOS")
pl([(15, 390), (W - 15, 390)], "3-TITULOS", 70)
pl([(W / 2, 388), (W / 2, 34)], "3-TITULOS", 35)

for x0, tit, sub, fichas in ((15, "OPACO", "panel liso de H°A c/ alma de EPS, vertical (Astori) · e = 20 cm", OPACO),
                             (W / 2 + 3, "VIDRIADO", "muro cortina de aluminio tipo stick · DVH", VIDRIADO)):
    txt(tit, x0, 383, 4.5, TA.LEFT, "3-TITULOS", True)
    pl([(x0, 381.6), (x0 + 22 if tit == "OPACO" else x0 + 31, 381.6)], "3-TITULOS", 35)
    txt(sub, x0 + (25 if tit == "OPACO" else 34), 383, 2.2, TA.LEFT, "3-TITULOS")
    for i, (cod, desc, dib, datos) in enumerate(fichas):
        col, fila = i % 2, i // 2
        ficha(x0 + col * (CW + 2.5), 378 - fila * (CH + 2.4), cod, desc, dib, datos)

# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 26
xs = [15, 41, 170, 237, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 20.4, 3.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt(f"FECHA: {FECHA}", (xs[0] + xs[1]) / 2, 15.0, 2.0, TA.MIDDLE_CENTER)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 22.6, 2.4)
txt("ALUMNA: Candelaria Vitale", xs[1] + 2, 19.0, 2.4)
txt("GRUPO: 13", xs[1] + 2, 15.4, 2.4)
txt("NIVEL:", xs[2] + 2, 22.6, 2.4); txt("OBS:", xs[2] + 2, 19.0, 2.4)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 21.0, 2.6, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 17.0, 2.6, TA.MIDDLE_CENTER)

if FOTOS:
    import json, shutil
    json.dump(RECTS, open(f"{OUT}/fotos_rects.json", "w"))
    shutil.copy(os.path.join(FOTOS_DIR, "CREDITOS_FOTOS.txt"), f"{OUT}/fotos/CREDITOS_FOTOS.txt")
doc.saveas(f"{OUT}/Lamina4_Catalogo_Fichas_A3.dxf")
print("ok")
