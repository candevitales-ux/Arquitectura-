# -*- coding: utf-8 -*-
"""Edificio adoptado para el TP6 ACERO (mismo edificio estándar del cómputo de la Lámina 4).
Unidades: mm reales."""
LARGO, ANCHO = 20000, 12000      # planta rectangular
VANO = 4000                      # separación de pórticos (ejes 1 a 6)
SEC = 2000                       # separación de vigas secundarias
EJES_X = [i * VANO for i in range(6)]            # ejes 1..6
EJES_Y = [0, 4000, 8000, 12000]                  # ejes A..D (A = frente vidriado, D = contrafrente)
N1, N2, CUP = 3800, 7400, 8000   # entrepiso, cubierta (NPT / sup. losa) y cupertina
LOSA = 140                       # losa colaborante: chapa 76 + 64 de hormigón sobre cresta
H_DECK = 76
FUND = -1500                     # fondo de la base aislada
PB = 0

# perfiles adoptados
COL = "HEB200"                   # columna HEB 200 (alas paralelas; pandeo verificado en ambas direcciones)
COLN = "HEB 200"                 # nombre para los textos
BASE, BASE_E = 1600, 450         # base aislada 1,60 x 1,60 x 0,45 m
PL_A, PL_B, PL_E = 380, 250, 20  # placa base (A en el sentido del alma)
PX, PY = 150, 60                 # pernos de anclaje a +-PX (fuera de las alas) y +-PY
VP = 500                         # viga principal de pórtico IPN 500 (luz 12,00 m)
VS = 200                         # viga secundaria y de borde IPN 200 (luz 4,00 m)

# orden de las láminas: clave del dibujo -> (título para el índice, punto de la consigna)
ORDEN = [
    ("sistema", "Sistema adoptado: memoria, planta y corte", "-"),
    ("axo", "Axonometría estructural y listado de elementos", "1"),
    ("fund", "Fundación, pernos, placa base y columna", "1"),
    ("vigas", "Vigas y piezas de unión", "1"),
    ("deck", "Losa colaborante: chapa y piezas", "1"),
    ("arr", "Arriostramiento, bulones, soldadura, fijaciones", "1"),
    ("uesq", "Juntas y uniones: esquema y clasificación", "2"),
    ("u13", "Uniones U1, U2, U3 y funcionamiento", "2"),
    ("u47", "Uniones U4 a U7", "2"),
    ("u810", "Uniones U8 a U10 (cerramientos)", "2"),
    ("maq", "Máquinas y herramientas", "3"),
    ("plan", "Alquiler, armado y acceso a obra", "3"),
    ("cw", "Muro cortina (CW) stick", "4"),
    ("panel", "Panel sándwich 80 mm (integral)", "4"),
    ("comp", "Comparación CW / panel y justificación", "4"),
]
ALIAS = {"deck2": "deck", "fij": "arr", "u12": "u13", "u3": "u13", "maq2": "maq", "cw2": "cw", "caratula": "sistema"}
NUM = {k: i + 1 for i, (k, t, p) in enumerate(ORDEN)}
NUM.update({a: NUM[k] for a, k in ALIAS.items()})
LAMINAS = [(NUM[k], t, p) for k, t, p in ORDEN]


def lam(k):
    return f"{NUM[k]:02d}"
