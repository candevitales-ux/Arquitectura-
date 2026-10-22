# -*- coding: utf-8 -*-
"""CORTE INTEGRAL - ESTRUCTURA DE ACERO (perfiles laminados) c/ losa colaborante (steel deck).
VARIANTE = "opaco" (panel sándwich metálico PIR 100 s/ correas C) o "vidriado" (muro cortina stick de aluminio).
Se define VARIANTE en el namespace antes de ejecutar (por defecto "opaco").
Geometría en mm reales; x+ hacia el interior, y+ hacia arriba, ±0,00 = NPT planta baja. Escala de dibujo 1:20.

Sistema (corregido respecto del corte de referencia):
 - Columnas HEB 240 (no IPN: el IPN tiene alas angostas y poca inercia en el eje débil), alas paralelas a la fachada.
 - Vigas principales IPE 400 perpendiculares a la fachada c/ 2,50 m (en vista), unidas al ala de la columna c/ placa extrema
   20 mm + 6 bulones M20 calidad 8.8.  Viga de borde IPE 300 a lo largo de la fachada (cortada), unida al alma de la
   columna c/ doble ángulo L 90x90x9 + bulones M16 8.8.
 - Losa colaborante: chapa trapezoidal galv. h 75 mm e 0,9 mm + H-25, espesor total 13 cm, malla Q188, conectores de corte
   (pernos Nelson Ø19 h 100) soldados a través de la chapa a las vigas, frentín (pour stop) de chapa plegada en el borde.
 - Base: placa base 450x450x25 c/ cartelas, 4 pernos de anclaje Ø24 c/ tuerca niveladora, grout sin contracción 30 mm, sobre
   cuello (pedestal) 60x60 de H°A y zapata aislada 1,80x1,80x0,45; dado de H° de protección hasta el contrapiso.
 - Cerramiento opaco: panel sándwich (chapa prepintada 0,5 + PIR 100 + chapa 0,5) vertical, atornillado a correas C 160x60x20
   galv. c/ tensores Ø10 a media luz; correas a las columnas c/ ángulos de clip; parapeto c/ montantes UPN 160 c/ 1,25 m.
 - Protección: fondo antióxido + pintura intumescente F60 en columnas y vigas; barrera cortafuego en el borde de losa."""
import os

VARIANTE = globals().get("VARIANTE", "opaco")
_HERE = os.path.dirname(os.path.abspath(globals().get("__file__", "src/acero_corte.py")))
_SRC = open(os.path.join(_HERE, "tp_corte.py"), encoding="utf-8").read()
exec(compile(_SRC[:_SRC.index("# =====================================================================================\n#  GEOMETRÍA")], "tp_corte(base)", "exec"))
# patrones propios
defs.append('''
<pattern id="pPIR" patternUnits="userSpaceOnUse" width="2.4" height="2.4">
 <rect width="2.4" height="2.4" fill="#fbf0c2"/><path d="M0.6 0.3 l0.6 0 l0.3 0.5 l-0.3 0.5 l-0.6 0 l-0.3 -0.5z M1.8 1.5 l0.6 0 M0 1.5 l0.3 0" fill="none" stroke="#b39a2a" stroke-width="0.07"/></pattern>
<pattern id="pYeso" patternUnits="userSpaceOnUse" width="1" height="1"><rect width="1" height="1" fill="#f4f4f4"/><circle cx="0.5" cy="0.5" r="0.05" fill="#999"/></pattern>
<pattern id="pCem" patternUnits="userSpaceOnUse" width="1" height="1"><rect width="1" height="1" fill="#d9d4c7"/><circle cx="0.3" cy="0.6" r="0.07" fill="#777"/></pattern>
''')
REB = "#7a1f1f"
STC = "#4d545c"       # acero cortado
STV = "#dfe3e7"       # acero en vista
GALV = "#8f989f"      # chapa galvanizada
OP = VARIANTE == "opaco"
XR = 2700             # borde derecho del dibujo

# ------------------------------------------------------------------ perfiles
def I_cut(xc, ytop, h, b, tw, tf):
    poly([(xc - b / 2, ytop), (xc + b / 2, ytop), (xc + b / 2, ytop - tf), (xc + tw / 2, ytop - tf), (xc + tw / 2, ytop - h + tf),
          (xc + b / 2, ytop - h + tf), (xc + b / 2, ytop - h), (xc - b / 2, ytop - h), (xc - b / 2, ytop - h + tf), (xc - tw / 2, ytop - h + tf),
          (xc - tw / 2, ytop - tf), (xc - b / 2, ytop - tf)], fill=STC, stroke="#000", sw=0.22)
def I_vista(x0, x1, ytop, h, tf):
    rect(x0, ytop - h, x1, ytop, fill=STV, **VIEW)
    for yy in (ytop - tf, ytop - h + tf): line(x0, yy, x1, yy, stroke="#666", sw=0.08)
def columna(y0, y1):
    """HEB 240 en vista: alas (17 mm) vistas de canto, alma de frente"""
    rect(330, y0, 570, y1, fill=STV, **VIEW)
    for xx in (347, 553): line(xx, y0, xx, y1, stroke="#666", sw=0.08)
def correa(y0):
    """correa C 160x60x20x2,5 galv. (alma horizontal), ala exterior atornillada al panel"""
    pline([(120, y0 + 60), (100, y0 + 60), (100, y0), (260, y0), (260, y0 + 60), (240, y0 + 60)], stroke="#000", sw=0.35)
def clip(y0):
    """ángulo de clip L 100x100x8 (en vista) correa / ala de la columna + 2 bulones M12"""
    rect(260, y0 - 20, 330, y0 + 80, fill=STV, stroke="#333", sw=0.12)
    for yy in (y0 + 10, y0 + 50): line(250, yy, 345, yy, stroke="#000", sw=0.22)
def tornillo_panel(yy):
    line(-6, yy, 118, yy, stroke="#000", sw=0.22); rect(-9, yy - 9, -1, yy + 9, fill="#222", stroke="none", sw=0)

def losa(yt, x0=300):
    """losa colaborante: chapa trapezoidal h 75 + H-25, e total 130; frentín en x0; conector de corte s/ viga de borde"""
    yb = yt - 130
    prof = [(470, yb)]
    x = 470
    while x < XR:
        for dx, dy in ((110, 0), (140, 75), (270, 75), (300, 0)):
            prof.append((min(x + dx, XR), yb + dy))
        x += 300
    conc = [(x0 + 2, yt), (XR, yt)] + prof[::-1] + [(x0 + 2, yb + 2)]
    poly(conc, fill="url(#pHAis)", **CUT)
    pline(prof, stroke="#000", sw=0.32)                                                     # chapa colaborante
    for i in range(0, len(prof) - 1, 4):
        a, b = prof[i + 1], prof[i + 2]
        if a[0] < XR: circ((a[0] + b[0]) / 2, yb + 18, 0.24, fill=REB)                       # barra adicional en el valle
    pline([(x0 + 15, yt - 25), (XR, yt - 25)], stroke=REB, sw=0.12, extra='stroke-dasharray="2 0.5"')   # malla Q188
    for xx in range(x0 + 60, XR, 150): circ(xx, yt - 25, 0.17, fill=REB)
    # frentín (pour stop) chapa plegada 2 mm: ala vertical en x0 + ala horizontal soldada al ala sup. de la viga de borde
    pline([(x0, yt), (x0, yb), (465, yb)], stroke="#000", sw=0.4)
    # conector de corte Nelson Ø19 h 100 (cortado) s/ viga de borde
    rect(440, yb, 459, yb + 100, fill=STC, stroke="#000", sw=0.08); rect(434, yb + 92, 465, yb + 100, fill=STC, stroke="#000", sw=0.06)
    return yb

def entrepiso_estructura(yt):
    """yt = sup. de losa. Viga de borde IPE 300 cortada (eje 450), viga IPE 400 en vista c/ placa extrema, conector, losa"""
    yb = yt - 130
    I_vista(585, XR, yb, 400, 13.5)                                                         # IPE 400 (en vista)
    rect(570, yb - 420, 585, yb, fill=STV, stroke="#333", sw=0.14)                          # placa extrema 20 mm
    for yy in (yb - 60, yb - 200, yb - 340):
        for xx in (578,): circ(xx, yy, 0.55, fill="#333")
    for yy in (yb - 60, yb - 200, yb - 340): line(555, yy, 600, yy, stroke="#000", sw=0.25)  # bulones M20 (vista)
    rect(560, yb - 400, 570, yb, fill="none", stroke="#333", sw=0.1, extra=DASH)            # rigidizador del alma de la columna (oculto)
    I_cut(450, yb, 300, 150, 7.1, 10.7)                                                     # IPE 300 viga de borde
    # doble ángulo de unión viga de borde / alma de columna (oculto tras la viga)
    rect(395, yb - 260, 505, yb - 40, fill="none", stroke="#333", sw=0.1, extra=DASH)
    losa(yt)
    # pintura intumescente (indicada en el ala inferior de la viga de borde)
    pline([(372, yb - 302), (528, yb - 302)], stroke="#c0392b", sw=0.2)

def cielorraso(y, x0, ybeam):
    rect(x0, y, XR, y + 12.5, fill="#f2f2f2", **CUTT)
    for xx in range(900, XR, 400): rect(xx, y + 12.5, xx + 35, y + 47, fill=ALU, stroke="#444", sw=0.08)
    pline([(x0, y + 60), (x0, y), (x0 + 40, y)], stroke="#000", sw=0.2)
    for xc in (1300, 2200): line(xc, y + 47, xc, ybeam, stroke="#555", sw=0.15)              # velas a la viga (grampa de ala)

# ================================================================== TERRENO Y FUNDACIÓN (cortada por el eje de columna)
rect(-750, -1900, XR, -330, fill="url(#pTierra)", stroke="none", sw=0)
line(-750, -330, -24, -330, sw=0.2)
rect(-530, -1850, 1430, -1800, fill="url(#pH)", **CUTT)                                       # H° de limpieza
rect(-480, -1800, 1380, -1350, fill="url(#pHAis)", **CUT)                                    # zapata
poly([(150, -1350), (750, -1350), (750, -350), (225, -350), (225, -30), (-20, -30), (-20, -630), (150, -630)], fill="url(#pHAis)", **CUT)   # cuello + viga de fundación
# armaduras
pline([(-420, -1660), (-420, -1740), (1320, -1740), (1320, -1660)], stroke=REB, sw=0.22)
for xx in range(-400, 1320, 150): circ(xx, -1725, 0.28, fill=REB)
for xx in (190, 710): pline([(xx + (60 if xx < 450 else -60), -1740), (xx, -1740), (xx, -390)], stroke=REB, sw=0.2)
for yy in range(-1300, -380, 150): pline([(190, yy), (710, yy)], stroke=REB, sw=0.08, extra='stroke-dasharray="1.5 0.6"')
pline([(10, -600), (190, -600), (190, -60), (10, -60), (10, -600)], stroke=REB, sw=0.1)       # estribo viga de fundación
for xx, yy in ((30, -580), (170, -580), (30, -80), (170, -80)): circ(xx, yy, 0.3, fill=REB)
# piso sobre terreno
xs0 = 100 if OP else 190
rect(720, -320, XR, -172, fill="url(#pTosca)", **CUTT)
rect(720, -172, XR, -170, fill="#000", stroke="none", sw=0)                                   # film 200 µ
rect(720, -170, XR, -50, fill="url(#pH)", **CUTT)                                             # contrapiso armado
pline([(740, -110), (XR - 10, -110)], stroke=REB, sw=0.1, extra='stroke-dasharray="2 0.5"')
rect(225, -50, XR, -30, fill="url(#pHid)", **CUTT)                                            # carpeta hidrófuga
rect(xs0, -30, XR, -10, fill="url(#pMort)", **CUTT)                                           # carpeta niveladora
rect(274 if OP else 190, -15, XR, -10, fill="#8d8d8d", stroke="none", sw=0)
rect(274 if OP else 190, -10, XR, 0, fill="url(#pPorc)", **CUTT)
for xx in range(900, XR, 400): line(xx, -10, xx, 0, sw=0.15)
columna(-295, 7855)
rect(330, 7855, 570, 7870, fill=STV, stroke="#333", sw=0.12)                                   # placa de cierre sup. (bajo la losa)
# dado de H° de protección de la base (hasta el contrapiso) + juntas
rect(240, -320, 700, -50, fill="url(#pH)", **CUTT)
rect(330, -295, 570, -50, fill="none", stroke="#444", sw=0.12, extra=DASH)                      # columna embebida en el dado (oculta)
rect(225, -350, 240, -30, fill="url(#pEPSv)", stroke="#000", sw=0.08)
rect(700, -330, 720, -30, fill="url(#pEPSv)", stroke="#000", sw=0.08)
# grout + placa base + cartelas + pernos de anclaje
rect(225, -350, 675, -320, fill="url(#pGrout)", **CUTT)
rect(225, -320, 675, -295, fill=STC, stroke="#000", sw=0.2)
for x0_, x1_ in ((225, 330), (570, 675)):
    xa, xb = (x0_, x1_) if x0_ < 330 else (x1_, x0_)
    poly([(xa, -295), (xb, -295), (xb, -95), (xa, -265)], fill="none", stroke="#444", sw=0.12, extra=DASH)  # cartelas 12 mm (ocultas)
for xx in (270, 630):
    rect(xx - 12, -1150, xx + 12, -255, fill=STC, stroke="#000", sw=0.08)                     # perno Ø24
    rect(xx - 45, -1160, xx + 45, -1140, fill=STC, stroke="#000", sw=0.08)                    # placa de anclaje inferior
    rect(xx - 22, -343, xx + 22, -322, fill="#222", stroke="none", sw=0)                      # tuerca niveladora
    rect(xx - 28, -295, xx + 28, -289, fill=STC, stroke="#000", sw=0.05)                      # arandela
    rect(xx - 22, -289, xx + 22, -268, fill="#222", stroke="none", sw=0)                      # tuerca
# vereda exterior
rect(-750, -330, -24, -250, fill="url(#pTosca)", **CUTT)
poly([(-750, -250), (-32, -250), (-32, -150), (-750, -157)], fill="url(#pH)", **CUTT)
rect(-32, -250, -24, -150, fill="url(#pEPSv)", stroke="#000", sw=0.06); rect(-32, -162, -24, -150, fill=NEO, stroke="none", sw=0)
line(-22, -150, -22, -330, stroke="#000", sw=0.45)                                            # pintura asfáltica (cara enterrada)

# ================================================================== ESTRUCTURA
entrepiso_estructura(3970)
entrepiso_estructura(8000)
# piso planta alta
rect(300, 3970, XR, 3990, fill="url(#pMort)", **CUTT)
rect(300, 3990, XR, 3995, fill="#8d8d8d", stroke="none", sw=0)
rect(300, 3995, XR, 4005, fill="url(#pPorc)", **CUTT)
for xx in range(860, XR, 400): line(xx, 3995, xx, 4005, sw=0.15)
cielorraso(3200, 262 if OP else 190, 3440)
cielorraso(7200, 262 if OP else 190, 7470)

def barrera_fuego(yt, x0):
    """lana mineral 120 kg/m³ comprimida en el borde de losa, s/ ángulo de chapa galv. fijado al frentín + sellador intumescente"""
    yb = yt - 130
    poly([(x0, yb), (x0, yb - 45), (300, yb - 45), (300, yb - 120), (293, yb - 120), (293, yb - 38), (x0 + 7, yb - 38), (x0 + 7, yb)], fill=GALV, stroke="#000", sw=0.05)
    rect(x0, yb, 300, yt - 8, fill="url(#pLana)", **CUTT)
    rect(x0, yt - 8, 300, yt, fill="#c0392b", stroke="none", sw=0)

if OP:
    # ---------------------------------------------------------------- PANEL SÁNDWICH METÁLICO (cerramiento opaco)
    def panel(y0, y1):
        rect(0, y0, 100, y1, fill="url(#pPIR)", **CUTT)
        for xx in (0.6, 99.4): line(xx, y0, xx, y1, stroke="#000", sw=0.3)                   # chapas prepintadas 0,5 mm
    panel(-25, 4290); panel(4310, 8850)
    # junta horizontal: babeta Z de chapa prepintada + sellador
    rect(0, 4290, 100, 4310, fill=NEO, stroke="none", sw=0)
    pline([(118, 4380), (100, 4380), (100, 4300), (-20, 4300), (-20, 4262)], stroke="#000", sw=0.25)
    for y0 in (400, 2200, 3650, 4450, 6200, 7650):
        correa(y0); clip(y0); tornillo_panel(y0 + 30)
    for a, b in ((460, 2200), (2260, 3650), (4510, 6200), (6260, 7650)):
        line(180, a, 180, b, stroke="#000", sw=0.16)                                          # tensores Ø10 (anti-pandeo de correas)
    # arranque: perfil L 50x50 galv. s/ viga de fundación, babeta-goterón, sellador
    pline([(-22, -75), (-22, -28), (150, -28)], stroke="#000", sw=0.3)                       # babeta-goterón
    rect(100, -25, 150, -20, fill=GALV, stroke="#000", sw=0.05); rect(100, -20, 105, 30, fill=GALV, stroke="#000", sw=0.05)   # perfil de arranque
    line(125, -25, 125, -110, stroke="#000", sw=0.22)                                         # broca
    rect(-8, -25, 0, 10, fill=NEO, stroke="none", sw=0)                                        # sellador exterior
    # revestimiento interior: placa de roca de yeso 12,5 mm s/ las correas (oculta correas y cavidad)
    rect(262, 0, 274.5, 3200, fill="url(#pYeso)", **CUTT)
    rect(262, 4005, 274.5, 7200, fill="url(#pYeso)", **CUTT)
    rect(262, 0, 274.5, 80, fill="#cdbb9c", stroke="#000", sw=0.08); rect(262, 4005, 274.5, 4085, fill="#cdbb9c", stroke="#000", sw=0.08)  # zócalos
    # borde de losa: barrera cortafuego + cubrejunta / solera de arranque del revestimiento
    barrera_fuego(3970, 100); barrera_fuego(8000, 100)
    rect(262, 3970, 300, 4005, fill=GALV, stroke="#000", sw=0.06)
    # parapeto: montantes UPN 160 c/ 1,25 m (en vista) abulonados a ménsula soldada a la viga de borde; revestimiento interior
    rect(100, 7700, 260, 8830, fill=STV, **VIEW); line(108, 7700, 108, 8830, stroke="#666", sw=0.08); line(252, 7700, 252, 8830, stroke="#666", sw=0.08)
    rect(260, 7560, 375, 7860, fill=STV, stroke="#333", sw=0.12)                              # ménsula de chapa 12 mm (vista)
    for yy in (7620, 7800): line(250, yy, 390, yy, stroke="#000", sw=0.22)
    for yy in (8250, 8700): tornillo_panel(yy)
    rect(260, 8000, 272, 8830, fill="url(#pCem)", **CUTT)                                     # placa cementicia 12 mm
    xl = 272
else:
    # ---------------------------------------------------------------- MURO CORTINA (cerramiento vidriado)
    montante(40, 4190); montante(4210, 8840)
    rect(32, 4190, 182, 4210, fill="#fff", stroke="#444", sw=0.1)
    rect(60, 4100, 150, 4320, fill="none", stroke="#444", sw=0.1, extra=DASH)                 # manguito
    def bandeja_spandrel(y0, y1):
        rect(40, y0 + 6, 90, y1 - 6, fill="url(#pLanaV)", **CUTT)
        poly([(40, y0), (93, y0), (93, y1), (40, y1), (40, y1 - 6), (87, y1 - 6), (87, y0 + 6), (40, y0 + 6)], fill=STEEL, stroke="#000", sw=0.05)
    # arranque PB: suplemento de mortero s/ viga de fundación + perfil guía (el montante desliza: cuelga del entrepiso)
    rect(25, -30, 190, 0, fill="url(#pMort)", **CUTT)
    rect(25, 0, 190, 40, fill=ALU, **CUTT); rect(32, 6, 182, 40, fill="#fff", stroke="#000", sw=0.06)
    for xx in (60, 150): line(xx, 0, xx, -110, stroke="#000", sw=0.14)
    rect(-30, 0, 25, 4, fill="#222", stroke="none", sw=0)
    pline([(30, -2), (-24, -2), (-24, -75)], stroke="#000", sw=0.3)                          # babeta-goterón
    travesano(40, 60, glass_below=False)
    dvh(110, 3140); travesano(3150, 60)
    dvh(3220, 4050, spandrel=True); bandeja_spandrel(3210, 4060)
    travesano(4060, 60)
    dvh(4130, 7140); travesano(7150, 60)
    dvh(7220, 8840, spandrel=True); bandeja_spandrel(7210, 8840)
    rect(-32, 8840, 190, 8880, fill=ALU, **CUTT); rect(-25, 8846, 183, 8874, fill="#fff", stroke="#000", sw=0.06)
    barrera_fuego(3970, 93); barrera_fuego(8000, 93)
    # anclaje (en cada montante, en vista): grapa regulable s/ placa de anclaje 12 mm c/ pernos soldados embebida en la losa
    def grapa(yt):
        yy = yt + 4
        rect(200, yt - 12, 330, yt, fill=STC, stroke="#000", sw=0.06)                         # placa embebida
        for xx in (230, 300): line(xx, yt - 12, xx, yt - 90, stroke="#000", sw=0.25)         # pernos soldados
        poly([(185, yy - 150), (195, yy - 150), (195, yy), (300, yy), (300, yy + 10), (185, yy + 10)], fill=STEEL, stroke="#000", sw=0.08)
        line(160, yy - 110, 200, yy - 110, stroke="#000", sw=0.25)                            # bulón M12 inox al montante
        line(265, yy + 22, 265, yt - 14, stroke="#000", sw=0.3)                               # bulón a la placa (soldado)
    grapa(3970); grapa(8000)
    pline([(182, 4008), (330, 4008)], stroke="#000", sw=0.25)
    # parapeto: montantes tubo 60x100 (vista) + placa cementicia
    rect(200, 7700, 260, 8830, fill=STV, **VIEW)
    rect(200, 7560, 375, 7860, fill=STV, stroke="#333", sw=0.12)
    for yy in (7620, 7800): line(190, yy, 390, yy, stroke="#000", sw=0.22)
    rect(260, 8000, 272, 8830, fill="url(#pCem)", **CUTT)
    xl = 272

# ================================================================== CUBIERTA
rect(xl, 8000, XR, 8003, fill="#000", stroke="none", sw=0)                                    # barrera de vapor
def ypend(x, b): return b + (x - xl) * 0.02
poly([(xl, 8003), (XR, 8003), (XR, ypend(XR, 8063)), (xl, 8063)], fill="url(#pEPS)", **CUTT)     # contrapiso liviano H° c/ EPS, pend. 2 %
poly([(xl, 8063), (XR, ypend(XR, 8063)), (XR, ypend(XR, 8083)), (xl, 8083)], fill="url(#pMort)", **CUTT)   # carpeta
poly([(xl, 8083), (xl + 60, 8083), (xl, 8143)], fill="url(#pMort)", **CUTT)                      # media caña
pline([(XR, ypend(XR, 8087)), (xl + 60, 8087), (xl + 4, 8143), (xl + 4, 8350)], stroke="#000", sw=0.45)   # membrana
pline([(xl + 30, 8400), (xl + 2, 8400), (xl + 2, 8320)], stroke="#000", sw=0.22)                 # babeta
rect(xl, 8392, xl + 10, 8408, fill="#222", stroke="none", sw=0)
# embudo (oculto) c/ rejilla junto al parapeto -> caño de lluvia PVC Ø110 interior junto a la columna
rect(xl + 120, 7930, xl + 220, 8083, fill="none", stroke="#333", sw=0.13, extra=DASH)
# cupertina (pend. al interior, goterones) atornillada c/ arandela de neopreno
pline([(-42, 8800), (-42, 8890), (xl + 20, 8865), (xl + 20, 8815)], stroke="#000", sw=0.32)
line(140, 8848, 140, 8885, stroke="#000", sw=0.18)
rect(-20 if OP else -32, 8850 if OP else 8880, xl, 8856 if OP else 8886, fill="#888", stroke="none", sw=0)
if OP: rect(100, 8830, 272, 8850, fill=GALV, stroke="#000", sw=0.05)                         # solera de coronamiento
