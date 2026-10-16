# -*- coding: utf-8 -*-
"""Lámina 1 - Corte integral 1:20. Sistema de hormigón premoldeado de grandes luces
con cerramiento vidriado (muro cortina stick).
Geometría en mm reales; x+ hacia el interior, y+ hacia arriba, ±0.00 = NPT planta baja."""
import math, os

S = 20.0                      # escala 1:20
PX0, XR0 = 14.0, -1100.0       # x de papel donde cae x real -1100
def X(x): return PX0 + (x - XR0) / S
def YC(y): return 1000.0 - y / S          # coordenada "continua" antes de cortar en bandas

# bandas (real lo, real hi, y papel superior)
BANDS = [(7880, 9960, 16.0), (2880, 5120, 128.0), (-2160, 820, 244.0)]
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

# ================================================================ FUNDACIÓN Y PB
# suelo
rect(-1100, -2160, 2600, -400, fill="url(#pTierra)", stroke="none", sw=0)
rect(250, -400, 2600, -330, fill="url(#pTierra)", stroke="none", sw=0)
line(-1100, -400, -50, -400, sw=0.2)
# Fundación en proyección (eje de columna, por detrás del plano de corte)
rect(-950, -2080, 1150, -2000, fill="url(#pH)", stroke="#555", sw=0.15, extra='fill-opacity="0.55" ' + DASH)
poly([(-900, -2000), (1100, -2000), (1100, -1650), (600, -1500), (-400, -1500), (-900, -1650)], fill="url(#pHAis)", stroke="#333", sw=0.18, extra='fill-opacity="0.45" ' + DASH)
# tintero (cáliz) y columna empotrada
poly([(-400, -1500), (600, -1500), (600, -620), (350, -620), (350, -1450), (-150, -1450), (-150, -620), (-400, -620)],
     fill="url(#pHAis)", stroke="#333", sw=0.18, extra='fill-opacity="0.45" ' + DASH)
rect(-150, -1450, 350, -620, fill="url(#pGrout)", stroke="#333", sw=0.13, extra='fill-opacity="0.6" ' + DASH)
rect(-100, -1400, 300, -620, fill="url(#pHA)", stroke="#333", sw=0.15, extra='fill-opacity="0.7" ' + DASH)
for yy in (-1300, -1100, -900):          # llaves de corte (rugosidad) en columna
    line(-100, yy, 300, yy, stroke="#555", sw=0.08, extra=DASH)
# armadura base (proyección)
pline([(-830, -1650), (-830, -1930), (1030, -1930), (1030, -1650)], stroke="#7a1f1f", sw=0.14, extra=DASH)
for xx in range(-800, 1050, 150): circ(xx, -1905, 0.22, fill="#7a1f1f")
# armadura en espera / anclajes columna-tintero
pline([(-320, -1880), (-320, -1080)], stroke="#7a1f1f", sw=0.12, extra=DASH)
pline([(520, -1880), (520, -1080)], stroke="#7a1f1f", sw=0.12, extra=DASH)

# Viga de fundación premoldeada VF 30x60
poly([(-50, -610), (250, -610), (250, 0), (-20, 0), (-50, -20)], fill="url(#pHA)", **CUT)
for xx in (-10, 210):
    for yy in (-570, -40): circ(xx, yy, 0.32)
rect(-20, -580, 220, -30, stroke="#7a1f1f", sw=0.1, extra='rx="0.4"')
rect(-50, -620, 250, -610, fill=NEO, stroke="none", sw=0)          # neopreno VF/tintero
# aislación hidrófuga vertical
pline([(-56, -200), (-56, -616)], stroke="#000", sw=0.4)
# exterior: vereda
rect(-1100, -400, -60, -300, fill="url(#pTosca)", **CUTT)
rect(-1100, -300, -60, -200, fill="url(#pH)", **CUTT)
for xx in (-1100, -60):
    pass
rect(-60, -300, -56, -200, fill=NEO, stroke="none", sw=0)          # junta c/ sellador
for xx in range(-650, -60, 180): line(xx, -200, xx + 30, -200, sw=0.1)
# babeta / goterón arranque
pline([(40, 8), (-20, 4), (-62, -10), (-62, -60), (-80, -78)], stroke="#000", sw=0.28)
# piso interior
rect(250, -330, 2600, -182, fill="url(#pTosca)", **CUTT)
rect(250, -182, 2600, -180, fill="#000", stroke="none", sw=0)        # film 200 micrones
rect(270, -180, 2600, -60, fill="url(#pHAis)", **CUTT)                # contrapiso armado
pline([(290, -110), (2600, -110)], stroke="#7a1f1f", sw=0.1, extra='stroke-dasharray="2 0.5"')
rect(270, -60, 2600, -40, fill="url(#pHid)", **CUTT)                  # carpeta hidrófuga
rect(270, -40, 2600, -15, fill="url(#pMort)", **CUTT)                 # carpeta niv.
rect(275, -15, 2600, -10, fill="#8d8d8d", stroke="none", sw=0)        # adhesivo
rect(275, -10, 2600, 0, fill="url(#pPorc)", **CUTT)
for xx in range(875, 2600, 600): line(xx, -10, xx, 0, sw=0.15)
rect(250, -180, 270, -10, fill="url(#pEPSv)", **CUTT)                 # junta perimetral
rect(250, -10, 275, 0, fill=NEO, stroke="none", sw=0)                # sellador

# ================================================================ ESTRUCTURA
def columna_vista(y0, y1):
    rect(-100, y0, 300, y1, fill="#eceeef", **VIEW)
def mensula(ytop):
    poly([(300, ytop - 400), (300, ytop), (600, ytop), (600, ytop - 200)], fill="#e3e6e8", **VIEW)
    pline([(330, ytop - 360), (330, ytop - 30), (570, ytop - 30), (570, ytop - 190)], stroke="#7a1f1f", sw=0.1, extra='stroke-dasharray="0.6 0.4"')
def viga_L(yb):
    yt = yb + 700
    poly([(300, yb), (800, yb), (800, yb + 330), (600, yb + 330), (600, yt), (300, yt)], fill="url(#pHA)", **CUT)
    rect(330, yb + 30, 570, yt - 30, stroke="#7a1f1f", sw=0.1, extra='fill="none"')
    pline([(570, yb + 30), (770, yb + 30), (770, yb + 300), (570, yb + 300)], stroke="#7a1f1f", sw=0.1)
    for xx in (360, 450, 540, 660, 740): circ(xx, yb + 60, 0.33)
    for xx in (360, 540): circ(xx, yt - 55, 0.28)
    # estribos salientes (vinculación con capa de compresión)
    pline([(470, yt - 120), (470, yt - 25), (1350, yt - 25)], stroke="#7a1f1f", sw=0.16)
    # perno/bulón ménsula-viga (vaina grouteada) en vista
    rect(430, yb - 400 + 60, 470, yb + 400, fill="none", stroke="#333", sw=0.1, extra=DASH)
    rect(300, yb - 10, 600, yb, fill=NEO, stroke="none", sw=0)
def losa(yb):          # losa alveolar e=30, cortada por un alvéolo
    yt = yb + 300
    rect(640, yb - 10, 790, yb, fill=NEO, stroke="none", sw=0)           # neopreno
    poly([(620, yb), (2600, yb), (2600, yb + 45), (920, yb + 45), (920, yt - 45), (2600, yt - 45), (2600, yt), (620, yt)], fill="url(#pHA)", **CUT)
    rect(920, yb + 45, 2600, yt - 45, fill="#f6f7f8", stroke="none", sw=0)  # alveolo (vacío)
    line(920, yb + 45, 2600, yb + 45, sw=0.2); line(920, yt - 45, 2600, yt - 45, sw=0.2)
    line(620, yb + 150, 920, yb + 150, sw=0.08, extra=DASH)
    rect(620, yb + 45, 920, yt - 45, fill="url(#pH)", stroke="#000", sw=0.15)  # tapón de H°
    pline([(650, yb + 28), (2600, yb + 28)], stroke="#7a1f1f", sw=0.16, extra='stroke-dasharray="3 0.8"')
    # junta viga-losa + capa de compresión
    poly([(600, yb - 10), (620, yb - 10), (620, yt), (2600, yt), (2600, yt + 60), (600, yt + 60)], fill="url(#pHAis)", **CUT)
    pline([(650, yt + 30), (2600, yt + 30)], stroke="#7a1f1f", sw=0.1, extra='stroke-dasharray="2 0.5"')
    for xx in range(800, 2600, 300): circ(xx, yt + 30, 0.18, fill="#7a1f1f")
def cielorraso(y):
    rect(200, y, 2600, y + 12.5, fill="#f2f2f2", **CUTT)
    rect(200, y + 12.5, 2600, y + 47, fill="none", stroke="#555", sw=0.1)
    for xx in range(500, 2600, 400): rect(xx, y + 12.5, xx + 35, y + 47, fill=ALU, stroke="#444", sw=0.08)
    pline([(200, y + 60), (200, y), (240, y)], stroke="#000", sw=0.2)

# columna vista PB y PA
columna_vista(0, 8400); mensula(3750); mensula(8250)
viga_L(3760); losa(4100)
viga_L(8260); losa(8600)
cielorraso(3500)
cielorraso(8100)
for xx in (1100, 2300):
    line(xx + 17, 3547, xx + 17, 4090, stroke="#555", sw=0.1)
    line(xx + 17, 8147, xx + 17, 8590, stroke="#555", sw=0.1)

# piso entrepiso
rect(300, 4460, 2600, 4485, fill="url(#pMort)", **CUTT)
rect(300, 4485, 2600, 4490, fill="#8d8d8d", stroke="none", sw=0)
rect(300, 4490, 2600, 4500, fill="url(#pPorc)", **CUTT)
for xx in range(860, 2600, 600): line(xx, 4490, xx, 4500, sw=0.15)

# ================================================================ MURO CORTINA
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

montante(40, 4700); montante(4720, 8400)
rect(32, 4700, 182, 4720, fill="#fff", stroke="#444", sw=0.1)                 # junta dilatación
rect(60, 4600, 150, 4840, fill="none", stroke="#444", sw=0.1, extra=DASH)   # manguito interior

# arranque PB
rect(25, 0, 190, 40, fill=ALU, **CUTT)
rect(32, 6, 182, 34, fill="#fff", stroke="#000", sw=0.06)
for xx in (60, 150): line(xx, 0, xx, -140, stroke="#000", sw=0.14)          # tarugos/anclaje a VF
rect(-30, 0, 25, 4, fill="#222", stroke="none", sw=0)                       # sellador
travesano(40, 60, glass_below=False)
dvh(110, 3490)
travesano(3500, 60)
dvh(3570, 4550, spandrel=True)
rect(40, 3570, 90, 4550, fill="url(#pLanaV)", **CUTT)                       # lana mineral spandrel
rect(90, 3570, 93, 4550, fill=STEEL, stroke="none", sw=0)                   # bandeja galv
travesano(4560, 60)
dvh(4630, 8330)
travesano(8340, 60, glass_above=False)
rect(-30, 8400, 30, 8420, fill="#222", stroke="none", sw=0)                 # sellador sup + fondo de junta
circ(0, 8410, 0.45, fill="#fff", stroke="#000", sw=0.08)

# barrera cortafuego entrepiso
rect(93, 4340, 300, 4350, fill=STEEL, stroke="none", sw=0)
rect(93, 4350, 300, 4455, fill="url(#pLana)", **CUTT)
rect(93, 4455, 300, 4462, fill="#c0392b", stroke="none", sw=0)             # sellador intumescente
pline([(182, 4503), (380, 4503)], stroke="#000", sw=0.25)                    # cubrejunta

# grapas de anclaje (en vista) + riel embutido
def grapa_sup(ytop):
    rect(330, ytop - 45, 390, ytop, fill="none", stroke="#333", sw=0.1, extra=DASH)    # riel tipo Halfen
    poly([(185, ytop), (420, ytop), (420, ytop + 10), (195, ytop + 10), (195, ytop - 160), (185, ytop - 160)], fill=STEEL, stroke="#000", sw=0.08)
    line(360, ytop - 45, 360, ytop + 25, stroke="#000", sw=0.2)              # bulón T
    line(165, ytop - 110, 200, ytop - 110, stroke="#000", sw=0.25)           # bulón M12 a montante
grapa_sup(4460)
# grapa inferior PB (a VF) y superior (a cara de viga de cubierta)
poly([(185, 40), (195, 40), (195, 180), (250, 180), (250, 190), (185, 190)], fill=STEEL, stroke="#000", sw=0.08)
poly([(185, 8270), (300, 8270), (300, 8390), (290, 8390), (290, 8280), (185, 8280)], fill=STEEL, stroke="#000", sw=0.08)
line(290, 8340, 380, 8340, stroke="#000", sw=0.25)                           # anclaje químico

# ================================================================ CUBIERTA / PARAPETO
# panel sándwich premoldeado (cenefa/parapeto)
pan = [(-40, 8420), (110, 8420), (110, 9380), (90, 9380), (90, 9400), (110, 9400), (110, 9780), (-40, 9800)]
poly([(-40, 8420), (20, 8420), (20, 9790), (-40, 9800)], fill="url(#pHA)", **CUT)
rect(20, 8460, 70, 9760, fill="url(#pEPSv)", **CUTT)
poly([(20, 8420), (110, 8420), (110, 9380), (90, 9380), (90, 9400), (110, 9400), (110, 9782), (20, 9790), (20, 9760), (70, 9760), (70, 8460), (20, 8460)], fill="url(#pHA)", **CUT)
rect(-28, 8420, -16, 8432, fill="#fff", stroke="#000", sw=0.12)              # goterón (buña)
for yy in range(8650, 9700, 400): line(5, yy, 85, yy + 80, stroke="#7a1f1f", sw=0.14)   # conectores
pline([(-28, 8600), (-28, 9760)], stroke="#7a1f1f", sw=0.08, extra='stroke-dasharray="2 0.5"')  # malla ext
# cupertina
pline([(-58, 9720), (-62, 9740), (-62, 9818), (128, 9798), (128, 9745), (132, 9730)], stroke="#000", sw=0.3)
line(30, 9760, 30, 9812, stroke="#000", sw=0.18)

# cierre de cámara panel/viga
rect(110, 8460, 160, 8890, fill="url(#pLanaV)", **CUTT)
rect(110, 8408, 300, 8414, fill=STEEL, stroke="none", sw=0)
rect(110, 8900, 300, 8960, fill="url(#pHAis)", **CUT)                         # relleno H° in situ
# unión mecánica panel-viga (en vista)
poly([(115, 8960), (420, 8960), (420, 8972), (127, 8972), (127, 8990), (115, 8990)], fill=STEEL, stroke="#000", sw=0.08)
poly([(115, 8862), (127, 8862), (127, 8960), (115, 8960)], fill=STEEL, stroke="#000", sw=0.08)
line(60, 8915, 160, 8915, stroke="#000", sw=0.25)                            # bulón a inserto
line(370, 8890, 370, 8985, stroke="#000", sw=0.25)                           # anclaje químico
poly([(115, 8520), (300, 8520), (300, 8530), (127, 8530), (127, 8600), (115, 8600)], fill=STEEL, stroke="#000", sw=0.08)

# paquete de cubierta
x0, x1 = 110, 2600
def ypend(x, base): return base + (x - x0) * 0.02
rect(x0, 8960, x1, 8963, fill="#000", stroke="none", sw=0)                   # barrera de vapor
rect(x0, 8963, x1, 9013, fill="url(#pEPS)", **CUTT)
poly([(x0, 9013), (x1, 9013), (x1, ypend(x1, 9053)), (x0, 9053)], fill="url(#pH)", **CUTT)
poly([(x0, 9053), (x1, ypend(x1, 9053)), (x1, ypend(x1, 9073)), (x0, 9073)], fill="url(#pMort)", **CUTT)
poly([(x0, 9073), (x0 + 60, 9073), (x0, 9133)], fill="url(#pMort)", **CUTT)   # media caña
pline([(x1, ypend(x1, 9077)), (x0 + 60, 9077), (x0 + 4, 9133), (x0 + 4, 9378), (95, 9390)], stroke="#000", sw=0.42)
pline([(130, 9405), (112, 9405), (112, 9330)], stroke="#000", sw=0.22)         # babeta chapa
rect(92, 9381, 110, 9399, fill="#222", stroke="none", sw=0)                   # sellador

# ================================================================ COMPOSICIÓN EN BANDAS
out = []
out.append('<g id="full">' + "\n".join(full) + "</g>")
uses = []
for i, (lo, hi, top) in enumerate(BANDS):
    dy = top - YC(hi)
    defs.append(f'<clipPath id="cb{i}" clipPathUnits="userSpaceOnUse"><rect x="0" y="{f(YC(hi))}" width="{f(X(2600)+0.01)}" height="{f((hi-lo)/S)}"/></clipPath>')
    uses.append(f'<g transform="translate(0,{f(dy)})"><g clip-path="url(#cb{i})"><use href="#full"/></g></g>')

def A(s): ann.append(s)
def T(x, y, s, size=2.0, anchor="start", weight="normal", fill="#000", rot=None, ital=False):
    r = f' transform="rotate({rot},{f(x)},{f(y)})"' if rot is not None else ""
    st = ' font-style="italic"' if ital else ""
    A(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}{r}>{s}</text>')
def L(x0, y0, x1, y1, sw=0.15, stroke="#000", extra=""):
    A(f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

# líneas de interrupción horizontales
def zig_h(py, x0p, x1p):
    xm = (x0p + x1p) / 2
    pts = [(x0p, py), (xm - 1.5, py), (xm - 0.6, py - 2), (xm + 0.6, py + 2), (xm + 1.5, py), (x1p, py)]
    A('<polyline points="' + " ".join(f"{f(a)},{f(b)}" for a, b in pts) + '" fill="none" stroke="#000" stroke-width="0.18"/>')
xa, xb = X(-1100), X(2600)
for i, (lo, hi, top) in enumerate(BANDS):
    bot = top + (hi - lo) / S
    if i > 0: zig_h(top, xa, xb)
    if i < len(BANDS) - 1: zig_h(bot, xa, xb)
# interrupción vertical derecha
for lo, hi, top in BANDS:
    bot = top + (hi - lo) / S; xm = X(2600); ym = (top + bot) / 2
    A(f'<polyline points="{f(xm)},{f(top)} {f(xm)},{f(ym-1.5)} {f(xm+2)},{f(ym-0.6)} {f(xm-2)},{f(ym+0.6)} {f(xm)},{f(ym+1.5)} {f(xm)},{f(bot)}" fill="none" stroke="#000" stroke-width="0.18"/>')

# eje de columna
for lo, hi, top in BANDS:
    bot = top + (hi - lo) / S
    L(X(100), top, X(100), bot, sw=0.12, stroke="#b03030", extra='stroke-dasharray="4 0.8 0.6 0.8"')
A(f'<circle cx="{f(X(100))}" cy="{f(Y(9960)-0)}" r="2.6" fill="#fff" stroke="#b03030" stroke-width="0.2"/>')
T(X(100), Y(9960) + 0.9, "C", 2.6, "middle", "bold", "#b03030")
L(X(100), Y(9960) + 2.6, X(100), Y(9960) + 3.0, stroke="#b03030")

# niveles
def nivel(y, txt, xpos, side="r", sub=""):
    DX.append(dict(t='nivel', y=y, x=xpos, txt=txt, sub=sub, side=side))
    px, py = X(xpos), Y(y)
    A(f'<path d="M{f(px)},{f(py)} l-1.3,-2.1 h2.6 z" fill="#000"/>')
    L(px - 4, py, px + 4, py, sw=0.15)
    ax = px + 1.8 if side == "r" else px - 1.8
    an = "start" if side == "r" else "end"
    T(ax, py - 2.6, txt, 2.1, an, "bold")
    if sub: T(ax, py - 0.6 + 2.6, sub, 1.5, an, ital=True)
nivel(9800, "+9,80", -300, "r", "Cota sup. parapeto")
nivel(9077, "+9,08", 2150, "l", "Cubierta terminada (mín.)")
nivel(8960, "+8,96", 2500, "l", "N.S.E. cubierta")
nivel(8100, "+8,10", 1500, "r", "Cielorraso PA")
nivel(4500, "+4,50", 1700, "r", "N.P.T. Planta Alta")
nivel(4460, "", 2500)
nivel(3500, "+3,50", 1500, "r", "Cielorraso PB")
nivel(0, "±0,00", 1700, "r", "N.P.T. Planta Baja")
nivel(-200, "-0,20", -500, "r", "Vereda / N.T.N.")
nivel(-620, "-0,62", 1200, "r", "Sup. tintero")
nivel(-2080, "-2,08", -380, "r", "Fondo de fundación")

# cotas verticales (lado izquierdo)
def cota_v(y0, y1, xpos, txt=None):
    DX.append(dict(t='cota', a=(xpos, y0), b=(xpos, y1), v=True, txt=txt))
    px = X(xpos); p0, p1 = Y(y0), Y(y1)
    L(px, p0, px, p1, 0.12)
    for p in (p0, p1):
        L(px - 0.8, p + 0.8, px + 0.8, p - 0.8, 0.25); L(px - 1.2, p, px + 1.6, p, 0.1)
    v = txt or (f"{abs(y1 - y0)/1000:.2f}".replace(".", ","))
    T(px - 0.7, (p0 + p1) / 2, v, 1.7, "middle", rot=-90)
cota_v(0, 4500, -1000); cota_v(4500, 8960, -1000); cota_v(8960, 9800, -1000, "0,84")
cota_v(-2080, 0, -1000)
cota_v(3760, 4460, 850, "0,70"); cota_v(8260, 8960, 850, "0,70")
cota_v(4100, 4400, 2450, "0,30"); cota_v(4400, 4460, 2350, "")
cota_v(-2000, -1500, 1250, "0,50"); cota_v(-1450, -620, 1250, "0,83")
cota_v(-610, 0, 380, "0,61")
# cotas horizontales
def cota_h(x0, x1, ypos, txt=None, below=False):
    DX.append(dict(t='cota', a=(x0, ypos), b=(x1, ypos), v=False, txt=txt))
    py = Y(ypos); a, b = X(x0), X(x1)
    L(a, py, b, py, 0.12)
    for p in (a, b):
        L(p - 0.8, py + 0.8, p + 0.8, py - 0.8, 0.25); L(p, py - 1.2, p, py + 1.2, 0.1)
    v = txt if txt is not None else f"{abs(x1-x0)/10:.0f}".replace(".", ",")
    T((a + b) / 2, py + (2.3 if below else -0.6), v, 1.6, "middle")
cota_h(-30, 182, 3050, "21"); cota_h(182, 300, 3050, "12"); cota_h(-100, 300, 3230, "40 (columna)")
cota_h(300, 600, 5050, "30"); cota_h(600, 800, 5050, "20"); cota_h(-40, 110, 9880, "15")
cota_h(-900, 1100, -2120, "2,00 (base s/cálculo)", below=True)
cota_h(-400, 600, -1560, "1,00", below=True)
cota_h(-50, 250, -700, "30", below=True)

# ------------------------------------------------ referencias numeradas
REFS = []   # (n, x, y, bx_off, by_off)
def ref(n, x, y, dx, dy):
    DX.append(dict(t='ref', n=n, a=(x, y), b=(x + dx * S, y - dy * S)))
    px, py = X(x), Y(y)
    bx, by = px + dx, py + dy
    A(f'<circle cx="{f(px)}" cy="{f(py)}" r="0.35" fill="#c0392b"/>')
    L(px, py, bx, by, 0.12, "#c0392b")
    A(f'<circle cx="{f(bx)}" cy="{f(by)}" r="1.75" fill="#fff" stroke="#c0392b" stroke-width="0.18"/>')
    T(bx, by + 0.7, str(n), 1.9 if n < 100 else 1.6, "middle", "bold", "#c0392b")

# Fundación y PB
ref(1, 1000, -2040, 12, 6)
ref(2, 900, -1800, 18, 0)
ref(3, 480, -1200, 30, 0)
ref(4, -125, -1000, -16, -4)
ref(5, 100, -400, -26, 6)
ref(6, 0, -615, -24, 9)
ref(7, -56, -500, -10, 12)
ref(8, 2000, -700, 6, 6)
ref(9, 2400, -260, 2, 9)
ref(10, 2200, -181, 7, 12)
ref(11, 2000, -120, 2, 15)
ref(12, 1600, -50, -4, 18)
ref(13, 1300, -28, -6, 22)
ref(14, 2200, -5, 4, -10)
ref(15, 260, -90, 14, 22)
ref(16, -400, -250, 0, -12)
ref(17, -62, -30, -17, -6)
ref(41, 190, 20, 26, -16)
ref(42, 100, 20, 30, -10)
ref(43, -5, 2, -19, -12)
# Estructura
ref(18, 230, 2950, 40, 0)
ref(18, 230, 7950, 50, 6)
ref(19, 500, 3550, 30, 0)
ref(20, 450, 4200, 40, 18)
ref(21, 540, 3820, 40, 6)
ref(22, 2000, 4300, 0, -14)
ref(23, 770, 4250, 14, -16)
ref(24, 750, 4095, 28, 8)
ref(25, 610, 4300, 46, 21)
ref(26, 2050, 4430, 0, -13)
ref(27, 450, 3620, 22, 10)
ref(28, 120, 3000, -20, 2)
ref(29, 100, 3530, 30, 4)
ref(30, -8, 3480, -18, 2)
ref(31, -25, 3600, -16, 4)
ref(32, 27, 3470, 34, 18)
ref(33, 12, 2950, -19, -6)
ref(34, 12, 3483, -22, 10)
ref(35, 12, 4625, -24, -2)
ref(36, 190, 4400, 47, -9)
ref(37, 360, 4440, 54, 1)
ref(38, 100, 4710, 32, 0)
ref(39, 3, 4100, -16, 0)
ref(40, 65, 4000, -24, 9)
ref(44, 92, 4400, -26, 10)
ref(45, 300, 4503, 30, -9)
ref(46, 1700, 4495, 0, -12)
ref(47, 1400, 3540, 0, 8)
ref(48, 1117, 4000, 8, -2)
# Cubierta
ref(49, 1700, 8961, 4, 9)
ref(50, 1500, 8990, 8, 12)
ref(51, 1700, 9040, 0, -10)
ref(52, 2150, 9067, 2, -14)
ref(53, 1200, 9077, -2, -12)
ref(54, 135, 9085, 22, -16)
ref(55, 112, 9380, 22, -4)
ref(56, -10, 9500, -18, 0)
ref(57, 45, 9490, -26, 8)
ref(58, -28, 9100, -16, 6)
ref(59, -22, 8426, -22, -3)
ref(60, 50, 9805, -9, -5)
ref(61, 121, 8930, 34, -20)
ref(62, 121, 8560, 30, 6)
ref(63, 135, 8700, 40, 6)
ref(64, 180, 8930, 42, -2)
ref(65, 270, 8330, 32, 6)
ref(66, 0, 8410, -14, 11)
ref(67, 2000, 8105, 0, 9)

# rótulos directos (cortos)
def lab(x, y, s, size=1.7, anchor="start", ital=True, fill="#333"):
    DX.append(dict(t='text', p=(x, y), s=s, h=size * S))
    T(X(x), Y(y), s, size, anchor, ital=ital, fill=fill)
lab(-900, 8000, "EXTERIOR", 2.4, ital=False, fill="#555")
lab(800, 5000, "INTERIOR · PLANTA ALTA", 2.2, ital=False, fill="#555")
lab(800, 2980, "INTERIOR · PLANTA BAJA", 2.2, ital=False, fill="#555")
lab(800, 700, "INTERIOR · PLANTA BAJA", 2.2, ital=False, fill="#555")
lab(-1080, 700, "EXTERIOR", 2.4, ital=False, fill="#555")
lab(-1080, 5000, "EXTERIOR", 2.4, ital=False, fill="#555")
lab(1300, 9160, "pend. 2 % →  hacia canaleta perimetral", 1.6)
A(f'<path d="M{f(X(2400))},{f(Y(9150))} l-14,0.3" stroke="#000" stroke-width="0.15" marker-end="url(#arr)"/>')
lab(1350, -1000, "Fundación (base, tintero y", 1.5); lab(1350, -1080, "columna) en proyección, sobre", 1.5); lab(1350, -1160, "eje de columna – línea de trazos", 1.5)
lab(700, 3300, "Columna y ménsulas en vista", 1.5)
lab(700, 3220, "(corte entre ejes, a ½ luz de viga)", 1.5)
lab(1300, 4850, "Vidrio de seguridad laminado: protección contra caídas", 1.45)

defs.append('<marker id="arr" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4 z" fill="#000"/></marker>')

# ================================================================ RÓTULO + LEYENDA
LEG = [
("FUNDACIÓN Y PISO SOBRE TERRENO", None),
(1, "Hormigón de limpieza H-8, e = 8 cm."),
(2, "Base aislada H°A° in situ H-25 (dim. y armadura s/ cálculo y estudio de suelos)."),
(3, "Tintero / cáliz H°A° in situ, empotramiento de columna ≥ 1,5 b (83 cm)."),
(4, "Columna empotrada c/ llaves de corte + grout cementicio sin retracción (5 cm)."),
(5, "Viga de fundación premoldeada H°A° 30x61 (VF) apoyada en tinteros, centrada en el eje de bases."),
(6, "Apoyo de neopreno e = 10 mm, VF / tintero."),
(7, "Aislación hidrófuga vertical: pintura asfáltica 2 manos + film 200 µ."),
(8, "Suelo natural compactado."),
(9, "Tosca compactada e = 15 cm (95 % Proctor)."),
(10, "Film de polietileno 200 µ, solapes 20 cm (barrera de humedad)."),
(11, "Contrapiso H°A° e = 12 cm c/ malla Q188."),
(12, "Carpeta hidrófuga 1:3 + 10 % hidrófugo, e = 2 cm."),
(13, "Carpeta de nivelación 1:3, e = 2,5 cm."),
(14, "Porcelanato 60x60 s/ adhesivo cementicio impermeable."),
(15, "Junta perimetral EPS 20 mm + sellador poliuretánico."),
(16, "Vereda H° peinado e = 10 cm s/ tosca + junta c/ sellador."),
(17, "Babeta chapa galv. N°24 plegada c/ goterón."),
("ESTRUCTURA PREMOLDEADA (GRANDES LUCES)", None),
(18, "Columna premoldeada H°A° 40x40 H-30 en el eje de fachada (en vista); el muro cortina se interrumpe en cada columna c/ perfil de encuentro + sellador."),
(19, "Ménsula corta interior de columna, apoyo de viga (en vista)."),
(20, "Viga portante premoldeada pretensada tipo “L” 30/70 c/ talón 20x33, H-40."),
(21, "Cordones de pretensado Ø 12,7 mm + estribos / armadura pasiva."),
(22, "Losa alveolar pretensada e = 30 cm (luces hasta 14 m), corte por alvéolo."),
(23, "Tapón de H° en alvéolos de apoyo (30 cm)."),
(24, "Apoyo de neopreno continuo 10 mm, losa / talón de viga."),
(25, "Junta viga–losa llenada c/ H° in situ (llave de corte)."),
(26, "Capa de compresión H°A° in situ H-25 e = 6 cm c/ malla Q188 (diafragma)."),
(27, "Bulón Ø 20 ménsula–viga en vaina grouteada + neopreno (en vista)."),
("MURO CORTINA – SISTEMA STICK, MÓDULO 1,25 m", None),
(28, "Montante aluminio 50x150 anodizado (en vista)."),
(29, "Travesaño aluminio 50x120 (corte)."),
(30, "Presor de aluminio + tornillo inox c/ 25 cm."),
(31, "Tapa exterior clipada (cubre-presor)."),
(32, "Burletes EPDM interior y exterior."),
(33, "DVH: 6 templado + 12 cámara + 3+3 laminado PVB."),
(34, "Separador alum. c/ desecante + butilo + silicona estructural."),
(35, "Calzos de apoyo de EPDM (2 por paño)."),
(36, "Grapa de anclaje acero galv. regulable 3D, agujeros colisos + bulón M12 inox."),
(37, "Riel de anclaje (tipo Halfen) embutido en viga + bulón T."),
(38, "Junta de dilatación de montante 20 mm c/ manguito interior."),
(39, "Spandrel: vidrio templado 6 mm esmaltado + cámara ventilada."),
(40, "Lana mineral 50 mm + bandeja de chapa galv. (back-pan)."),
(41, "Grapa inferior a VF (anclaje mecánico)."),
(42, "Perfil de arranque alum. c/ drenaje + tarugos a VF."),
(43, "Sellador de silicona neutra s/ fondo de junta."),
(44, "Barrera cortafuego: lana mineral 100 kg/m³ comprimida s/ chapa galv."),
(45, "Cubrejunta perfil aluminio + sellador intumescente."),
(46, "Carpeta 2,5 cm + adhesivo + porcelanato (piso PA)."),
(47, "Cielorraso suspendido placa de roca de yeso 12,5 mm junta tomada s/ perfilería galv."),
(48, "Vela rígida a losa (perfil galv.)."),
("CUBIERTA Y PARAPETO", None),
(49, "Barrera de vapor: imprimación asfáltica + film 200 µ."),
(50, "Aislación térmica EPS 30 kg/m³ e = 5 cm."),
(51, "H° de pendiente alivianado, mín. 4 cm, pend. 2 %."),
(52, "Carpeta cementicia 1:3 e = 2 cm."),
(53, "Membrana asfáltica 4 mm c/ geotextil + pintura reflectiva."),
(54, "Media caña de mortero (encuentro con parapeto)."),
(55, "Babeta: membrana en buña + perfil chapa + sellador."),
(56, "Panel sándwich premoldeado (cenefa/parapeto): H°A° 6 + EPS 5 + H°A° 4 cm."),
(57, "Conectores de acero inox entre capas del panel."),
(58, "Malla electrosoldada del panel."),
(59, "Goterón (buña 12x12)."),
(60, "Cupertina chapa galv. N°22 c/ goterones, tornillo + sellador."),
(61, "Unión mecánica panel–viga: perfil L 100x10 galv. + inserto roscado + anclaje químico M16."),
(62, "Perfil L de restricción inferior del panel."),
(63, "Lana mineral 50 mm en cámara panel–viga."),
(64, "H° de relleno in situ s/ chapa galv. (cierre de cámara)."),
(65, "Grapa superior de montante a viga (anclaje químico)."),
(66, "Sellador + fondo de junta: travesaño sup. / panel."),
(67, "Cielorraso suspendido PA (ídem 47) – plenos de instalaciones."),
]

def legend():
    x0, y = 204.0, 14.0
    A(f'<rect x="{x0-2}" y="9" width="{297-x0-4}" height="402" fill="none" stroke="#000" stroke-width="0.3"/>')
    T(x0, y, "REFERENCIAS", 2.6, weight="bold"); y += 1.5
    for item in LEG:
        if item[1] is None:
            y += 2.3
            A(f'<rect x="{x0-0.5}" y="{f(y-2.0)}" width="{297-x0-5.5}" height="2.7" fill="#2f3b45"/>')
            T(x0, y, item[0], 1.75, weight="bold", fill="#fff"); y += 2.45
            continue
        n, txt = item
        # partir texto en líneas
        words, lines, cur = txt.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 50: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
        T(x0 + 1.6, y, str(n), 1.8, "middle", "bold", "#c0392b")
        for ln in lines:
            T(x0 + 3.8, y, ln, 1.8); y += 2.25
        y += 0.15
    return y
yend = legend()

# leyenda de materiales (rayados)
def sw_(x, y, fill, txt):
    A(f'<rect x="{f(x)}" y="{f(y)}" width="6" height="3" fill="{fill}" stroke="#000" stroke-width="0.15"/>')
    T(x + 7, y + 2.3, txt, 1.5)
my = yend + 1.5
T(204, my, "CONVENCIONES", 2.0, weight="bold"); my += 1.5
mats = [("url(#pHA)", "H°A° premoldeado"), ("url(#pHAis)", "H°A° in situ"), ("url(#pH)", "H° simple / pendiente"),
        ("url(#pMort)", "Mortero / carpeta"), ("url(#pGrout)", "Grout s/ retracción"), ("url(#pTierra)", "Suelo natural"),
        ("url(#pTosca)", "Tosca compactada"), ("url(#pEPS)", "EPS"), ("url(#pLana)", "Lana mineral"),
        (GLASS, "Vidrio"), (ALU, "Aluminio"), (STEEL, "Acero galv. / neopreno")]
for i, (fl, t) in enumerate(mats):
    sw_(204 + (i % 3) * 28.5, my + (i // 3) * 4.0, fl, t)
my += 4 * 4.0 + 0.5
A(f'<line x1="204" y1="{my}" x2="211" y2="{my}" stroke="#444" stroke-width="0.13" stroke-dasharray="1.2 0.6"/>'); T(212, my + 0.6, "Proyección / oculto", 1.5)
A(f'<line x1="240" y1="{my}" x2="247" y2="{my}" stroke="#b03030" stroke-width="0.13" stroke-dasharray="4 0.8 0.6 0.8"/>'); T(248, my + 0.6, "Eje de columna", 1.5)
my += 3
NOTAS = ["Sistema: columnas premoldeadas empotradas en tinteros + vigas “L” pretensadas",
 "s/ ménsulas + losas alveolares pretensadas (luces 10–14 m). Uniones mecánicas",
 "(bulones, perfiles, insertos) y húmedas (grout / H° in situ: capa de compresión).",
 "Corte entre ejes de columnas (a ½ luz de viga); columna y ménsulas en vista.",
 "Eje único de fachada: muro cortina, VF, columna, tintero y base alineados.",
 "Muro cortina stick: montantes colgados de cada entrepiso (grapa superior fija,",
 "inferior deslizante) c/ junta de dilatación 20 mm para absorber deformaciones.",
 "Tolerancias de montaje premoldeado ±10 mm, absorbidas por grapas regulables 3D.",
 "Juntas de fachada c/ fondo de junta + sellador; drenaje y ventilación de travesaños.",
 "Barrera cortafuego continua en cada borde de losa (sectorización por piso).",
 "Cotas en m (niveles) y cm (detalles). Verificar todo s/ cálculo estructural."]
my += 1.5
T(204, my, "NOTAS DEL SISTEMA", 2.0, weight="bold"); my += 2.6
for nt in NOTAS:
    T(204, my, nt, 1.55); my += 2.15

# rótulo
ry = 411 - 44
A(f'<line x1="202" y1="{ry}" x2="291" y2="{ry}" stroke="#000" stroke-width="0.3"/>')
T(204, ry + 5, "LÁMINA 2 · CORTE INTEGRAL", 3.0, weight="bold")
T(204, ry + 9.5, "Sistema de hormigón premoldeado de grandes luces", 2.0)
T(204, ry + 12.5, "Cerramiento vidriado – muro cortina (sistema stick)", 2.0)
A(f'<line x1="202" y1="{ry+15}" x2="291" y2="{ry+15}" stroke="#000" stroke-width="0.2"/>')
rows = [("MATERIA", "Construcciones II"), ("CÁTEDRA", "Arq. ________________"), ("ALUMNO/A", "______________________"),
        ("GRUPO", "______"), ("ESCALA", "1:20 (impresión al 100 % en A3)"), ("HOJA", "1 de 2 · A3 · 2026")]
for i, (k, v) in enumerate(rows):
    yy = ry + 19 + i * 4.1
    T(204, yy, k, 1.6, weight="bold"); T(222, yy, v, 1.8)
A(f'<rect x="202" y="{ry}" width="89" height="44" fill="none" stroke="#000" stroke-width="0.3"/>')
# escala gráfica
sx, sy = 14, 411.5
for i in range(5):
    A(f'<rect x="{sx + i*5}" y="{sy-1.2}" width="5" height="1.2" fill="{"#000" if i%2==0 else "#fff"}" stroke="#000" stroke-width="0.12"/>')
    T(sx + i * 5, sy - 1.8, f"{i*10}", 1.3, "middle")
T(sx + 25, sy - 1.8, "50 cm", 1.3, "middle"); T(sx + 32, sy, "ESC. 1:20", 1.8, weight="bold")

# título del corte
T(X(-1100), 12.5, "CORTE INTEGRAL — FACHADA VIDRIADA · HORMIGÓN PREMOLDEADO", 3.0, weight="bold")
T(X(-1100) + 140, 12.5, "ESC. 1:20", 3.0, weight="bold")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="297mm" height="420mm" viewBox="0 0 297 420"
 font-family="Liberation Sans, Arial, sans-serif">
<defs>{"".join(defs)}<g id="fullg">{"".join(full)}</g></defs>
<rect x="0" y="0" width="297" height="420" fill="#fff"/>
<rect x="5" y="5" width="287" height="410" fill="none" stroke="#000" stroke-width="0.5"/>
{"".join(uses).replace('href="#full"', 'href="#fullg"')}
{"".join(ann)}
</svg>'''
os.makedirs("build", exist_ok=True)
open("build/lamina1.svg", "w").write(svg)
open("build/lamina1.html", "w").write(f'''<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:297mm 420mm;margin:0}}html,body{{margin:0;padding:0}}svg{{display:block}}</style></head>
<body>{svg}<script>window.READY=true</script></body></html>''')
print("ok", yend)
import json
json.dump(dict(DX=DX, LEG=LEG, NOTAS=NOTAS), open("build/lamina1_dx.json", "w"), ensure_ascii=False)
