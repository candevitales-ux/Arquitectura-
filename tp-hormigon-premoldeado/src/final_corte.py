# -*- coding: utf-8 -*-
"""Lámina final - Corte integral 1:20 (A3 apaisada) + referencias + 3 nudos axonométricos. Sistema de hormigón premoldeado de grandes luces
con cerramiento vidriado (muro cortina stick).
Geometría en mm reales; x+ hacia el interior, y+ hacia arriba, ±0.00 = NPT planta baja."""
import math, os

S = 20.0                      # escala 1:20
PX0, XR0 = 9.0, -600.0        # x de papel donde cae x real -600
def X(x): return PX0 + (x - XR0) / S
def YC(y): return 1000.0 - y / S          # coordenada "continua" antes de cortar en bandas

# bandas (real lo, real hi, y papel superior)
BANDS = [(7600, 9540, 10.0), (3200, 5000, 111.0), (-2180, 1500, 205.0)]
def band_of(y):
    for lo, hi, top in BANDS:
        if lo - 1 <= y <= hi + 1: return (lo, hi, top)
    return None
def Y(y):
    lo, hi, top = band_of(y)
    return YC(y) + (top - YC(hi))

full, ann, defs = [], [], []
DX = []   # registro de entidades en coordenadas reales (para exportar a DXF/DWG)
f = lambda v: f"{v:.3f}"

def poly(pts, fill="none", stroke="#000", sw=0.3, extra="", dest=None):
    DX.append(dict(t='poly', pts=list(pts), fill=fill, stroke=stroke, sw=sw, extra=extra))
    d = " ".join(f"{f(X(x))},{f(YC(y))}" for x, y in pts)
    (dest if dest is not None else full).append(
        f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
def rect(x0, y0, x1, y1, **k): poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)
def line(x0, y0, x1, y1, stroke="#000", sw=0.18, extra=""):
    DX.append(dict(t='pline', pts=[(x0, y0), (x1, y1)], stroke=stroke, sw=sw, extra=extra))
    full.append(f'<line x1="{f(X(x0))}" y1="{f(YC(y0))}" x2="{f(X(x1))}" y2="{f(YC(y1))}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" {extra}/>')
def pline(pts, stroke="#000", sw=0.18, extra="", fill="none"):
    DX.append(dict(t='pline', pts=list(pts), stroke=stroke, sw=sw, extra=extra))
    d = " ".join(f"{f(X(x))},{f(YC(y))}" for x, y in pts)
    full.append(f'<polyline points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
def circ(x, y, r, fill="#000", stroke="none", sw=0.1):
    DX.append(dict(t='circ', c=(x, y), r=r * S, fill=fill, stroke=stroke))
    full.append(f'<circle cx="{f(X(x))}" cy="{f(YC(y))}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

CUT = dict(stroke="#000", sw=0.35)
CUTT = dict(stroke="#000", sw=0.2)
VIEW = dict(stroke="#444", sw=0.13)
HID = dict(stroke="#444", sw=0.13, extra='stroke-dasharray="1.2 0.6"')
DASH = 'stroke-dasharray="1.2 0.6"'

# ---------------------------------------------------------------- patrones
defs.append('''
<pattern id="pHA" patternUnits="userSpaceOnUse" width="1.3" height="1.3" patternTransform="rotate(45)">
 <rect width="1.3" height="1.3" fill="#d3d6d9"/><line x1="0" y1="0" x2="0" y2="1.3" stroke="#4a4f55" stroke-width="0.09"/></pattern>
<pattern id="pHAis" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)">
 <rect width="2.2" height="2.2" fill="#dedad2"/><line x1="0" y1="0" x2="0" y2="2.2" stroke="#4a4f55" stroke-width="0.09"/>
 <circle cx="1.1" cy="0.55" r="0.13" fill="#4a4f55"/><circle cx="1.4" cy="1.6" r="0.09" fill="#4a4f55"/></pattern>
<pattern id="pH" patternUnits="userSpaceOnUse" width="3" height="3">
 <rect width="3" height="3" fill="#e6e4df"/><circle cx="0.6" cy="0.7" r="0.16" fill="#666"/><circle cx="2.1" cy="1.9" r="0.12" fill="#666"/>
 <path d="M1.7 0.4 l0.35 0.55 h-0.7z" fill="none" stroke="#666" stroke-width="0.07"/><path d="M0.5 2.2 l0.3 0.45 h-0.6z" fill="none" stroke="#666" stroke-width="0.07"/>
 <circle cx="2.6" cy="0.5" r="0.07" fill="#666"/><circle cx="1.2" cy="2.7" r="0.07" fill="#666"/></pattern>
<pattern id="pMort" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
 <rect width="1.2" height="1.2" fill="#e9e9e9"/><circle cx="0.3" cy="0.3" r="0.08" fill="#777"/><circle cx="0.9" cy="0.85" r="0.06" fill="#777"/></pattern>
<pattern id="pHid" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
 <rect width="1.2" height="1.2" fill="#c9dbe6"/><circle cx="0.3" cy="0.3" r="0.08" fill="#456"/><circle cx="0.9" cy="0.85" r="0.06" fill="#456"/></pattern>
<pattern id="pGrout" patternUnits="userSpaceOnUse" width="0.8" height="0.8">
 <rect width="0.8" height="0.8" fill="#bdbdbd"/><circle cx="0.2" cy="0.2" r="0.08" fill="#333"/><circle cx="0.6" cy="0.6" r="0.08" fill="#333"/></pattern>
<pattern id="pTierra" patternUnits="userSpaceOnUse" width="6" height="6">
 <rect width="6" height="6" fill="#ece3d2"/>
 <g stroke="#8a7350" stroke-width="0.12"><line x1="0.5" y1="2" x2="2" y2="0.5"/><line x1="1.1" y1="2.3" x2="2.4" y2="1"/><line x1="1.7" y1="2.6" x2="2.8" y2="1.5"/>
 <line x1="3.5" y1="5.2" x2="5" y2="3.7"/><line x1="4.1" y1="5.5" x2="5.4" y2="4.2"/></g>
 <circle cx="4.6" cy="1.2" r="0.15" fill="#8a7350"/><circle cx="1.3" cy="4.6" r="0.15" fill="#8a7350"/></pattern>
<pattern id="pTosca" patternUnits="userSpaceOnUse" width="2" height="2">
 <rect width="2" height="2" fill="#efe4c8"/><circle cx="0.5" cy="0.5" r="0.18" fill="#9b8459"/><circle cx="1.5" cy="1.4" r="0.12" fill="#9b8459"/></pattern>
<pattern id="pEPS" patternUnits="userSpaceOnUse" width="1.6" height="1.6">
 <rect width="1.6" height="1.6" fill="#fff5bf"/><path d="M0 0.8 L0.4 0.3 L0.8 0.8 L1.2 1.3 L1.6 0.8" fill="none" stroke="#a08a1a" stroke-width="0.09"/></pattern>
<pattern id="pEPSv" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(90)">
 <rect width="1.6" height="1.6" fill="#fff5bf"/><path d="M0 0.8 L0.4 0.3 L0.8 0.8 L1.2 1.3 L1.6 0.8" fill="none" stroke="#a08a1a" stroke-width="0.09"/></pattern>
<pattern id="pLana" patternUnits="userSpaceOnUse" width="2" height="1.2">
 <rect width="2" height="1.2" fill="#fbe2a8"/><path d="M0 0.6 C0.5 0 0.5 0 1 0.6 S1.5 1.2 2 0.6" fill="none" stroke="#b07b18" stroke-width="0.09"/></pattern>
<pattern id="pLanaV" patternUnits="userSpaceOnUse" width="2" height="1.2" patternTransform="rotate(90)">
 <rect width="2" height="1.2" fill="#fbe2a8"/><path d="M0 0.6 C0.5 0 0.5 0 1 0.6 S1.5 1.2 2 0.6" fill="none" stroke="#b07b18" stroke-width="0.09"/></pattern>
<pattern id="pPorc" patternUnits="userSpaceOnUse" width="4" height="4"><rect width="4" height="4" fill="#cdbb9c"/></pattern>
''')
GLASS = "#bfe3f0"; ALU = "#9aa3ab"; STEEL = "#3b3b3b"; NEO = "#111"
def dvh(y0, y1, spandrel=False):
    if spandrel:
        rect(0, y0, 6, y1, fill="#6f8796", **CUTT)
        return
    rect(0, y0, 6, y1, fill=GLASS, **CUTT)
    rect(18, y0, 25, y1, fill=GLASS, **CUTT)
    line(21.5, y0, 21.5, y1, stroke="#333", sw=0.05)          # PVB
    for yy in (y0, y1 - 14):
        rect(6, yy, 18, yy + 14, fill=ALU, stroke="#000", sw=0.06)
    rect(6, y0, 18, y0 + 4, fill=NEO, stroke="none", sw=0); rect(6, y1 - 4, 18, y1, fill=NEO, stroke="none", sw=0)

def travesano(a, h=60, glass_below=True, glass_above=True):
    """travesaño cortado: cuerpo tubular 50x120 + adaptador + presor + tapa + burletes"""
    rect(32, a, 150, a + h, fill=ALU, **CUTT)
    rect(36, a + 4, 146, a + h - 4, fill="#fff", stroke="#000", sw=0.06)
    line(36, a + h / 2, 146, a + h / 2, stroke="#000", sw=0.06)
    rect(8, a + h / 2 - 8, 32, a + h / 2 + 8, fill=ALU, stroke="#000", sw=0.08)        # lengüeta/adaptador
    rect(-14, a - 22 if glass_below else a, -2, a + h + 22 if glass_above else a + h, fill=ALU, stroke="#000", sw=0.1)  # presor
    poly([(-30, a - 18), (-14, a - 22), (-14, a + h + 22), (-30, a + h + 18)], fill="#b9c0c6", stroke="#000", sw=0.1)  # tapa
    line(-14, a + h / 2, 70, a + h / 2, stroke="#000", sw=0.12)                        # tornillo inox
    for yy in ([a - 20] if glass_below else []) + ([a + h + 8] if glass_above else []):
        rect(-2, yy, 0, yy + 12, fill=NEO, stroke="none", sw=0)
        rect(25, yy, 30, yy + 12, fill=NEO, stroke="none", sw=0)
    if glass_above: rect(2, a + h, 24, a + h + 6, fill="#333", stroke="none", sw=0)    # calzo

# montante en vista (x 32..182) y tapa vista (x -30..-14)
def montante(y0, y1):
    rect(32, y0, 182, y1, fill="#e3e7ea", **VIEW)
    line(150, y0, 150, y1, stroke="#666", sw=0.08)
    rect(-30, y0, -14, y1, fill="#e9ecee", stroke="#666", sw=0.08)


# =====================================================================================
#  GEOMETRÍA (mm reales).  Corte por el apoyo de la VL sobre la ménsula (niveles superiores)
#  y por el eje de columna en la fundación (línea de corte quebrada a nivel ±0,00).
#  Columna x 250..650 · VL 40x70 x 250..650 · muro cortina x -32..182 · eje de columna x = 450
# =====================================================================================
REB = "#7a1f1f"

# ------------------------------------------------------------------ TERRENO Y FUNDACIÓN (corte por eje de columna)
rect(-750, -2180, 2700, -327, fill="url(#pTierra)", stroke="none", sw=0)
line(-750, -400, -56, -400, sw=0.2)
rect(-600, -2150, 1500, -2050, fill="url(#pH)", **CUTT)                                   # H° de limpieza
poly([(-550, -2050), (1450, -2050), (1450, -1750), (975, -1450), (-75, -1450), (-550, -1750)], fill="url(#pHAis)", **CUT)   # base
poly([(-75, -1450), (975, -1450), (975, -510), (725, -510), (725, -1350), (175, -1350), (175, -510), (-75, -510)], fill="url(#pHAis)", **CUT)  # cuello
rect(175, -1350, 725, -510, fill="url(#pGrout)", **CUTT)                                  # relleno cementicio
rect(250, -1300, 650, 0, fill="url(#pHA)", **CUT)                                         # tronco de columna
# armadura de base y cuello
pline([(-480, -1890), (-480, -1975), (1380, -1975), (1380, -1890)], stroke=REB, sw=0.22)
for xx in range(-450, 1400, 120): circ(xx, -1958, 0.28, fill=REB)
for xx in (-30, 120, 780, 930):
    pline([(xx + (40 if xx < 450 else -40), -1975), (xx, -1975), (xx, -560)], stroke=REB, sw=0.18)
for yy in range(-1400, -540, 140):
    pline([(-30, yy), (930, yy)], stroke=REB, sw=0.08, extra='stroke-dasharray="1.5 0.6"')
# anclaje mecánico húmedo: horquillas entrelazadas columna / cuello
for side in (0, 1):
    xc, xw = (250, 175) if side == 0 else (650, 725)
    s = -1 if side == 0 else 1
    for k, yy in enumerate(range(-1240, -560, 115)):
        pline([(xc, yy), (xc + s * 55, yy), (xc + s * 55, yy + 38), (xc + s * 15, yy + 38)], stroke=REB, sw=0.2)          # de columna
        pline([(xw, yy + 58), (xw - s * 55, yy + 58), (xw - s * 55, yy + 96), (xw - s * 15, yy + 96)], stroke=REB, sw=0.2)  # de cuello
# armadura de vinculación fundación–columna (en vainas grouteadas de la columna)
for xx in (360, 540):
    pline([(xx - 90 if xx < 450 else xx + 90, -1930), (xx, -1930), (xx, -760)], stroke=REB, sw=0.3)
    rect(xx - 18, -1300, xx + 18, -740, fill="none", stroke="#555", sw=0.1, extra=DASH)
# armadura de la columna (estribos y barras)
for xx in (290, 610): pline([(xx, -1290), (xx, -10)], stroke=REB, sw=0.12)
# caño pluvial PVC Ø110 dentro de la columna, sale hacia el interior
pline([(395, -10), (395, -330), (430, -390), (650, -400), (2700, -440)], stroke="#2b5d8a", sw=0.18)
pline([(505, -10), (505, -260), (520, -285), (650, -290), (2700, -330)], stroke="#2b5d8a", sw=0.18)
# viga perimetral portamuro (VPP) 30x50 premoldeada s/ banda de neopreno
rect(-50, -510, 250, -500, fill=NEO, stroke="none", sw=0)
poly([(-50, -500), (250, -500), (250, 0), (-20, 0), (-50, -25)], fill="url(#pHA)", **CUT)
rect(-15, -470, 215, -35, stroke=REB, sw=0.12, extra='fill="none"')
for xx in (5, 195):
    for yy in (-450, -55): circ(xx, yy, 0.3, fill=REB)
pline([(95, -300), (95, -40), (155, -40), (155, -300)], stroke=REB, sw=0.2)            # 1Ø16 / estribo de anclaje
# aislación hidrófuga vertical + vereda exterior
pline([(-56, -150), (-56, -505)], stroke="#000", sw=0.45)
rect(-750, -400, -60, -250, fill="url(#pTosca)", **CUTT)
poly([(-750, -250), (-60, -250), (-60, -150), (-750, -157)], fill="url(#pH)", **CUTT)
rect(-60, -250, -56, -150, fill=NEO, stroke="none", sw=0)
# babeta / goterón del arranque
pline([(40, 8), (-20, 4), (-64, -12), (-64, -60), (-84, -80)], stroke="#000", sw=0.3)
# piso sobre terreno (empieza en la cara de la columna: plano por eje de columna)
rect(650, -327, 2700, -177, fill="url(#pTosca)", **CUTT)
rect(650, -177, 2700, -175, fill="#000", stroke="none", sw=0)                             # film 200 µ
rect(670, -175, 2700, -55, fill="url(#pH)", **CUTT)                                       # contrapiso H° pobre
rect(670, -55, 2700, -35, fill="url(#pHid)", **CUTT)                                      # carpeta hidrófuga
rect(670, -35, 2700, -15, fill="url(#pMort)", **CUTT)                                     # carpeta niveladora
rect(675, -15, 2700, -10, fill="#8d8d8d", stroke="none", sw=0)
rect(675, -10, 2700, 0, fill="url(#pPorc)", **CUTT)
for xx in range(975, 2700, 400): line(xx, -10, xx, 0, sw=0.15)
rect(650, -175, 670, -10, fill="url(#pEPSv)", **CUTT)                                     # junta perimetral
rect(650, -10, 675, 0, fill=NEO, stroke="none", sw=0)

# ------------------------------------------------------------------ ESTRUCTURA (corte por apoyo VL / ménsula)
def columna_vista(y0, y1):
    rect(250, y0, 650, y1, fill="#eceeef", **VIEW)
    for xx in (395, 505): line(xx, y0, xx, y1, stroke="#2b5d8a", sw=0.1, extra=DASH)    # caño pluvial
def vp_vista(ytop, yb):
    rect(650, yb, 2700, ytop, fill="#e9ebed", **VIEW)
    line(650, yb + 200, 2700, yb + 200, stroke="#888", sw=0.08)                           # talón (viga T invertida)
def mensula(ytop):
    rect(250, ytop - 400, 650, ytop, fill="url(#pHA)", **CUT)
    pline([(285, ytop - 40), (615, ytop - 40)], stroke=REB, sw=0.18)
    for xx in (285, 615): circ(xx, ytop - 60, 0.3, fill=REB)
def viga_VL(yb, bulon=True):
    yt = yb + 700
    P = [(250, yb), (650, yb), (650, yb + 150), (530, yb + 210), (510, yb + 210), (510, yt - 190), (530, yt - 190), (650, yt - 130), (650, yt),
         (250, yt), (250, yt - 130), (370, yt - 190), (390, yt - 190), (390, yb + 210), (370, yb + 210), (250, yb + 150)]
    poly(P, fill="url(#pHA)", **CUT)
    for xx in (290, 370, 450, 530, 610): circ(xx, yb + 45, 0.32)                            # cordones
    for xx in (330, 570): circ(xx, yb + 100, 0.32)
    for xx in (290, 450, 610): circ(xx, yt - 45, 0.28, fill=REB)
    pline([(400, yb + 30), (400, yt - 30)], stroke=REB, sw=0.1); pline([(500, yb + 30), (500, yt - 30)], stroke=REB, sw=0.1)
    # estribos salientes 2Ø10 p/ vinculación c/ capa de compresión
    pline([(420, yt - 80), (420, yt + 40), (480, yt + 40), (480, yt - 80)], stroke=REB, sw=0.22)
    rect(250, yb - 10, 650, yb, fill=NEO, stroke="none", sw=0)                              # neopreno
    rect(440, yb - 210, 460, yb + 140, fill=STEEL, stroke="#000", sw=0.06)                 # perno de fijación Ø20
    if bulon:   # bulón pasante Ø3/4" por el alma: placa de anclaje exterior + tubo separador + arandela Ø90 y tuerca interior
        yy = yb + 350
        rect(232, yy - 60, 250, yy + 60, fill=STEEL, stroke="#000", sw=0.06)                          # placa de anclaje
        rect(250, yy - 14, 390, yy + 14, fill="#fff", stroke="#000", sw=0.08)                         # tubo separador
        rect(222, yy - 8, 548, yy + 8, fill=STEEL, stroke="#000", sw=0.06)                            # bulón Ø3/4"
        rect(510, yy - 45, 520, yy + 45, fill="#555", stroke="#000", sw=0.06)                         # arandela Ø90
        rect(520, yy - 14, 542, yy + 14, fill="#555", stroke="#000", sw=0.06)                         # tuerca
        rect(214, yy - 14, 222, yy + 14, fill="#555", stroke="#000", sw=0.06)                         # cabeza
def panel_TT(ytop, stems=(1275, 2525)):
    yf = ytop - 50
    rect(660, yf, 2700, ytop, fill="url(#pHA)", **CUT)
    for xc in stems:
        poly([(xc - 90, yf), (xc + 90, yf), (xc + 60, ytop - 600), (xc - 60, ytop - 600)], fill="url(#pHA)", **CUT)
        for yy in (ytop - 560, ytop - 500): circ(xc, yy, 0.3)
        line(xc, ytop - 590, xc, yf, stroke=REB, sw=0.1)
    rect(650, yf, 660, ytop, fill="url(#pGrout)", stroke="none", sw=0)
def capa_compresion(ytop, x0=250):
    rect(x0, ytop, 2700, ytop + 50, fill="url(#pHAis)", **CUT)
    pline([(x0 + 30, ytop + 25), (2700, ytop + 25)], stroke=REB, sw=0.12, extra='stroke-dasharray="2 0.5"')
    for xx in range(x0 + 100, 2700, 150): circ(xx, ytop + 25, 0.17, fill=REB)
def cielorraso(y, ytt):
    rect(190, y, 2700, y + 12.5, fill="#f2f2f2", **CUTT)
    for xx in range(500, 2700, 400): rect(xx, y + 12.5, xx + 35, y + 47, fill=ALU, stroke="#444", sw=0.08)
    pline([(190, y + 70), (190, y), (230, y)], stroke="#000", sw=0.2)
    for xc in (1275, 2525): line(xc, y + 47, xc, ytt - 600, stroke="#555", sw=0.15)       # gancho/vela a nervio del TT

# PB y PA: columna en vista + VP en vista
columna_vista(0, 3305); columna_vista(4465, 7805)
vp_vista(4365, 3615); vp_vista(8865, 8115)
# entrepiso
mensula(3705); viga_VL(3715); panel_TT(4415); capa_compresion(4415)
rect(250, 4465, 2700, 4485, fill="url(#pMort)", **CUTT)
rect(260, 4485, 2700, 4490, fill="#8d8d8d", stroke="none", sw=0)
rect(260, 4490, 2700, 4500, fill="url(#pPorc)", **CUTT)
for xx in range(860, 2700, 400): line(xx, 4490, xx, 4500, sw=0.15)
cielorraso(3450, 4415)
# cubierta
mensula(8205); viga_VL(8215); panel_TT(8915); capa_compresion(8915)
cielorraso(7950, 8915)

# ------------------------------------------------------------------ MURO CORTINA
montante(40, 4700); montante(4720, 9390)
rect(32, 4700, 182, 4720, fill="#fff", stroke="#444", sw=0.1)
rect(60, 4600, 150, 4840, fill="none", stroke="#444", sw=0.1, extra=DASH)
# arranque PB sobre VPP
rect(25, 0, 190, 40, fill=ALU, **CUTT); rect(32, 6, 182, 34, fill="#fff", stroke="#000", sw=0.06)
for xx in (60, 150): line(xx, 0, xx, -140, stroke="#000", sw=0.14)
rect(-30, 0, 25, 4, fill="#222", stroke="none", sw=0)
travesano(40, 60, glass_below=False)
dvh(110, 3440)
travesano(3450, 60)
dvh(3520, 4550, spandrel=True)
rect(40, 3520, 90, 4550, fill="url(#pLanaV)", **CUTT); rect(90, 3520, 93, 4550, fill=STEEL, stroke="none", sw=0)
travesano(4560, 60)
dvh(4630, 7940)
travesano(7950, 60)
dvh(8020, 9380, spandrel=True)
rect(40, 8020, 90, 9380, fill="url(#pLanaV)", **CUTT); rect(90, 8020, 93, 9380, fill=STEEL, stroke="none", sw=0)
# cierre superior del muro cortina
rect(-32, 9380, 190, 9420, fill=ALU, **CUTT); rect(-25, 9386, 183, 9414, fill="#fff", stroke="#000", sw=0.06)
# barrera cortafuego entrepiso
rect(93, 4355, 250, 4365, fill=STEEL, stroke="none", sw=0)
rect(93, 4365, 250, 4458, fill="url(#pLana)", **CUTT)
rect(93, 4458, 250, 4466, fill="#c0392b", stroke="none", sw=0)
pline([(182, 4503), (330, 4503)], stroke="#000", sw=0.25)
# grapas (en vista) fijadas a la placa/bulón pasante de la VL
def grapa(yy):
    poly([(185, yy - 70), (240, yy - 70), (240, yy + 70), (185, yy + 70)], fill=STEEL, stroke="#000", sw=0.08)
    line(160, yy, 200, yy, stroke="#000", sw=0.25)
grapa(4065); grapa(8565)
poly([(185, 40), (195, 40), (195, 180), (250, 180), (250, 190), (185, 190)], fill=STEEL, stroke="#000", sw=0.08)

# ------------------------------------------------------------------ CUBIERTA
yb0 = 8965
rect(250, 8965, 2700, 8968, fill="#000", stroke="none", sw=0)                               # barrera de vapor (bajo zócalo y paquete)
# zócalo superior H°A° in situ (carga) c/ barras de atado
poly([(260, 8968), (400, 8968), (400, 9410), (260, 9440)], fill="url(#pHAis)", **CUT)
rect(380, 9330, 400, 9350, fill="#fff", stroke="#000", sw=0.1)                              # buña p/ babeta
pline([(300, 8870), (300, 9390), (360, 9390), (360, 8870)], stroke=REB, sw=0.22)
x0, x1 = 400, 2700
def ypend(x, b): return b + (x - x0) * 0.02
rect(x0, 8968, x1, 9018, fill="url(#pEPS)", **CUTT)                                         # EPS 5 cm
poly([(x0, 9018), (x1, 9018), (x1, ypend(x1, 9068)), (x0, 9068)], fill="url(#pH)", **CUTT)   # contrapiso liviano
poly([(x0, 9068), (x1, ypend(x1, 9068)), (x1, ypend(x1, 9088)), (x0, 9088)], fill="url(#pMort)", **CUTT)  # carpeta
poly([(x0, 9088), (x0 + 60, 9088), (x0, 9148)], fill="url(#pMort)", **CUTT)                # media caña
pline([(x1, ypend(x1, 9092)), (x0 + 60, 9092), (x0 + 4, 9148), (x0 + 4, 9335), (385, 9340)], stroke="#000", sw=0.45)
pline([(420, 9356), (402, 9356), (402, 9300)], stroke="#000", sw=0.2)
rect(381, 9331, 399, 9349, fill="#222", stroke="none", sw=0)
# cupertina
pline([(-50, 9380), (-52, 9400), (-52, 9472), (430, 9452), (430, 9395), (436, 9380)], stroke="#000", sw=0.32)
line(330, 9441, 330, 9480, stroke="#000", sw=0.18)
rect(185, 9420, 260, 9440, fill="#222", stroke="none", sw=0)                                 # sellador cierre / zócalo

# =====================================================================================
#  COMPOSICIÓN
# =====================================================================================
XMAX = 1700
uses = []
for i, (lo, hi, top) in enumerate(BANDS):
    dy = top - YC(hi)
    defs.append(f'<clipPath id="cb{i}" clipPathUnits="userSpaceOnUse"><rect x="{f(X(-600))}" y="{f(YC(hi))}" width="{f(X(XMAX) - X(-600))}" height="{f((hi-lo)/S)}"/></clipPath>')
    uses.append(f'<g transform="translate(0,{f(dy)})"><g clip-path="url(#cb{i})"><use href="#fullg"/></g></g>')

def A(s): ann.append(s)
def T(x, y, s, size=2.0, anchor="start", weight="normal", fill="#000", rot=None, ital=False):
    r = f' transform="rotate({rot},{f(x)},{f(y)})"' if rot is not None else ""
    st = ' font-style="italic"' if ital else ""
    A(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{r}>{s}</text>')
def L(x0, y0, x1, y1, sw=0.15, stroke="#000", extra=""):
    A(f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

xa, xb = X(-600), X(XMAX)
def zig_h(py):
    xm = (xa + xb) / 2
    A(f'<polyline points="{f(xa)},{f(py)} {f(xm-1.5)},{f(py)} {f(xm-0.6)},{f(py-2)} {f(xm+0.6)},{f(py+2)} {f(xm+1.5)},{f(py)} {f(xb)},{f(py)}" fill="none" stroke="#000" stroke-width="0.18"/>')
for i, (lo, hi, top) in enumerate(BANDS):
    bot = top + (hi - lo) / S
    if i > 0: zig_h(top)
    if i < len(BANDS) - 1: zig_h(bot)
    L(X(450), top, X(450), bot, sw=0.12, stroke="#b03030", extra='stroke-dasharray="4 0.8 0.6 0.8"')

def nivel(y, txt, xpos, side="r", sub=""):
    DX.append(dict(t='nivel', y=y, x=xpos, txt=txt, sub=sub, side=side))
    px, py = X(xpos), Y(y)
    A(f'<path d="M{f(px)},{f(py)} l-1.2,-2 h2.4 z" fill="#000"/>')
    L(px - 3.6, py, px + 3.6, py, sw=0.15)
    ax = px + 1.7 if side == "r" else px - 1.7; an = "start" if side == "r" else "end"
    T(ax, py - 2.4, txt, 1.9, an, "bold")
    if sub: T(ax, py + 2.2, sub, 1.4, an, ital=True)
nivel(9472, "+9,47", -600, "r", "Cupertina")
nivel(9092, "+9,09", 1650, "l", "Cubierta terminada")
nivel(8915, "+8,92", 1350, "r", "N.S. estructura")
nivel(7950, "+7,95", 1000, "r", "Cielorraso PA")
nivel(4500, "+4,50", 1250, "r", "N.P.T. P. Alta")
nivel(3450, "+3,45", 1000, "r", "Cielorraso PB")
nivel(0, "±0,00", 1250, "r", "N.P.T. P. Baja")
nivel(-150, "-0,15", -420, "r", "Vereda")
nivel(-510, "-0,51", 1650, "l", "Sup. cuello")
nivel(-2150, "-2,15", -300, "r", "Fundación")

def cota_v(y0, y1, xpos, txt=None):
    DX.append(dict(t='cota', a=(xpos, y0), b=(xpos, y1), v=True, txt=txt))
    px = X(xpos); p0, p1 = Y(y0), Y(y1)
    L(px, p0, px, p1, 0.12)
    for p in (p0, p1): L(px - 0.7, p + 0.7, px + 0.7, p - 0.7, 0.25); L(px - 1.1, p, px + 1.4, p, 0.1)
    v = txt or f"{abs(y1 - y0)/1000:.2f}".replace(".", ",")
    T(px - 0.7, (p0 + p1) / 2, v, 1.6, "middle", rot=-90)
def cota_h(x0, x1, ypos, txt, below=False):
    DX.append(dict(t='cota', a=(x0, ypos), b=(x1, ypos), v=False, txt=txt))
    py = Y(ypos); a, b = X(x0), X(x1)
    L(a, py, b, py, 0.12)
    for p in (a, b): L(p - 0.7, py + 0.7, p + 0.7, py - 0.7, 0.25); L(p, py - 1.1, p, py + 1.1, 0.1)
    T((a + b) / 2, py + (2.2 if below else -0.6), txt, 1.5, "middle")
cota_v(0, 4500, -560); cota_v(4500, 8915, -560, "4,42"); cota_v(-2150, 0, -560)
cota_v(3715, 4415, 760, "0,70"); cota_v(8215, 8915, 760, "0,70"); cota_v(4365, 4415 - 600 + 0, 2620, "")
cota_v(3815, 4415, 1640, "0,60")
cota_v(-2050, -1750, 1560, "0,30"); cota_v(-1350, -510, 1150, "0,84")
cota_v(-500, 0, -150, "0,50"); cota_v(8968, 9440, 220, "0,47")
cota_h(-32, 182, 3330, "21"); cota_h(182, 250, 3330, "7"); cota_h(250, 650, 3330, "40")
cota_h(-550, 1450, -2170, "2,00 (s/ cálculo)", below=True); cota_h(-75, 975, -1420, "1,05")
cota_h(-50, 250, -620, "30", below=True)
T(X(-590), Y(9300), "EXTERIOR", 2.0, fill="#555"); T(X(900), Y(9420), "INTERIOR", 2.0, fill="#555")
T(X(-590), Y(4900), "EXTERIOR", 2.0, fill="#555"); T(X(800), Y(4900), "INTERIOR · PLANTA ALTA", 2.0, fill="#555")
T(X(-590), Y(1300), "EXTERIOR", 2.0, fill="#555"); T(X(800), Y(1300), "INTERIOR · PLANTA BAJA", 2.0, fill="#555")
T(X(700), Y(9200), "pend. 2 % → embudo y caño pluvial en columna", 1.4, ital=True, fill="#333")
T(X(1050), Y(-1000), "Fundación cortada por el eje de columna", 1.4, ital=True, fill="#333")
T(X(1050), Y(-1070), "(línea de corte quebrada en ±0,00)", 1.4, ital=True, fill="#333")
T(X(700), Y(3280), "Columna y VP en vista; ménsula y VL cortadas", 1.4, ital=True, fill="#333")

# círculo de eje
A(f'<circle cx="{f(X(450))}" cy="{f(BANDS[0][2] + 2.2)}" r="2.1" fill="#fff" stroke="#b03030" stroke-width="0.2"/>')
T(X(450), BANDS[0][2] + 2.95, "C", 2.2, "middle", "bold", "#b03030")

# ------------------------------------------------------------------ REFERENCIAS
def ref(n, x, y, dx, dy):
    DX.append(dict(t='ref', n=n, a=(x, y), b=(x + dx * S, y - dy * S)))
    px, py = X(x), Y(y); bx, by = px + dx, py + dy
    A(f'<circle cx="{f(px)}" cy="{f(py)}" r="0.32" fill="#000"/>')
    L(px, py, bx, by, 0.11, "#000")
    A(f'<circle cx="{f(bx)}" cy="{f(by)}" r="1.6" fill="#fff" stroke="#000" stroke-width="0.17"/>')
    T(bx, by + 0.62, str(n), 1.7, "middle", "bold", "#000")

REFS_POS = [
 (1, 200, 9462, 4, -6), (2, 80, 9400, -14, -3), (3, 1000, 9092, 0, -8), (4, 1300, 9080, 2, -10), (5, 1500, 9050, 0, 7), (6, 1640, 8995, 0, 9),
 (7, 1000, 8967, 0, 8), (8, 330, 9250, 12, -12), (9, 420, 9110, 24, -3),
 (10, 1550, 8945, 0, 12), (11, 470, 8980, 34, -16), (12, 1275, 8600, 9, 9), (13, 450, 8500, 20, 2), (14, 1550, 8300, 0, 7),
 (15, 450, 7880, 14, 0), (16, 300, 8000, -14, 3), (17, 450, 8207, 18, 6), (18, 600, 8565, 20, 10), (19, 505, 7900, 22, -3),
 (20, 1500, 4495, 0, -7), (21, 1600, 4475, 0, -9), (22, 1300, 3456, 0, 6), (23, 1550, 3475, 0, 6), (24, 1275, 3700, 9, 3),
 (25, 120, 4200, -16, 0), (26, 100, 4590, -20, 7), (27, 12, 4665, -24, 14), (28, 3, 4100, -14, 3), (29, 65, 3900, -16, 4),
 (30, 170, 4410, -22, -4), (31, 210, 4065, 26, -14), (32, 100, 4708, -28, 1), (33, 100, 20, -18, -5), (34, -5, 2, -14, 3),
 (35, 950, -5, 0, -6), (36, 1150, -25, 0, -8), (37, 1350, -45, 0, -10), (38, 1100, -120, 0, 12), (39, 1550, -176, 0, 9),
 (40, 1350, -260, 0, 10), (41, 660, -100, 10, 12), (42, 100, -250, -18, -2), (43, 0, -505, -12, 6), (44, -60, -40, -10, -4),
 (45, -300, -200, 6, -9), (46, 450, -900, 14, 0), (47, 700, -800, 20, 0), (48, 690, -1200, 22, 0), (49, 540, -1600, 20, 2),
 (50, 850, -700, 18, 12), (51, 1200, -1800, 9, 0), (52, 1100, -1960, 10, -4), (53, 1400, -2100, 4, 3), (54, 1400, -1350, 0, 5),
 (55, 1200, -420, 2, 9), (5, 0, 0, 0, 0),
]
for n, x, y, dx, dy in REFS_POS:
    if (dx, dy) != (0, 0): ref(n, x, y, dx, dy)

LEG = [
("CUBIERTA", None),
(1, "Cupertina chapa galv. N°22 plegada c/ goterones, tornillos y sellador."),
(2, "Perfil de cierre superior del muro cortina + sellador de silicona."),
(3, "Membrana asfáltica 4 mm c/ aluminio; babeta en buña + perfil + sellador."),
(4, "Carpeta niveladora 1:3 c/ 10 % de hidrófugo, e = 2 cm."),
(5, "Contrapiso liviano H° c/ EPS 1:6, pend. 2 % (mín. 5 cm)."),
(6, "Aislación térmica EPS 30 kg/m³, e = 5 cm (IRAM 11605)."),
(7, "Barrera de vapor: imprimación asfáltica + film 200 µ."),
(8, "Zócalo superior H°A° in situ c/ barras de atado a la VL."),
(9, "Media caña de mortero."),
("ESTRUCTURA PREMOLDEADA (SISTEMA PI)", None),
(10, "Capa de compresión H° e = 5 cm c/ malla electrosoldada Ø6 c/15."),
(11, "Estribos salientes de la VL (2Ø10) p/ vinculación c/ capa de compresión."),
(12, "Panel TT pretensado (corte transversal), apoyado en VP."),
(13, "Viga pretensada VL 40x70 (doble T), perimetral."),
(14, "Viga pretensada VP (en vista), apoyo de paneles TT."),
(15, "Columna pretensada 40x40 c/ caño pluvial (en vista)."),
(16, "Ménsula de columna p/ apoyo de viga."),
(17, "Apoyo de neopreno c/ perno de fijación Ø20."),
(18, "Bulón pasante Ø3/4\" c/ tuerca y arandela Ø90 + sellado c/ masilla (anclaje)."),
(19, "Caño de desagüe pluvial PVC Ø110 embutido en la columna."),
("ENTREPISO Y CIELORRASOS", None),
(20, "Solado cerámico s/ adhesivo cementicio."),
(21, "Carpeta niveladora MHR 1:1/4:3, e = 2 cm."),
(22, "Cielorraso suspendido placa de roca de yeso 12,5 mm."),
(23, "Montantes y soleras de chapa galv. 35 mm."),
(24, "Gancho / vela de fijación a los nervios del panel TT."),
("MURO CORTINA (STICK, MÓDULO 1,25 m)", None),
(25, "Montante de aluminio 50x150 (en vista)."),
(26, "Travesaño de aluminio + presor + tapa + burletes EPDM."),
(27, "DVH: 6 templado + cámara 12 + 3+3 laminado PVB."),
(28, "Spandrel: vidrio templado 6 mm esmaltado."),
(29, "Lana mineral 50 mm + bandeja de chapa galv."),
(30, "Barrera cortafuego: lana mineral 100 kg/m³ + sellador intumescente."),
(31, "Grapa de acero galv. regulable (colisos) + bulón M12 inox."),
(32, "Junta de dilatación del montante 20 mm + manguito."),
(33, "Perfil de arranque alum. c/ drenaje + tarugos a la VPP."),
(34, "Sellador de silicona neutra s/ fondo de junta."),
("PLANTA BAJA Y FUNDACIÓN", None),
(35, "Solado cerámico s/ adhesivo cementicio."),
(36, "Carpeta niveladora MHR 1:1/4:3."),
(37, "Carpeta hidrófuga MCI 1:3 c/ aditivo hidrófugo."),
(38, "Contrapiso de H° pobre e = 12 cm."),
(39, "Separador de suelos: film de polietileno 200 µ."),
(40, "Tosca compactada e = 15 cm."),
(41, "Junta de dilatación perimetral EPS 2 cm + sellador."),
(42, "Viga perimetral portamuro (VPP) premoldeada 30x50."),
(43, "Banda de neopreno s/ cuello p/ apoyo de la VPP."),
(44, "Babeta/goterón chapa galv. + aislación hidrófuga vertical."),
(45, "Vereda de H° peinado s/ tosca + junta c/ sellador."),
(46, "Tronco de columna dentro del cuello."),
(47, "Anclaje mecánico húmedo: horquillas entrelazadas columna/cuello."),
(48, "Relleno de H° cementicio entre cuello y columna."),
(49, "Armadura de vinculación fundación–columna."),
(50, "Cuello de la base, H°A° colado in situ."),
(51, "Base de H°A° colada in situ (s/ cálculo)."),
(52, "Armadura de fundación s/ cálculo estructural."),
(53, "H° de limpieza (hidráulico pobre) e = 10 cm."),
(54, "Terreno natural."),
(55, "Caño pluvial PVC Ø110 a cámara de inspección y colectora."),
]

RX = 130.0
LX, LY = 130.0, 12.0
def legend():
    T(LX, LY, "REFERENCIAS (corte integral y nudos)", 2.4, weight="bold")
    A(f'<line x1="{LX}" y1="{LY+1.2}" x2="290" y2="{LY+1.2}" stroke="#000" stroke-width="0.2"/>')
    cols = [(LX, LY + 5.5), (LX + 81, LY + 5.5)]; ci = 0; x0, y = cols[0]; ymax = 113.0
    blocks = []; cur = None
    for item in LEG:
        if item[1] is None: cur = [item[0], []]; blocks.append(cur)
        else: cur[1].append(item)
    for title, items in blocks:
        if y + 8 > ymax and ci == 0: ci = 1; x0, y = cols[1]
        T(x0, y, title, 1.6, weight="bold"); y += 2.3
        for n, txt in items:
            words, lines, cur2 = txt.split(), [], ""
            for w in words:
                if len(cur2) + len(w) + 1 > 64: lines.append(cur2); cur2 = w
                else: cur2 = (cur2 + " " + w).strip()
            lines.append(cur2)
            if y + 1.95 * len(lines) > ymax and ci == 0: ci = 1; x0, y = cols[1]
            T(x0 + 1.4, y, str(n), 1.55, "middle", "bold", "#000")
            for ln in lines: T(x0 + 3.3, y, ln, 1.55); y += 1.95
            y += 0.1
        y += 1.0
    return y
yend = legend(); my = yend
# rótulo (sin recuadro)
ry = 398.0
A(f'<line x1="{RX}" y1="{ry-3}" x2="290" y2="{ry-3}" stroke="#000" stroke-width="0.25"/>')
T(RX, ry + 1, "CORTE INTEGRAL 1:20 + NUDOS AXONOMÉTRICOS — VIDRIADO", 2.8, weight="bold")
T(RX, ry + 5, "Hormigón premoldeado de grandes luces (sistema Pi) · cerramiento vidriado – muro cortina", 1.7)
cells = [("MATERIA", "Construcciones II"), ("CÁTEDRA", "Arq. Tucci"), ("ALUMNO/A", "_____________"), ("GRUPO", "____"),
         ("ESCALAS", "Corte 1:20 · N1-N2 1:12,5 · N3 1:10"), ("HOJA", "A3 · 2026")]
for i, (k, v) in enumerate(cells):
    x = RX + (i % 3) * 54; y = ry + 9.5 + (i // 3) * 5.2
    T(x, y, k, 1.25, weight="bold"); T(x + 15, y, v, 1.6)
T(X(-590), 395.5, "ESC. 1:20 — corte por apoyo de VL / ménsula; fundación por eje de columna (corte quebrado en ±0,00)", 1.5, weight="bold")
sx, sy = X(-590), 401.5
for i in range(5):
    A(f'<rect x="{sx + i*5}" y="{sy-1.1}" width="5" height="1.1" fill="{"#000" if i%2==0 else "#fff"}" stroke="#000" stroke-width="0.12"/>')
T(sx, sy - 1.6, "0", 1.2, "middle"); T(sx + 25, sy - 1.6, "50 cm", 1.2, "middle")

SVG_BODY = f'''<defs>{"".join(defs)}<g id="fullg">{"".join(full)}</g></defs>
<rect x="0" y="0" width="297" height="420" fill="#fff"/>
<rect x="4" y="4" width="289" height="412" fill="none" stroke="#000" stroke-width="0.4"/>
{"".join(uses)}
{"".join(ann)}'''
import json
os.makedirs("build", exist_ok=True)
open("build/final_corte.svgpart", "w").write(SVG_BODY)
json.dump(dict(DX=DX, LEG=LEG, NOTAS=[]), open("build/final_dx.json", "w"), ensure_ascii=False)
print("ok", yend, my)
