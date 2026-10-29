# -*- coding: utf-8 -*-
"""TP N°6 - Corte integral acero / frente integral (A3 vertical).

Se usa el CORTE ORIGINAL de la alumna (original/corte_original.pdf, vectores de AutoCAD convertidos a SVG) sin redibujarlo:
se recorta la zona del corte y se ubica a ESCALA 1:20 real (el original está dibujado a 1:10 en mm de papel).
Sobre él solo se agregan las correcciones marcadas por la docente (original/correcciones_docente.jpg):
  36 chapa plegada p/ anclaje del panel sándwich · 37 tubo soldado a la viga IPN p/ anclar la columna del frente integral
  38 brocas de la baranda a la losa · 39 vela rígida a losa p/ cielorraso · 40 dado estructural p/ columna y frente integral
  + rayado que distingue el hormigón del dado del contrapiso, y líneas de interrupción en los paños vidriados
    (las alturas de vidrio del original no son reales: con la interrupción el dibujo queda en escala).
Coordenadas "P": mm de papel del PDF original (x a la derecha, y hacia abajo) -> 1 mm P = 10 mm reales.
"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build"); os.makedirs(B, exist_ok=True)
svg_src = os.path.join(B, "original.svg")
if not os.path.exists(svg_src):
    subprocess.run(["pdftocairo", "-svg", os.path.join(ROOT, "original", "corte_original.pdf"), svg_src], check=True,
                   stderr=subprocess.DEVNULL)
raw = open(svg_src).read()
inner = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")]

PT = 25.4 / 72                      # pt -> mm de papel del original
K = 0.5                             # original 1:10 -> 1:20
TX, TY = 141.5, 6.0                 # ubicación del corte en la lámina (mm)
f = lambda v: f"{v:.3f}"

# ------------------------------------------------------------------ patrones
DEFS = '''
<pattern id="kHA" patternUnits="userSpaceOnUse" width="2.4" height="2.4" patternTransform="rotate(45)">
 <line x1="0" y1="0" x2="0" y2="2.4" stroke="#000" stroke-width="0.12"/><circle cx="1.2" cy="0.6" r="0.16" fill="#000"/><circle cx="1.6" cy="1.8" r="0.12" fill="#000"/></pattern>
<pattern id="kCP" patternUnits="userSpaceOnUse" width="3.2" height="3.2">
 <circle cx="0.7" cy="0.8" r="0.17" fill="#444"/><circle cx="2.3" cy="2.1" r="0.13" fill="#444"/><circle cx="2.7" cy="0.5" r="0.09" fill="#444"/>
 <path d="M1.8 0.6 l0.4 0.6 h-0.8z" fill="none" stroke="#444" stroke-width="0.08"/><path d="M0.6 2.3 l0.35 0.5 h-0.7z" fill="none" stroke="#444" stroke-width="0.08"/></pattern>
'''

# ------------------------------------------------------------------ dibujo en coordenadas P (se escala con el corte)
under, over = [], []
def poly(dst, pts, fill="none", stroke="#000", sw=0.25, extra=""):
    dst.append(f'<polygon points="{" ".join(f"{f(x)},{f(y)}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')
def pl(dst, pts, sw=0.25, stroke="#000", extra="", fill="none"):
    dst.append(f'<polyline points="{" ".join(f"{f(x)},{f(y)}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
def rect(dst, x0, y0, x1, y1, **k): poly(dst, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)
def circ(dst, x, y, r, fill="#fff", stroke="#000", sw=0.2):
    dst.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(dst, x, y, s, size=2.4, anchor="start", w="normal", fill="#000"):
    dst.append(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}">{s}</text>')

# --- 40 · DADO ESTRUCTURAL H°A° (zona entre el contrapiso y el cuello de la zapata, bajo columna y frente integral)
DX0, DX1, DY0, DY1 = 178.3, 218.4, 263.75, 271.5
rect(under, DX0, DY0, DX1, DY1, fill="url(#kHA)", stroke="none", sw=0)
# contrapiso H° (4) a ambos lados del dado: rayado propio para que no se confunda con el hormigón
poly(under, [(118.7, 264.45), (DX0, 263.9), (DX0, DY1), (118.7, DY1)], fill="url(#kCP)", stroke="none", sw=0)
rect(under, DX1, DY0, 278.3, DY1, fill="url(#kCP)", stroke="none", sw=0)
for xx in (DX0, DX1): pl(over, [(xx, DY0), (xx, DY1 + 0.3)], sw=0.45)                    # caras del dado (antes ocultas)

# --- 36 · chapa plegada galv. de anclaje del panel sándwich (entre panel y membrana), fijada a la losa con brocas
def chapa_panel():
    pl(over, [(187.78, 17.2), (187.78, 37.72), (197.2, 37.72)], sw=0.32)
    for yy in (21.0, 33.0): pl(over, [(184.2, yy), (188.0, yy)], sw=0.22); pl(over, [(187.9, yy - 0.5), (187.9, yy + 0.5)], sw=0.28)  # autoperforantes
    for xx in (192.0, 195.6):                                                                 # brocas
        rect(over, xx - 0.22, 37.75, xx + 0.22, 41.6, fill="#000", stroke="none", sw=0)
        rect(over, xx - 0.55, 37.25, xx + 0.55, 37.72, fill="#000", stroke="none", sw=0)
chapa_panel()

# --- 37 · tubo soldado a la viga IPN (espiga dentro de la columna del frente integral) + bulón pasante
def tubo(yb):
    """yb: cara inferior del ala inferior de la IPN"""
    rect(over, 198.0, yb, 202.0, yb + 13.5, fill="none", stroke="#000", sw=0.22, extra='stroke-dasharray="0.9 0.45"')
    rect(over, 198.35, yb, 201.65, yb + 13.5, fill="none", stroke="#000", sw=0.1, extra='stroke-dasharray="0.9 0.45"')
    for xa, xb in ((198.0, 197.2), (202.0, 202.8)): poly(over, [(xa, yb), (xb, yb), (xa, yb + 0.8)], fill="#000", stroke="none", sw=0)  # soldadura
    circ(over, 200.0, yb + 9.5, 0.75, fill="#fff", stroke="#000", sw=0.18); circ(over, 200.0, yb + 9.5, 0.28, fill="#000", stroke="none", sw=0)  # bulón pasante
tubo(70.25); tubo(183.75)

# --- 38 · brocas de la baranda a la losa (entrepiso)
for xx in (204.45, 207.5):
    rect(over, xx - 0.2, 148.55, xx + 0.2, 154.3, fill="#000", stroke="none", sw=0)
    rect(over, xx - 0.5, 147.9, xx + 0.5, 148.4, fill="#000", stroke="none", sw=0)

# --- 39 · velas rígidas a losa p/ cielorraso (montante 35 + ángulo de fijación a la losa)
def vela(x, ytop, ybot):
    rect(over, x - 1.75, ytop + 0.6, x + 1.75, ybot, fill="#fff", stroke="#000", sw=0.2)
    pl(over, [(x - 1.75, ytop + 0.6), (x - 1.75, ytop + 0.1), (x + 3.2, ytop + 0.1)], sw=0.25)
    pl(over, [(x + 2.4, ytop - 0.1), (x + 2.4, ytop - 2.2)], sw=0.3)                          # clavo / tornillo a losa
    pl(over, [(x - 1.2, ybot - 1.2), (x + 1.2, ybot - 1.2)], sw=0.2)
for x in (211.0, 270.9):
    vela(x, 48.35, 65.9)        # cielorraso de planta alta (bajo cubierta)
    vela(x, 161.85, 179.5)      # cielorraso de planta baja (bajo entrepiso)

# --- interrupción de los paños vidriados (alturas no representadas)
def corte_h(y):
    x0, x1, xm = 179.0, 292.0, 238.0
    rect(over, x0, y - 0.9, x1, y + 0.9, fill="#fff", stroke="none", sw=0)
    for dy in (-0.9, 0.9):
        pl(over, [(x0, y + dy), (xm - 2.2, y + dy), (xm - 1.0, y + dy - 2.2), (xm + 1.0, y + dy + 2.2), (xm + 2.2, y + dy), (x1, y + dy)], sw=0.22)
corte_h(99.5); corte_h(211.0)

# --- globos de las correcciones (mismo estilo que los del original)
def globo(n, bx, by, tx, ty):
    pl(over, [(bx, by), (tx, ty)], sw=0.25)
    circ(over, tx, ty, 0.45, fill="#000", stroke="none", sw=0)
    circ(over, bx, by, 5.2, fill="#fff", stroke="#000", sw=0.25)
    txt(over, bx, by + 2.55, str(n), 7.2, "middle")
globo(36, 152.0, 26.0, 187.78, 26.0)
globo(37, 229.0, 94.0, 200.0, 79.75)
globo(37, 229.0, 207.0, 200.0, 193.25)
globo(38, 228.0, 141.5, 207.5, 151.5)
globo(39, 284.0, 57.0, 272.65, 57.0)
globo(39, 284.0, 170.5, 272.65, 170.5)
globo(40, 258.0, 281.0, 214.0, 267.6)

# ------------------------------------------------------------------ composición del corte
CLIP = [(164.6, 2), (296.5, 2), (296.5, 384.3), (117, 384.3), (117, 238), (164.6, 238)]
clip = f'<clipPath id="kClip" clipPathUnits="userSpaceOnUse"><polygon points="{" ".join(f"{x},{y}" for x, y in CLIP)}"/></clipPath>'
CORTE = (f'<g transform="translate({TX},{TY}) scale({K})">'
         f'<g clip-path="url(#kClip)">{"".join(under)}<g transform="scale({PT})">{inner}</g></g>'
         f'{"".join(over)}</g>')

# ------------------------------------------------------------------ lámina (mm)
ann = []
def T(x, y, s, size=2.4, anchor="start", w="normal", fill="#000"): txt(ann, x, y, s, size, anchor, w, fill)
def L(x0, y0, x1, y1, sw=0.25): pl(ann, [(x0, y0), (x1, y1)], sw=sw)

LEG = [
 (1, "CUPERTINA ZINGUERÍA ESTANCA"), (2, "AISLACIÓN HIDRÓFUGA MEMBRANA ASFÁLTICA"), (3, "CARPETA DE NIVELACIÓN MHR"),
 (4, "CONTRAPISO H°LIVIANO"), (5, "BARRERA DE VAPOR FILM POLIETILENO 200µ"), (6, "CAPA DE COMPRESIÓN SOBRE MALLA ELECTROSOLDADA"),
 (7, "SEPARADOR DE HORMIGÓN PARA MALLA ELECTROSOLDADA"), (8, "CONECTORES DE CORTANTE SOBRE VIGA IPN"),
 (9, "CERRAMIENTO EXTERIOR VERTICAL TERMOPANELES|SANDWICH CON NÚCLEO DE POLIURETANO 40MM"), (10, "PERFIL L PARA PAQUETE DE CONTRAPISO"),
 (11, "ESTRUCTURA SECUNDARIA PARA PANELES VERTICALES:|PERFIL OMEGA Y SUJECION INFERIOR PERFIL Z"), (12, "ZINGUERIA DE BORDE CON SUJECIÓN A CHAPA GALVADECK"),
 (13, "VIGA IPN 200 CON ANCLAJE A COLUMNA MEDIANTE UNIÓN|SOLDADA Y MECÁNICA DE BULONES"), (14, "PERFIL Z BUÑA EN CIELORRASO INDEPENDIENTE"),
 (15, "CIELORRASO PLACA DURLOCK e= 9.5 mm"), (16, "VIGA IPN 180 CON ANCLAJE A COLUMNA MEDIANTE UNIÓN|SOLDADA Y MECÁNICA DE BULONES"),
 (17, "PLACA COLABORANTE GALVADECK PARA LOSA"), (18, "PERFIL C CON BANDA DE NEOPRENO FIJADO A VIGA PARA|CIELORRASO INDEPENDIENTE"),
 (19, "ZINGUERIA A MEDIDA PARA CERRAMIENTO Y BUÑA"),
 (20, "FRENTE INTEGRAL: TRAVESAÑO CON MT-0817 TAPA INTERIOR|Y MT-0819 TAPA EXTERIOR. ANCLAJE DE BULÓN A PERFIL IPN"),
 (21, "FRENTE INTEGRAL: COLUMNA CON MT-0817 TAPA INTERIOR Y|MT-0819 TAPA EXTERIOR. ANCLAJE DE BULÓN A PERFIL IPN"),
 (22, "DOBLE VIDRIO HERMÉTICO"), (23, "PERFIL HEB 200 COLUMNA"), (24, "SELLADOR JUNTA + BANDA DE NEOPRENO"),
 (25, "ZINGUERIA  A MEDIDA ALFEIZAR CON PENDIENTE"), (26, "BARANDA POSAPIE PARA PROTECCIÓN ACERO INOXIDABLE"),
 (27, "SOLADO SOBRE ADHESIVO CEMENTICIO"), (28, "AISLACIÓN TÉRMICA: PLACA DE EPS 40MM"),
 (29, "PLATABANDA PARA ANCLAJE A FUNDACIÓN|Y COLUMNA SOLDADA"), (30, "TUERCA / CONTRATUERCA / TUERCA DE NIVELACIÓN"),
 (31, "PERNOS DE ANCLAJE A FUNDACIÓN"), (32, "SEPARADOR DE SUELO FILM POLIETILENO 200µ"),
 (33, "CARPETA HIDRÓFUGA MCI + 10% ADITIVO HIDRÓFUGO"), (34, "ZAPATA DE H° A° ARMADURA SEGÚN CÁLCULO"), (35, "SUELO COMPACTO"),
 (36, "CHAPA PLEGADA GALVANIZADA PARA ANCLAJE DE PANEL|SANDWICH, ATORNILLADA AL PANEL Y FIJADA A LOSA CON BROCAS"),
 (37, "TUBO ESTRUCTURAL SOLDADO A VIGA IPN PARA ANCLAJE DE|COLUMNA DE FRENTE INTEGRAL CON BULÓN PASANTE"),
 (38, "BROCAS DE ANCLAJE A LOSA PARA BARANDA"),
 (39, "VELA RÍGIDA A LOSA PARA CIELORRASO (PERFIL MONTANTE|GALVANIZADO 35mm + ÁNGULO DE FIJACIÓN)"),
 (40, "DADO ESTRUCTURAL DE H° A° PARA COLUMNA|Y FRENTE INTEGRAL"),
]
def referencias(x, y, items, dy=3.05, sz=2.25):
    for n, s in items:
        circ(ann, x + 1.45, y - 0.8, 1.45, fill="#fff", stroke="#000", sw=0.15)
        T(x + 1.45, y + 0.05, str(n), 1.9 if n < 10 else 1.75, "middle")
        for k, line in enumerate(s.split("|")):
            T(x + 3.5, y + k * 2.7, line, sz)
        y += dy + 2.7 * (len(s.split("|")) - 1)
    return y

T(8, 14.5, "CORTE INTEGRAL ACERO FRENTE INTEGRAL. ESC 1:20", 5.2, w="bold")
T(8, 20.5, "DETALLES EN AXONOMETRÍA ESC 1:10", 3.6, w="bold")
# referencias debajo del corte (columna derecha)
T(200.5, 207.0, "REFERENCIAS", 2.6)
L(200.5, 207.6, 216.0, 207.6, 0.15)
yend = referencias(200.5, 212.0, LEG)

# escalas gráficas
def escala(x0, y0, den, total, step, lab):
    w = total * 1000 / den; n = round(total / step)
    for k in range(n):
        ann.append(f'<rect x="{f(x0 + k * w / n)}" y="{f(y0)}" width="{f(w / n)}" height="1.1" fill="{"#000" if k % 2 == 0 else "#fff"}" stroke="#000" stroke-width="0.12"/>')
    for k in range(n + 1): T(x0 + k * w / n, y0 + 3.9, (f"{k * step:.2f}".rstrip("0").rstrip(".")).replace(".", ","), 2.0, "middle")
    T(x0 + w + 2, y0 + 1.2, lab, 2.0)
escala(8, 27.0, 20, 1.0, 0.25, "m (corte 1:20)")
escala(85, 27.0, 10, 0.5, 0.1, "m (detalles 1:10)")

# rótulo (mismo formato que el original)
R0, R1 = 384.8, 416.0
ann.append(f'<rect x="7.6" y="{R0}" width="283.9" height="{f(R1 - R0)}" fill="none" stroke="#000" stroke-width="0.4"/>')
for xx in (39.0, 130.0, 221.8):
    ann.append(f'<line x1="{xx}" y1="{R0}" x2="{xx}" y2="{R1}" stroke="#000" stroke-width="0.3"/>')
T(23.3, 395.0, "TP", 6.2, "middle"); T(23.3, 405.0, "N°6", 6.2, "middle")
T(9.2, 413.6, "FECHA:", 2.6); T(19.5, 413.6, "29/10/2026", 2.0)
T(40.6, 390.4, "DOCENTE:", 3.4)
T(41.6, 402.0, "ALUMNA:", 3.4); T(59.0, 402.0, "VITALE, CANDELARIA", 2.6)
T(40.6, 413.0, "GRUPO:", 3.4); T(55.0, 413.0, "13", 2.6)
T(131.8, 390.4, "NIVEL:", 3.4); T(131.8, 401.0, "OBS:", 3.4)
T(256.6, 398.2, "CONSTRUCCIONES II", 3.0, "middle"); T(256.6, 403.2, "CATEDRA: ARQ. TUCCI", 3.0, "middle")

SVG = f'''<defs>{DEFS}{clip}</defs>
<rect x="0" y="0" width="297" height="420" fill="#fff"/>
{CORTE}
{"".join(ann)}'''
open(os.path.join(B, "lamina.svgpart"), "w").write(SVG)
print("ok; referencias hasta y =", round(yend, 1))
