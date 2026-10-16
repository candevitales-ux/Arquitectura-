# -*- coding: utf-8 -*-
"""Lámina 3 – Detalles en CORTE de las uniones, extraídos del corte integral (Lámina 1).
Mismo plano de corte y mismas coordenadas (mm reales; x+ interior, y+ arriba, ±0,00 = NPT PB).
Cada detalle es una ventana del mismo dibujo, a escala 1:5, con mayor nivel de detalle."""
import math, json, os

E = []          # entidades en coordenadas reales
def poly(pts, fill="none", stroke="#000", sw=0.35, dash=False, lay=None):
    E.append(dict(t="poly", pts=[tuple(p) for p in pts], fill=fill, stroke=stroke, sw=sw, dash=dash, lay=lay))
def rect(x0, y0, x1, y1, **k): poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)
def pline(pts, stroke="#000", sw=0.25, dash=False, lay=None):
    E.append(dict(t="pline", pts=[tuple(p) for p in pts], stroke=stroke, sw=sw, dash=dash, lay=lay))
def line(x0, y0, x1, y1, **k): pline([(x0, y0), (x1, y1)], **k)
def circ(x, y, r, fill="#000", stroke="#000", sw=0.15, dash=False):
    E.append(dict(t="circ", c=(x, y), r=r, fill=fill, stroke=stroke, sw=sw, dash=dash))
def rrect(x0, y0, x1, y1, r, n=4):          # rectángulo de esquinas redondeadas (polilínea)
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts
def oblong(cx, cy, L, h, horiz=True):        # agujero coliso
    r = h / 2; pts = []
    for k in range(9):
        a = math.radians(90 + 180 * k / 8); pts.append((cx - L / 2 + r * math.cos(a), cy + r * math.sin(a)) if horiz else (cx + r * math.cos(a + math.pi / 2), cy - L / 2 + r * math.sin(a + math.pi / 2)))
    for k in range(9):
        a = math.radians(-90 + 180 * k / 8); pts.append((cx + L / 2 + r * math.cos(a), cy + r * math.sin(a)) if horiz else (cx + r * math.cos(a + math.pi / 2), cy + L / 2 + r * math.sin(a + math.pi / 2)))
    return pts
def hexa(cx, cy, r):
    return [(cx + r * math.cos(math.radians(30 + 60 * k)), cy + r * math.sin(math.radians(30 + 60 * k))) for k in range(6)]

REB = "#8e2a1a"; ALU = "#9aa3ab"; ALU2 = "#c3c9ce"; STEEL = "#4a4f55"; GALV = "#8d959c"; NEO = "#151515"
GLASS = "#bfe3f0"; EPDM = "#222"; PA = "#3c4650"; SIL = "#555"; INOX = "#b4bac0"
CUT = dict(stroke="#000", sw=0.45)
CUTT = dict(stroke="#000", sw=0.25)
VIEW = dict(stroke="#555", sw=0.18)

# ================================================================== ESTRUCTURA
def columna_vista(y0, y1):
    rect(250, y0, 650, y1, fill="#eceeef", **VIEW)
def mensula_con_corte(ytop, yb):
    """ménsula en vista + corte parcial (rotura) que muestra el bulón y su anclaje"""
    rect(250, ytop - 400, 650, ytop, fill="#e3e6e8", **VIEW)
    # rotura (zona cortada) alrededor del bulón
    z = [(372, ytop - 380), (392, ytop - 355), (378, ytop - 320), (395, ytop - 280), (380, ytop - 240), (396, ytop - 200),
         (380, ytop - 160), (394, ytop - 120), (378, ytop - 80), (392, ytop - 40), (380, ytop)]
    zr = [(900 - x, y) for x, y in z][::-1]
    poly(z + zr, fill="url(#pHA)", stroke="#000", sw=0.25)
    rect(440, ytop - 330, 460, ytop + 2, fill=STEEL, stroke="#000", sw=0.18)                 # bulón Ø20 anclado
    rect(420, ytop - 345, 480, ytop - 330, fill=STEEL, stroke="#000", sw=0.18)               # placa de anclaje
    for k in range(int((330) / 12)):
        line(440, ytop - 320 + k * 12, 460, ytop - 314 + k * 12, stroke="#999", sw=0.08)
    # armadura de la ménsula (en la rotura)
    pline([(395, ytop - 30), (505, ytop - 30)], stroke=REB, sw=0.35)
    circ(410, ytop - 45, 6, fill=REB, stroke=REB); circ(490, ytop - 45, 6, fill=REB, stroke=REB)
def viga_L(yb, rail=False, bulon=False, estribos_sal=True):
    yt = yb + 700; c = 15
    poly([(250 + c, yb), (750 - c, yb), (750, yb + c), (750, yb + 330), (550, yb + 330), (550, yt), (250, yt), (250, yb + c)], fill="url(#pHA)", **CUT)
    # armadura: estribos + barras + cordones
    pline(rrect(280, yb + 30, 520, yt - 30, 18) + [rrect(280, yb + 30, 520, yt - 30, 18)[0]], stroke=REB, sw=0.3)
    pline([(520, yb + 30), (705, yb + 30), (720, yb + 45), (720, yb + 285), (705, yb + 300), (520, yb + 300)], stroke=REB, sw=0.3)
    for x in (310, 400, 490, 610, 690): circ(x, yb + 62, 6.35)
    for x in (310, 490): circ(x, yb + 128, 6.35)
    for x in (300, 400, 500): circ(x, yt - 50, 6, fill=REB, stroke=REB)
    for y in (yb + 250, yb + 400): circ(292, y, 5, fill=REB, stroke=REB); circ(508, y, 5, fill=REB, stroke=REB)
    if estribos_sal:
        pline([(470, yt - 160), (470, yt - 25), (1400, yt - 25)], stroke=REB, sw=0.4)
    if rail:   # riel tipo Halfen embutido (en vista, en el eje del montante)
        P = [(270, yt), (270, yt - 46), (330, yt - 46), (330, yt), (318, yt), (318, yt - 6), (325, yt - 6), (325, yt - 41), (275, yt - 41), (275, yt - 6), (282, yt - 6), (282, yt)]
        poly(P, fill="none", stroke="#333", sw=0.2, dash=True)
        for xx in (285, 315): line(xx, yt - 46, xx, yt - 130, stroke="#333", sw=0.2, dash=True)
    if bulon:  # bulón ménsula-viga y vaina dentro de la viga (oculto) + cajeado superior
        rect(425, yb, 475, yt - 80, fill="none", stroke="#333", sw=0.2, dash=True)          # vaina corrugada Ø50
        rect(440, yb - 2, 460, yt - 40, fill="none", stroke="#333", sw=0.2, dash=True)      # bulón
        rect(390, yt - 80, 510, yt, fill="none", stroke="#333", sw=0.2, dash=True)          # cajeado con grout
        rect(410, yt - 46, 490, yt - 40, fill="none", stroke="#333", sw=0.2, dash=True)     # arandela
        rect(430, yt - 40, 470, yt - 22, fill="none", stroke="#333", sw=0.2, dash=True)     # tuerca
    rect(250, yb - 10, 650, yb, fill=NEO, stroke="none", sw=0)                               # neopreno ménsula/viga
def losa(yb, xe=1600):
    yt = yb + 300
    rect(590, yb - 10, 740, yb, fill=NEO, stroke="none", sw=0)
    poly([(570, yb), (xe, yb), (xe, yb + 45), (870, yb + 45), (870, yt - 45), (xe, yt - 45), (xe, yt), (570, yt)], fill="url(#pHA)", **CUT)
    rect(870, yb + 45, xe, yt - 45, fill="#f7f8f9", stroke="none", sw=0)
    line(870, yb + 45, xe, yb + 45, sw=0.3); line(870, yt - 45, xe, yt - 45, sw=0.3)
    rect(570, yb + 45, 870, yt - 45, fill="url(#pH)", stroke="#000", sw=0.25)                 # tapón de H°
    pline([(600, yb + 26), (xe, yb + 26)], stroke=REB, sw=0.3, dash=True)                     # cordón (nervio, en vista)
    # junta viga-losa + capa de compresión
    poly([(550, yb - 10), (570, yb - 10), (570, yt), (xe, yt), (xe, yt + 60), (550, yt + 60)], fill="url(#pHAis)", **CUT)
    circ(560, yb + 150, 5, fill=REB, stroke=REB)                                              # barra en junta
    pline([(580, yt + 30), (xe, yt + 30)], stroke=REB, sw=0.25)
    for x in range(650, int(xe), 150): circ(x, yt + 30, 3, fill=REB, stroke=REB)
def piso(y):     # carpeta + adhesivo + porcelanato sobre capa de compresión (y = sup. estructural)
    rect(250, y, 1600, y + 25, fill="url(#pMort)", **CUTT)
    rect(260, y + 25, 1600, y + 30, fill="#8d8d8d", stroke="none", sw=0)
    rect(260, y + 30, 1600, y + 40, fill="url(#pPorc)", **CUTT)
    for x in (860, 1460): line(x, y + 30, x, y + 40, sw=0.2)
def cielorraso(y, x0=200):
    rect(x0, y, 1600, y + 12.5, fill="#f2f2f2", **CUTT)
    for x in range(500, 1600, 400):     # perfiles omega
        pline([(x - 10, y + 12.5), (x, y + 12.5), (x + 5, y + 47), (x + 30, y + 47), (x + 35, y + 12.5), (x + 45, y + 12.5)], stroke="#333", sw=0.25)
    pline([(x0, y + 60), (x0, y + 12.5), (x0 + 40, y + 12.5)], stroke="#000", sw=0.35)
    for x in (1100,):
        rect(x, y + 47, x + 35, y + 590, fill=ALU2, stroke="#444", sw=0.15)
def topes_vela(y):
    pass

# ================================================================== MURO CORTINA (perfiles detallados)
def dvh(y0, y1, edge_lo=True, edge_hi=True):
    rect(0, y0, 6, y1, fill=GLASS, **CUTT)
    rect(18, y0, 21, y1, fill=GLASS, **CUTT); rect(21, y0, 21.76, y1, fill="#e8f3f7", stroke="none", sw=0)
    rect(21.76, y0, 24.76, y1, fill=GLASS, **CUTT)
    for e, s in ((y0, 1), (y1, -1)):
        if (s == 1 and not edge_lo) or (s == -1 and not edge_hi): continue
        a, b = sorted((e, e + s * 5)); rect(6, a, 18, b, fill=SIL, stroke="none", sw=0)                       # silicona estructural
        a, b = sorted((e + s * 5, e + s * 14)); rect(6.6, a, 17.4, b, fill=ALU, stroke="#000", sw=0.12)       # separador
        rect(8.5, a + 1.5, 15.5, b - 1.5, fill="#e9e2c3", stroke="none", sw=0)                                 # desecante
        rect(6, a, 6.6, b, fill=NEO, stroke="none", sw=0); rect(17.4, a, 18, b, fill=NEO, stroke="none", sw=0)  # butilo
def burlete(x0, x1, y0, y1, ext=True):
    # burlete EPDM con aletas
    poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill=EPDM, stroke="none", sw=0)
    for k in range(3):
        yy = y0 + (k + 0.5) * (y1 - y0) / 3
        line(x1 if ext else x0, yy, x1 + (1.5 if ext else -1.5), yy + 1, stroke=EPDM, sw=0.25)
def travesano(a, below=True, above=True):
    """travesaño 50x120 en corte + adaptador + poliamida + presor + tapa + burletes + calzo"""
    poly([(32, a), (150, a), (150, a + 60), (32, a + 60)], fill=ALU, stroke="#000", sw=0.25)
    rect(34.5, a + 2.5, 89.5, a + 57.5, fill="#fff", stroke="#000", sw=0.12)
    rect(92, a + 2.5, 147.5, a + 57.5, fill="#fff", stroke="#000", sw=0.12)
    poly([(12, a + 22), (32, a + 22), (32, a + 38), (12, a + 38)], fill=ALU, stroke="#000", sw=0.18)   # nariz
    circ(22, a + 30, 3.2, fill="#fff", stroke="#000", sw=0.1)                                            # canal tornillo
    rect(8, a + 20, 12, a + 40, fill=PA, stroke="#000", sw=0.1)                                          # poliamida
    lo = a - 22 if below else a; hi = a + 82 if above else a + 60
    rect(-16, lo, -4, hi, fill=ALU, stroke="#000", sw=0.18)                                              # presor
    poly([(-16, lo - 2), (-32, lo + 3), (-32, hi - 3), (-16, hi + 2), (-16, hi - 1), (-29, hi - 5), (-29, lo + 5), (-16, lo + 1)], fill=ALU2, stroke="#000", sw=0.18)  # tapa
    line(-14, a + 30, 28, a + 30, stroke="#000", sw=0.35)                                                # tornillo inox
    poly(hexa(-17.5, a + 30, 4.5), fill=INOX, stroke="#000", sw=0.1)
    if below:
        burlete(-4, 0, a - 20, a - 6, ext=True); burlete(25, 32, a - 20, a - 6, ext=False)
    if above:
        burlete(-4, 0, a + 66, a + 80, ext=True); burlete(25, 32, a + 66, a + 80, ext=False)
        rect(4, a + 58, 32, a + 62, fill=ALU, stroke="#000", sw=0.12)                                    # apoyo de vidrio
        rect(3, a + 62, 23, a + 70, fill="#333", stroke="#000", sw=0.1)                                  # calzo EPDM
    rect(-16, (a - 12) if below else a + 8, -12, (a - 4) if below else a + 14, fill="#fff", stroke="none", sw=0)  # ranura de drenaje
def montante_vista(y0, y1):
    rect(32, y0, 182, y1, fill="#e3e7ea", **VIEW)
    line(91, y0, 91, y1, stroke="#888", sw=0.1, dash=True)
    rect(-32, y0, -16, y1, fill="#e9ecee", stroke="#777", sw=0.12)

def grapa_doble(ytop, rail_x=300):
    """grapa en vista: ala vertical frente al montante (vista de frente) + ala horizontal s/ viga"""
    poly([(120, ytop - 170), (200, ytop - 170), (200, ytop), (120, ytop)], fill=GALV, stroke="#000", sw=0.2)
    poly(oblong(145, ytop - 70, 40, 14), fill="#fff", stroke="#000", sw=0.15)                         # coliso vertical-horizontal
    poly(hexa(145, ytop - 70, 10), fill=INOX, stroke="#000", sw=0.15); circ(145, ytop - 70, 6, fill="none", stroke="#000", sw=0.1)
    rect(190, ytop, 380, ytop + 10, fill=GALV, stroke="#000", sw=0.2)                                   # ala horizontal (de canto)
    rect(rail_x - 6, ytop - 40, rail_x + 6, ytop + 26, fill=INOX, stroke="#000", sw=0.15)              # bulón cabeza martillo
    rect(rail_x - 14, ytop - 42, rail_x + 14, ytop - 34, fill=INOX, stroke="#000", sw=0.12)            # cabeza martillo
    rect(rail_x - 16, ytop + 10, rail_x + 16, ytop + 13, fill=INOX, stroke="#000", sw=0.12)            # arandela
    rect(rail_x - 10, ytop + 13, rail_x + 10, ytop + 26, fill=INOX, stroke="#000", sw=0.12)            # tuerca
    rect(115, ytop - 172, 120, ytop + 2, fill=NEO, stroke="none", sw=0)                                 # separador aislante

# ================================================================== CONJUNTO (mismas cotas que Lámina 1)
# columna + ménsulas
columna_vista(3000, 3350); mensula_con_corte(3750, 3760)
columna_vista(4500, 7850); rect(250, 7850, 650, 8250, fill="#e3e6e8", **VIEW)
viga_L(3760, rail=True, bulon=True); losa(4100); piso(4460)
viga_L(8260, rail=False, bulon=True); losa(8600)
cielorraso(3500); cielorraso(8100)
# muro cortina
montante_vista(3000, 4700); montante_vista(4720, 8400)
rect(32, 4700, 182, 4720, fill="#fff", stroke="#555", sw=0.15)
rect(38, 4620, 176, 4800, fill="none", stroke="#555", sw=0.15, dash=True)              # manguito
dvh(3000, 3490, edge_lo=False)
travesano(3500)
rect(0, 3570, 6, 4550, fill="#6f8796", **CUTT)                                            # spandrel esmaltado
rect(40, 3570, 90, 4550, fill="url(#pLanaV)", **CUTT)
rect(90, 3570, 92, 4550, fill=STEEL, stroke="none", sw=0)
pline([(92, 4550), (92, 4556), (150, 4556)], stroke=STEEL, sw=0.3)
travesano(4560)
dvh(4630, 8330)
travesano(8340, above=False)
rect(-32, 8402, 30, 8420, fill="#262626", stroke="none", sw=0)                           # sellador
circ(0, 8411, 8, fill="#fff", stroke="#000", sw=0.15)                                    # fondo de junta
# barrera cortafuego + cubrejunta
pline([(93, 4342), (248, 4342), (248, 4280)], stroke=GALV, sw=0.5)
line(248, 4300, 300, 4300, stroke="#000", sw=0.3)                                         # tornillo/taco
grapa_doble(4460)
rect(93, 4344, 250, 4455, fill="url(#pLana)", **CUTT)
rect(93, 4455, 250, 4462, fill="#c0392b", stroke="none", sw=0)
pline([(182, 4503), (182, 4500), (330, 4500), (330, 4503)], stroke="#000", sw=0.35)
# grapa superior (cara de viga de cubierta)
poly([(120, 8270), (200, 8270), (200, 8390), (120, 8390)], fill=GALV, stroke="#000", sw=0.2)
poly(oblong(150, 8330, 36, 14), fill="#fff", stroke="#000", sw=0.15); poly(hexa(150, 8330, 10), fill=INOX, stroke="#000", sw=0.15)
rect(240, 8270, 250, 8390, fill=GALV, stroke="#000", sw=0.2); rect(200, 8270, 240, 8280, fill=GALV, stroke="#000", sw=0.2)
rect(250, 8324, 360, 8336, fill="none", stroke="#333", sw=0.2, dash=True)                 # anclaje químico M12
rect(232, 8320, 240, 8340, fill=INOX, stroke="#000", sw=0.12)
# panel sándwich (cenefa) + cámara + uniones
poly([(-40, 8420), (20, 8420), (20, 8900), (-40, 8900)], fill="url(#pHA)", **CUT)
rect(20, 8460, 70, 8900, fill="url(#pEPSv)", **CUTT)
poly([(20, 8420), (110, 8420), (110, 8900), (70, 8900), (70, 8460), (20, 8460)], fill="url(#pHA)", **CUT)
rect(-30, 8420, -16, 8434, fill="#fff", stroke="#000", sw=0.2)                            # goterón
pline([(-25, 8470), (-25, 8900)], stroke=REB, sw=0.25, dash=True); pline([(95, 8470), (95, 8900)], stroke=REB, sw=0.25, dash=True)
for y in (8560, 8760): line(5, y, 85, y + 60, stroke=REB, sw=0.35)                         # conectores inox
rect(110, 8460, 160, 8890, fill="url(#pLanaV)", **CUTT)
rect(110, 8406, 250, 8414, fill=STEEL, stroke="none", sw=0)
poly([(115, 8520), (250, 8520), (250, 8530), (127, 8530), (127, 8600), (115, 8600)], fill=GALV, stroke="#000", sw=0.15)
rect(60, 8560, 140, 8572, fill="none", stroke="#333", sw=0.2, dash=True)                   # inserto roscado

# ================================================================== VENTANAS DE DETALLE
DET = [
    dict(id="D1", win=(185, 3300, 900, 4540), sc=5, t="DETALLE 1 · UNIÓN COLUMNA – VIGA (ENTREPISO)",
         st="Corte integral, zona de entrepiso: viga “L” cortada; columna y ménsula en vista con rotura parcial en el bulón"),
    dict(id="D3", win=(-60, 4280, 640, 4690), sc=5, t="DETALLE 3 · UNIÓN VIDRIO – VIGA DE ENTREPISO",
         st="Corte integral, borde de losa: grapa del montante, spandrel, barrera cortafuego"),
    dict(id="D2", win=(-70, 8080, 330, 8640), sc=5, t="DETALLE 2 · UNIÓN VIDRIO – MURO (PANEL)",
         st="Corte integral, remate superior: muro cortina contra panel premoldeado"),
]

REFS = {
"D1": [
 (1, "Columna premoldeada H°A° 40x40 H-30 (en vista).", (300, 3320)),
 (2, "Ménsula corta (en vista) c/ rotura parcial.", (300, 3450)),
 (3, "Bulón Ø20 anclado en la ménsula c/ placa de anclaje.", (450, 3600)),
 (4, "Armadura de la ménsula (Ø12 + estribos).", (410, 3705)),
 (5, "Apoyo de neopreno 10 mm ménsula / viga.", (330, 3755)),
 (6, "Viga “L” pretensada 30/70 c/ talón 20x33 (corte).", (360, 4200)),
 (7, "Cordones de pretensado Ø12,7.", (690, 3822)),
 (8, "Estribos Ø8 c/15 y barras Ø12 / Ø10 de piel.", (520, 4000)),
 (9, "Vaina corrugada Ø50 + bulón (oculto) llenado c/ grout.", (450, 4050)),
 (10, "Cajeado sup.: arandela + tuerca, llenado c/ grout.", (450, 4440)),
 (11, "Neopreno continuo losa / talón 10 mm.", (700, 4095)),
 (12, "Losa alveolar pretensada e = 30 cm (corte por alvéolo).", (900, 4250)),
 (13, "Tapón de H° en alvéolos (30 cm).", (720, 4300)),
 (14, "Junta viga–losa c/ H° in situ + barra Ø10.", (560, 4180)),
 (15, "Capa de compresión H°A° 6 cm c/ malla Q188.", (850, 4430)),
 (16, "Estribos salientes de la viga (vinculación).", (470, 4380)),
 (17, "Carpeta 2,5 cm + adhesivo + porcelanato.", (650, 4495)),
 (18, "Riel de anclaje tipo Halfen embutido (en vista).", (300, 4440)),
 (19, "Cielorraso placa de roca de yeso 12,5 s/ omegas.", (820, 3506)),
],
"D3": [
 (1, "Viga “L” pretensada (borde de losa).", (420, 4300)),
 (2, "Riel Halfen embutido + pernos de anclaje (vista).", (290, 4440)),
 (3, "Bulón cabeza martillo M12 + arandela + tuerca.", (300, 4476)),
 (4, "Grapa acero galv. regulable 3D (ala horizontal).", (360, 4465)),
 (5, "Ala vertical frente al montante c/ coliso.", (175, 4320)),
 (6, "Bulón M12 inox pasante por el montante.", (145, 4390)),
 (7, "Separador aislante de neopreno (par galvánico).", (117, 4300)),
 (8, "Montante 50x150 (en vista).", (60, 4600)),
 (9, "Manguito interior de empalme (junta de dilatación 20 mm sobre +4,70).", (60, 4660)),
 (10, "Travesaño 50x120: cámaras, nariz y poliamida.", (60, 4590)),
 (11, "Presor + tornillo inox + tapa clipada.", (-24, 4590)),
 (12, "Burletes EPDM exterior / interior.", (-2, 4648)),
 (13, "Calzo EPDM s/ apoyo de vidrio.", (13, 4626)),
 (14, "DVH 6 + 12 + 3+3 laminado PVB.", (12, 4670)),
 (15, "Spandrel: vidrio templado 6 mm esmaltado.", (3, 4400)),
 (16, "Lana mineral 50 + bandeja chapa galv.", (65, 4380)),
 (17, "Barrera cortafuego: lana mineral 100 kg/m³.", (220, 4400)),
 (18, "Sellador intumescente.", (230, 4459)),
 (19, "Ángulo soporte chapa galv. atornillado a viga.", (248, 4300)),
 (20, "Cubrejunta aluminio.", (300, 4501)),
 (21, "Capa de compresión + carpeta + porcelanato.", (600, 4480)),
],
"D2": [
 (1, "Panel sándwich premoldeado: H°A° 6 + EPS 5 + H°A° 4.", (-10, 8540)),
 (2, "Conectores inox entre capas.", (45, 8590)),
 (3, "Goterón (buña 14x14).", (-23, 8427)),
 (4, "Sellador silicona neutra + fondo de junta.", (0, 8411)),
 (5, "Travesaño superior + presor + tapa.", (90, 8370)),
 (6, "DVH 6 + 12 + 3+3 laminado.", (12, 8250)),
 (7, "Montante 50x150 (en vista).", (60, 8220)),
 (8, "Grapa superior c/ coliso + bulón M12.", (150, 8330)),
 (9, "Anclaje químico M12 a la viga.", (300, 8330)),
 (10, "Chapa galv. de cierre de cámara.", (180, 8410)),
 (11, "Lana mineral 50 mm en cámara.", (135, 8600)),
 (12, "Perfil L de restricción del panel.", (200, 8525)),
 (13, "Inserto roscado embutido en el panel.", (100, 8566)),
 (14, "Viga “L” de cubierta (corte).", (300, 8500)),
 (15, "Cielorraso placa de roca de yeso.", (300, 8106)),
],
}

# ================================================================== SVG
PAT = '''
<pattern id="pHA" patternUnits="userSpaceOnUse" width="1.3" height="1.3" patternTransform="rotate(45)"><rect width="1.3" height="1.3" fill="#d3d6d9"/><line x1="0" y1="0" x2="0" y2="1.3" stroke="#4a4f55" stroke-width="0.09"/></pattern>
<pattern id="pHAis" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)"><rect width="2.2" height="2.2" fill="#dedad2"/><line x1="0" y1="0" x2="0" y2="2.2" stroke="#4a4f55" stroke-width="0.09"/><circle cx="1.1" cy="0.55" r="0.13" fill="#4a4f55"/><circle cx="1.4" cy="1.6" r="0.09" fill="#4a4f55"/></pattern>
<pattern id="pH" patternUnits="userSpaceOnUse" width="3" height="3"><rect width="3" height="3" fill="#e6e4df"/><circle cx="0.6" cy="0.7" r="0.16" fill="#666"/><circle cx="2.1" cy="1.9" r="0.12" fill="#666"/><path d="M1.7 0.4 l0.35 0.55 h-0.7z" fill="none" stroke="#666" stroke-width="0.07"/><path d="M0.5 2.2 l0.3 0.45 h-0.6z" fill="none" stroke="#666" stroke-width="0.07"/></pattern>
<pattern id="pMort" patternUnits="userSpaceOnUse" width="1.2" height="1.2"><rect width="1.2" height="1.2" fill="#e9e9e9"/><circle cx="0.3" cy="0.3" r="0.08" fill="#777"/><circle cx="0.9" cy="0.85" r="0.06" fill="#777"/></pattern>
<pattern id="pEPSv" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(90)"><rect width="1.6" height="1.6" fill="#fff5bf"/><path d="M0 0.8 L0.4 0.3 L0.8 0.8 L1.2 1.3 L1.6 0.8" fill="none" stroke="#a08a1a" stroke-width="0.09"/></pattern>
<pattern id="pLana" patternUnits="userSpaceOnUse" width="2" height="1.2"><rect width="2" height="1.2" fill="#fbe2a8"/><path d="M0 0.6 C0.5 0 0.5 0 1 0.6 S1.5 1.2 2 0.6" fill="none" stroke="#b07b18" stroke-width="0.09"/></pattern>
<pattern id="pLanaV" patternUnits="userSpaceOnUse" width="2" height="1.2" patternTransform="rotate(90)"><rect width="2" height="1.2" fill="#fbe2a8"/><path d="M0 0.6 C0.5 0 0.5 0 1 0.6 S1.5 1.2 2 0.6" fill="none" stroke="#b07b18" stroke-width="0.09"/></pattern>
<pattern id="pPorc" patternUnits="userSpaceOnUse" width="4" height="4"><rect width="4" height="4" fill="#cdbb9c"/></pattern>
<marker id="arr" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4 z" fill="#000"/></marker>
'''
f = lambda v: f"{v:.3f}"

class View:
    def __init__(s, det, ox, oy):
        s.d = det; s.x0, s.y0, s.x1, s.y1 = det["win"]; s.S = det["sc"]; s.ox, s.oy = ox, oy
        s.w = (s.x1 - s.x0) / s.S; s.h = (s.y1 - s.y0) / s.S
    def X(s, x): return s.ox + (x - s.x0) / s.S
    def Y(s, y): return s.oy + (s.y1 - y) / s.S
    def svg(s):
        o = [f'<clipPath id="c{s.d["id"]}"><rect x="{f(s.ox)}" y="{f(s.oy)}" width="{f(s.w)}" height="{f(s.h)}"/></clipPath>', f'<g clip-path="url(#c{s.d["id"]})">']
        k = 20 / s.S       # grosor: escala los anchos pensados para 1:20... ajustado a 1:5
        for e in E:
            dash = ' stroke-dasharray="1.6 0.8"' if e.get("dash") else ""
            if e["t"] == "poly":
                pts = " ".join(f"{f(s.X(x))},{f(s.Y(y))}" for x, y in e["pts"])
                o.append(f'<polygon points="{pts}" fill="{e["fill"]}" stroke="{e["stroke"]}" stroke-width="{e["sw"]}" stroke-linejoin="round"{dash}/>')
            elif e["t"] == "pline":
                pts = " ".join(f"{f(s.X(x))},{f(s.Y(y))}" for x, y in e["pts"])
                o.append(f'<polyline points="{pts}" fill="none" stroke="{e["stroke"]}" stroke-width="{e["sw"]}" stroke-linejoin="round" stroke-linecap="round"{dash}/>')
            elif e["t"] == "circ":
                o.append(f'<circle cx="{f(s.X(e["c"][0]))}" cy="{f(s.Y(e["c"][1]))}" r="{f(e["r"] / s.S)}" fill="{e["fill"]}" stroke="{e["stroke"]}" stroke-width="{e["sw"]}"{dash}/>')
        o.append("</g>")
        o.append(f'<rect x="{f(s.ox)}" y="{f(s.oy)}" width="{f(s.w)}" height="{f(s.h)}" fill="none" stroke="#000" stroke-width="0.2" stroke-dasharray="3 1"/>')
        return "\n".join(o)

ann = []
def T(x, y, s, size=2.0, anchor="start", weight="normal", fill="#000", ital=False, rot=None):
    r = f' transform="rotate({rot},{f(x)},{f(y)})"' if rot is not None else ""
    ann.append(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{" font-style=\"italic\"" if ital else ""}{r}>{s}</text>')
def L(pts, sw=0.15, st="#c0392b", extra=""):
    ann.append(f'<polyline points="{" ".join(f"{f(a)},{f(b)}" for a, b in pts)}" fill="none" stroke="{st}" stroke-width="{sw}" {extra}/>')

def balloons(v, refs, bx_left, bx_right):
    pts = []
    for n, txt, (x, y) in refs:
        pts.append(dict(n=n, ax=v.X(x), ay=v.Y(y)))
    xm = v.ox + v.w / 2
    for side in (True, False):
        Ls = sorted([p for p in pts if (p["ax"] < xm) == side], key=lambda p: p["ay"])
        gap, ymin, ymax = 5.0, v.oy + 3, v.oy + v.h - 3
        for k, p in enumerate(Ls): p["by"] = max(p["ay"], Ls[k - 1]["by"] + gap if k else ymin)
        for k in range(len(Ls) - 1, -1, -1):
            lim = ymax if k == len(Ls) - 1 else Ls[k + 1]["by"] - gap
            if Ls[k]["by"] > lim: Ls[k]["by"] = lim
        bx = bx_left if side else bx_right
        for p in Ls:
            ex = bx + 2 if side else bx - 2
            L([(p["ax"], p["ay"]), (ex + (3 if side else -3), p["by"]), (ex, p["by"])])
            ann.append(f'<circle cx="{f(p["ax"])}" cy="{f(p["ay"])}" r="0.45" fill="#c0392b"/>')
            ann.append(f'<circle cx="{f(bx)}" cy="{f(p["by"])}" r="1.95" fill="#fff" stroke="#c0392b" stroke-width="0.22"/>')
            T(bx, p["by"] + 0.72, p["n"], 2.0, "middle", "bold", "#c0392b")

def reflist(refs, x, y, width_chars, size=1.75, lh=2.25):
    for n, txt, _ in refs:
        words, lines, cur = txt.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > width_chars: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
        T(x + 1.6, y, n, size, "middle", "bold", "#c0392b")
        for ln in lines: T(x + 3.6, y, ln, size); y += lh
        y += 0.2
    return y

def header(x, y, w, t, st):
    ann.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="5" fill="#2f3b45"/>')
    T(x + 1.5, y + 3.6, t, 2.7, weight="bold", fill="#fff")
    T(x + w - 1.5, y + 3.6, "CORTE · ESC. 1:5", 2.0, "end", "bold", "#fff")
    T(x, y + 7.6, st, 1.75, ital=True, fill="#333")

def cota_h(v, x0, x1, yr, txt, off=0):
    py = v.Y(yr) + off; a, b = v.X(x0), v.X(x1)
    ann.append(f'<line x1="{f(a)}" y1="{f(py)}" x2="{f(b)}" y2="{f(py)}" stroke="#000" stroke-width="0.12"/>')
    for p in (a, b): ann.append(f'<line x1="{f(p-0.8)}" y1="{f(py+0.8)}" x2="{f(p+0.8)}" y2="{f(py-0.8)}" stroke="#000" stroke-width="0.25"/>')
    T((a + b) / 2, py - 0.6, txt, 1.6, "middle")
def cota_v(v, y0, y1, xr, txt, off=0):
    px = v.X(xr) + off; a, b = v.Y(y0), v.Y(y1)
    ann.append(f'<line x1="{f(px)}" y1="{f(a)}" x2="{f(px)}" y2="{f(b)}" stroke="#000" stroke-width="0.12"/>')
    for p in (a, b): ann.append(f'<line x1="{f(px-0.8)}" y1="{f(p+0.8)}" x2="{f(px+0.8)}" y2="{f(p-0.8)}" stroke="#000" stroke-width="0.25"/>')
    T(px - 0.7, (a + b) / 2, txt, 1.6, "middle", rot=-90)
def nivel(v, y, xr, txt):
    px, py = v.X(xr), v.Y(y)
    ann.append(f'<path d="M{f(px)},{f(py)} l-1.2,-2 h2.4 z" fill="#000"/>')
    ann.append(f'<line x1="{f(px-3.5)}" y1="{f(py)}" x2="{f(px+3.5)}" y2="{f(py)}" stroke="#000" stroke-width="0.15"/>')
    T(px + 1.8, py - 2.3, txt, 1.8, weight="bold")

# --------------------------------------------- layout A3 apaisada
views = {}
v1 = View(DET[0], 18, 24); views["D1"] = v1                       # 143 x 251
v3 = View(DET[1], 264, 24); views["D3"] = v3                      # 140 x 91
v2 = View(DET[2], 264, 158); views["D2"] = v2                     # 80 x 94
header(10, 12.5, 238, DET[0]["t"], DET[0]["st"])
header(256, 12.5, 158, DET[1]["t"], DET[1]["st"])
header(256, 146.5, 158, DET[2]["t"], DET[2]["st"])
balloons(v1, REFS["D1"], 13, v1.ox + v1.w + 5)
balloons(v3, REFS["D3"], 259, v3.ox + v3.w + 5)
balloons(v2, REFS["D2"], 259, v2.ox + v2.w + 5)
reflist(REFS["D1"], 172, 30, 40)
yy = reflist(REFS["D3"][:11], 258, 112, 46, 1.6, 2.0); reflist(REFS["D3"][11:], 337, 112, 46, 1.6, 2.0)
reflist(REFS["D2"], 356, 164, 33, 1.6, 2.05)
# cotas y niveles
cota_h(v1, 250, 550, 3330, "30", 0); cota_h(v1, 550, 750, 3330, "20", 0); cota_h(v1, 250, 650, 3330, "40", 4)
cota_v(v1, 3760, 4460, 880, "70"); cota_v(v1, 4100, 4400, 840, "30"); cota_v(v1, 3350, 3750, 225, "40")
nivel(v1, 4500, 720, "+4,50 NPT"); nivel(v1, 3500, 950, "+3,50 cielorraso")
cota_h(v3, -32, 182, 4295, "21,4", 0); cota_h(v3, 182, 250, 4295, "6,8", 0); cota_v(v3, 4560, 4620, 600 - 380, "6")
nivel(v3, 4500, 470, "+4,50")
cota_h(v2, -40, 110, 8650 - 30, "15", 0); cota_v(v2, 8402, 8420, 40, "2")
#T(v1.ox, v1.oy + v1.h + 4, "Columna, ménsula y riel en vista (plano de corte a ½ luz de viga, idem Lámina 1). Rotura parcial en la ménsula para mostrar el bulón.", 1.6, ital=True, fill="#444")

# rótulo
ry = 297 - 23
title = f'''<rect x="7" y="{ry}" width="409" height="17" fill="none" stroke="#000" stroke-width="0.3"/>'''
T(10, ry + 6.5, "LÁMINA 3 · DETALLES DE UNIONES EN CORTE (del corte integral)", 4, weight="bold")
T(10, ry + 11.5, "Sistema de hormigón premoldeado de grandes luces · Cerramiento vidriado – muro cortina (sistema stick, módulo 1,25 m)", 2.3)
T(10, ry + 15, "Ventanas ampliadas del mismo corte integral de la Lámina 1 (mismo plano y cotas), a escala 1:5. Cotas en cm salvo indicación.", 1.8, ital=True, fill="#333")
cx = 238
for k, v in [("MATERIA", "Construcciones II"), ("CÁTEDRA", "Arq. ____________"), ("ALUMNO/A", "__________________"), ("GRUPO", "____"), ("HOJA", "3 de 3 · A3 · 2026")]:
    w = 46 if k == "ALUMNO/A" else 18 if k == "GRUPO" else 36
    title += f'<line x1="{cx}" y1="{ry}" x2="{cx}" y2="{ry+17}" stroke="#000" stroke-width="0.2"/>'
    T(cx + 1.5, ry + 5, k, 1.7, weight="bold"); T(cx + 1.5, ry + 11, v, 2.1); cx += w
# escala gráfica 1:5
sx, sy = 172, 262
for i in range(5):
    ann.append(f'<rect x="{sx + i*4}" y="{sy-1}" width="4" height="1" fill="{"#000" if i%2==0 else "#fff"}" stroke="#000" stroke-width="0.1"/>')
T(sx, sy - 1.6, "0", 1.3, "middle"); T(sx + 20, sy - 1.6, "10 cm", 1.3, "middle"); T(sx + 24, sy, "ESC. 1:5", 1.7, weight="bold")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" font-family="Liberation Sans, Arial, sans-serif">
<defs>{PAT}</defs><rect width="420" height="297" fill="#fff"/>
<rect x="3" y="3" width="414" height="291" fill="none" stroke="#000" stroke-width="0.5"/>
{v1.svg()}{v3.svg()}{v2.svg()}
{title}{"".join(ann)}</svg>'''
os.makedirs("build", exist_ok=True)
open("build/lamina3.html", "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:420mm 297mm;margin:0}}html,body{{margin:0}}svg{{display:block}}</style></head><body>{svg}<script>window.READY=true</script></body></html>')
json.dump(dict(E=E, DET=DET, REFS={k: [[n, t, list(p)] for n, t, p in v] for k, v in REFS.items()}), open("build/lamina3_dx.json", "w"), ensure_ascii=False)
print("ok")
