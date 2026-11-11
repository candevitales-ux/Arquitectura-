# -*- coding: utf-8 -*-
"""Lámina A3 apaisada: instalación eléctrica de un edificio PB + 4 pisos (1 departamento por planta).
Esquema de montantes + esquema unifilar (acometida, CT, medidores, TP, TPSG, TS, TSG, TB, TA, TR).
Un mismo dibujo se exporta a SVG/HTML (-> PDF y PNG con Chromium) y a DXF (mm de papel, escala 1:1 de la hoja).
uso: python3 src/unifilar.py  (desde tp-electricidad/)"""
import math, os, html
import ezdxf
from ezdxf.enums import TextEntityAlignment

W, H = 420.0, 297.0
OUT = os.path.join(os.path.dirname(__file__), "..", "build")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ colores / capas
NEG = "#000000"; DEP = "#1d5fbf"; SG = "#c0392b"; PE = "#1e8a4c"; PAL = "#d77a00"; GRI = "#777777"
LAYERS = {"0-MARCO": 7, "1-ACOMETIDA": 7, "2-DEPTOS": 5, "3-SERV-GRALES": 1, "4-PE-TIERRA": 3, "5-PALIER": 30,
          "6-SIMBOLOS": 7, "7-TABLEROS": 7, "8-TEXTOS": 7, "9-EDIFICIO": 8}
COLLAY = {NEG: "1-ACOMETIDA", DEP: "2-DEPTOS", SG: "3-SERV-GRALES", PE: "4-PE-TIERRA", PAL: "5-PALIER", GRI: "9-EDIFICIO"}

doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
for n, c in LAYERS.items(): doc.layers.add(n, color=c)
msp = doc.modelspace()
svg = []

def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def P(x, y): return (x, H - y)
def lwt(w):
    for k in (13, 18, 25, 35, 50, 70, 100):
        if w * 100 <= k + 2: return k
    return 100
def attrs(col, w, layer, dash):
    a = {"layer": layer or COLLAY.get(col, "6-SIMBOLOS"), "lineweight": lwt(w)}
    if col != NEG: a["true_color"] = ezdxf.colors.rgb2int(rgb(col))
    if dash: a["linetype"] = "DASHED"; a["ltscale"] = 0.08 if dash == "pe" else 0.06
    return a
DASH = {"pe": "1.6 0.8", "box": "1.2 0.7", "fine": "0.8 0.6"}

def line(pts, col=NEG, w=0.25, dash=None, layer=None):
    svg.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.2f"%s stroke-linejoin="round"/>' % (
        " ".join("%.2f,%.2f" % p for p in pts), col, w, ' stroke-dasharray="%s"' % DASH[dash] if dash else ""))
    msp.add_lwpolyline([P(*p) for p in pts], dxfattribs=attrs(col, w, layer, dash))

def rect(x, y, w, h, col=NEG, lw=0.25, fill=None, dash=None, layer=None):
    if fill:
        svg.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" stroke="none"/>' % (x, y, w, h, fill))
        hh = msp.add_hatch(dxfattribs={"layer": layer or "7-TABLEROS"}); hh.set_solid_fill(rgb=rgb(fill))
        hh.paths.add_polyline_path([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], is_closed=True)
    if lw:
        line([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], col, lw, dash, layer)

def poly_fill(pts, fill, layer="6-SIMBOLOS"):
    svg.append('<polygon points="%s" fill="%s" stroke="none"/>' % (" ".join("%.2f,%.2f" % p for p in pts), fill))
    hh = msp.add_hatch(dxfattribs={"layer": layer}); hh.set_solid_fill(rgb=rgb(fill))
    hh.paths.add_polyline_path([P(*p) for p in pts], is_closed=True)

def circle(cx, cy, r, col=NEG, w=0.25, fill=None, layer=None):
    svg.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"/>' % (cx, cy, r, fill or "none", col, w))
    if fill:
        hh = msp.add_hatch(dxfattribs={"layer": layer or "6-SIMBOLOS"}); hh.set_solid_fill(rgb=rgb(fill))
        hh.paths.add_edge_path().add_arc(P(cx, cy), r, 0, 360)
    msp.add_circle(P(cx, cy), r, dxfattribs=attrs(col, w, layer, None))

def arc(cx, cy, r, a0, a1, col=NEG, w=0.25, layer=None):
    """ángulos en grados, sentido antihorario (con y hacia arriba)"""
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    large = 1 if ((a1 - a0) % 360) > 180 else 0
    svg.append('<path d="M%.2f,%.2f A%.2f,%.2f 0 %d 0 %.2f,%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (
        p0[0], p0[1], r, r, large, p1[0], p1[1], col, w))
    msp.add_arc(P(cx, cy), r, a0, a1, dxfattribs=attrs(col, w, layer, None))

def text(x, y, s, size=1.8, anchor="start", bold=False, rot=0, col=NEG, layer="8-TEXTOS", italic=False):
    tr = ' transform="rotate(%d %.2f %.2f)"' % (-rot, x, y) if rot else ""
    svg.append('<text x="%.2f" y="%.2f" font-size="%.2f" text-anchor="%s"%s%s fill="%s"%s>%s</text>' % (
        x, y, size * 1.43, anchor, ' font-weight="bold"' if bold else "", ' font-style="italic"' if italic else "",
        col, tr, html.escape(s)))
    al = {"start": TextEntityAlignment.LEFT, "middle": TextEntityAlignment.CENTER, "end": TextEntityAlignment.RIGHT}[anchor]
    a = {"layer": layer, "height": size, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "rotation": rot, "width": 0.9}
    if col != NEG: a["true_color"] = ezdxf.colors.rgb2int(rgb(col))
    msp.add_text(s, dxfattribs=a).set_placement(P(x, y), align=al)

def dot(x, y, col=NEG, r=0.55): circle(x, y, r, col, 0.1, fill=col)

def arrow(x, y, col=NEG, down=True):
    d = 1 if down else -1
    poly_fill([(x, y), (x - 0.9, y - 2.2 * d), (x + 0.9, y - 2.2 * d)], col)

# ------------------------------------------------------------------ símbolos (sentido de la energía: hacia abajo)
def slashes(x, y, n, col):
    for i in range(n):
        yy = y + (i - (n - 1) / 2) * 0.75
        line([(x - 1.1, yy + 0.7), (x + 1.1, yy - 0.7)], col, 0.18)

def device(x, y, kind, n, col=NEG, labels=(), lab_dx=2.8, lab_rot=False):
    """kind: PIA (termomagnético), ID (diferencial), SEC (int. manual), GM (guardamotor), K (contactor). alto = 10 mm"""
    line([(x, y), (x, y + 3)], col, 0.3)
    if kind in ("PIA", "ID", "GM"):
        line([(x - 0.7, y + 2.3), (x + 0.7, y + 3.7)], col, 0.25); line([(x - 0.7, y + 3.7), (x + 0.7, y + 2.3)], col, 0.25)
    elif kind == "SEC":
        line([(x - 0.9, y + 3), (x + 0.9, y + 3)], col, 0.25)
    elif kind == "K":
        arc(x, y + 3.6, 0.6, 0, 180, col, 0.22)
    line([(x, y + 7.2), (x - 2.3, y + 3.3)], col, 0.3)
    line([(x, y + 7.2), (x, y + 10)], col, 0.3)
    if n: slashes(x, y + 1.4, n, col)
    if kind == "ID":
        svg.append('<ellipse cx="%.2f" cy="%.2f" rx="1.8" ry="0.75" fill="none" stroke="%s" stroke-width="0.22"/>' % (x, y + 8.6, col))
        msp.add_ellipse(P(x, y + 8.6), major_axis=(1.8, 0), ratio=0.75 / 1.8, dxfattribs=attrs(col, 0.22, None, None))
        line([(x - 1.8, y + 8.6), (x - 2.4, y + 8.6), (x - 2.4, y + 6.0), (x - 1.3, y + 5.2)], col, 0.15, "fine")
    if kind == "GM":
        rect(x - 1.1, y + 7.9, 2.2, 1.5, col, 0.18)
        line([(x - 0.7, y + 8.9), (x - 0.2, y + 8.9), (x - 0.2, y + 8.4), (x + 0.4, y + 8.4)], col, 0.15)
    if lab_rot:
        for i, s in enumerate(labels):
            text(x + lab_dx + i * 2.3, y + 9.8, s, 1.55, rot=90, bold=(i == 0))
    else:
        for i, s in enumerate(labels):
            text(x + lab_dx, y + 4.6 + i * 2.4, s, 1.6, bold=(i == 0))
    return y + 10

def fuse(x, y, col=NEG):
    line([(x, y), (x, y + 2)], col, 0.3); rect(x - 1, y + 2, 2, 5, col, 0.25); line([(x, y + 2), (x, y + 7)], col, 0.18)
    line([(x, y + 7), (x, y + 9)], col, 0.3); return y + 9

def meter(x, y, tri=False, col=NEG):
    line([(x, y), (x, y + 1.5)], col, 0.3); circle(x, y + 5, 3.5, col, 0.3, fill="#ffffff")
    text(x, y + 5.0 if tri else y + 5.6, "kWh", 1.45, "middle", True)
    if tri: text(x, y + 7.2, "3~", 1.3, "middle")
    line([(x, y + 8.5), (x, y + 10)], col, 0.3); return y + 10

def motor(x, y, col=NEG, r=3.0, lab="M"):
    circle(x, y + r, r, col, 0.3, fill="#ffffff"); text(x, y + r - 0.1, lab, 1.6, "middle", True)
    text(x, y + r + 1.8, "3~", 1.2, "middle"); return y + 2 * r

def earth(x, y, col=PE):
    line([(x, y), (x, y + 2)], col, 0.3)
    for i, ww in enumerate((2.2, 1.4, 0.6)):
        line([(x - ww, y + 2 + i * 0.8), (x + ww, y + 2 + i * 0.8)], col, 0.3)

def lamp(x, y, col=NEG, r=1.5):
    circle(x, y, r, col, 0.22, fill="#ffffff")
    k = r * 0.707; line([(x - k, y - k), (x + k, y + k)], col, 0.2); line([(x - k, y + k), (x + k, y - k)], col, 0.2)

def socket(x, y, col=NEG):
    """tomacorriente: semicírculo con trazo (conexión desde arriba)"""
    line([(x, y), (x, y + 1)], col, 0.22); line([(x - 1.8, y + 1), (x + 1.8, y + 1)], col, 0.22)
    arc(x, y + 1, 1.5, 180, 360, col, 0.22)

def load_box(x, y, s, col=NEG, w=4.2):
    rect(x - w / 2, y, w, 2.8, col, 0.22, fill="#ffffff"); text(x, y + 2.05, s, 1.25, "middle", True)

def board(x, y, w=7, h=5, col=NEG, fill="#555555"):
    """símbolo de tablero (rectángulo con medio triángulo lleno)"""
    rect(x, y, w, h, col, 0.3, fill="#ffffff"); poly_fill([(x, y + h), (x + w, y), (x + w, y + h)], fill)
    rect(x, y, w, h, col, 0.3)

# =================================================================== MARCO Y TÍTULO
rect(0, 0, W, H, "#ffffff", 0, fill="#ffffff", layer="0-MARCO")
rect(10, 5, 405, 287, NEG, 0.5, layer="0-MARCO")
rect(10, 5, 405, 8.5, NEG, 0.35, layer="0-MARCO")
text(14, 11.2, "INSTALACIÓN ELÉCTRICA — ESQUEMA UNIFILAR Y DE MONTANTES", 3.4, bold=True)
text(411, 11.2, "EDIFICIO DE VIVIENDAS PB + 4 PISOS (1 DEPARTAMENTO POR PLANTA) · ASCENSOR · 3x380/220 V", 2.3, "end")

# =================================================================== 1. ESQUEMA DE MONTANTES
text(13, 19.5, "1. ESQUEMA DE MONTANTES (CORTE ESQUEMÁTICO)", 2.5, bold=True)
text(13, 23.2, "Distribución vertical: tableros, montantes y alimentaciones", 1.6, italic=True)
LV = {"AZ": 56, "4": 87, "3": 118, "2": 149, "1": 180, "PB": 211}
NAME = {"4": "4° PISO", "3": "3° PISO", "2": "2° PISO", "1": "1° PISO", "PB": "PLANTA BAJA"}
X0, X1 = 23, 113            # fachada (L.M.) / medianera
# losas
for k, y in LV.items():
    rect(X0, y, X1 - X0, 1.3, GRI, 0.15, fill="#c9c9c9", layer="9-EDIFICIO")
line([(X0, 211), (X0, 56)], GRI, 0.35); line([(X1, 211), (X1, 56)], GRI, 0.35)
line([(X0, 56), (X0, 52.5)], GRI, 0.35); line([(X1, 56), (X1, 52.5)], GRI, 0.35)      # carga
line([(12, 211), (X0, 211)], GRI, 0.35); line([(12, 212.3), (X1 + 3, 212.3)], GRI, 0.15)  # vereda / terreno
text(13, 215.0, "vereda", 1.3, col=GRI, italic=True)
text(X0 + 0.6, 223.5, "L.M.", 1.3, col=GRI, italic=True)
line([(X0, 212.3), (X0, 225)], GRI, 0.12, "fine")
# niveles
for k, y in LV.items():
    lvl = {"AZ": "+15,00", "4": "+12,00", "3": "+9,00", "2": "+6,00", "1": "+3,00", "PB": "±0,00"}[k]
    poly_fill([(15, y), (14, y - 1.4), (16, y - 1.4)], NEG); line([(13, y), (21, y)], NEG, 0.15)
    text(16.8, y - 0.5, lvl, 1.3)
# montante (plenum) y hueco de ascensor
rect(40, 57.3, 19, 153.7, GRI, 0.2, dash="box", layer="9-EDIFICIO")
text(39, 117.5, "MONTANTE ELÉCTRICO", 1.4, "middle", rot=90, col=GRI)
rect(76, 57.3, 16, 153.7, GRI, 0.25, fill="#f2f2f2", layer="9-EDIFICIO")
rect(78, 132, 12, 15, GRI, 0.25, fill="#e2e2e2", layer="9-EDIFICIO")
text(84, 141, "cabina", 1.3, "middle", col=GRI, italic=True)
text(84, 110, "HUECO ASCENSOR", 1.4, "middle", rot=90, col=GRI)
for yy in (60, 205): line([(80, yy), (80, 132)] if yy == 60 else [(80, 147), (80, yy)], GRI, 0.12, "fine")
# azotea: sala de máquinas + tanque de reserva
rect(72, 30, 26, 26, GRI, 0.3, fill="#fafafa", layer="9-EDIFICIO")
text(85, 33.5, "SALA DE MÁQUINAS", 1.35, "middle", True, col=GRI)
rect(25, 30, 22, 11, GRI, 0.3, fill="#dbeaf5", layer="9-EDIFICIO")
text(36, 35.0, "TANQUE DE", 1.3, "middle", True, col=GRI); text(36, 37.6, "RESERVA", 1.3, "middle", True, col=GRI)
line([(28, 41), (28, 56)], GRI, 0.2); line([(44, 41), (44, 56)], GRI, 0.2)
# nombres de plantas
for k in ("4", "3", "2", "1"):
    y = LV[k]
    text(95, y - 24, NAME[k], 1.9, bold=True); text(95, y - 21.2, "Departamento %s°" % k, 1.5)
text(94, 185.5, "PLANTA BAJA", 1.7, bold=True); text(94, 188.0, "Dpto. PB · hall", 1.35)
text(14, 40, "AZOTEA", 1.9, bold=True)

# --- acometida y CT
line([(12, 221), (20.5, 221), (20.5, 203.5)], NEG, 0.55)
text(12.5, 219.6, "acometida", 1.3, italic=True)
rect(17.5, 194, 6, 9.5, NEG, 0.35, fill="#ffffff"); text(20.5, 192.8, "CT", 1.7, "middle", True)
fuse(20.5, 194.3)
# gabinete de medidores + TP
rect(25.5, 188.5, 25, 20.5, NEG, 0.35, fill="#ffffff", layer="7-TABLEROS")
line([(23.5, 198.5), (25.5, 198.5)], NEG, 0.55)
for i in range(6):
    cx = 28.3 + i * 3.9
    circle(cx, 195.5, 1.5, DEP if i < 5 else SG, 0.22, fill="#ffffff")
    rect(cx - 1.3, 199.5, 2.6, 2.6, DEP if i < 5 else SG, 0.22, fill="#ffffff")
    line([(cx, 197), (cx, 199.5)], DEP if i < 5 else SG, 0.2)
text(38, 205.0, "GABINETE MEDIDORES", 1.15, "middle", True); text(38, 207.3, "+ TP (5) + medidor SG", 1.15, "middle")
# montantes de departamentos D1..D4
DX = {"1": 42, "2": 44, "3": 46, "4": 48}
for k, x in DX.items():
    ytsl = LV[k] - 16
    line([(x, 188.5), (x, ytsl), (36, ytsl)], DEP, 0.4)
    board(27, ytsl - 3, 9, 6, DEP, "#1d5fbf")
    text(31.5, ytsl + 5.4, "TS-%s°" % k, 1.5, "middle", True, col=DEP)
text(49.2, 70, "2x10+PE", 1.25, rot=90, col=DEP)
# TPSG
rect(51, 196, 9, 12.5, SG, 0.35, fill="#ffffff", layer="7-TABLEROS"); poly_fill([(51, 208.5), (60, 196), (60, 208.5)], SG)
rect(51, 196, 9, 12.5, SG, 0.35)
line([(50.5, 202), (51, 202)], SG, 0.4)
text(53.6, 194.8, "TPSG", 1.4, "middle", True, col=SG)
# SG -> azotea (TA y TR)
line([(58, 196), (58, 47), (76, 47)], SG, 0.4); line([(58, 45), (40, 45)], SG, 0.4)
line([(58, 45), (58, 47)], SG, 0.4)
text(60.8, 74, "a TA y TR", 1.25, rot=90, col=SG)
board(76, 44, 8, 6, SG, SG); text(80, 42.6, "TA", 1.6, "middle", True, col=SG)
line([(84, 47), (88, 47)], SG, 0.35); motor(91, 44.2, SG, 2.8)
text(85, 53.8, "máquina ascensor", 1.2, "middle", col=GRI, italic=True)
board(32, 42.5, 8, 6, SG, SG); text(36, 51.8, "TR", 1.6, "middle", True, col=SG)
line([(40, 45.5), (40, 45)], SG, 0.4)
# TSG + palieres
line([(60, 200), (63, 200)], SG, 0.4)
board(63, 196.5, 8, 6, SG, SG); text(67, 195.2, "TSG", 1.4, "middle", True, col=SG)
line([(67, 196.5), (67, LV["4"] - 27)], PAL, 0.3)
for k in ("PB", "1", "2", "3", "4"):
    yl = LV[k] - 27 if k != "PB" else 184
    line([(67, yl), (71.5, yl)], PAL, 0.25); lamp(73, yl, PAL, 1.3)
text(69.6, 178, "ilum. palieres / IE", 1.25, rot=90, col=PAL)
# TB (sala de bombas) y TS-PB (alimentación bajo contrapiso)
line([(57, 208.5), (57, 217.5), (106, 217.5), (106, 210)], SG, 0.4)
board(103, 204, 8, 6, SG, SG); text(107, 202.8, "TB", 1.4, "middle", True, col=SG)
motor(109.5, 197.6, SG, 1.6, "B")
line([(111, 207), (111.6, 207), (111.6, 199.2), (111.1, 199.2)], SG, 0.25)
line([(36, 209), (36, 215), (101, 215)], DEP, 0.4)
line([(101, 215), (101, 213)], DEP, 0.4)
line([(98, 213), (98, 199)], DEP, 0.4)
line([(98, 213), (101, 213)], DEP, 0.4)
board(94.5, 193, 8, 6, DEP, DEP); text(98.5, 191.8, "TS-PB", 1.4, "middle", True, col=DEP)
text(60, 214.4, "bajo contrapiso", 1.15, col=GRI, italic=True)
# puesta a tierra
line([(30, 209), (30, 222)], PE, 0.3, "pe"); earth(30, 222); line([(30, 225.5), (30, 228)], PE, 0.4)
text(32, 225.5, "jabalina (PE)", 1.25, col=PE)

# =================================================================== 2. UNIFILAR GENERAL
BX = 124
line([(120.5, 16), (120.5, 290)], NEG, 0.2, layer="0-MARCO")
text(BX, 19.5, "2. ESQUEMA UNIFILAR GENERAL — ACOMETIDA, MEDICIÓN, TP Y TPSG", 2.5, bold=True)
text(BX, 25.5, "RED PÚBLICA BT", 1.7, bold=True); text(BX, 28.0, "3x380/220 V · 50 Hz", 1.5)
XA = 136
line([(XA, 29.5), (XA, 46)], NEG, 0.6); slashes(XA, 36, 4, NEG)
text(XA + 2.4, 34.2, "Acometida subt.", 1.45, bold=True); text(XA + 2.4, 36.6, "3x35/16 mm²", 1.45)
text(XA + 2.4, 39.0, "Cu XLPE 1,1 kV", 1.45)
rect(127, 44, 34, 18, NEG, 0.3, dash="box", layer="7-TABLEROS")
fuse(XA, 46.5); text(XA + 2.4, 50.5, "Fusibles NH", 1.45, bold=True); text(XA + 2.4, 52.9, "3x100 A", 1.45)
line([(XA, 46), (XA, 46.5)], NEG, 0.6)
text(128.3, 48.0, "CT", 1.9, bold=True); text(XA + 2.4, 56.6, "Caja de toma (L.M.)", 1.4, italic=True)
line([(XA, 55.5), (XA, 76)], NEG, 0.6); slashes(XA, 66, 4, NEG)
text(XA + 2.4, 66.0, "L. principal", 1.45, bold=True); text(XA + 2.4, 68.4, "3x35/16 mm²", 1.45)
# barra general
line([(XA, 76), (322, 76)], NEG, 0.9)
text(XA + 2.4, 74.6, "BARRA GENERAL (gabinete de medidores)  R · S · T · N", 1.5, bold=True)
dot(XA, 76)
# datos generales
notes = ["DATOS GENERALES",
         "• Suministro trifásico 3x380/220 V – 50 Hz. Esquema de conexión a tierra TT (AEA 90364-7-771).",
         "• Acometida subterránea de la red pública a la Caja de Toma (CT) sobre línea municipal.",
         "• 5 unidades (PB a 4°): medidor monofásico 220 V + TP c/u. Servicios generales: medidor trifásico + TPSG.",
         "• Reparto de fases: PB y 3° → R · 1° y 4° → S · 2° → T · SG → R-S-T (cargas equilibradas).",
         "• Dpto. ≈ 85 m², grado de electrificación MEDIO, DPMS ≈ 7 kVA.  SG ≈ 12 kVA (ascensor 5,5 kW, bombas 2x1,1 kW).",
         "• Todo circuito lleva conductor de protección PE (verde-amarillo) unido a la barra PE y a la jabalina (R ≤ 10 Ω)."]
for i, s in enumerate(notes):
    text(170, 30 + i * 4.6, s, 1.75 if i else 2.0, bold=(i == 0))

# departamentos
DEPTS = [("PB", "R"), ("1°", "S"), ("2°", "T"), ("3°", "R"), ("4°", "S")]
for i, (nm, ph) in enumerate(DEPTS):
    c = 152 + i * 20
    dot(c, 76, DEP); line([(c, 76), (c, 80)], DEP, 0.35)
    text(c + 1.2, 79.4, "%s+N" % ph, 1.35, col=DEP)
    meter(c, 80, col=DEP); text(c + 4.3, 84.6, "Med. 1~", 1.35, col=DEP)
    rect(c - 4.5, 91.3, 19.5, 14.5, DEP, 0.3, dash="box", layer="7-TABLEROS")
    line([(c, 90), (c, 92.5)], DEP, 0.35)
    device(c, 92.5, "PIA", 2, DEP, ("PIA", "2x40 A"))
    text(c + 2.8, 104.6, "TP-%s" % nm, 1.6, bold=True, col=DEP)
    line([(c, 102.5), (c, 124)], DEP, 0.35); arrow(c, 126, DEP)
    text(c + 1.6, 125.5, "2x10+PE → TS-%s" % nm, 1.3, rot=90, col=DEP)
    line([(c + 10, 105.8), (c + 10, 110)], PE, 0.25, "pe")
# servicios generales
c = 322
dot(c, 76, SG); line([(c, 76), (c, 80)], SG, 0.4); text(c + 1.2, 79.4, "R+S+T+N", 1.35, col=SG)
meter(c, 80, True, SG); text(c + 4.3, 84.6, "Med. 3~ servicios generales", 1.35, col=SG)
rect(251, 91.3, 158, 33.7, SG, 0.3, dash="box", layer="7-TABLEROS")
text(252.5, 95.0, "TPSG", 2.0, bold=True, col=SG)
text(252.5, 97.6, "Tablero principal de", 1.35, col=SG); text(252.5, 99.8, "servicios generales", 1.35, col=SG)
line([(c, 90), (c, 92.5)], SG, 0.4)
device(c, 92.5, "PIA", 4, SG, ("IG · PIA", "4x40 A"))
line([(c, 102.5), (c, 107)], SG, 0.4)
SGX = {"TSG": 262, "TB": 312, "TA": 352, "TR": 390}
line([(262, 107), (390, 107)], SG, 0.8); dot(c, 107, SG)
OUTS = {"TSG": ("2x25 A", "2x6+PE", 2), "TB": ("4x16 A", "4x4+PE", 4), "TA": ("4x32 A", "4x10+PE", 4), "TR": ("2x16 A", "2x4+PE", 2)}
for k, x in SGX.items():
    pr, cab, n = OUTS[k]
    dot(x, 107, SG); line([(x, 107), (x, 109)], SG, 0.4)
    device(x, 109, "PIA", n, SG, ("PIA " + pr, "→ " + k))
    line([(x, 119), (x, 135)], SG, 0.4)
    text(x - 1.0, 137.5, cab, 1.3, rot=90, col=SG)
# PE / jabalina
line([(XA - 6, 110), (334, 110)], PE, 0.3, "pe")
text(XA - 5.5, 108.8, "barra PE", 1.35, col=PE)
line([(XA - 6, 110), (XA - 6, 113)], PE, 0.3); earth(XA - 6, 113)
text(XA - 3, 116.6, "Jabalina Cu-acero", 1.35, col=PE); text(XA - 3, 118.9, "Ø ¾\" x 1,5 m", 1.35, col=PE)
text(XA - 3, 121.2, "R ≤ 10 Ω", 1.35, col=PE)
line([(334, 110), (334, 113)], PE, 0.25, "pe")

# =================================================================== 3. TS TÍPICO DEPARTAMENTO
line([(BX - 3.5, 128.5), (412, 128.5)], NEG, 0.2, layer="0-MARCO")
text(BX, 133, "3. TS TÍPICO DE DEPARTAMENTO (PB a 4°) — 1~ 220 V", 2.3, bold=True, col=DEP)
X = 132
arrow(X, 137.5, DEP); line([(X, 135.4), (X, 140)], DEP, 0.35)
text(X + 2.2, 138.6, "desde TP · 2x10+PE mm²", 1.45, col=DEP)
device(X, 140, "SEC", 2, DEP, ("IG · int. manual", "2x40 A"))
device(X, 150, "ID", 2, DEP, ("ID · diferencial", "2x40 A · 30 mA"))
line([(X, 160), (X, 163)], DEP, 0.35)
CIRC = [("C1", "IUG", "Ilum. estar-comedor, cocina, hall, balcón", "PIA 2x10 A", "2x1,5+PE 1,5", "lamp"),
        ("C2", "IUG", "Ilum. dormitorios, baño, lavadero", "PIA 2x10 A", "2x1,5+PE 1,5", "lamp"),
        ("C3", "TUG", "Tomas estar-comedor y dormitorios", "PIA 2x16 A", "2x2,5+PE 2,5", "sock"),
        ("C4", "TUG", "Tomas cocina, lavadero y baño", "PIA 2x16 A", "2x2,5+PE 2,5", "sock"),
        ("C5", "TUE", "Aire acondicionado estar (3000 fg)", "PIA 2x20 A", "2x4+PE 2,5", "AA"),
        ("C6", "TUE", "Aire acond. dormitorio + termotanque", "PIA 2x20 A", "2x4+PE 2,5", "AA")]
cx0, st = 138, 19.5
line([(X, 163), (cx0 + 5 * st, 163)], DEP, 0.8); dot(X, 163, DEP)
for i, cc in enumerate(CIRC):
    x = cx0 + i * st
    dot(x, 163, DEP); line([(x, 163), (x, 165)], DEP, 0.35)
    device(x, 165, "PIA", 2, DEP, (cc[3][4:],), lab_dx=2.6)
    line([(x, 175), (x, 179.5)], DEP, 0.35)
    if cc[5] == "lamp": lamp(x, 181, DEP)
    elif cc[5] == "sock": socket(x, 179.5, DEP)
    else: load_box(x, 179.5, "AA", DEP)
    text(x, 187.0, "%s · %s" % (cc[0], cc[1]), 1.5, "middle", True, col=DEP)
# planilla de circuitos
TX = [BX, BX + 9, BX + 18, BX + 70, BX + 90, BX + 122]
ty = 189.5; rh = 4.2
hdr = ["Circ.", "Tipo", "Destino", "Protección", "Conductor Cu (mm²)"]
rect(TX[0], ty, TX[-1] - TX[0], rh, NEG, 0.2, fill="#e8eef8")
for j, s in enumerate(hdr): text(TX[j] + 1, ty + 2.9, s, 1.5, bold=True)
for i, cc in enumerate(CIRC):
    yy = ty + rh * (i + 1)
    if i % 2: rect(TX[0], yy, TX[-1] - TX[0], rh, NEG, 0, fill="#f5f7fb")
    for j, s in enumerate([cc[0], cc[1], cc[2], cc[3], cc[4]]): text(TX[j] + 1, yy + 2.9, s, 1.45)
for i in range(8): line([(TX[0], ty + rh * i), (TX[-1], ty + rh * i)], NEG, 0.15)
for x in TX: line([(x, ty), (x, ty + rh * 7)], NEG, 0.15)
text(BX, ty + rh * 7 + 3.2, "IUG: ilum. uso general · TUG: tomas uso general · TUE: tomas uso especial. Máx. 15 bocas por circuito.", 1.35, italic=True)

# =================================================================== 4. TABLEROS DE SERVICIOS GENERALES
line([(250, 128.5), (250, 232)], NEG, 0.2, layer="0-MARCO")
text(265, 131.4, "4. SECCIONALES DE", 1.9, bold=True, col=SG); text(265, 134.4, "SERV. GENERALES", 1.9, bold=True, col=SG)
def sg_board(head, title, sub, ig, idd, circs):
    """circs: lista de (x, protección, (líneas descripción), carga, segundo_dispositivo)"""
    text(head + 2.2, 138.0, title, 1.7, bold=True, col=SG); text(head + 2.2, 140.3, sub, 1.35, col=SG)
    y = 141
    device(head, y, "SEC", ig[1], SG, ("IG", ig[0])); y += 10
    if idd:
        device(head, y, "ID", idd[1], SG, ("ID", idd[0])); y += 10
    xs = [c[0] for c in circs]
    line([(head, y), (head, 163)], SG, 0.4)
    line([(min(xs + [head]), 163), (max(xs + [head]), 163)], SG, 0.8); dot(head, 163, SG)
    for (x, prot, desc, load, dev2) in circs:
        dot(x, 163, SG); line([(x, 163), (x, 164)], SG, 0.35)
        kind = "GM" if prot.startswith("GM") else "PIA"
        n = 4 if ("4x" in prot or kind == "GM") else 2
        yb = device(x, 164, kind, n, SG, (prot.replace("GM ", ""),), lab_dx=2.4, lab_rot=True)
        if dev2:
            k2, l2 = dev2
            yb = device(x, yb, k2, 0 if k2 == "K" else (4 if "4x" in l2 else 2), SG, (l2,), lab_dx=4.6 if k2 == "ID" else 2.4, lab_rot=True)
        else:
            line([(x, yb), (x, 184.5)], SG, 0.35); yb = 184.5
        line([(x, yb), (x, 186)], SG, 0.35)
        if load == "lamp": lamp(x, 187.5, SG)
        elif load == "sock": socket(x, 186, SG)
        elif load == "M": motor(x, 186, SG, 2.6)
        else: load_box(x, 186, load, SG, 5.0)
        for j, s in enumerate(desc):
            text(x - 0.3 + j * 2.3, 193.5, s, 1.4, "end", bold=(j == 0), rot=90, col=SG)

sg_board(262, "TSG", "hall PB · 1~ (R)", ("2x25 A", 2), ("2x40 A 30 mA", 2), [
    (256, "2x10 A", ("C1 IUG", "palieres y escalera", "autom. de escalera"), "lamp", None),
    (265, "2x10 A", ("C2 IUG", "hall, acceso, fachada", "fotocélula · 2x1,5"), "lamp", None),
    (274, "2x16 A", ("C3 TUG", "hall y limpieza", "2x2,5+PE"), "sock", None),
    (283, "2x10 A", ("C4 IE", "luces de emergencia", "autónomas · 2x1,5"), "IE", None),
    (292, "2x6 A", ("C5 MBTS", "portero eléctrico", "trafo 220/12 V"), "12V", None)])
sg_board(312, "TB", "sala de bombas PB · 3~", ("4x16 A", 4), ("4x25 A 30 mA", 4), [
    (303, "GM 2,5-4 A", ("B1 bomba", "elevadora 1,1 kW", "4x2,5+PE"), "M", ("K", "K1")),
    (317, "GM 2,5-4 A", ("B2 bomba", "elevadora 1,1 kW", "(alternada)"), "M", ("K", "K2")),
    (331, "2x6 A", ("C3 mando", "alternador, flotan-", "tes cisterna/TR"), "CTRL", None)])
sg_board(352, "TA", "sala máq. azotea · 3~", ("4x32 A", 4), None, [
    (347, "4x25 A", ("F ascensor", "controlador + M", "5,5 kW · 4x6+PE"), "M", ("ID", "4x40 300mA")),
    (359, "2x10 A", ("C2 IUG", "cabina, hueco", "y sala máq."), "lamp", ("ID", "2x25 30mA")),
    (371, "2x16 A", ("C3 TUG", "sala de", "máquinas"), "sock", ("ID", "2x25 30mA"))])
sg_board(390, "TR", "tanque reserva · 1~ (S)", ("2x16 A", 2), ("2x25 A 30 mA", 2), [
    (385, "2x6 A", ("C1 nivel", "control tanque", "(señal a TB)"), "CTRL", None),
    (395, "2x10 A", ("C2 IUG", "azotea y", "tanque"), "lamp", None),
    (404, "2x16 A", ("C3 TUG", "azotea"), "sock", None)])

# =================================================================== LEYENDA, ABREVIATURAS, NOTAS, RÓTULO
line([(10, 232), (415, 232)], NEG, 0.35, layer="0-MARCO")
text(13, 236.5, "REFERENCIAS — SÍMBOLOS", 2.1, bold=True)
LG = [("PIA", "Interruptor termomagnético (PIA)"), ("ID", "Interruptor diferencial (ID)"),
      ("SEC", "Interruptor manual / seccionador"), ("GM", "Guardamotor (magnetotérmico)"),
      ("K", "Contactor"), ("FUSE", "Fusible NH (caja de toma)"), ("MET", "Medidor de energía (kWh)"),
      ("MOT", "Motor trifásico (bomba / ascensor)")]
for i, (k, s) in enumerate(LG):
    col, row = i // 4, i % 4
    x, y = 16 + col * 52, 239 + row * 12.2
    if k in ("PIA", "ID", "SEC", "GM", "K"): device(x, y, k, 2 if k != "K" else 0, NEG)
    elif k == "FUSE": fuse(x, y + 0.5)
    elif k == "MET": meter(x, y)
    else: motor(x, y + 2)
    text(x + 4.5, y + 6, s, 1.55)
x0 = 120
SY = [("lamp", "Boca de iluminación (IUG)"), ("sock", "Tomacorriente (TUG)"), ("AA", "Toma uso especial (TUE)"),
      ("board", "Tablero"), ("earth", "Puesta a tierra / jabalina")]
for i, (k, s) in enumerate(SY):
    y = 240 + i * 6.6
    if k == "lamp": lamp(x0, y + 1.6)
    elif k == "sock": socket(x0, y)
    elif k == "AA": load_box(x0, y + 0.3, "AA")
    elif k == "board": board(x0 - 3, y - 0.5, 6, 4)
    else: earth(x0, y - 0.8, NEG)
    text(x0 + 4.5, y + 2.4, s, 1.55)
LN = [(NEG, 0.6, None, "Acometida / línea principal"), (DEP, 0.4, None, "Alimentación departamentos"),
      (SG, 0.4, None, "Servicios generales"), (PAL, 0.3, None, "Circuito palieres (TSG)"),
      (PE, 0.3, "pe", "Conductor de protección PE"), (NEG, 0.9, None, "Barra de tablero")]
for i, (c_, w_, d_, s) in enumerate(LN):
    y = 240 + i * 5.4
    line([(160, y + 1.4), (170, y + 1.4)], c_, w_, d_); text(172, y + 2.0, s, 1.55)
slashes(165, 274.0, 3, NEG); line([(160, 274), (170, 274)], NEG, 0.3)
text(172, 274.6, "N° de polos (trazos)", 1.55)
rect(160, 277.3, 10, 4, NEG, 0.25, dash="box"); text(172, 280.2, "Límite de tablero", 1.55)

line([(213, 232), (213, 292)], NEG, 0.2, layer="0-MARCO")
text(216, 236.5, "ABREVIATURAS", 2.1, bold=True)
AB = [("CT", "Caja de toma (fusibles de la distribuidora)"), ("TP", "Tablero principal de cada departamento"),
      ("TS", "Tablero seccional (dentro del departamento)"), ("TPSG", "Tablero principal de servicios generales"),
      ("TSG", "Tablero seccional de servicios generales"), ("TB", "Tablero de bombas (elevación de agua)"),
      ("TA", "Tablero de ascensor (sala de máquinas)"), ("TR", "Tablero del tanque de reserva (azotea)"),
      ("IG / ID", "Interruptor general / diferencial"), ("IE / MBTS", "Ilum. emergencia / muy baja tensión"),
      ("DPMS", "Demanda de potencia máx. simultánea")]
for i, (a, s) in enumerate(AB):
    y = 241 + i * 4.4
    text(216, y, a, 1.55, bold=True); text(231, y, s, 1.55)

line([(290, 232), (290, 292)], NEG, 0.2, layer="0-MARCO")
text(293, 236.5, "NOTAS", 2.1, bold=True)
NT = ["1. Cañerías embutidas de acero semipesado o PVC ignífugo;",
      "   montante en plenum registrable en palier.",
      "2. Secciones mínimas: línea principal 4 mm², circuitos",
      "   IUG 1,5 mm², TUG 2,5 mm², TUE 2,5 mm² (Cu, IRAM 247-3).",
      "3. ID 30 mA en todo circuito terminal; ID 300 mA (sel.)",
      "   en fuerza motriz del ascensor.",
      "4. Selectividad: TP 40 A > IG TS; TPSG 40 A > seccionales.",
      "5. Montante de SG alimenta TA y TR (azotea); TB y TSG",
      "   en PB. El control de nivel del TR comanda las bombas."]
for i, s in enumerate(NT): text(293, 241 + i * 3.7, s, 1.45)

rect(353, 268, 62, 24, NEG, 0.35, layer="0-MARCO")
text(355, 272.5, "INSTALACIONES — ELECTRICIDAD", 1.8, bold=True)
text(355, 276.3, "Esquema unifilar · edificio PB + 4 pisos", 1.5)
line([(353, 278.2), (415, 278.2)], NEG, 0.2)
text(355, 281.6, "Lámina: E-01", 1.5, bold=True); text(388, 281.6, "Escala: S/E", 1.5)
text(355, 285.4, "Hoja: A3 apaisada", 1.5); text(388, 285.4, "Fecha: 11/11/2026", 1.5)
text(355, 289.3, "Norma: AEA 90364-7-771", 1.5)

# =================================================================== salida
body = "\n".join(svg)
svgdoc = ('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
          'font-family="Arial, Liberation Sans, Helvetica, sans-serif">\n%s\n</svg>' % body)
open(os.path.join(OUT, "unifilar.svg"), "w").write(svgdoc)
open(os.path.join(OUT, "unifilar.html"), "w").write(
    '<!doctype html><html><head><meta charset="utf-8"><style>@page{size:420mm 297mm;margin:0}html,body{margin:0}'
    'svg{display:block}</style></head><body>%s<script>window.READY=true</script></body></html>' % svgdoc)
doc.saveas(os.path.join(OUT, "ESQUEMA_UNIFILAR_A3.dxf"))
print("ok", len(svg), "elementos")
