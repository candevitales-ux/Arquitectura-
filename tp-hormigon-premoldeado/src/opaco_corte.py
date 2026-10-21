# -*- coding: utf-8 -*-
"""Lámina TP final - HORMIGÓN PREMOLDEADO DE GRANDES LUCES · CERRAMIENTO OPACO (A3 vertical).
Corte integral 1:20 + referencias + rótulo (los 3 nudos 3D los agrega src/opaco.html).
Geometría en mm reales; x+ hacia el interior, y+ hacia arriba, ±0.00 = NPT planta baja.

Corte ENTRE columnas (vigas VP cortadas, columna y ménsulas en vista detrás); bajo ±0,00 el corte
se quiebra al eje de la columna para mostrar columna, cáliz y base cortados.
  panel sándwich  x -220..-20   (hoja ext. 60 | EPS 60 | hoja int. portante 80)
  junta           x  -20..0
  columna / VP-70 x    0..400
"""
import os

S = 20.0
XR0, XMAX = -700.0, 1100.0
PX0 = 196.0
def X(x): return PX0 + (x - XR0) / S
def YC(y): return 1000.0 - y / S

# bandas (real lo, real hi, y papel superior)
BANDS = [(8050, 10300, 8.0), (2850, 4700, 124.5), (-2050, 1300, 221.0)]
def Y(y):
    for lo, hi, top in BANDS:
        if lo - 1 <= y <= hi + 1: return YC(y) + (top - YC(hi))
    raise ValueError(y)

full, ann, defs = [], [], []
f = lambda v: f"{v:.3f}"

def poly(pts, fill="none", stroke="#000", sw=0.3, extra=""):
    d = " ".join(f"{f(X(x))},{f(YC(y))}" for x, y in pts)
    full.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
def rect(x0, y0, x1, y1, **k): poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)
def line(x0, y0, x1, y1, stroke="#000", sw=0.18, extra=""):
    full.append(f'<line x1="{f(X(x0))}" y1="{f(YC(y0))}" x2="{f(X(x1))}" y2="{f(YC(y1))}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" {extra}/>')
def pline(pts, stroke="#000", sw=0.18, extra="", fill="none"):
    d = " ".join(f"{f(X(x))},{f(YC(y))}" for x, y in pts)
    full.append(f'<polyline points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
def circ(x, y, r, fill="#000", stroke="none", sw=0.1):
    full.append(f'<circle cx="{f(X(x))}" cy="{f(YC(y))}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

CUT = dict(stroke="#000", sw=0.35)      # contorno de elemento cortado
CUTT = dict(stroke="#000", sw=0.2)      # contorno de capa delgada cortada
VIEW = dict(stroke="#555", sw=0.13)     # en vista
DASH = 'stroke-dasharray="1.2 0.6"'
REB = "#3a3a3a"                          # armaduras (escala de grises)
STEEL = "#4a4a4a"; GALV = "#8c8c8c"; NEO = "#111"; VISTA = "#f0f0f0"; VISTA2 = "#e4e4e4"

# ---------------------------------------------------------------- rayados (escala de grises, SIEMPRE a 45° en el mismo sentido)
defs.append('''
<pattern id="pHA" patternUnits="userSpaceOnUse" width="1.2" height="1.2" patternTransform="rotate(45)">
 <rect width="1.2" height="1.2" fill="#d6d6d6"/><line x1="0" y1="0" x2="0" y2="1.2" stroke="#3c3c3c" stroke-width="0.09"/></pattern>
<pattern id="pHAis" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)">
 <rect width="2.2" height="2.2" fill="#e2e2e2"/><line x1="0" y1="0" x2="0" y2="2.2" stroke="#3c3c3c" stroke-width="0.09"/>
 <circle cx="1.1" cy="0.55" r="0.13" fill="#3c3c3c"/><circle cx="1.5" cy="1.6" r="0.09" fill="#3c3c3c"/></pattern>
<pattern id="pH" patternUnits="userSpaceOnUse" width="3" height="3">
 <rect width="3" height="3" fill="#ebebeb"/><circle cx="0.6" cy="0.7" r="0.16" fill="#555"/><circle cx="2.1" cy="1.9" r="0.12" fill="#555"/>
 <path d="M1.7 0.4 l0.35 0.55 h-0.7z" fill="none" stroke="#555" stroke-width="0.07"/><path d="M0.5 2.2 l0.3 0.45 h-0.6z" fill="none" stroke="#555" stroke-width="0.07"/>
 <circle cx="2.6" cy="0.5" r="0.07" fill="#555"/><circle cx="1.2" cy="2.7" r="0.07" fill="#555"/></pattern>
<pattern id="pLiv" patternUnits="userSpaceOnUse" width="1.6" height="1.6">
 <rect width="1.6" height="1.6" fill="#f3f3f3"/><circle cx="0.4" cy="0.45" r="0.22" fill="none" stroke="#666" stroke-width="0.06"/>
 <circle cx="1.2" cy="1.15" r="0.17" fill="none" stroke="#666" stroke-width="0.06"/><circle cx="1.25" cy="0.3" r="0.05" fill="#666"/></pattern>
<pattern id="pMort" patternUnits="userSpaceOnUse" width="1.0" height="1.0">
 <rect width="1" height="1" fill="#ececec"/><circle cx="0.25" cy="0.3" r="0.07" fill="#666"/><circle cx="0.75" cy="0.8" r="0.05" fill="#666"/></pattern>
<pattern id="pHid" patternUnits="userSpaceOnUse" width="1.0" height="1.0">
 <rect width="1" height="1" fill="#c8c8c8"/><circle cx="0.25" cy="0.3" r="0.08" fill="#222"/><circle cx="0.75" cy="0.8" r="0.06" fill="#222"/></pattern>
<pattern id="pGrout" patternUnits="userSpaceOnUse" width="0.8" height="0.8">
 <rect width="0.8" height="0.8" fill="#b9b9b9"/><circle cx="0.2" cy="0.2" r="0.08" fill="#222"/><circle cx="0.6" cy="0.6" r="0.08" fill="#222"/></pattern>
<pattern id="pTierra" patternUnits="userSpaceOnUse" width="5" height="5" patternTransform="rotate(45)">
 <rect width="5" height="5" fill="#ececec"/><g stroke="#6a6a6a" stroke-width="0.12"><line x1="0.5" y1="0" x2="0.5" y2="1.6"/><line x1="1.1" y1="0" x2="1.1" y2="1.6"/>
 <line x1="3" y1="2.6" x2="3" y2="4.2"/><line x1="3.6" y1="2.6" x2="3.6" y2="4.2"/></g>
 <circle cx="4.2" cy="1" r="0.14" fill="#6a6a6a"/><circle cx="1.4" cy="3.7" r="0.14" fill="#6a6a6a"/></pattern>
<pattern id="pTosca" patternUnits="userSpaceOnUse" width="2" height="2">
 <rect width="2" height="2" fill="#dedede"/><circle cx="0.5" cy="0.5" r="0.18" fill="#5a5a5a"/><circle cx="1.5" cy="1.4" r="0.12" fill="#5a5a5a"/></pattern>
<pattern id="pEPS" patternUnits="userSpaceOnUse" width="1.6" height="1.6">
 <rect width="1.6" height="1.6" fill="#fafafa"/><path d="M0 0.8 L0.4 0.3 L0.8 0.8 L1.2 1.3 L1.6 0.8" fill="none" stroke="#6a6a6a" stroke-width="0.09"/></pattern>
<pattern id="pEPSv" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(90)">
 <rect width="1.6" height="1.6" fill="#fafafa"/><path d="M0 0.8 L0.4 0.3 L0.8 0.8 L1.2 1.3 L1.6 0.8" fill="none" stroke="#6a6a6a" stroke-width="0.09"/></pattern>
<pattern id="pLana" patternUnits="userSpaceOnUse" width="1.2" height="1.0" patternTransform="rotate(90)">
 <rect width="1.2" height="1" fill="#f2f2f2"/><path d="M0 0.5 C0.3 0 0.3 0 0.6 0.5 S0.9 1 1.2 0.5" fill="none" stroke="#5a5a5a" stroke-width="0.08"/></pattern>
<pattern id="pPorc" patternUnits="userSpaceOnUse" width="4" height="4"><rect width="4" height="4" fill="#a9a9a9"/></pattern>
''')

# =====================================================================================
#  GEOMETRÍA
# =====================================================================================
def vp_shape(yb):
    """viga VP-70 pretensada doble T (Astori): b = 0,40, h = 0,70, alma 0,12"""
    P = [(0, 0), (400, 0), (400, 130), (260, 190), (260, 520), (400, 580), (400, 700), (0, 700), (0, 580), (140, 520), (140, 190), (0, 130)]
    return [(x, yb + y) for x, y in P]
def viga_vp(yb):
    poly(vp_shape(yb), fill="url(#pHA)", **CUT)
    for xx in (50, 125, 200, 275, 350): circ(xx, yb + 45, 0.3)              # cordones de pretensado
    for xx in (170, 230): circ(xx, yb + 100, 0.3)
    for xx in (40, 360): circ(xx, yb + 660, 0.25, fill=REB)
    pline([(25, yb + 25), (375, yb + 25), (375, yb + 110), (235, yb + 170), (235, yb + 540), (375, yb + 600), (375, yb + 675),
           (25, yb + 675), (25, yb + 600), (165, yb + 540), (165, yb + 170), (25, yb + 110), (25, yb + 25)], stroke=REB, sw=0.1, extra=DASH)

def fija_panel(yy):
    """fija panel completo: riel embutido en el panel + bulón T, ángulo 1 (al panel), ángulo 2 (al alma de la VP)
    unidos con bulón en agujeros ovalados (regulación) + bulón M16 pasante en vaina del alma, arandela y tuerca."""
    # riel de anclaje (tipo Halfen) embutido en la hoja interior, en corte
    poly([(-20, yy - 20), (-50, yy - 20), (-50, yy + 20), (-20, yy + 20), (-20, yy + 11), (-44, yy + 11), (-44, yy - 11), (-20, yy - 11)], fill=STEEL, stroke="#000", sw=0.06)
    for dy in (-15, 15): line(-50, yy + dy, -88, yy + dy, stroke="#000", sw=0.16)    # anclajes del riel
    rect(-42, yy - 9, -30, yy + 9, fill="#222", stroke="none", sw=0)                  # cabeza del bulón T
    line(-30, yy, -6, yy, stroke="#000", sw=0.3)                                       # bulón T M16
    rect(-10, yy - 9, -4, yy + 9, fill="#222", stroke="none", sw=0)                    # tuerca
    # ángulo 1 (L 100x100x10) contra el panel
    poly([(-20, yy - 50), (-10, yy - 50), (-10, yy + 30), (90, yy + 30), (90, yy + 40), (-20, yy + 40)], fill=GALV, stroke="#000", sw=0.08)
    # ángulo 2 (L 100x100x10) contra el alma de la VP
    poly([(30, yy + 40), (140, yy + 40), (140, yy + 140), (130, yy + 140), (130, yy + 50), (30, yy + 50)], fill=GALV, stroke="#000", sw=0.08)
    line(60, yy + 15, 60, yy + 70, stroke="#000", sw=0.3)                              # bulón de regulación (ovalados)
    rect(50, yy + 50, 70, yy + 58, fill="#222", stroke="none", sw=0); rect(50, yy + 22, 70, yy + 30, fill="#222", stroke="none", sw=0)
    rect(140, yy + 78, 260, yy + 102, fill="none", stroke="#333", sw=0.1, extra=DASH)  # vaina en el alma
    line(118, yy + 90, 292, yy + 90, stroke="#000", sw=0.32)                           # bulón M16 pasante
    rect(118, yy + 78, 130, yy + 102, fill="#222", stroke="none", sw=0)
    rect(260, yy + 74, 266, yy + 106, fill="#222", stroke="none", sw=0); rect(266, yy + 80, 282, yy + 100, fill="#222", stroke="none", sw=0)

def panel(y0, y1):
    """panel sándwich premoldeado e = 0,20: hoja ext. H°A 60 | EPS 60 | hoja int. portante H°A 80; bordes macizos"""
    rect(-220, y0, -20, y1, fill="url(#pHA)", **CUT)
    rect(-160, y0 + 60, -100, y1 - 60, fill="url(#pEPSv)", stroke="#000", sw=0.12)
    for xx in (-190, -60): line(xx, y0 + 30, xx, y1 - 30, stroke=REB, sw=0.09, extra='stroke-dasharray="2 0.6"')   # mallas
    for yy in range(y0 + 500, y1 - 300, 700): line(-170, yy, -90, yy + 60, stroke="#222", sw=0.16)                # conectores de fibra de vidrio
    # buña para la babeta (cara interior, en el parapeto)
    rect(-38, 9930, -20, 9950, fill="#fff", stroke="#000", sw=0.1)

def columna_vista(y0, y1):
    rect(0, y0, 400, y1, fill=VISTA, **VIEW)
def mensula_lateral_vista(ytop):
    """ménsula lateral (apoyo de la VP) vista de frente: cara frontal + diagonal a 45° hasta la columna"""
    rect(0, ytop - 450, 400, ytop, fill=VISTA2, stroke="#333", sw=0.15)
    line(0, ytop - 250, 400, ytop - 250, stroke="#666", sw=0.1)
    rect(10, ytop, 390, ytop + 10, fill=NEO, stroke="none", sw=0)
def mensula_interior_vista(ytop):
    """ménsula interior de la columna (apoyo del recorte de losa) en vista de perfil: sup. horizontal, frente 0,25, diagonal 45°"""
    poly([(400, ytop), (600, ytop), (600, ytop - 250), (400, ytop - 450)], fill=VISTA2, stroke="#333", sw=0.18)
    rect(420, ytop, 590, ytop + 10, fill=NEO, stroke="none", sw=0)
    pline([(380, ytop - 40), (570, ytop - 40), (570, ytop - 240), (400, ytop - 410)], stroke=REB, sw=0.1, extra=DASH)

# ---------------------------------------------------------------- TERRENO Y FUNDACIÓN (corte por eje de columna)
rect(-700, -2050, 1100, -380, fill="url(#pTierra)", stroke="none", sw=0)
rect(-750, -1950, 1150, -1900, fill="url(#pH)", **CUTT)                                # H° de limpieza
def teeth(x, ya, yb, s):
    pts = []; y = ya; k = 0
    while y < yb - 1:
        pts += [(x, y), (x + s * 15, y + 25), (x + s * 15, y + 75), (x, y + 100)]; y += 100
    return pts
left_in = teeth(-50, -1400, -650, 1)                                                   # cara interior pared izq. (de abajo hacia arriba)
right_in = [(x, y) for x, y in reversed(teeth(450, -1400, -650, -1))]                  # pared der. (de arriba hacia abajo)
base = [(-700, -1900), (1100, -1900), (1100, -1650), (700, -1400), (650, -1400), (650, -650), (450, -650)] + right_in + \
       [(450, -1400), (-50, -1400)] + left_in + [(-50, -650), (-250, -650), (-250, -1400), (-300, -1400), (-700, -1650)]
rect(-50, -1400, 450, -650, fill="url(#pGrout)", **CUTT)                              # relleno grout sin contracción
poly(base, fill="url(#pHAis)", **CUT)
rect(0, -1350, 400, 0, fill="url(#pHA)", **CUT)                                        # columna empotrada (cortada)
rect(-40, -1400, 440, -1350, fill="url(#pMort)", **CUTT)                               # mortero de nivelación bajo columna
rect(0, -1350, 400, 0, fill="url(#pHA)", **CUT)
for xx in (45, 355): line(xx, -1320, xx, 0, stroke=REB, sw=0.12)
for yy in range(-1300, 0, 150): line(30, yy, 370, yy, stroke=REB, sw=0.07, extra=DASH)
# armadura de base y pedestal
pline([(-640, -1780), (-640, -1850), (1040, -1850), (1040, -1780)], stroke=REB, sw=0.22)
for xx in range(-600, 1050, 120): circ(xx, -1835, 0.26, fill=REB)
for xx in (-200, -110, 510, 600):
    pline([(xx + (-60 if xx < 200 else 60), -1850), (xx, -1850), (xx, -700)], stroke=REB, sw=0.16)
for yy in range(-1300, -680, 160): pline([(-210, yy), (-90, yy)], stroke=REB, sw=0.08, extra=DASH); pline([(490, yy), (610, yy)], stroke=REB, sw=0.08, extra=DASH)
# viga portapanel premoldeada (solo bajo los paneles) s/ neopreno en la pared del cáliz
rect(-245, -650, -50, -640, fill=NEO, stroke="none", sw=0)
poly([(-245, -640), (-20, -640), (-20, -50), (-220, -50), (-245, -75)], fill="url(#pHA)", **CUT)
for xx, yy in ((-215, -600), (-50, -600), (-215, -110), (-50, -110)): circ(xx, yy, 0.3, fill=REB)
pline([(-228, -620), (-36, -620), (-36, -90), (-228, -90), (-228, -620)], stroke=REB, sw=0.1, extra=DASH)
line(-247, -640, -247, -205, stroke="#000", sw=0.5)                                    # pintura asfáltica (cara enterrada)
rect(-20, -640, 0, -50, fill="url(#pEPSv)", **CUTT)                                    # junta EPS viga / columna
# arranque del panel: mortero de asiento + calces de neopreno, pasador Ø16 en vaina c/ grout, sellador exterior
rect(-220, -50, -20, -40, fill="url(#pMort)", **CUTT)
rect(-180, -50, -140, -40, fill=NEO, stroke="none", sw=0)
rect(-75, -330, -45, 230, fill="url(#pGrout)", stroke="#333", sw=0.1)
line(-60, -320, -60, 220, stroke="#000", sw=0.32)
rect(-232, -52, -219, -38, fill="#111", stroke="none", sw=0)
rect(-20, -50, 0, 0, fill=NEO, stroke="none", sw=0)                                     # sellador junta panel / columna (interior)
# vereda exterior
def yv(x): return -200 - (-245 - x) * 0.02
poly([(-700, yv(-700) - 180), (-255, -380), (-255, -280), (-700, yv(-700) - 80)], fill="url(#pTosca)", **CUTT)
poly([(-700, yv(-700) - 80), (-255, -280), (-255, -200), (-700, yv(-700))], fill="url(#pH)", **CUTT)
rect(-255, -280, -247, -200, fill="url(#pEPSv)", stroke="#000", sw=0.08); rect(-255, -212, -247, -200, fill=NEO, stroke="none", sw=0)
line(-700, yv(-700) - 180, -700, yv(-700), sw=0.1)
# piso sobre terreno (interior)
rect(400, -420, 1100, -157, fill="url(#pTosca)", **CUTT)
rect(420, -157, 1100, -155, fill="#000", stroke="none", sw=0)                           # film 200 µ
rect(420, -155, 1100, -35, fill="url(#pH)", **CUTT)                                     # contrapiso H° armado
pline([(440, -95), (1100, -95)], stroke=REB, sw=0.1, extra='stroke-dasharray="2 0.5"')
rect(420, -35, 1100, -15, fill="url(#pHid)", **CUTT)                                    # carpeta hidrófuga
rect(420, -15, 1100, -10, fill="#777", stroke="none", sw=0)                             # adhesivo
rect(420, -10, 1100, 0, fill="url(#pPorc)", **CUTT)                                     # cerámico
for xx in (750,): line(xx, -10, xx, 0, sw=0.15)
rect(400, -400, 420, 0, fill="url(#pEPSv)", **CUTT); rect(400, -10, 420, 0, fill=NEO, stroke="none", sw=0)
line(1100, -420, 1100, 0, sw=0.1)

# ---------------------------------------------------------------- ESTRUCTURA EN VISTA (detrás del plano de corte)
columna_vista(0, 3335); columna_vista(4500, 8300)
rect(0, 3335, 400, 3345, fill=NEO, stroke="none", sw=0)
rect(0, 8300, 400, 8310, fill=NEO, stroke="none", sw=0)                                 # neopreno s/ cabeza de columna
mensula_lateral_vista(3335)
mensula_interior_vista(4045)
line(400, 4500, 400, 4045, stroke="#555", sw=0.13)

# ---------------------------------------------------------------- PANEL
panel(-40, 10200)

# ---------------------------------------------------------------- ENTREPISO (NPT +4,50)
viga_vp(3345)
rect(-20, 3345, 0, 4355, fill="url(#pLana)", **CUTT)                                    # junta c/ lana mineral (cortafuego)
rect(-20, 3345, 0, 3360, fill=NEO, stroke="none", sw=0)                                 # sellador inferior
fija_panel(3680)
rect(100, 4045, 390, 4055, fill=NEO, stroke="none", sw=0)                               # neopreno continuo s/ VP
# losa alveolar ALV-30: cáscaras cortadas, alvéolo (vista de su tabique) y tapón macizo en el apoyo
rect(10, 4055, 1100, 4355, fill="url(#pHA)", **CUT)
rect(170, 4095, 1100, 4315, fill=VISTA, stroke="#000", sw=0.15)
rect(10, 4095, 170, 4315, fill="url(#pHAis)", stroke="#000", sw=0.15)
line(20, 4075, 1100, 4075, stroke="#000", sw=0.22)                                       # cordón de pretensado
# capa de compresión + paquete de piso hasta el panel (junta perimetral)
rect(-10, 4355, 1100, 4405, fill="url(#pHAis)", **CUT)
pline([(10, 4380), (1100, 4380)], stroke=REB, sw=0.12, extra='stroke-dasharray="2 0.5"')
for xx in range(60, 1100, 150): circ(xx, 4380, 0.16, fill=REB)
rect(-10, 4405, 1100, 4465, fill="url(#pLiv)", **CUTT)
rect(-10, 4465, 1100, 4485, fill="url(#pMort)", **CUTT)
rect(-10, 4485, 1100, 4490, fill="#777", stroke="none", sw=0)
rect(-10, 4490, 1100, 4500, fill="url(#pPorc)", **CUTT)
line(700, 4490, 700, 4500, sw=0.15)
rect(-20, 4355, -10, 4500, fill="url(#pEPSv)", stroke="#000", sw=0.08); rect(-20, 4488, -10, 4500, fill=NEO, stroke="none", sw=0)
rect(-20, 4500, -10, 4600, fill="#bdbdbd", stroke="#000", sw=0.1)                       # zócalo
# cielorraso suspendido (PB)
rect(-8, 3250, 1100, 3262.5, fill="#f7f7f7", **CUTT)
pline([(-20, 3330), (-20, 3245), (25, 3245)], stroke="#000", sw=0.25)                   # perfil perimetral (buña)
for xx in (250, 650, 1000): rect(xx - 17, 3262.5, xx + 17, 3297.5, fill=GALV, stroke="#333", sw=0.08)
for xx in (650, 1000):
    line(xx, 3297.5, xx, 4055, stroke="#333", sw=0.16)                                  # vela regulable
    rect(xx - 25, 4048, xx + 25, 4055, fill="#333", stroke="none", sw=0)

# ---------------------------------------------------------------- CUBIERTA
viga_vp(8310)
rect(-20, 8310, 0, 9010, fill="url(#pLana)", **CUTT)
rect(-20, 8310, 0, 8325, fill=NEO, stroke="none", sw=0)
fija_panel(8645)
# panel Pi: nervio en vista, losa superior cortada (el corte pasa entre nervios)
rect(400, 9020, 1100, 9460, fill=VISTA, **VIEW)
rect(220, 9010, 390, 9020, fill=NEO, stroke="none", sw=0)
rect(200, 9460, 1100, 9520, fill="url(#pHA)", **CUT)
line(200, 9020, 400, 9020, stroke="#555", sw=0.1, extra=DASH)
rect(298, 8800, 312, 9300, fill="none", stroke="#222", sw=0.12, extra=DASH)             # pasador Ø16 (oculto)
# H° in situ: macizado entre nervios s/ la viga + canaleta
poly([(0, 9010), (400, 9010), (400, 9460), (200, 9460), (200, 9250), (0, 9250)], fill="url(#pHAis)", **CUT)
for xx in (120, 280): pline([(xx - 40, 8930), (xx - 40, 9200), (xx + 40, 9200), (xx + 40, 8930)], stroke=REB, sw=0.2)  # estribos salientes VP
for xx in (80, 320): circ(xx, 9180, 0.25, fill=REB)
rect(-20, 9010, 0, 9250, fill="url(#pEPSv)", **CUTT)                                    # junta EPS panel / H° in situ
# paquete de cubierta (pendiente 2 % hacia la canaleta)
x0, x1 = 200, 1100
def sl(x, b): return b + (x - x0) * 0.02
rect(x0, 9520, x1, 9523, fill="#000", stroke="none", sw=0)                              # barrera de vapor
rect(x0, 9523, x1, 9573, fill="url(#pEPS)", **CUTT)                                     # plancha EPS 50
poly([(x0, 9573), (x1, 9573), (x1, sl(x1, 9633)), (x0, 9633)], fill="url(#pLiv)", **CUTT)   # contrapiso liviano H°-EPS
poly([(x0, 9633), (x1, sl(x1, 9633)), (x1, sl(x1, 9653)), (x0, 9653)], fill="url(#pMort)", **CUTT)  # carpeta
# canaleta: carpeta + medias cañas, membrana continua desde la cubierta hasta la babeta del parapeto
rect(-20, 9250, 200, 9270, fill="url(#pMort)", **CUTT)
rect(185, 9270, 200, 9633, fill="url(#pMort)", **CUTT)
poly([(185, 9270), (145, 9270), (185, 9310)], fill="url(#pMort)", **CUTT)
poly([(-20, 9270), (20, 9270), (-20, 9310)], fill="url(#pMort)", **CUTT)
pline([(x1, sl(x1, 9656)), (200, 9656), (181, 9637), (181, 9312), (143, 9274), (22, 9274), (-16, 9312), (-16, 9890)], stroke="#000", sw=0.45)
pline([(-38, 9940), (-26, 9940), (-11, 9925), (-11, 9860)], stroke="#000", sw=0.25)    # babeta
rect(-37, 9931, -21, 9949, fill="#222", stroke="none", sw=0)
# cupertina (pendiente hacia el interior, goterones a ambos lados) fijada c/ tornillo + arandela de neopreno
pline([(-262, 10095), (-245, 10112), (-245, 10222), (8, 10210), (8, 10112), (25, 10095)], stroke="#000", sw=0.32)
line(-110, 10150, -110, 10220, stroke="#000", sw=0.2); rect(-125, 10217, -95, 10224, fill="#222", stroke="none", sw=0)
rect(-220, 10200, -20, 10206, fill="#888", stroke="none", sw=0)                          # cordón sellador / asiento

# =====================================================================================
#  COMPOSICIÓN
# =====================================================================================
uses = []
for i, (lo, hi, top) in enumerate(BANDS):
    dy = top - YC(hi)
    defs.append(f'<clipPath id="cb{i}" clipPathUnits="userSpaceOnUse"><rect x="{f(X(XR0))}" y="{f(YC(hi))}" width="{f(X(XMAX) - X(XR0))}" height="{f((hi-lo)/S)}"/></clipPath>')
    uses.append(f'<g transform="translate(0,{f(dy)})"><g clip-path="url(#cb{i})"><use href="#fullg"/></g></g>')

def A(s): ann.append(s)
TMIN = 2.8
def T(x, y, s, size=2.0, anchor="start", weight="normal", fill="#000", rot=None, ital=False):
    size = max(size, TMIN)
    r = f' transform="rotate({rot},{f(x)},{f(y)})"' if rot is not None else ""
    st = ' font-style="italic"' if ital else ""
    A(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{r}>{s}</text>')
def L(x0, y0, x1, y1, sw=0.15, stroke="#000", extra=""):
    A(f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

xa, xb = X(XR0), X(XMAX)
def zig_h(py):
    xm = (xa + xb) / 2 + 20
    A(f'<polyline points="{f(xa)},{f(py)} {f(xm-1.5)},{f(py)} {f(xm-0.6)},{f(py-2)} {f(xm+0.6)},{f(py+2)} {f(xm+1.5)},{f(py)} {f(xb)},{f(py)}" fill="none" stroke="#000" stroke-width="0.18"/>')
for i, (lo, hi, top) in enumerate(BANDS):
    bot = top + (hi - lo) / S
    if i > 0: zig_h(top)
    if i < len(BANDS) - 1: zig_h(bot)
# línea de corte quebrado a ±0,00 (arriba: entre columnas · abajo: eje de columna)
A(f'<line x1="{f(X(-20))}" y1="{f(Y(0))}" x2="{f(X(1100))}" y2="{f(Y(0))}" stroke="#000" stroke-width="0.12" stroke-dasharray="3 0.6 0.6 0.6"/>')

def nivel(y, txt, xpos, side="r", sub=""):
    px, py = X(xpos), Y(y)
    A(f'<path d="M{f(px)},{f(py)} l-1.2,-2 h2.4 z" fill="#000"/>')
    L(px - 3.6, py, px + 3.6, py, sw=0.15)
    ax = px + 1.7 if side == "r" else px - 1.7; an = "start" if side == "r" else "end"
    st = f' <tspan font-weight="normal" font-style="italic" font-size="2.6">{sub}</tspan>' if sub else ""
    A(f'<text x="{f(ax)}" y="{f(py - 1.6)}" font-size="2.8" text-anchor="{an}" font-weight="bold">{txt}{st}</text>')
nivel(10222, "+10,22", -650, "r")
nivel(9660, "+9,66", 1080, "l")
nivel(8310, "+8,31", 1080, "l", "fondo VP")
nivel(4500, "+4,50", 1080, "l", "NPT")
nivel(3250, "+3,25", 1080, "l", "cielorraso")
nivel(0, "±0,00", 1080, "l", "NPT")
nivel(-200, "-0,20", -650, "r")
nivel(-650, "-0,65", 1080, "l", "sup. cáliz")
nivel(-1950, "-1,95", 1080, "l", "fundación")

def cota_v(y0, y1, xpos, txt=None):
    px = X(xpos); p0, p1 = Y(y0), Y(y1)
    L(px, p0, px, p1, 0.12)
    for p in (p0, p1): L(px - 0.7, p + 0.7, px + 0.7, p - 0.7, 0.25); L(px - 1.1, p, px + 1.4, p, 0.1)
    v = txt or f"{abs(y1 - y0)/1000:.2f}".replace(".", ",")
    T(px - 0.7, (p0 + p1) / 2, v, 1.6, "middle", rot=-90)
def cota_h(x0, x1, ypos, txt, below=False):
    py = Y(ypos); a, b = X(x0), X(x1)
    L(a, py, b, py, 0.12)
    for p in (a, b): L(p - 0.7, py + 0.7, p + 0.7, py - 0.7, 0.25); L(p, py - 1.1, p, py + 1.1, 0.1)
    T((a + b) / 2, py + (3.2 if below else -0.6), txt, 1.5, "middle")
cota_v(0, 4500, -650); cota_v(4500, 9660, -650, "5,16"); cota_v(-1950, 0, -650)
cota_v(8310, 9010, 520, "0,70"); cota_v(9020, 9520, 1000, "0,50"); cota_v(4055, 4355, 1050, "0,30")
cota_v(9660, 10200, -380, "0,54")
cota_v(-1400, -650, 1000, "0,75")
cota_h(-220, -20, 4650, "20"); cota_h(0, 400, 4650, "40")
cota_h(-700, 1100, -2030, "1,80 (s/ cálculo)", below=True)

T(X(-680), Y(8150), "EXTERIOR", 2.0, fill="#555"); T(X(500), Y(8150), "INTERIOR · P. ALTA", 2.0, fill="#555")
T(X(-620), Y(2950), "EXTERIOR", 2.0, fill="#555")
T(X(-680), Y(1150), "EXTERIOR", 2.0, fill="#555"); T(X(450), Y(1150), "INTERIOR · P. BAJA", 2.0, fill="#555")
T(275, 31, "pend. 2 %", 1.4, ital=True, fill="#333")
T(X(500), Y(2900), "Columna y ménsulas en vista", 1.4, ital=True, fill="#333")
T(266, 324, "Corte por eje", 1.4, ital=True, fill="#333")
T(266, 327.4, "de columna", 1.4, ital=True, fill="#333")

# ------------------------------------------------------------------ REFERENCIAS (globos)
def ref(n, x, y, bx=None, by=None):
    px, py = X(x), Y(y)
    if bx is None: bx, by = px, py
    else:
        A(f'<circle cx="{f(px)}" cy="{f(py)}" r="0.32" fill="#000"/>')
        L(px, py, bx, by, 0.11, "#000")
    A(f'<circle cx="{f(bx)}" cy="{f(by)}" r="2.35" fill="#fff" stroke="#000" stroke-width="0.2"/>')
    T(bx, by + 1.0, str(n), 2.8, "middle", "bold", "#000")

LEG = [
 # CUBIERTA
 (1, "Cupertina chapa galv. N°22, pend. al interior, c/ goterones"),
 (2, "Tornillo autoperforante c/ arandela de neopreno + sellador"),
 (3, "Babeta chapa galv. en buña del panel + sellador PU"),
 (4, "Membrana asfáltica 4 mm c/ aluminio, continua en canaleta"),
 (5, "Carpeta de nivelación MCI 1:3, e = 2 cm"),
 (6, "Contrapiso liviano H° c/ EPS, e mín. 6 cm, pend. 2 %"),
 (7, "Aislación térmica: plancha EPS 25 kg/m³, e = 5 cm"),
 (8, "Barrera de vapor: imprimación asfáltica + film 200 µ"),
 (9, "Panel Pi pretensado h 0,50 (Astori): losa cortada, nervio en vista"),
 (10, "Canaleta H°A in situ s/ VP, pend. 1 % a desagüe lateral"),
 (11, "Media caña de mortero"),
 (12, "Estribos salientes de la VP (Ø10) anclados al H° in situ"),
 (13, "Neopreno 10 mm + pasador Ø16 en vaina c/ grout"),
 (14, "Junta EPS 20 mm panel / H° in situ"),
 # ESTRUCTURA
 (15, "Viga VP-70 pretensada doble T 0,40 x 0,70 (Astori)"),
 (16, "Columna premoldeada H°A 0,40 x 0,40 (en vista)"),
 (17, "Ménsula lateral: apoyo de la VP (en vista)"),
 (18, "Ménsula interior: apoyo del recorte de losa (en vista)"),
 (19, "Losa alveolar pretensada h 0,30 (ALV-30 Astori)"),
 (20, "Capa de compresión H°A e = 5 cm + malla Ø6 c/15"),
 (21, "Banda de neopreno continua 10 mm s/ VP"),
 # CERRAMIENTO INTEGRAL
 (22, "Panel sándwich premoldeado e = 0,20 (apoyado en la base)"),
 (23, "Alma de EPS 6 cm + conectores de fibra de vidrio"),
 (24, "Hoja interior portante H°A 8 cm / hoja ext. 6 cm"),
 (25, "Riel de anclaje embutido (tipo Halfen) + bulón T M16"),
 (26, "Fija panel: 2 ángulos L 100x100x10 galv. c/ ovalados"),
 (27, "Bulón M16 pasante en vaina del alma + arandela y tuerca"),
 (28, "Junta 20 mm: lana mineral cortafuego + sellador"),
 (29, "Junta perimetral EPS 10 mm + sellador"),
 # ENTREPISO Y CIELORRASO
 (30, "Solado cerámico s/ adhesivo cementicio + zócalo"),
 (31, "Carpeta niveladora MCI 1:3, e = 2 cm"),
 (32, "Contrapiso liviano H° c/ EPS, e = 6 cm (acústico)"),
 (33, "Cielorraso placa de yeso 12,5 mm s/ perfiles galv. 35 mm"),
 (34, "Vela de cuelgue regulable fijada a la losa"),
 (35, "Perfil perimetral (buña) de cielorraso"),
 # PLANTA BAJA Y FUNDACIÓN
 (36, "Solado cerámico s/ adhesivo cementicio"),
 (37, "Carpeta hidrófuga MCI 1:3 + 10 % hidrófugo, e = 2 cm"),
 (38, "Contrapiso H° armado e = 12 cm c/ malla Ø4,2 c/15"),
 (39, "Film de polietileno 200 µ"),
 (40, "Tosca compactada en capas de 15 cm"),
 (41, "Junta de dilatación EPS 20 mm + sellador"),
 (42, "Mortero de asiento + calces de neopreno"),
 (43, "Pasador Ø16 panel / viga en vaina c/ grout"),
 (44, "Viga portapanel premoldeada 0,25 x 0,60 (solo bajo paneles)"),
 (45, "Neopreno de apoyo s/ pared del cáliz"),
 (46, "Sellador PU s/ fondo de junta (junta horizontal ext.)"),
 (47, "Pintura asfáltica en caras enterradas"),
 (48, "Vereda H° peinado e = 8 cm, pend. 2 % hacia afuera"),
 (49, "Contrapiso de tosca bajo vereda"),
 (50, "Junta vereda / viga EPS 10 mm + sellador"),
 (51, "Columna empotrada en el cáliz 0,70 (≥ 1,5 lado)"),
 (52, "Cáliz H°A in situ c/ paredes dentadas (llaves de corte)"),
 (53, "Relleno grout sin contracción (H-30)"),
 (54, "Base aislada H°A in situ (dimensiones s/ cálculo)"),
 (55, "Armadura de base Ø12 c/15 (s/ cálculo)"),
 (56, "Hormigón de limpieza e = 5 cm"),
 (57, "Terreno natural compactado"),
 (58, "Mortero de nivelación bajo columna"),
 (59, "Junta vertical entre paneles: fondo de junta + sellador PU"),
 (60, "Junta EPS 20 mm viga portapanel / columna"),
]

EX = 204.0   # columna de globos del lado exterior
REFS_POS = [
 # ---- cubierta (banda 1)
 (1, -245, 10180, 206, 20), (2, -110, 10222, 233, 8.5), (3, -11, 9880, 238, 16), (10, 80, 9450, 233.5, 30),
 (4, 260, 9656, 244, 22), (5, 380, 9643, 250, 22), (6, 500, 9606, 256, 22), (7, 620, 9548, 262, 22), (8, 740, 9521.5, 268, 22),
 (9, 900, 9300, 272, 62), (11, 160, 9285, 249, 63.5), (12, 280, 9150, 256, 69), (13, 305, 9015, 262, 76),
 (27, 280, 8735, 262, 82), (15, 200, 8450, 262, 88), (16, 200, 8150, None, None),
 (22, -200, 9600, EX, 40), (23, -130, 9350, EX, 47), (24, -60, 9100, EX, 54), (14, -10, 9150, EX, 61),
 (25, -35, 8645, EX, 75), (26, 85, 8680, EX, 81.5), (28, -10, 8450, EX, 89),
 # ---- entrepiso (banda 2)
 (30, 300, 4495, 246, 131), (31, 500, 4475, 252, 131), (32, 700, 4435, 258, 131), (20, 900, 4380, 264, 131),
 (29, -15, 4430, EX, 138), (24, -60, 4100, EX, 152), (28, -10, 3900, EX, 162), (26, 85, 3720, EX, 170), (25, -35, 3680, EX, 177),
 (19, 550, 4200, 268, 149.5), (21, 300, 4050, 266, 160), (18, 520, 3900, 272, 168), (27, 285, 3770, 256, 175),
 (15, 200, 3420, 256, 190), (34, 1000, 3600, 289, 179.5), (33, 850, 3256, 273.5, 203), (35, -20, 3270, EX, 196),
 (17, 200, 3100, 250, 205),
 # ---- planta baja y fundación (banda 3)
 (16, 200, 1000, None, None), (22, -200, 700, EX, 251), (23, -130, 500, EX, 261), (24, -60, 300, EX, 271),
 (43, -60, 150, EX, 277), (42, -160, -45, 210.5, 282), (46, -226, -45, EX, 287),
 (48, -560, -215, EX, 302), (49, -400, -330, 210, 308), (50, -251, -240, EX, 314), (47, -247, -500, 210, 320),
 (45, -150, -645, EX, 326), (60, -10, -600, 210, 332), (44, -130, -350, None, None), (57, -500, -1150, None, None),
 (56, -650, -1925, EX, 391),
 (36, 600, -5, 254, 277), (37, 750, -25, 260, 277), (38, 900, -95, 266, 277), (39, 1000, -156, 289, 294), (40, 900, -300, 289, 301),
 (41, 410, -300, 262, 307), (51, 200, -1000, None, None), (52, 550, -1000, 270, 338), (53, 425, -1200, 270, 347),
 (58, 200, -1375, 262, 357), (54, 900, -1750, 284, 366), (55, 500, -1850, 250, 384),
]
for r in REFS_POS: ref(*r)

# ---------------- FORMATO TP (plantilla HORMIGON_VIDRIADO_A3)
T(16, 31.9, "CORTE INTEGRAL", 7.4)
T(16, 39.9, "CERRAMIENTO OPACO", 7.4)
T(16, 47.7, "ESCALA 1:20", 4.7)
T(110, 31.9, "Hormigón premoldeado de grandes luces", 3.0)
T(110, 36.3, "Panel sándwich de H°A · Sistema Pi (Astori)", 3.0)
T(110, 40.7, "Cerramiento integral: apoyado en la base,", 3.0)
T(110, 45.1, "vinculado a la estructura en cada nivel", 3.0)
T(16, 61.8, "REFERENCIAS", 5.0)
NROW = 30
y0 = 66.4; dy = 3.2
for k, (n, txt) in enumerate(LEG):
    col, row = (0, k) if k < NROW else (1, k - NROW)
    xn = 15.6 if col == 0 else 103.6
    T(xn, y0 + row * dy, str(n), 2.8, "end", "bold")
    T(xn + 1.2, y0 + row * dy, txt, 2.8)
YREF_END = y0 + (NROW - 1) * dy
# rótulo (idéntico a la plantilla)
A('<rect x="10.7" y="400.1" width="274.9" height="11.2" fill="none" stroke="#000" stroke-width="0.35"/>')
for xx in (39.5, 150.9, 244.3):
    A(f'<line x1="{xx}" y1="400.1" x2="{xx}" y2="411.3" stroke="#000" stroke-width="0.25"/>')
T(12.6, 405.0, "TP FINAL", 4.2, weight="bold")
T(12.6, 409.4, "FECHA: 19/10/2026", 2.8)
T(41.2, 403.6, "DOCENTE: Arq. Tucci y Arq. Cardozo", 2.8)
T(41.2, 406.8, "ALUMNA: Candelaria Vitale", 2.8)
T(41.2, 410.0, "GRUPO: 13", 2.8)
T(152.4, 403.6, "NIVEL:", 2.8)
T(152.4, 406.8, "OBS:", 2.8)
T(249.4, 404.8, "CONSTRUCCIONES II", 2.8)
T(249.4, 408.6, "CATEDRA: ARQ. TUCCI", 2.8)

SVG_BODY = f'''<defs>{"".join(defs)}<g id="fullg">{"".join(full)}</g></defs>
<rect x="0" y="0" width="297" height="420" fill="#fff"/>
<rect x="0.3" y="0.3" width="296.4" height="419.4" fill="none" stroke="#000" stroke-width="0.4"/>
{"".join(uses)}
{"".join(ann)}'''
os.makedirs("build", exist_ok=True)
open("build/opaco_corte.svgpart", "w").write(SVG_BODY)
open("build/opaco_corte_solo.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="420mm" viewBox="0 0 297 420" font-family="Liberation Sans, Arial, sans-serif">{SVG_BODY}</svg>')
print("ok refs hasta y =", YREF_END)
