# -*- coding: utf-8 -*-
"""Lámina final - Corte integral 1:20 (A3 apaisada) + referencias + 3 nudos axonométricos. Sistema de hormigón premoldeado de grandes luces
con cerramiento vidriado (muro cortina stick).
Geometría en mm reales; x+ hacia el interior, y+ hacia arriba, ±0.00 = NPT planta baja."""
import math, os

S = 20.0                      # escala 1:20
PX0, XR0 = 170.0, -600.0        # x de papel donde cae x real -600
def X(x): return PX0 + (x - XR0) / S
def YC(y): return 1000.0 - y / S          # coordenada "continua" antes de cortar en bandas

# bandas (real lo, real hi, y papel superior)
BANDS = [(7600, 9540, 8.0), (3200, 5000, 109.0), (-2180, 1500, 203.0)]
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
#  GEOMETRÍA (mm reales).  Corte ENTRE columnas: viga L cortada, columna y ménsula en vista
#  y por el eje de columna en la fundación (línea de corte quebrada a nivel ±0,00).
#  Columna x 250..650 · VL 40x70 x 250..650 · muro cortina x -32..182 · eje de columna x = 450
# =====================================================================================
REB = "#7a1f1f"

# ------------------------------------------------------------------ TERRENO Y FUNDACIÓN (corte por eje de columna)
rect(-750, -2180, 2700, -327, fill="url(#pTierra)", stroke="none", sw=0)
line(-750, -327, -64, -327, sw=0.2)
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
# SIN viga perimetral: el muro cortina de PB cuelga del entrepiso; abajo solo una guía deslizante sobre el contrapiso
# aislación hidrófuga vertical + vereda exterior
pline([(-64, -150), (-64, -327)], stroke="#000", sw=0.45)
rect(-750, -327, -66, -250, fill="url(#pTosca)", **CUTT)
poly([(-750, -250), (-66, -250), (-66, -150), (-750, -157)], fill="url(#pH)", **CUTT)
rect(-70, -250, -66, -150, fill=NEO, stroke="none", sw=0)
# babeta / goterón del arranque
pline([(40, 8), (-20, 4), (-68, -12), (-68, -140), (-88, -160)], stroke="#000", sw=0.3)
# piso sobre terreno: tramo exterior (fachada–columna) y tramo interior, separados de la columna por junta de dilatación
for xa, xb, sol in ((-62, 230, (182, 230)), (670, 2700, (675, 2700))):
    rect(xa, -327, xb, -177, fill="url(#pTosca)", **CUTT)
    rect(xa, -177, xb, -175, fill="#000", stroke="none", sw=0)                            # film 200 µ
    rect(xa, -175, xb, -55, fill="url(#pH)", **CUTT)                                      # contrapiso
    pline([(xa + 20, -120), (xb - 10, -120)], stroke=REB, sw=0.1, extra='stroke-dasharray="2 0.5"')  # malla
    rect(xa, -55, xb, -35, fill="url(#pHid)", **CUTT)                                     # carpeta hidrófuga
    rect(xa, -35, xb, -15 if xa > 0 else 0, fill="url(#pMort)", **CUTT)                   # carpeta niveladora
    rect(sol[0], -15, sol[1], -10, fill="#8d8d8d", stroke="none", sw=0)
    rect(sol[0], -10, sol[1], 0, fill="url(#pPorc)", **CUTT)
rect(182, -35, 230, -15, fill="url(#pMort)", **CUTT)
for xx in range(975, 2700, 400): line(xx, -10, xx, 0, sw=0.15)
# JUNTAS DE DILATACIÓN piso / columna (EPS 2 cm desde el cuello hasta el piso + sellador)
for xa in (230, 650):
    rect(xa, -327, xa + 20, -10, fill="url(#pEPSv)", **CUTT)
    rect(xa, -10, xa + 20, 0, fill=NEO, stroke="none", sw=0)
# ------------------------------------------------------------------ ESTRUCTURA (corte entre columnas: viga L cortada, columna y ménsula en vista)
def columna_vista(y0, y1):
    rect(250, y0, 650, y1, fill="#eceeef", **VIEW)
def mensula_vista(ytop):
    """ménsula corta en vista: cara superior horizontal, frente vertical y diagonal inferior hasta la columna"""
    poly([(250, ytop), (760, ytop), (760, ytop - 160), (650, ytop - 470), (250, ytop - 470)], fill="#e3e6e8", stroke="#222", sw=0.2)
    line(650, ytop - 470, 650, ytop, stroke="#666", sw=0.1)                                # cara de la columna
    pline([(300, ytop - 40), (720, ytop - 40), (720, ytop - 150), (640, ytop - 400)], stroke=REB, sw=0.12, extra=DASH)  # armadura (oculta)
    rect(440, ytop - 260, 460, ytop + 160, fill="none", stroke="#333", sw=0.12, extra=DASH)  # perno Ø20 (oculto)
def viga_L(yt):
    """VL doble T 40x70 pretensada (perimetral, portante) apoyada en la ménsula + ENCIMA viga L de borde
    premoldeada (alma 15 x 26 hasta tope capa de compresión + talón 25 x 15) que cubre el hueco hasta el nivel de losa y recibe el ala del TT."""
    yb = yt - 910; yv = yt - 210                                                            # VL: yb..yv ; L: yv..yt
    P = [(250, yb), (650, yb), (650, yb + 150), (530, yb + 210), (510, yb + 210), (510, yv - 190), (530, yv - 190), (650, yv - 130), (650, yv),
         (250, yv), (250, yv - 130), (370, yv - 190), (390, yv - 190), (390, yb + 210), (370, yb + 210), (250, yb + 150)]
    poly(P, fill="url(#pHA)", **CUT)                                                       # VL doble T (cortada)
    for xx in (290, 370, 450, 530, 610): circ(xx, yb + 45, 0.32)                            # cordones
    for xx in (330, 570): circ(xx, yb + 100, 0.32)
    for xx in (290, 450, 610): circ(xx, yv - 45, 0.28, fill=REB)
    pline([(400, yb + 30), (400, yv - 30)], stroke=REB, sw=0.1); pline([(500, yb + 30), (500, yv - 30)], stroke=REB, sw=0.1)
    rect(250, yb - 10, 650, yb, fill=NEO, stroke="none", sw=0)                             # neopreno VL / ménsula
    # viga L de borde (encima de la VL)
    poly([(250, yv), (650, yv), (650, yt - 60), (400, yt - 60), (400, yt + 50), (250, yt + 50)], fill="url(#pHA)", **CUT)
    pline([(270, yv + 20), (630, yv + 20), (630, yt - 80), (380, yt - 80), (380, yt + 30), (270, yt + 30), (270, yv + 20)], stroke=REB, sw=0.12)
    for xx in (290, 610): circ(xx, yv + 40, 0.26, fill=REB)
    for xx in (330, 520): pline([(xx, yv - 120), (xx, yv + 125)], stroke=REB, sw=0.25)       # barras de vinculación VL / L (en grout)
    rect(250, yv - 3, 650, yv + 3, fill="url(#pGrout)", stroke="none", sw=0)              # junta VL / L c/ mortero
    pline([(320, yt - 150), (320, yt + 25), (640, yt + 25)], stroke=REB, sw=0.22)              # estribos salientes 2Ø10 (anclan la capa)
    # riel de anclaje embutido en la VL (grapas del muro cortina)
    yy = yt - 350
    poly([(250, yy - 26), (292, yy - 26), (292, yy + 26), (250, yy + 26), (250, yy + 18), (284, yy + 18), (284, yy - 18), (250, yy - 18)], fill=STEEL, stroke="#000", sw=0.06)
    for dy in (-22, 22): line(292, yy + dy, 345, yy + dy, stroke="#000", sw=0.14)
    rect(268, yy - 8, 284, yy + 8, fill="#555", stroke="#000", sw=0.05)
def panel_TT(yt):
    """panel TT h = 0,65 en corte transversal: ala cortada apoyada en el ala de la viga L s/ neopreno; nervio cortado"""
    yf = yt - 50
    rect(760, yt - 750, 2700, yf, fill="#e9ebed", **VIEW)                                  # viga VP (en vista)
    line(760, yt - 600, 2700, yt - 600, stroke="#888", sw=0.08)
    rect(420, yf, 2700, yt, fill="url(#pHA)", **CUT)                                       # ala del TT (cortada)
    for xc in (1170,):
        poly([(xc - 90, yf), (xc + 90, yf), (xc + 60, yt - 650), (xc - 60, yt - 650)], fill="url(#pHA)", **CUT)
        for yy in (yt - 610, yt - 560): circ(xc, yy, 0.3)
        line(xc, yt - 640, xc, yf, stroke=REB, sw=0.1)
    rect(430, yt - 60, 640, yt - 50, fill=NEO, stroke="none", sw=0)                        # neopreno ala TT / ala viga L
    rect(400, yt - 60, 420, yt, fill="url(#pGrout)", stroke="none", sw=0)                  # junta L / panel c/ grout
def capa_compresion(ytop, x0=250):
    rect(x0, ytop, 2700, ytop + 50, fill="url(#pHAis)", **CUT)
    pline([(x0 + 30, ytop + 25), (2700, ytop + 25)], stroke=REB, sw=0.12, extra='stroke-dasharray="2 0.5"')
    for xx in range(x0 + 100, 2700, 150): circ(xx, ytop + 25, 0.17, fill=REB)
def cielorraso(y, ytt):
    rect(190, y, 2700, y + 12.5, fill="#f2f2f2", **CUTT)
    for xx in range(900, 2700, 400): rect(xx, y + 12.5, xx + 35, y + 47, fill=ALU, stroke="#444", sw=0.08)
    pline([(190, y + 70), (190, y), (230, y)], stroke="#000", sw=0.2)
    for xc in (1275, 2125): line(xc, y + 47, xc, ytt - 650, stroke="#555", sw=0.15)       # vela de cuelgue al nervio del TT

# columnas en vista
columna_vista(0, 2975); columna_vista(4465, 7475)
# entrepiso
mensula_vista(3495); viga_L(4415); panel_TT(4415); capa_compresion(4415, 400)
rect(250, 4465, 2700, 4485, fill="url(#pMort)", **CUTT)
rect(260, 4485, 2700, 4490, fill="#8d8d8d", stroke="none", sw=0)
rect(260, 4490, 2700, 4500, fill="url(#pPorc)", **CUTT)
for xx in range(860, 2700, 400): line(xx, 4490, xx, 4500, sw=0.15)
cielorraso(3300, 4415)
# cubierta
mensula_vista(7995); viga_L(8915); panel_TT(8915); capa_compresion(8915, 400)
cielorraso(7800, 8915)

# ------------------------------------------------------------------ MURO CORTINA
montante(40, 4700); montante(4720, 9390)
rect(32, 4700, 182, 4720, fill="#fff", stroke="#444", sw=0.1)
rect(60, 4600, 150, 4840, fill="none", stroke="#444", sw=0.1, extra=DASH)
# arranque PB: perfil guía (U) fijado al contrapiso; el montante desliza dentro (cuelga del entrepiso)
rect(25, 0, 190, 40, fill=ALU, **CUTT); rect(32, 6, 182, 40, fill="#fff", stroke="#000", sw=0.06)
for xx in (60, 150): line(xx, 0, xx, -110, stroke="#000", sw=0.14)
rect(-30, 0, 25, 4, fill="#222", stroke="none", sw=0)
travesano(40, 60, glass_below=False)
dvh(110, 3240)
travesano(3250, 60)
dvh(3320, 4550, spandrel=True)
rect(40, 3450, 90, 4550, fill="url(#pLanaV)", **CUTT); rect(90, 3450, 93, 4550, fill=STEEL, stroke="none", sw=0)
travesano(4560, 60)
dvh(4630, 7740)
travesano(7750, 60)
dvh(7820, 9380, spandrel=True)
rect(40, 7950, 90, 9380, fill="url(#pLanaV)", **CUTT); rect(90, 7950, 93, 9380, fill=STEEL, stroke="none", sw=0)
# cierre superior del muro cortina
rect(-32, 9380, 190, 9420, fill=ALU, **CUTT); rect(-25, 9386, 183, 9414, fill="#fff", stroke="#000", sw=0.06)
# barrera cortafuego entrepiso
rect(93, 4355, 250, 4365, fill=STEEL, stroke="none", sw=0)
rect(93, 4365, 250, 4458, fill="url(#pLana)", **CUTT)
rect(93, 4458, 250, 4466, fill="#c0392b", stroke="none", sw=0)
pline([(182, 4503), (330, 4503)], stroke="#000", sw=0.25)
# grapas (en vista) abulonadas al riel embutido de la viga L
def grapa(yy):
    poly([(185, yy - 70), (195, yy - 70), (195, yy - 5), (250, yy - 5), (250, yy + 5), (195, yy + 5), (195, yy + 70), (185, yy + 70)], fill=STEEL, stroke="#000", sw=0.08)
    line(160, yy + 40, 200, yy + 40, stroke="#000", sw=0.25)
    line(240, yy, 272, yy, stroke="#000", sw=0.3)
grapa(4065); grapa(8565)

# ------------------------------------------------------------------ CUBIERTA
yb0 = 8965
rect(250, 8965, 2700, 8968, fill="#000", stroke="none", sw=0)                               # barrera de vapor (bajo zócalo y paquete)
# zócalo superior H°A° in situ (carga) c/ barras de atado
poly([(260, 8968), (400, 8968), (400, 9410), (260, 9440)], fill="url(#pHAis)", **CUT)
rect(380, 9330, 400, 9350, fill="#fff", stroke="#000", sw=0.1)                              # buña p/ babeta
pline([(300, 8870), (300, 9390), (360, 9390), (360, 8870)], stroke=REB, sw=0.22)
x0, x1 = 400, 2700
def ypend(x, b): return b + (x - x0) * 0.02
poly([(x0, 8968), (x1, 8968), (x1, ypend(x1, 9068)), (x0, 9068)], fill="url(#pEPS)", **CUTT)   # contrapiso liviano H° c/ EPS (aislante + pendiente)
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
TMIN = 2.8   # font-size mínimo (mm) -> altura de letra ≥ 2,0 mm impresa
def T(x, y, s, size=2.0, anchor="start", weight="normal", fill="#000", rot=None, ital=False):
    size = max(size, TMIN)
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
nivel(8915, "+8,92", 800, "r", "")
nivel(7800, "+7,80", 1350, "r", "")
nivel(4500, "+4,50", 1250, "r", "N.P.T. P. Alta")
nivel(3300, "+3,30", 1350, "r", "")
nivel(0, "±0,00", 1250, "r", "N.P.T. P. Baja")
nivel(-150, "-0,15", -560, "r", "")
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
cota_v(3505, 4205, 900, "0,70"); cota_v(4205, 4465, 900, "0,26"); cota_v(8005, 8705, 900, "0,70"); cota_v(8705, 8965, 900, "0,26")
cota_v(3765, 4415, 1550, "0,65")
cota_v(-2050, -1750, 1560, "0,30"); cota_v(-1350, -510, 1150, "0,84")
cota_v(8968, 9440, 220, "0,47")
cota_h(-32, 182, 3330, "21"); cota_h(182, 250, 3330, "7"); cota_h(250, 650, 3330, "40")
cota_h(-550, 1450, -2170, "2,00 (s/ cálculo)", below=True); cota_h(-75, 975, -1420, "1,05")

T(X(-590), Y(9300), "EXTERIOR", 2.0, fill="#555"); T(X(900), Y(9420), "INTERIOR", 2.0, fill="#555")
T(X(-590), Y(4900), "EXTERIOR", 2.0, fill="#555"); T(X(800), Y(4900), "INTERIOR · PLANTA ALTA", 2.0, fill="#555")
T(X(-590), Y(1300), "EXTERIOR", 2.0, fill="#555"); T(X(800), Y(1300), "INTERIOR · PLANTA BAJA", 2.0, fill="#555")
T(X(1150), Y(9200), "pend. 2 %", 1.4, ital=True, fill="#333")
T(X(1000), Y(-1000), "Fundación cortada", 1.4, ital=True, fill="#333")
T(X(1000), Y(-1090), "por eje de columna", 1.4, ital=True, fill="#333")
T(X(700), Y(3280), "Columna y ménsula en vista", 1.4, ital=True, fill="#333")


# ------------------------------------------------------------------ REFERENCIAS
def ref(n, x, y, dx, dy):
    DX.append(dict(t='ref', n=n, a=(x, y), b=(x + dx * S, y - dy * S)))
    px, py = X(x), Y(y); bx, by = px + dx, py + dy
    A(f'<circle cx="{f(px)}" cy="{f(py)}" r="0.32" fill="#000"/>')
    L(px, py, bx, by, 0.11, "#000")
    A(f'<circle cx="{f(bx)}" cy="{f(by)}" r="2.35" fill="#fff" stroke="#000" stroke-width="0.2"/>')
    T(bx, by + 1.0, str(n), 2.8, "middle", "bold", "#000")

REFS_POS = [
 (1, 200, 9462, 4, -6), (2, 80, 9400, -14, -3), (3, 1000, 9092, 0, -8), (4, 1300, 9080, 2, -10), (5, 1500, 9050, 0, 7), (6, 410, 9356, 14, -4),
 (7, 1000, 8967, 0, 8), (8, 330, 9250, 12, -12), (9, 420, 9110, 24, -3),
 (10, 1550, 8945, 0, 12), (11, 470, 8980, 34, -16), (12, 1170, 8500, 9, 0), (13, 330, 8800, 20, 3), (14, 450, 8100, 30, 6),
 (15, 450, 7640, 14, 0), (16, 700, 7720, 14, 6), (17, 500, 8000, 26, 6), (18, 272, 8565, 22, 9), (19, 540, 4358, 30, 12),
 (20, 1500, 4495, 0, -7), (21, 1600, 4475, 0, -9), (22, 1300, 3306, 0, 6), (23, 1550, 3325, 0, 6), (24, 1275, 3500, 9, 3),
 (25, 120, 4200, -16, 0), (26, 100, 4590, 14, -8), (27, 12, 4665, -24, 14), (28, 3, 4100, -14, 3), (29, 65, 3900, -16, 4),
 (30, 170, 4410, -22, -4), (31, 210, 4065, 24, -4), (32, 100, 4708, -28, 1), (33, 100, 20, -18, -5), (34, -5, 2, 4, -14),
 (35, 950, -5, 0, -6), (36, 1150, -25, 0, -8), (37, 1350, -45, 0, -10), (38, 1100, -120, 0, 12), (39, 1550, -176, 0, 9),
 (40, 1350, -260, 0, 10), (41, 660, -250, 14, 10), (42, 100, -120, -16, 6), (43, 120, 600, 14, 0), (44, -60, -40, -10, -4),
 (45, -300, -200, 6, -9), (46, 450, -900, 14, 0), (47, 700, -800, 20, 0), (48, 690, -1200, 22, 0), (49, 540, -1600, 20, 2),
 (50, 850, -700, 18, 12), (51, 1200, -1800, 9, 0), (52, 1100, -1960, 10, -4), (53, 1400, -2100, 4, 3), (54, 1400, -1350, 0, 5),
 (55, 60, -70, -6, 16), (5, 0, 0, 0, 0),
]
for n, x, y, dx, dy in REFS_POS:
    if (dx, dy) != (0, 0): ref(n, x, y, dx, dy)

LEG = [
("CUBIERTA", None),
(1, "Cupertina chapa galv. N°22 c/ goterones"),
(2, "Perfil de cierre sup. muro cortina + sellador"),
(3, "Membrana asfáltica 4 mm c/ aluminio + babeta"),
(4, "Carpeta 1:3 c/ 10 % hidrófugo, e = 2 cm"),
(5, "Contrapiso liviano H° c/ EPS (aislante), pend. 2 %"),
(6, "Babeta chapa galv. + sellador en buña"),
(7, "Barrera de vapor: imprimación + film 200 µ"),
(8, "Zócalo sup. H°A° in situ c/ barras a viga L"),
(9, "Media caña de mortero"),
("ESTRUCTURA PREMOLDEADA (SISTEMA PI)", None),
(10, "Capa de compresión 5 cm c/ malla Ø6 c/15"),
(11, "Estribos salientes viga L (2Ø10)"),
(12, "Panel TT h 0,65: ala y nervios cortados"),
(13, "Viga L de borde s/ VL (recibe el TT)"),
(14, "Viga VL doble T 40x70 pretensada"),
(15, "Columna pretensada 40x40 (en vista)"),
(16, "Ménsula de columna c/ diagonal (en vista)"),
(17, "Neopreno + perno Ø20 (VL / ménsula)"),
(18, "Riel de anclaje embutido + bulón T"),
(19, "Ala del TT s/ ala viga L + neopreno"),
("ENTREPISO Y CIELORRASOS", None),
(20, "Solado cerámico s/ adhesivo cementicio"),
(21, "Carpeta niveladora MHR 1:1/4:3, e = 2 cm"),
(22, "Cielorraso placa de roca de yeso 12,5 mm"),
(23, "Montantes y soleras chapa galv. 35 mm"),
(24, "Gancho / vela a los nervios del panel TT"),
("MURO CORTINA (STICK, MÓDULO 1,25 m)", None),
(25, "Mullion: montante alum. 50x150"),
(26, "Travesaño + presor + tapa + burletes EPDM"),
(27, "DVH 6 templado + 12 + 3+3 laminado PVB"),
(28, "Spandrel: vidrio templado 6 mm esmaltado"),
(29, "Lana mineral 50 mm + bandeja chapa galv."),
(30, "Barrera cortafuego lana mineral + intumescente"),
(31, "Grapa acero galv. regulable + bulón M12 inox"),
(32, "Junta de dilatación 20 mm + manguito"),
(33, "Perfil guía de arranque (deslizante)"),
(34, "Sellador silicona neutra s/ fondo de junta"),
("PLANTA BAJA Y FUNDACIÓN", None),
(35, "Solado cerámico s/ adhesivo cementicio"),
(36, "Carpeta niveladora MHR 1:1/4:3"),
(37, "Carpeta hidrófuga MCI 1:3"),
(38, "Contrapiso de H° pobre, e = 12 cm"),
(39, "Film de polietileno 200 µ"),
(40, "Tosca compactada, e = 15 cm"),
(41, "Junta de dilatación EPS 2 cm + sellador"),
(42, "Contrapiso armado hasta la fachada"),
(43, "Montante colgado del entrepiso"),
(44, "Babeta chapa galv. + aislación hidrófuga"),
(45, "Vereda de H° peinado s/ tosca"),
(46, "Tronco de columna dentro del cuello"),
(47, "Anclaje mecánico húmedo (horquillas)"),
(48, "Relleno de H° cementicio cuello/columna"),
(49, "Armadura de vinculación fundación–columna"),
(50, "Cuello de la base, H°A° in situ"),
(51, "Base de H°A° colada in situ (s/ cálculo)"),
(52, "Armadura de fundación s/ cálculo"),
(53, "H° de limpieza, e = 10 cm"),
(54, "Terreno natural"),
(55, "Broca c/ prisionero Ø9,5 x 80 + tuerca"),
]

# ---------------- FORMATO TP (según plantilla de la cátedra)
T(16, 31.9, "CORTE INTEGRAL", 7.4)
T(16, 39.9, "MURO CORTINA", 7.4)
T(16, 47.7, "ESCALA 1:20", 4.7)
T(16, 65.8, "REFERENCIAS", 5.0)
items = [it for it in LEG if it[1] is not None]
y0 = 70.4; dy = 3.25
for k, (n, txt) in enumerate(items):
    col, row = (0, k) if k < 30 else (1, k - 30)
    xn = 18.6 if col == 0 else 90.4
    T(xn, y0 + row * dy, str(n), 2.8, "end", "bold")
    T(xn + 1.3, y0 + row * dy, txt, 2.8)
yend = my = y0 + 30 * dy
# rótulo (como la plantilla)
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
import json
os.makedirs("build", exist_ok=True)
open("build/tp_corte.svgpart", "w").write(SVG_BODY)
json.dump(dict(DX=DX, LEG=LEG, NOTAS=[]), open("build/tp_dx.json", "w"), ensure_ascii=False)
print("ok", yend, my)
