# -*- coding: utf-8 -*-
"""Lámina TP final - CERRAMIENTO OPACO (A3 vertical). Es el MISMO edificio que src/tp_corte.py (muro cortina) visto
del otro lado: misma estructura (columna + ménsula, VL doble T + viga L de borde, panel TT, capa), misma fundación,
mismos colores, rayados, bandas y formato. Este script toma el código del vidriado y reemplaza solo lo propio del
cerramiento opaco: panel sándwich premoldeado (apoyado en viga portapanel, vinculado con fija paneles), cubierta con
parapeto del panel, vereda/arranque y referencias.
Panel x 30..230 (hoja ext. 60 | EPS 60 | hoja int. portante 80) · junta 230..250 · columna / VL x 250..650."""
import os

SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tp_corte.py"), encoding="utf-8").read()

def cut(src, a, b, new):
    i = src.index(a); j = src.index(b, i)
    return src[:i] + new + src[j:]

# ------------------------------------------------------------------ fundación: arranque del panel en viga portapanel
SRC = cut(SRC, "# SIN viga perimetral", "# JUNTAS DE DILATACIÓN", '''# viga portapanel premoldeada (SOLO bajo los paneles) apoyada en el cuello de la base s/ neopreno
rect(10, -510, 175, -500, fill=NEO, stroke="none", sw=0)
poly([(10, -500), (230, -500), (230, -50), (30, -50), (10, -70)], fill="url(#pHA)", **CUT)
for xx, yy in ((40, -470), (200, -470), (40, -90), (200, -90)): circ(xx, yy, 0.3, fill=REB)
pline([(25, -485), (215, -485), (215, -65), (25, -65), (25, -485)], stroke=REB, sw=0.1, extra=DASH)
line(8, -500, 8, -160, stroke="#000", sw=0.45)                                            # pintura asfáltica (caras enterradas)
rect(230, -500, 250, -327, fill="url(#pEPSv)", **CUTT)                                    # junta EPS viga / columna
# arranque del panel: mortero de asiento + calces de neopreno, pasador Ø16 en vaina c/ grout, selladores
rect(30, -50, 230, -40, fill="url(#pMort)", **CUTT)
rect(70, -50, 110, -40, fill=NEO, stroke="none", sw=0)
rect(175, -330, 205, 230, fill="url(#pGrout)", stroke="#333", sw=0.1)
line(190, -320, 190, 220, stroke="#000", sw=0.32)
rect(18, -52, 31, -38, fill="#111", stroke="none", sw=0)
rect(230, -50, 250, 0, fill=NEO, stroke="none", sw=0)
# vereda exterior hasta la viga portapanel (junta EPS + sellador)
rect(-750, -327, 0, -250, fill="url(#pTosca)", **CUTT)
poly([(-750, -250), (0, -250), (0, -150), (-750, -157)], fill="url(#pH)", **CUTT)
rect(0, -250, 8, -150, fill="url(#pEPSv)", stroke="#000", sw=0.08); rect(0, -162, 8, -150, fill=NEO, stroke="none", sw=0)
# piso sobre terreno (interior), separado de la columna por junta de dilatación
for xa, xb, sol in ((670, 2700, (675, 2700)),):
    rect(xa, -327, xb, -177, fill="url(#pTosca)", **CUTT)
    rect(xa, -177, xb, -175, fill="#000", stroke="none", sw=0)                            # film 200 µ
    rect(xa, -175, xb, -55, fill="url(#pH)", **CUTT)                                      # contrapiso
    pline([(xa + 20, -120), (xb - 10, -120)], stroke=REB, sw=0.1, extra='stroke-dasharray="2 0.5"')  # malla
    rect(xa, -55, xb, -35, fill="url(#pHid)", **CUTT)                                     # carpeta hidrófuga
    rect(xa, -35, xb, -15, fill="url(#pMort)", **CUTT)                                    # carpeta niveladora
    rect(sol[0], -15, sol[1], -10, fill="#8d8d8d", stroke="none", sw=0)
    rect(sol[0], -10, sol[1], 0, fill="url(#pPorc)", **CUTT)
for xx in range(975, 2700, 400): line(xx, -10, xx, 0, sw=0.15)
''')

# ------------------------------------------------------------------ la VL no lleva riel para muro cortina (el fija panel pasa por el alma)
SRC = cut(SRC, "    # riel de anclaje embutido en la VL", "def panel_TT", "")
SRC = SRC.replace("# columnas en vista", '\nimport math as _m\ndef viga_borde_canaleta(yt):\n    """cubierta (lado opaco, como el corte de referencia): VL doble T s/ ménsula + viga de borde premoldeada (apoyo del ala del TT)\n    + CANALETA de H°A colada in situ c/ hueco semicircular entre el parapeto del panel y el TT"""\n    yb = yt - 910; yv = yt - 210; yl = yt - 60\n    P = [(250, yb), (650, yb), (650, yb + 150), (530, yb + 210), (510, yb + 210), (510, yv - 190), (530, yv - 190), (650, yv - 130), (650, yv),\n         (250, yv), (250, yv - 130), (370, yv - 190), (390, yv - 190), (390, yb + 210), (370, yb + 210), (250, yb + 150)]\n    poly(P, fill="url(#pHA)", **CUT)\n    for xx in (290, 370, 450, 530, 610): circ(xx, yb + 45, 0.32)\n    for xx in (330, 570): circ(xx, yb + 100, 0.32)\n    for xx in (290, 450, 610): circ(xx, yv - 45, 0.28, fill=REB)\n    pline([(400, yb + 30), (400, yv - 30)], stroke=REB, sw=0.1); pline([(500, yb + 30), (500, yv - 30)], stroke=REB, sw=0.1)\n    rect(250, yb - 10, 650, yb, fill=NEO, stroke="none", sw=0)\n    rect(250, yv - 3, 650, yv + 3, fill="url(#pGrout)", stroke="none", sw=0)\n    rect(250, yv + 3, 650, yl, fill="url(#pHA)", **CUT)                                    # viga de borde premoldeada\n    for xx in (290, 610): circ(xx, yv + 40, 0.26, fill=REB)\n    for xx in (330, 520): pline([(xx, yv - 120), (xx, yv + 110)], stroke=REB, sw=0.25)\n    arc = [(430 + 110 * _m.cos(t), 9040 + 110 * _m.sin(t)) for t in [-k * _m.pi / 24 for k in range(25)]]\n    poly([(250, yl), (560, yl), (560, 9040), (540, 9040)] + arc[1:-1] + [(320, 9040), (320, 9150), (250, 9150)], fill="url(#pHAis)", **CUT)   # canaleta in situ\n    for xx in (285, 560 - 15): pline([(xx, yl - 90), (xx, 9010 if xx < 300 else 9010)], stroke=REB, sw=0.2)               # estribos salientes\n    pline([(285, 9010), (285, 9120)], stroke=REB, sw=0.2)\n    circ(285, 9100, 0.22, fill=REB); circ(545, 9000, 0.22, fill=REB)\ndef panel_TT_c(yt):\n    yf = yt - 50\n    rect(760, yt - 750, 2700, yf, fill="#e9ebed", **VIEW)\n    line(760, yt - 600, 2700, yt - 600, stroke="#888", sw=0.08)\n    rect(580, yf, 2700, yt, fill="url(#pHA)", **CUT)\n    for xc in (1170,):\n        poly([(xc - 90, yf), (xc + 90, yf), (xc + 60, yt - 650), (xc - 60, yt - 650)], fill="url(#pHA)", **CUT)\n        for yy in (yt - 610, yt - 560): circ(xc, yy, 0.3)\n        line(xc, yt - 640, xc, yf, stroke=REB, sw=0.1)\n    rect(590, yt - 60, 645, yt - 50, fill=NEO, stroke="none", sw=0)\n    rect(560, yt - 60, 580, yt, fill="url(#pGrout)", stroke="none", sw=0)\n' + "\n# columnas en vista", 1)
SRC = SRC.replace("mensula_vista(7995); viga_L(8915); panel_TT(8915); capa_compresion(8915, 400)", "mensula_vista(7995); viga_borde_canaleta(8915); panel_TT_c(8915); capa_compresion(8915, 570)")
# cielorraso: arranca en el panel (no en el muro cortina)
SRC = SRC.replace("rect(190, y, 2700, y + 12.5,", "rect(242, y, 2700, y + 12.5,").replace("pline([(190, y + 70), (190, y), (230, y)]", "pline([(230, y + 70), (230, y - 5), (270, y - 5)]")

# ------------------------------------------------------------------ cerramiento: panel sándwich + fija paneles + juntas
PANEL = '''# ------------------------------------------------------------------ PANEL SÁNDWICH PREMOLDEADO (cerramiento integral opaco)
def panel(y0, y1):
    rect(30, y0, 230, y1, fill="url(#pHA)", **CUT)
    rect(90, y0 + 60, 150, y1 - 60, fill="url(#pEPSv)", stroke="#000", sw=0.12)
    for xx in (60, 190): line(xx, y0 + 30, xx, y1 - 30, stroke=REB, sw=0.09, extra='stroke-dasharray="2 0.6"')   # mallas
    for yy in range(y0 + 500, y1 - 300, 700): line(80, yy, 160, yy + 60, stroke="#222", sw=0.16)                   # conectores fibra de vidrio
    rect(212, 9330, 230, 9350, fill="#fff", stroke="#000", sw=0.1)                                                 # buña p/ babeta
def fija_panel(yy):
    """anclaje pasante (sistema Astori): rehundido Ø100 prof. 3 cm en la cara exterior (tapado c/ mortero), agujero ovalado
    40x60 a través de TODO el panel, calce de neopreno en la junta, vaina pasante en el ala superior de la VL y tuerca + arandela del lado interior"""
    rect(30, yy - 50, 60, yy + 50, fill="url(#pMort)", stroke="#000", sw=0.12)                 # rehundido tapado c/ mortero
    rect(60, yy - 22, 230, yy + 22, fill="#fff", stroke="#333", sw=0.1, extra=DASH)          # agujero ovalado 40x60 en el panel
    rect(232, yy - 40, 248, yy + 40, fill=NEO, stroke="none", sw=0)                           # calce de neopreno en la junta
    rect(250, yy - 16, 650, yy + 16, fill="#fff", stroke="#333", sw=0.1, extra=DASH)          # vaina pasante en el ala de la VL
    line(40, yy, 700, yy, stroke="#000", sw=0.36)                                             # bulón pasante M20
    rect(60, yy - 40, 68, yy + 40, fill=STEEL, stroke="#000", sw=0.06); rect(44, yy - 15, 60, yy + 15, fill="#222", stroke="none", sw=0)   # arandela + cabeza
    rect(650, yy - 40, 660, yy + 40, fill=STEEL, stroke="#000", sw=0.06); rect(660, yy - 16, 682, yy + 16, fill="#222", stroke="none", sw=0)  # arandela + tuerca
panel(-40, 9440)
# juntas panel / estructura: lana mineral cortafuego + selladores; piso del entrepiso hasta el panel
rect(230, 3505, 250, 4465, fill="url(#pLanaV)", **CUTT); rect(230, 3505, 250, 3520, fill=NEO, stroke="none", sw=0)
rect(230, 4465, 240, 4500, fill="url(#pEPSv)", stroke="#000", sw=0.08); rect(230, 4490, 240, 4500, fill=NEO, stroke="none", sw=0)
rect(240, 4465, 250, 4485, fill="url(#pMort)", **CUTT); rect(240, 4485, 250, 4490, fill="#8d8d8d", stroke="none", sw=0); rect(240, 4490, 250, 4500, fill="url(#pPorc)", **CUTT)
rect(230, 4500, 240, 4600, fill="#cdbb9c", stroke="#000", sw=0.1)                                 # zócalo
rect(230, 8005, 250, 8855, fill="url(#pLanaV)", **CUTT); rect(230, 8005, 250, 8020, fill=NEO, stroke="none", sw=0)
fija_panel(4140); fija_panel(8640)

'''
SRC = cut(SRC, "# ------------------------------------------------------------------ MURO CORTINA", "# ------------------------------------------------------------------ CUBIERTA", PANEL)

# ------------------------------------------------------------------ cubierta: paquete hasta el parapeto del panel
SRC = cut(SRC, "# ------------------------------------------------------------------ CUBIERTA", "# =====================================================================================\n#  COMPOSICIÓN", '''# ------------------------------------------------------------------ CUBIERTA (el panel sube como parapeto)
rect(570, 8965, 2700, 8968, fill="#000", stroke="none", sw=0)                               # barrera de vapor
rect(230, 8855, 250, 9150, fill="url(#pEPSv)", stroke="#000", sw=0.08)                      # junta EPS panel / canaleta
x0, x1 = 570, 2700
def ypend(x, b): return b + (x - x0) * 0.02
poly([(x0, 8968), (x1, 8968), (x1, ypend(x1, 9068)), (630, ypend(630, 9068)), (x0, 9010)], fill="url(#pEPS)", **CUTT)   # contrapiso liviano H° c/ EPS
poly([(x0, 9010), (630, ypend(630, 9068)), (x1, ypend(x1, 9068)), (x1, ypend(x1, 9088)), (630, ypend(630, 9088)), (560, 9040), (x0, 9040)], fill="url(#pMort)", **CUTT)  # carpeta (baja a la canaleta)
import math as _m
arcm = [(430 + 106 * _m.cos(t), 9040 + 106 * _m.sin(t)) for t in [-k * _m.pi / 24 for k in range(25)]]
pline([(x1, ypend(x1, 9092)), (630, ypend(630, 9092)), (560, 9044), (540, 9044)] + arcm[1:-1] + [(324, 9044), (324, 9154), (234, 9154), (234, 9335), (214, 9340)], stroke="#000", sw=0.45)   # membrana continua
pline([(214, 9346), (238, 9346), (238, 9290)], stroke="#000", sw=0.2)                       # babeta
rect(213, 9331, 229, 9349, fill="#222", stroke="none", sw=0)
# cupertina (pendiente al interior, goterones) fijada c/ tornillo + arandela de neopreno
pline([(-2, 9375), (12, 9390), (12, 9472), (248, 9458), (248, 9395), (262, 9380)], stroke="#000", sw=0.32)
line(130, 9440, 130, 9470, stroke="#000", sw=0.18); rect(118, 9466, 142, 9472, fill="#222", stroke="none", sw=0)
rect(30, 9440, 230, 9446, fill="#888", stroke="none", sw=0)

''')

# ------------------------------------------------------------------ cotas propias
SRC = cut(SRC, "cota_v(0, 4500, -560)", "T(X(-590), Y(9300)", '''cota_v(0, 4500, -560); cota_v(4500, 8915, -560, "4,42"); cota_v(-2150, 0, -560)
cota_v(3505, 4205, 900, "0,70"); cota_v(4205, 4465, 900, "0,26"); cota_v(8005, 8705, 900, "0,70"); cota_v(8705, 8965, 900, "0,26")
cota_v(3765, 4415, 1550, "0,65")
cota_v(-2050, -1750, 1560, "0,30"); cota_v(-1350, -510, 1150, "0,84")
cota_v(9092, 9440, -60, "0,35")
cota_h(30, 230, 3330, "20"); cota_h(230, 250, 3330, "2"); cota_h(250, 650, 3330, "40")
cota_h(-550, 1450, -2170, "2,00 (s/ cálculo)", below=True); cota_h(-75, 975, -1420, "1,05")

''')

REFS = '''# ------------------------------------------------------------------ REFERENCIAS
def ref(n, x, y, bx, by):
    """globo en posición absoluta de papel (bx, by)"""
    DX.append(dict(t='ref', n=n, a=(x, y), b=(x + (bx - X(x)) * S, y - (by - Y(y)) * S)))
    px, py = X(x), Y(y)
    A(f'<circle cx="{f(px)}" cy="{f(py)}" r="0.32" fill="#000"/>')
    L(px, py, bx, by, 0.11, "#000")
    A(f'<circle cx="{f(bx)}" cy="{f(by)}" r="2.35" fill="#fff" stroke="#000" stroke-width="0.2"/>')
    T(bx, by + 1.0, str(n), 2.8, "middle", "bold", "#000")
EX = 191.0
REFS_POS = [
 # cubierta
 (1, 12, 9440, 193, 8.5), (2, 130, 9468, 218, 6.5), (6, 236, 9310, 222, 14), (3, 1000, 9093, 250, 22.4), (4, 1300, 9100, 266, 20.4),
 (5, 1500, 9050, 275, 44.5), (7, 1000, 8967, 250, 44.8), (9, 430, 8960, 226, 26), (8, 240, 9000, 223, 33),
 (10, 1550, 8945, 289.5, 46), (11, 285, 9060, 257.5, 20), (12, 1170, 8500, 238.5, 63.5), (13, 400, 8780, 236.5, 51), (14, 450, 8100, 252.5, 88),
 (15, 450, 7640, 236.5, 103), (16, 700, 7720, 248, 105), (17, 500, 8000, 248, 90.5), (18, 520, 8705, 247, 56), (19, 540, 8858, 258, 52),
 (25, 60, 9150, EX, 26), (26, 190, 9000, EX, 32.5), (27, 120, 8850, EX, 39), (28, 45, 8640, EX, 52), (30, 140, 8640, EX, 58.5), (31, 240, 8400, EX, 70.5), (29, 600, 8640, 247, 66),
 # entrepiso
 (20, 1500, 4495, 275, 127), (21, 1600, 4475, 280, 128.6), (22, 1300, 3306, 245, 200), (23, 1550, 3325, 257.5, 200), (24, 1275, 3500, 252.5, 187),
 (32, 235, 4520, EX, 128), (28, 45, 4140, EX, 147), (30, 140, 4140, EX, 154), (31, 240, 3900, EX, 165), (29, 600, 4140, 244, 162),
 (13, 330, 4300, 236.5, 148), (19, 540, 4358, 257, 150), (14, 450, 3600, 247, 176),
 # planta baja y fundación
 (25, 60, 900, EX, 228), (26, 190, 700, EX, 236), (27, 120, 500, EX, 244), (43, 120, -45, EX, 270), (34, 25, -45, EX, 277),
 (45, -300, -200, 180, 292), (56, 4, -200, EX, 288), (44, 8, -400, EX, 300), (55, 90, -505, EX, 312), (42, 120, -300, 180, 304),
 (35, 950, -5, 247.5, 272), (36, 1150, -25, 257.5, 271), (37, 1350, -45, 267.5, 270), (38, 1100, -120, 255, 294), (39, 1550, -176, 277.5, 297),
 (40, 1350, -260, 267.5, 301), (41, 660, -250, 247, 298), (46, 450, -900, 236.5, 327), (47, 700, -800, 255, 322), (48, 690, -1200, 256.5, 343),
 (49, 540, -1600, 247, 363), (50, 850, -700, 260.5, 330), (51, 1200, -1800, 269, 362), (52, 1100, -1960, 265, 368), (53, 1400, -2100, 274, 386), (54, 1400, -1350, 275, 352),
]
for r in REFS_POS: ref(*r)

LEG = [
("CUBIERTA", None),
(1, "Cupertina chapa galv. N°22 c/ goterones"),
(2, "Tornillo c/ arandela de neopreno + sellador"),
(3, "Membrana asfáltica 4 mm c/ aluminio"),
(4, "Carpeta 1:3 c/ 10 % hidrófugo, e = 2 cm"),
(5, "Contrapiso liviano H° c/ EPS (aislante), pend. 2 %"),
(6, "Babeta chapa galv. + sellador en buña del panel"),
(7, "Barrera de vapor: imprimación + film 200 µ"),
(8, "Junta EPS 2 cm panel / canaleta + sellador"),
(9, "Canaleta H°A in situ c/ hueco semicircular, pend. 1 %"),
("ESTRUCTURA PREMOLDEADA (SISTEMA PI)", None),
(10, "Capa de compresión 5 cm c/ malla Ø6 c/15"),
(11, "Estribos salientes Ø10 (anclan canaleta y capa)"),
(12, "Panel TT h 0,65: ala y nervios cortados"),
(13, "Viga de borde premold. s/ VL (L en entrepiso)"),
(14, "Viga VL doble T 40x70 pretensada"),
(15, "Columna pretensada 40x40 (en vista)"),
(16, "Ménsula de columna c/ diagonal (en vista)"),
(17, "Neopreno + perno Ø20 (VL / ménsula)"),
(18, "Barras de vinculación VL / L en mortero"),
(19, "Ala del TT s/ viga de borde + neopreno"),
("ENTREPISO Y CIELORRASOS", None),
(20, "Solado cerámico s/ adhesivo cementicio"),
(21, "Carpeta niveladora MHR 1:1/4:3, e = 2 cm"),
(22, "Cielorraso placa de roca de yeso 12,5 mm"),
(23, "Montantes y soleras chapa galv. 35 mm"),
(24, "Gancho / vela a los nervios del panel TT"),
("CERRAMIENTO INTEGRAL OPACO", None),
(25, "Panel sándwich premoldeado H°A, e = 20 cm"),
(26, "Hoja ext. H°A 6 cm / hoja int. portante 8 cm"),
(27, "Alma EPS 6 cm + conectores de fibra de vidrio"),
(28, "Rehundido Ø100 prof. 3 cm tapado c/ mortero"),
(29, "Bulón pasante M20: atraviesa panel y ala de VL"),
(30, "Agujero ovalado 40x60 + vaina, tuerca y arandela"),
(31, "Junta 2 cm: lana mineral cortafuego + sellador"),
(32, "Junta perimetral EPS 1 cm + zócalo"),
(33, "Junta vertical panel / panel: fondo + sellador PU"),
(34, "Sellador PU s/ fondo de junta (junta horizontal)"),
("PLANTA BAJA Y FUNDACIÓN", None),
(35, "Solado cerámico s/ adhesivo cementicio"),
(36, "Carpeta niveladora MHR 1:1/4:3"),
(37, "Carpeta hidrófuga MCI 1:3"),
(38, "Contrapiso de H° pobre, e = 12 cm"),
(39, "Film de polietileno 200 µ"),
(40, "Tosca compactada, e = 15 cm"),
(41, "Junta de dilatación EPS 2 cm + sellador"),
(42, "Viga portapanel premoldeada 22x45 (s/ cuellos)"),
(43, "Mortero de asiento + pasador Ø16 en vaina c/ grout"),
(44, "Pintura asfáltica en caras enterradas"),
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
(55, "Neopreno de apoyo viga portapanel / cuello"),
(56, "Junta vereda / viga EPS 1 cm + sellador"),
]

'''
SRC = cut(SRC, "# ------------------------------------------------------------------ REFERENCIAS", "# ---------------- FORMATO TP", REFS)
SRC = SRC.replace('T(16, 39.9, "MURO CORTINA", 7.4)', 'T(16, 39.9, "CERRAMIENTO OPACO", 7.4)')
SRC = SRC.replace('open("build/tp_corte.svgpart", "w")', 'open("build/opaco_corte.svgpart", "w")').replace('open("build/tp_dx.json", "w")', 'open("build/opaco_dx.json", "w")')
for must in ("CERRAMIENTO OPACO", "opaco_corte.svgpart", "fija_panel(4140)", "viga portapanel", "viga_borde_canaleta(8915)"):
    assert must in SRC, must
exec(compile(SRC, "opaco_corte(tp_corte)", "exec"))
open("build/opaco_corte_solo.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="420mm" viewBox="0 0 297 420" font-family="Liberation Sans, Arial, sans-serif">{SVG_BODY}</svg>')
