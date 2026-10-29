# -*- coding: utf-8 -*-
"""TP N°6 - Corte integral ACERO con FRENTE INTEGRAL, esc. 1:20 (A3 vertical) + referencias + rótulo.
Geometría en mm reales; x+ hacia el interior, y+ hacia arriba, ±0,00 = NPT planta baja.
Plano de corte entre montantes del frente integral (vidrio y travesaños cortados, montante en vista), 12,5 cm delante del eje de
columnas: columna HEB 200 y vigas IPN 180 en vista; viga perimetral IPN 200, losa, dado y zapata cortados (por la línea de pernos).

Correcciones de la docente incorporadas:
 - escala real 1:20 (corte) y 1:10 (detalles), formato A3 vertical único
 - chapa plegada p/ anclaje del panel sándwich (12) sobre montante de parapeto (13)
 - tubo estructural soldado a viga p/ anclaje del frente integral (29), en entrepiso y en cubierta
 - baranda fijada a losa c/ planchuela + brocas (37)
 - vela rígida a losa p/ cielorraso (45)
 - dado estructural de H°A° p/ columna y frente integral (23)
 - rayados diferenciados y rotulados: dado H°A° (estructural) / contrapiso H° pobre (relleno)
"""
import math, os, json

S = 20.0
XR0, PX0 = -560.0, 176.0
XMAX = 1560
def X(x): return PX0 + (x - XR0) / S
def YC(y): return 1000.0 - y / S

BANDS = [(4950, 6620, 15.0), (1820, 3780, 107.0), (-1640, 1480, 213.0)]
def band_of(y):
    for b in BANDS:
        if b[0] - 1 <= y <= b[1] + 1: return b
    return None
def Y(y):
    lo, hi, top = band_of(y)
    return YC(y) + (top - YC(hi))

full, ann, defs = [], [], []
f = lambda v: f"{v:.3f}"

def poly(pts, fill="none", stroke="#000", sw=0.3, extra=""):
    d = " ".join(f"{f(X(x))},{f(YC(y))}" for x, y in pts)
    full.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
def rect(x0, y0, x1, y1, **k): poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)
def pline(pts, stroke="#000", sw=0.18, extra="", fill="none"):
    d = " ".join(f"{f(X(x))},{f(YC(y))}" for x, y in pts)
    full.append(f'<polyline points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
def line(x0, y0, x1, y1, **k): pline([(x0, y0), (x1, y1)], **k)
def circ(x, y, r, fill="#000", stroke="none", sw=0.1):
    full.append(f'<circle cx="{f(X(x))}" cy="{f(YC(y))}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def label_in(x, y, s, size=1.9, fill="#222", anchor="middle", w="bold"):   # texto dentro del dibujo (se recorta con la banda)
    full.append(f'<text x="{f(X(x))}" y="{f(YC(y))}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}" letter-spacing="0.15">{s}</text>')

CUT = dict(stroke="#000", sw=0.35)
CUTT = dict(stroke="#000", sw=0.2)
VIEW = dict(stroke="#555", sw=0.13)
DASH = 'stroke-dasharray="1.2 0.6"'

defs.append('''
<pattern id="pHA" patternUnits="userSpaceOnUse" width="1.4" height="1.4" patternTransform="rotate(45)">
 <rect width="1.4" height="1.4" fill="#d9dcdf"/><line x1="0" y1="0" x2="0" y2="1.4" stroke="#4a4f55" stroke-width="0.09"/></pattern>
<pattern id="pHAis" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)">
 <rect width="2.2" height="2.2" fill="#d6d3cc"/><line x1="0" y1="0" x2="0" y2="2.2" stroke="#3a3f45" stroke-width="0.1"/>
 <circle cx="1.1" cy="0.55" r="0.14" fill="#3a3f45"/><circle cx="1.5" cy="1.6" r="0.1" fill="#3a3f45"/></pattern>
<pattern id="pH" patternUnits="userSpaceOnUse" width="3" height="3">
 <rect width="3" height="3" fill="#efede7"/><circle cx="0.6" cy="0.7" r="0.16" fill="#666"/><circle cx="2.1" cy="1.9" r="0.12" fill="#666"/>
 <path d="M1.7 0.4 l0.35 0.55 h-0.7z" fill="none" stroke="#666" stroke-width="0.07"/><path d="M0.5 2.2 l0.3 0.45 h-0.6z" fill="none" stroke="#666" stroke-width="0.07"/>
 <circle cx="2.6" cy="0.5" r="0.07" fill="#666"/><circle cx="1.2" cy="2.7" r="0.07" fill="#666"/></pattern>
<pattern id="pHL" patternUnits="userSpaceOnUse" width="2.4" height="2.4">
 <rect width="2.4" height="2.4" fill="#f3efe2"/><circle cx="0.6" cy="0.6" r="0.32" fill="none" stroke="#8a7d5a" stroke-width="0.07"/>
 <circle cx="1.8" cy="1.7" r="0.24" fill="none" stroke="#8a7d5a" stroke-width="0.07"/><circle cx="1.7" cy="0.5" r="0.07" fill="#8a7d5a"/></pattern>
<pattern id="pMort" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
 <rect width="1.2" height="1.2" fill="#ececec"/><circle cx="0.3" cy="0.3" r="0.08" fill="#777"/><circle cx="0.9" cy="0.85" r="0.06" fill="#777"/></pattern>
<pattern id="pHid" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
 <rect width="1.2" height="1.2" fill="#c9dbe6"/><circle cx="0.3" cy="0.3" r="0.08" fill="#456"/><circle cx="0.9" cy="0.85" r="0.06" fill="#456"/></pattern>
<pattern id="pGrout" patternUnits="userSpaceOnUse" width="0.8" height="0.8">
 <rect width="0.8" height="0.8" fill="#bdbdbd"/><circle cx="0.2" cy="0.2" r="0.08" fill="#333"/><circle cx="0.6" cy="0.6" r="0.08" fill="#333"/></pattern>
<pattern id="pTierra" patternUnits="userSpaceOnUse" width="6" height="6">
 <rect width="6" height="6" fill="#ece3d2"/>
 <g stroke="#8a7350" stroke-width="0.12"><line x1="0.5" y1="2" x2="2" y2="0.5"/><line x1="1.1" y1="2.3" x2="2.4" y2="1"/><line x1="1.7" y1="2.6" x2="2.8" y2="1.5"/>
 <line x1="3.5" y1="5.2" x2="5" y2="3.7"/><line x1="4.1" y1="5.5" x2="5.4" y2="4.2"/></g>
 <circle cx="4.6" cy="1.2" r="0.15" fill="#8a7350"/><circle cx="1.3" cy="4.6" r="0.15" fill="#8a7350"/></pattern>
<pattern id="pEPSv" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(90)">
 <rect width="1.6" height="1.6" fill="#fff5bf"/><path d="M0 0.8 L0.4 0.3 L0.8 0.8 L1.2 1.3 L1.6 0.8" fill="none" stroke="#a08a1a" stroke-width="0.09"/></pattern>
<pattern id="pPUR" patternUnits="userSpaceOnUse" width="1.0" height="1.0" patternTransform="rotate(90)">
 <rect width="1.0" height="1.0" fill="#f7e7a6"/><path d="M0 0.5 L0.25 0.2 L0.5 0.5 L0.75 0.8 L1 0.5" fill="none" stroke="#a07f1a" stroke-width="0.07"/></pattern>
<pattern id="pPorc" patternUnits="userSpaceOnUse" width="4" height="4"><rect width="4" height="4" fill="#cdbb9c"/></pattern>
''')
GLASS = "#cbe8f3"; ALU = "#a3abb3"; ALU2 = "#c9d0d6"; STEEL = "#2e3135"; STEELV = "#dfe2e5"; NEO = "#111"; GALV = "#7d858c"; REB = "#7a1f1f"; INOX = "#b9bec4"

# =====================================================================================================  FRENTE INTEGRAL
# vidrio 0..24 · montante / travesaño (cuerpo) 34..114 · tapa interior MT-0817 114..124 · presor -12..-2 · tapa exterior MT-0819 -20..-12
def dvh(y0, y1):
    rect(0, y0, 6, y1, fill=GLASS, **CUTT); rect(18, y0, 24, y1, fill=GLASS, **CUTT)
    for yy in (y0, y1 - 14): rect(6, yy, 18, yy + 14, fill=ALU, stroke="#000", sw=0.06)
    rect(6, y0, 18, y0 + 3, fill=NEO, stroke="none", sw=0); rect(6, y1 - 3, 18, y1, fill=NEO, stroke="none", sw=0)

def travesano(a, h=60, below=True, above=True):
    rect(34, a, 114, a + h, fill=ALU, **CUTT); rect(37, a + 3, 111, a + h - 3, fill="#fff", stroke="#000", sw=0.06)
    poly([(114, a + 4), (124, a + 4), (124, a + h - 4), (114, a + h - 4), (114, a + h - 10), (120, a + h - 10), (120, a + 10), (114, a + 10)], fill=ALU2, stroke="#000", sw=0.07)  # tapa int.
    rect(24, a + h / 2 - 7, 34, a + h / 2 + 7, fill=ALU, stroke="#000", sw=0.07)                                  # lengüeta
    lo = a - 20 if below else a; hi = a + h + 20 if above else a + h
    rect(-12, lo, -2, hi, fill=ALU, stroke="#000", sw=0.08)                                                       # presor
    poly([(-20, lo + 4), (-12, lo), (-12, hi), (-20, hi - 4)], fill=ALU2, stroke="#000", sw=0.08)                 # tapa ext.
    line(-12, a + h / 2, 60, a + h / 2, stroke="#000", sw=0.12)                                                    # tornillo
    for yy in ([a - 18] if below else []) + ([a + h + 6] if above else []):
        rect(-2, yy, 0, yy + 12, fill=NEO, stroke="none", sw=0); rect(24, yy, 26, yy + 12, fill=NEO, stroke="none", sw=0)
    if above: rect(4, a + h, 20, a + h + 5, fill="#333", stroke="none", sw=0)                                      # calzo

def montante(y0, y1):      # en vista (detrás del plano de corte)
    rect(34, y0, 124, y1, fill="#eef0f2", **VIEW); line(114, y0, 114, y1, stroke="#777", sw=0.07)
    rect(-20, y0, -12, y1, fill="#eef0f2", stroke="#777", sw=0.07)

def tubo_soldado(yc):      # tubo 80x40x2 soldado a la viga (en vista) + grapa ángulo + bulón al montante
    rect(124, yc - 40, 230, yc + 40, fill=STEELV, stroke="#222", sw=0.16)
    line(124, yc - 37, 230, yc - 37, stroke="#777", sw=0.06); line(124, yc + 37, 230, yc + 37, stroke="#777", sw=0.06)
    poly([(226, yc - 40), (230, yc - 40), (230, yc + 40), (226, yc + 40)], fill="#000", stroke="none")          # cordón de soldadura
    rect(70, yc - 50, 200, yc + 50, fill="#c9cdd1", stroke="#222", sw=0.12)                                       # grapa: doble planchuela
    for xb in (90, 170): circ(xb, yc, 0.45, fill="#fff", stroke="#000", sw=0.12); circ(xb, yc, 0.2, fill="#000")  # bulones M10

# =====================================================================================================  ESTRUCTURA METÁLICA
BX0, BX1 = 230, 320          # viga perimetral IPN 200 (ala 90)
def ipn200(yb):
    yt = yb + 200; xc = (BX0 + BX1) / 2
    P = [(BX0, yb), (BX1, yb), (BX1, yb + 11), (xc + 4, yb + 18), (xc + 4, yt - 18), (BX1, yt - 11), (BX1, yt), (BX0, yt), (BX0, yt - 11), (xc - 4, yt - 18), (xc - 4, yb + 18), (BX0, yb + 11)]
    poly(P, fill=STEEL, stroke="#000", sw=0.2)
def ipn180_vista(yt):
    rect(430, yt - 180, XMAX + 50, yt, fill=STEELV, **VIEW)
    line(430, yt - 10, XMAX + 50, yt - 10, stroke="#777", sw=0.08); line(430, yt - 170, XMAX + 50, yt - 170, stroke="#777", sw=0.08)
    rect(430, yt - 165, 520, yt - 15, fill="#c9cdd1", stroke="#333", sw=0.12)                                     # chapa de unión soldada a columna
    for yy in (yt - 130, yt - 90, yt - 50): circ(488, yy, 0.38, fill="#222")                                      # bulones
    line(431, yt - 165, 431, yt - 15, stroke="#000", sw=0.35)                                                     # soldadura
def columna_vista(y0, y1):
    rect(230, y0, 430, y1, fill=STEELV, **VIEW)
    line(245, y0, 245, y1, stroke="#777", sw=0.07); line(415, y0, 415, y1, stroke="#777", sw=0.07)

def losa(yb, x0=BX0, x1=XMAX + 50):
    """losa c/ placa colaborante: H° hasta yb+120"""
    prof = [(x0, yb)]
    x = x0 + 20
    while x < x1:
        prof += [(x, yb), (min(x + 25, x1), yb + 50 if x + 25 <= x1 else yb)]
        if x + 25 >= x1: break
        prof += [(min(x + 105, x1), yb + 50)]
        if x + 105 >= x1: break
        prof += [(min(x + 130, x1), yb)]
        x += 200
    prof.append((x1, yb))
    top = yb + 120
    poly(prof + [(x1, top), (x0, top)], fill="url(#pHA)", **CUT)
    pline(prof, stroke=GALV, sw=0.35)                                                                             # chapa galv.
    pline([(x0 + 30, yb + 95), (x1, yb + 95)], stroke=REB, sw=0.12, extra='stroke-dasharray="2 0.5"')              # malla
    for xx in range(x0 + 120, int(x1), 150): circ(xx, yb + 95, 0.17, fill=REB)
    for xx in range(x0 + 180, int(x1) - 50, 600): poly([(xx - 12, yb + 50), (xx + 12, yb + 50), (xx + 4, yb + 90), (xx - 4, yb + 90)], fill="#444", stroke="none")  # separador
    for xx in (262, 288): rect(xx - 5, yb, xx + 5, yb + 80, fill=STEEL, stroke="none"); rect(xx - 9, yb + 72, xx + 9, yb + 80, fill=STEEL, stroke="none")  # conectores
    pline([(x0 - 3, yb - 20), (x0 - 3, top), (x0 + 30, top)], stroke=GALV, sw=0.4)                                 # zinguería de borde
    return top

def cielorraso(y, yfix, xs=(480, 1100)):
    rect(150, y, XMAX + 50, y + 9.5, fill="#f4f4f2", **CUTT)
    for xx in range(260, XMAX + 50, 400): rect(xx, y + 9.5, xx + 35, y + 45, fill=GALV, stroke="#333", sw=0.07)    # montantes 35 (cortados)
    line(150, y + 45, XMAX + 50, y + 45, stroke="#555", sw=0.12)                                                  # solera / maestras
    pline([(150, y + 30), (150, y - 2), (134, y - 2), (134, y - 20)], stroke="#000", sw=0.28)                      # perfil Z buña
    for xc in xs:                                                                                                 # velas rígidas a losa
        rect(xc - 17, y + 45, xc + 17, yfix - 4, fill="#e5e8ea", stroke="#222", sw=0.12)
        rect(xc + 17, yfix - 45, xc + 21, yfix, fill=GALV, stroke="#000", sw=0.06); rect(xc + 21, yfix - 4, xc + 60, yfix, fill=GALV, stroke="#000", sw=0.06)
        line(xc + 45, yfix - 8, xc + 45, yfix + 25, stroke="#000", sw=0.22)                                       # tornillo/clavo a losa
    # perfil C perimetral c/ neopreno colgado de la viga
    rect(268, y + 45, 284, BEAMB[y] if y in BEAMB else y + 200, fill="#e5e8ea", stroke="#222", sw=0.12)
    rect(150, y + 9.5, 190, y + 45, fill="none", stroke="#000", sw=0.15); rect(150, y + 9.5, 153, y + 45, fill=NEO, stroke="none")

def baranda(yfl):
    rect(290, yfl, 390, yfl + 8, fill=INOX, stroke="#000", sw=0.1)                                                 # planchuela base
    for xx in (305, 375): rect(xx - 5, yfl - 90, xx + 5, yfl + 14, fill=STEEL, stroke="none"); rect(xx - 9, yfl + 8, xx + 9, yfl + 16, fill="#555", stroke="none")
    rect(330, yfl + 8, 350, yfl + 430, fill=INOX, stroke="#000", sw=0.12)                                           # parante Ø42 (vista)
    circ(340, yfl + 450, 21 / S, fill=INOX, stroke="#000", sw=0.12); circ(340, yfl + 450, 16 / S, fill="#fff", stroke="#000", sw=0.05)  # pasamanos/posapié Ø42

# ------------------------------------------------------------------- TERRENO Y FUNDACIÓN (cortada por la línea de pernos)
rect(-620, -1700, XMAX + 60, -200, fill="url(#pTierra)", stroke="none")
rect(700, -200, XMAX + 60, -175, fill="url(#pTierra)", stroke="none")
line(-620, -200, -40, -200, sw=0.2)
rect(-470, -1550, 1130, -1500, fill="url(#pH)", **CUTT)                                                            # H° de limpieza
poly([(-420, -1500), (1080, -1500), (1080, -1250), (700, -960), (-40, -960), (-420, -1250)], fill="url(#pHAis)", **CUT)   # zapata
poly([(-40, -960), (700, -960), (700, -250), (140, -250), (140, -20), (-40, -20)], fill="url(#pHAis)", **CUT)     # DADO H°A°
line(-40, -960, 700, -960, stroke="#000", sw=0.25, extra=DASH)                                                     # junta de hormigonado
# armaduras
pline([(-360, -1380), (-360, -1450), (1020, -1450), (1020, -1380)], stroke=REB, sw=0.22)
for xx in range(-330, 1020, 120): circ(xx, -1432, 0.26, fill=REB)
for xx in (0, 660): pline([(xx + (60 if xx < 300 else -60), -1450), (xx, -1450), (xx, -300 if xx > 300 else -60)], stroke=REB, sw=0.2)
pline([(100, -900), (100, -60), (40, -60)], stroke=REB, sw=0.18)
for yy in range(-900, -300, 150): pline([(0, yy), (660, yy)], stroke=REB, sw=0.09, extra='stroke-dasharray="1.5 0.6"')
for yy in (-250, -120): pline([(0, yy), (100, yy)], stroke=REB, sw=0.09, extra='stroke-dasharray="1.5 0.6"')
# pernos de anclaje en "J" + grout + platabanda + tuercas
for xx in (205, 455):
    pline([(xx, -160), (xx, -760), (xx + (50 if xx < 330 else -50), -810), (xx + (90 if xx < 330 else -90), -770)], stroke=STEEL, sw=0.55)
rect(155, -250, 505, -225, fill="url(#pGrout)", **CUTT)
rect(155, -225, 505, -200, fill=STEEL, stroke="#000", sw=0.15)
for xx in (205, 455):
    rect(xx - 17, -246, xx + 17, -230, fill="#555", stroke="#000", sw=0.05)                                          # tuerca de nivelación
    rect(xx - 20, -200, xx + 20, -196, fill="#777", stroke="#000", sw=0.04)                                         # arandela
    rect(xx - 17, -196, xx + 17, -180, fill="#555", stroke="#000", sw=0.05); rect(xx - 17, -180, xx + 17, -164, fill="#555", stroke="#000", sw=0.05)
# columna HEB 200 (en vista sobre el piso; oculta dentro del relleno) + cartelas
for xa, xb in ((230, 245), (415, 430)): rect(xa, -200, xb, -60, fill="none", stroke="#444", sw=0.12, extra=DASH)
for xx, s in ((230, -1), (430, 1)): pline([(xx, -100), (xx + s * 70, -200)], stroke="#444", sw=0.12, extra=DASH)
# vereda + aislación hidrófuga del dado
rect(-620, -200, -46, -100, fill="url(#pH)", **CUTT)
pline([(-620, -100), (-46, -100)], stroke="#000", sw=0.25)
rect(-46, -620, -40, -20, fill=NEO, stroke="none")
rect(-52, -200, -46, -100, fill="#333", stroke="none")                                                              # junta vereda / dado
# piso interior: contrapiso H° pobre (relleno, sobre suelo y sobre el dado) + film + carpetas + solado
rect(700, -177, XMAX + 60, -175, fill="#000", stroke="none")
poly([(140, -250), (700, -250), (700, -177), (XMAX + 60, -177), (XMAX + 60, -55), (140, -55)], fill="url(#pH)", **CUTT)
pline([(170, -100), (XMAX + 60, -100)], stroke=REB, sw=0.1, extra='stroke-dasharray="2 0.5"')
rect(140, -55, XMAX + 60, -35, fill="url(#pHid)", **CUTT)
rect(140, -35, XMAX + 60, -15, fill="url(#pMort)", **CUTT)
rect(140, -15, XMAX + 60, -10, fill="#8d8d8d", stroke="none"); rect(140, -10, XMAX + 60, 0, fill="url(#pPorc)", **CUTT)
for xx in range(540, XMAX + 60, 400): line(xx, -10, xx, 0, sw=0.15)
label_in(330, -560, "DADO H°A°", 2.3, "#111"); label_in(330, -640, "(estructural)", 1.7, "#111", w="normal")
label_in(1150, -130, "CONTRAPISO H° POBRE", 1.7, "#111"); label_in(560, -140, "RELLENO", 1.5, "#111")
label_in(330, -1330, "ZAPATA H°A°", 2.3, "#111")
# frente integral: arranque en el dado
rect(-20, -20, 130, 30, fill=ALU, **CUTT); rect(-14, -14, 124, 30, fill="#fff", stroke="#000", sw=0.06)            # perfil U de arranque
for xx in (10, 100): line(xx, -14, xx, -110, stroke="#000", sw=0.25); rect(xx - 9, -16, xx + 9, -12, fill="#555", stroke="none")  # brocas al dado
rect(130, -20, 140, 0, fill=NEO, stroke="none")                                                                     # sellador
pline([(-20, 28), (-34, 14), (-60, -6), (-60, -45), (-72, -58)], stroke="#000", sw=0.3)                            # alféizar ext. c/ pendiente + goterón
rect(-28, -20, -20, 10, fill="#222", stroke="none")

# ------------------------------------------------------------------- ESTRUCTURA
YE_B = 2640; YR_B = 5680          # fondo vigas IPN 200 entrepiso / cubierta
BEAMB = {2400: YE_B, 5380: YR_B}
columna_vista(0, YR_B + 200)
ipn180_vista(YE_B + 200); ipn180_vista(YR_B + 200)
ipn200(YE_B); ipn200(YR_B)
yE = losa(YE_B + 200); yR = losa(YR_B + 200)          # 2960 / 6000
cielorraso(2400, YE_B + 200); cielorraso(5380, YR_B + 200)
# entrepiso: carpeta + solado + EPS de frente + baranda
rect(BX0, 2960, XMAX + 50, 2985, fill="url(#pMort)", **CUTT)
rect(BX0, 2985, XMAX + 50, 2990, fill="#8d8d8d", stroke="none"); rect(BX0, 2990, XMAX + 50, 3000, fill="url(#pPorc)", **CUTT)
for xx in range(640, XMAX + 50, 400): line(xx, 2990, xx, 3000, sw=0.15)
pline([(124, 3000), (190, 3000), (232, 3008), (300, 3008)], stroke="#000", sw=0.3)                                 # cubrejunta / alféizar int.
rect(118, 2985, 126, 3006, fill=NEO, stroke="none")
baranda(3000)
baranda(0)

# ------------------------------------------------------------------- FRENTE INTEGRAL
montante(30, 5800)
travesano(30, 60, below=False)
dvh(90, 2580)
travesano(2580, 60)
rect(-8, 2640, 32, 3040, fill="url(#pPUR)", **CUTT); rect(-8, 2640, -7, 3040, fill=GALV, stroke="none"); rect(31, 2640, 32, 3040, fill=GALV, stroke="none")  # panel ciego
travesano(3040, 60)
dvh(3100, 5500)
travesano(5500, 60, above=False)
tubo_soldado(2740)
tubo_soldado(5740)
rect(190, 2600, 227, 2958, fill="url(#pEPSv)", **CUTT)

# ------------------------------------------------------------------- CUBIERTA Y PARAPETO
xL = BX0
def yp(x, b): return b + (x - xL) * 0.02
rect(xL, 6000, XMAX + 50, 6003, fill="#000", stroke="none")                                                          # barrera de vapor
poly([(xL + 4, 6003), (XMAX + 50, 6003), (XMAX + 50, yp(XMAX + 50, 6070)), (xL + 4, 6070)], fill="url(#pHL)", **CUTT)  # contrapiso liviano
poly([(xL + 4, 6070), (XMAX + 50, yp(XMAX + 50, 6070)), (XMAX + 50, yp(XMAX + 50, 6090)), (xL + 4, 6090)], fill="url(#pMort)", **CUTT)  # carpeta
pline([(XMAX + 50, yp(XMAX + 50, 6094)), (xL + 50, 6094), (xL + 8, 6136), (xL + 8, 6330)], stroke="#000", sw=0.45)  # membrana
pline([(xL + 3, 6000), (xL + 3, 6330), (xL - 6, 6330)], stroke=GALV, sw=0.35); pline([(xL + 3, 6003), (xL + 60, 6003)], stroke=GALV, sw=0.35)  # perfil L
# montante de parapeto (tubo 100x100) en vista, apoyado y soldado sobre el tubo de anclaje y a la viga
rect(130, 5780, 230, 6400, fill=STEELV, stroke="#222", sw=0.16)
line(133, 5780, 133, 6400, stroke="#777", sw=0.06); line(227, 5780, 227, 6400, stroke="#777", sw=0.06)
poly([(226, 5860), (230, 5860), (230, 5880), (226, 5880)], fill="#000", stroke="none")
# chapa plegada de anclaje del panel (perfil C cortado) + omega + perfil Z + panel sándwich
for yc in (5960, 6260):
    pline([(130, yc - 40), (55, yc - 40), (55, yc + 40), (130, yc + 40)], stroke="#000", sw=0.32)
    pline([(130, yc - 40), (130, yc + 40)], stroke="#000", sw=0.32)
    line(120, yc, 145, yc, stroke="#000", sw=0.22); line(40, yc + 20, 62, yc + 20, stroke="#000", sw=0.22)
rect(30, 5880, 55, 6380, fill="#e8eaec", stroke="#333", sw=0.1)                                                    # omega (vista)
pline([(-10, 5597), (32, 5597), (32, 5670)], stroke="#000", sw=0.32); line(28, 5640, 48, 5640, stroke="#000", sw=0.22)  # perfil Z sujeción inf.
rect(-10, 5600, 30, 6400, fill="url(#pPUR)", **CUTT); rect(-10, 5600, -9, 6400, fill=GALV, stroke="none"); rect(29, 5600, 30, 6400, fill=GALV, stroke="none")
pline([(30, 5598), (-10, 5598), (-30, 5570), (-30, 5552), (-20, 5560)], stroke="#000", sw=0.3)                     # zinguería de buña / goterón
rect(-12, 5566, -2, 5598, fill=NEO, stroke="none")
# cupertina
pline([(-28, 6330), (-28, 6405), (245, 6440), (245, 6350), (252, 6340)], stroke="#000", sw=0.35)
rect(-10, 6400, 230, 6405, fill=NEO, stroke="none")

# =====================================================================================  COMPOSICIÓN
uses = []
for i, (lo, hi, top) in enumerate(BANDS):
    dy = top - YC(hi)
    defs.append(f'<clipPath id="cb{i}" clipPathUnits="userSpaceOnUse"><rect x="{f(X(XR0))}" y="{f(YC(hi))}" width="{f(X(XMAX) - X(XR0))}" height="{f((hi-lo)/S)}"/></clipPath>')
    uses.append(f'<g transform="translate(0,{f(dy)})"><g clip-path="url(#cb{i})"><use href="#fullg"/></g></g>')

def A(s): ann.append(s)
TMIN = 2.8
def T(x, y, s, size=2.8, anchor="start", weight="normal", fill="#000", rot=None, ital=False):
    size = max(size, TMIN)
    r = f' transform="rotate({rot},{f(x)},{f(y)})"' if rot is not None else ""
    st = ' font-style="italic"' if ital else ""
    A(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{r}>{s}</text>')
def L(x0, y0, x1, y1, sw=0.15, stroke="#000", extra=""):
    A(f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

xa, xb = X(XR0), X(XMAX)
def zig_h(py):
    xm = xa + (xb - xa) * 0.62
    A(f'<polyline points="{f(xa)},{f(py)} {f(xm-1.5)},{f(py)} {f(xm-0.6)},{f(py-2)} {f(xm+0.6)},{f(py+2)} {f(xm+1.5)},{f(py)} {f(xb)},{f(py)}" fill="none" stroke="#000" stroke-width="0.18"/>')
for i, (lo, hi, top) in enumerate(BANDS):
    bot = top + (hi - lo) / S
    if i > 0: zig_h(top)
    if i < len(BANDS) - 1: zig_h(bot)

def nivel(y, txt, xpos, side="r", sub=""):
    px, py = X(xpos), Y(y)
    A(f'<path d="M{f(px)},{f(py)} l-1.2,-2 h2.4 z" fill="#000"/>')
    L(px - 3.6, py, px + 3.6, py, sw=0.15)
    ax = px + 1.7 if side == "r" else px - 1.7; an = "start" if side == "r" else "end"
    T(ax, py - 2.4 + 2.4 * 0, txt, 2.8, an, "bold")
    if sub: T(ax, py + 3.2, sub, 2.8, an, ital=True)
nivel(6450, "+6,45", -330, "r", "")
nivel(6000, "+6,00", 1250, "r", "")
nivel(3000, "+3,00", 1150, "r", "N.P.T. P. Alta")
nivel(2400, "+2,40", 1350, "r", "")
nivel(5380, "+5,38", 1350, "r", "")
nivel(0, "±0,00", 1150, "r", "N.P.T. P. Baja")
nivel(-100, "-0,10", -250, "r", "")
nivel(-1550, "-1,55", 1200, "r", "")

def cota_v(y0, y1, xpos, txt=None):
    px = X(xpos); p0, p1 = Y(y0), Y(y1)
    L(px, p0, px, p1, 0.12)
    for p in (p0, p1): L(px - 0.7, p + 0.7, px + 0.7, p - 0.7, 0.25); L(px - 1.1, p, px + 1.4, p, 0.1)
    v = txt or f"{abs(y1 - y0)/1000:.2f}".replace(".", ",")
    T(px - 0.8, (p0 + p1) / 2, v, 2.8, "middle", rot=-90)
def cota_h(x0, x1, ypos, txt, below=False):
    py = Y(ypos); a, b = X(x0), X(x1)
    L(a, py, b, py, 0.12)
    for p in (a, b): L(p - 0.7, py + 0.7, p + 0.7, py - 0.7, 0.25); L(p, py - 1.1, p, py + 1.1, 0.1)
    T((a + b) / 2, py + (3.2 if below else -0.7), txt, 2.8, "middle")
cota_v(-1550, 0, -330)
cota_v(2640, 2840, 900, "0,20"); cota_v(2840, 2960, 900, "0,12"); cota_v(5680, 5880, 900, "0,20"); cota_v(5880, 6000, 900, "0,12")
cota_v(-960, -250, 760, "0,71"); cota_v(-1500, -960, 1150, "0,54")
cota_h(-420, 1080, -1610, "1,50", below=True); cota_h(-40, 700, -910, "0,74")
cota_h(230, 430, 1300, "0,20")

T(X(-520), Y(6560), "EXTERIOR", 2.8, fill="#555"); T(X(950), Y(6560), "INTERIOR", 2.8, fill="#555")
T(X(-520), Y(3680), "EXTERIOR", 2.8, fill="#555"); T(X(660), Y(3680), "INTERIOR · PLANTA ALTA", 2.8, fill="#555")
T(X(-520), Y(1380), "EXTERIOR", 2.8, fill="#555"); T(X(660), Y(1380), "INTERIOR · PLANTA BAJA", 2.8, fill="#555")
T(X(1000), Y(6200), "pend. 2 %", 2.8, ital=True, fill="#333")
T(X(820), Y(-1050), "Fundación cortada", 2.8, ital=True, fill="#333")
T(X(820), Y(-1050) + 3.3, "por línea de pernos", 2.8, ital=True, fill="#333")
T(X(450), Y(1250), "Columna HEB 200 en vista", 2.8, ital=True, fill="#333")

# ------------------------------------------------------------------- REFERENCIAS
LEG = [
("CUBIERTA Y PARAPETO", None),
(1, "Cupertina chapa galv. N°22 c/ goterones"),
(2, "Membrana asfáltica 4 mm c/ alum. + babeta"),
(3, "Carpeta de nivelación MHR 1:3, e = 2 cm"),
(4, "Contrapiso H° liviano, pend. 2 %"),
(5, "Barrera de vapor: film polietileno 200 µ"),
(6, "Capa de compresión H°A° s/ malla electrosold."),
(7, "Separador de H° p/ malla electrosoldada"),
(8, "Conectores de corte (pernos) s/ viga IPN"),
(9, "Panel sándwich PUR 40 mm (termopanel)"),
(10, "Perfil L galv. borde de paquete de cubierta"),
(11, "Est. secundaria: omega + perfil Z inferior"),
(12, "Chapa plegada galv. C 75x80 e=2: anclaje panel"),
(13, "Montante parapeto tubo 100x100x3,2 soldado"),
("ESTRUCTURA METÁLICA Y FUNDACIÓN", None),
(14, "Viga perimetral IPN 200, unión sold. + bulones"),
(15, "Viga IPN 180 (vista): chapa sold. + bulones"),
(16, "Columna HEB 200 (en vista)"),
(17, "Placa colaborante galv. (tipo Galvadeck)"),
(18, "Zinguería de borde fijada a la chapa"),
(19, "Platabanda 350x350x25 soldada + cartelas"),
(20, "Tuerca de nivelación / tuerca / contratuerca"),
(21, "Pernos de anclaje Ø20 en \"J\""),
(22, "Grout de nivelación sin contracción, 25 mm"),
(23, "Dado estructural H°A° p/ columna y F. integral"),
(24, "Zapata de H°A°, armadura según cálculo"),
(25, "H° de limpieza, e = 5 cm"),
("FRENTE INTEGRAL", None),
(26, "Travesaño: tapa int. MT-0817 / ext. MT-0819"),
(27, "Columna F.I.: MT-0817 / MT-0819 (en vista)"),
(28, "Doble vidrio hermético 6 + 12 + 6"),
(29, "Tubo 80x50x2 soldado a viga: anclaje F.I."),
(30, "Grapa doble planchuela galv. + bulones M10"),
(31, "Sellador de junta + banda de neopreno"),
(32, "Zinguería a medida p/ cerramiento y buña"),
(33, "Zinguería a medida alféizar c/ pendiente"),
(34, "Aislación térmica: placa EPS 40 mm"),
(35, "Perfil U de arranque fijado al dado c/ brocas"),
(36, "Panel ciego PUR 40 mm en el frente integral"),
("PISOS, BARANDAS Y CIELORRASOS", None),
(37, "Baranda posapié acero inox. Ø42"),
(38, "Planchuela base + brocas Ø10 a losa"),
(39, "Solado s/ adhesivo cementicio"),
(40, "Carpeta hidrófuga MCI + 10 % hidrófugo"),
(41, "Contrapiso H° pobre e=12 cm (relleno)"),
(42, "Separador de suelo: film polietileno 200 µ"),
(43, "Suelo compactado"),
(44, "Cielorraso placa roca de yeso e = 9,5 mm"),
(45, "Vela rígida a losa: montante 35 + ángulo"),
(46, "Perfil Z buña en cielorraso independiente"),
(47, "Perfil C c/ banda neopreno colgado de viga"),
(48, "Vereda de H° peinado"),
(49, "Aislación hidrófuga vertical del dado"),
]

# globos: (n, x, y real, lado 'L'/'R')  -> se apilan por banda en dos columnas
BALL = [
 (1, 100, 6425, 'L'), (9, 10, 6150, 'L'), (11, 42, 6100, 'L'), (12, 90, 6220, 'L'), (13, 180, 6300, 'L'), (32, -25, 5575, 'L'),
 (26, 80, 5530, 'L'), (28, 3, 5200, 'L'), (27, 80, 5100, 'L'), (29, 180, 5745, 'L'), (30, 98, 5700, 'L'),
 (2, 600, 6094, 'R'), (3, 800, 6082, 'R'), (4, 1000, 6050, 'R'), (5, 1100, 6001, 'R'), (10, 233, 6200, 'R'), (6, 1240, 5975, 'R'),
 (7, 610, 5948, 'R'), (17, 1400, 5900, 'R'), (8, 262, 5940, 'R'), (14, 275, 5760, 'R'), (15, 900, 5800, 'R'), (45, 480, 5600, 'R'),
 (44, 1450, 5385, 'R'), (46, 142, 5370, 'L'), (16, 330, 5300, 'R'),
 # entrepiso
 (28, 3, 3400, 'L'), (31, 2, 3115, 'L'), (26, 80, 3070, 'L'), (36, 12, 2900, 'L'), (29, 180, 2760, 'L'), (30, 98, 2690, 'L'),
 (27, 80, 2450, 'L'), (46, 142, 2390, 'L'),
 (37, 340, 3300, 'R'), (38, 345, 3004, 'R'), (39, 900, 2995, 'R'), (3, 1100, 2972, 'R'), (33, 160, 3002, 'R'), (34, 208, 2900, 'R'),
 (18, 227, 2860, 'R'), (6, 1300, 2930, 'R'), (17, 1250, 2845, 'R'), (14, 300, 2700, 'R'), (15, 1000, 2760, 'R'),
 (45, 480, 2600, 'R'), (47, 276, 2500, 'R'), (44, 1450, 2405, 'R'), (16, 330, 2150, 'R'),
 # PB y fundación
 (28, 3, 600, 'L'), (37, 340, 300, 'R'), (26, 80, 60, 'L'), (31, 135, -8, 'R'), (35, 60, -5, 'L'), (33, -50, 0, 'L'),
 (48, -350, -150, 'L'), (49, -43, -400, 'L'), (23, 60, -600, 'L'), (21, 205, -500, 'L'), (24, -200, -1300, 'L'), (25, -300, -1525, 'L'),
 (38, 380, 4, 'R'), (39, 900, -5, 'R'), (3, 1000, -25, 'R'), (40, 1100, -45, 'R'), (41, 1250, -110, 'R'), (42, 1300, -176, 'R'),
 (20, 455, -172, 'R'), (19, 480, -212, 'R'), (22, 470, -238, 'R'), (43, 1400, -600, 'R'),
]
def balloons():
    for bi, (lo, hi, top) in enumerate(BANDS):
        bot = top + (hi - lo) / S
        for side in ('L', 'R'):
            pts = [dict(n=n, ax=X(x), ay=Y(y)) for n, x, y, sd in BALL if sd == side and lo <= y <= hi]
            pts.sort(key=lambda p: p['ay'])
            gap = 5.4; ymin = top + 3.0; ymax = bot - 3.0
            for k, p in enumerate(pts): p['by'] = max(p['ay'], pts[k - 1]['by'] + gap if k else ymin)
            for k in range(len(pts) - 1, -1, -1):
                lim = ymax if k == len(pts) - 1 else pts[k + 1]['by'] - gap
                if pts[k]['by'] > lim: pts[k]['by'] = lim
            bx = X(XR0) + 3.0 if side == 'L' else X(XMAX) + 5.5
            for p in pts:
                kx = bx + 2.35 if side == 'L' else bx - 2.35
                A(f'<circle cx="{f(p["ax"])}" cy="{f(p["ay"])}" r="0.32" fill="#000"/>')
                A(f'<polyline points="{f(p["ax"])},{f(p["ay"])} {f(kx + (3 if side == "L" else -3))},{f(p["by"])} {f(kx)},{f(p["by"])}" fill="none" stroke="#000" stroke-width="0.11"/>')
                A(f'<circle cx="{f(bx)}" cy="{f(p["by"])}" r="2.35" fill="#fff" stroke="#000" stroke-width="0.2"/>')
                T(bx, p['by'] + 1.0, str(p['n']), 2.8, "middle", "bold")
balloons()
for n, (x0, x1, y0, y1) in ((1, (-40, 510, 5400, 6470)), (2, (-40, 510, 2390, 3475)), (3, (-400, 850, -500, 200))):
    A(f'<rect x="{f(X(x0))}" y="{f(Y(y1))}" width="{f((x1 - x0) / S)}" height="{f((y1 - y0) / S)}" rx="2" fill="none" stroke="#c0392b" stroke-width="0.3" stroke-dasharray="1.6 0.8"/>')
    A(f'<rect x="{f(X(x1) - 6.2)}" y="{f(Y(y1) - 2.6)}" width="6.2" height="5.2" fill="#fff" stroke="#c0392b" stroke-width="0.3"/>')
    T(X(x1) - 3.1, Y(y1) + 1.0, f"D{n}", 2.8, "middle", "bold", "#c0392b")

# ------------------------------------------------------------------- TÍTULO, REFERENCIAS, RÓTULO
T(10, 17, "CORTE INTEGRAL ACERO", 6.2, weight="bold")
T(10, 24.5, "FRENTE INTEGRAL", 6.2, weight="bold")
T(10, 31, "Corte integral ESC. 1:20 · Detalles axonométricos ESC. 1:10", 3.2)
# escala gráfica 1:20 (0 a 1 m)
def escala_grafica(x0, y0, den, total_m, step_m, lab):
    w = total_m * 1000 / den; n = int(round(total_m / step_m))
    for k in range(n):
        A(f'<rect x="{f(x0 + k * w / n)}" y="{f(y0)}" width="{f(w / n)}" height="1.2" fill="{"#000" if k % 2 == 0 else "#fff"}" stroke="#000" stroke-width="0.12"/>')
    for k in range(n + 1):
        T(x0 + k * w / n, y0 + 4.4, (f"{k * step_m:.2f}".rstrip("0").rstrip(".")).replace(".", ","), 2.8, "middle")
    T(x0 + w + 2.5, y0 + 1.3, lab, 2.8)
escala_grafica(12, 35, 20, 1.0, 0.25, "m  · esc. 1:20")
escala_grafica(90, 35, 10, 0.5, 0.1, "m  · esc. 1:10")

T(10, 48.5, "REFERENCIAS", 4.2, weight="bold")
items = [it for it in LEG if it[1] is not None]
y0 = 53.2; dy = 3.05
NCOL = 25
for k, (n, txt) in enumerate(items):
    col, row = (0, k) if k < NCOL else (1, k - NCOL)
    xn = 13.6 if col == 0 else 92.0
    T(xn, y0 + row * dy, str(n), 2.8, "end", "bold")
    T(xn + 1.2, y0 + row * dy, txt, 2.8)
YREF_END = y0 + (NCOL - 1) * dy

# rótulo
A('<rect x="8" y="399" width="281" height="15.5" fill="none" stroke="#000" stroke-width="0.35"/>')
for xx in (38, 150, 236):
    A(f'<line x1="{xx}" y1="399" x2="{xx}" y2="414.5" stroke="#000" stroke-width="0.25"/>')
T(10, 405.2, "TP N°6", 5.0, weight="bold")
T(10, 409.4, "FECHA: 29/10/2026", 2.8)
T(10, 413.0, "LÁMINA: A3", 2.8)
T(40, 403.4, "DOCENTE: Arq. Tucci y Arq. Cardozo", 2.8)
T(40, 407.6, "ALUMNA: Candelaria Vitale", 2.8, weight="bold")
T(40, 411.8, "GRUPO: 13", 2.8)
T(152, 403.4, "NIVEL:", 2.8)
T(152, 407.6, "OBS: corte integral esc. 1:20 / detalles esc. 1:10", 2.8)
T(238.5, 405.0, "CONSTRUCCIONES II", 2.8)
T(238.5, 409.2, "CATEDRA: ARQ. TUCCI", 2.8)

SVG_BODY = f'''<defs>{"".join(defs)}<g id="fullg">{"".join(full)}</g></defs>
<rect x="0" y="0" width="297" height="420" fill="#fff"/>
<rect x="4" y="4" width="289" height="412" fill="none" stroke="#000" stroke-width="0.45"/>
{"".join(uses)}
{"".join(ann)}'''
os.makedirs("build", exist_ok=True)
open("build/corte.svgpart", "w").write(SVG_BODY)
json.dump(dict(LEG=LEG, YREF_END=YREF_END), open("build/corte.json", "w"), ensure_ascii=False)
print("ok refs hasta", YREF_END, "bandas:", [(t, t + (h - l) / S) for l, h, t in BANDS])
