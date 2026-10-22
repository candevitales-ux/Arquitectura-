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
COL = 300                        # columna IPN 300
VP = 500                         # viga principal de pórtico IPN 500 (luz 12,00 m)
VS = 200                         # viga secundaria y de borde IPN 200 (luz 4,00 m)

# orden de las láminas: clave del dibujo -> (número, título para el índice, punto de la consigna)
ORDEN = [
    ("caratula", "Carátula, consigna e índice", "-"),
    ("sistema", "Sistema adoptado: memoria, planta estructural y corte transversal", "-"),
    ("axo", "Axonometría estructural: elementos del sistema y referencias", "1"),
    ("fund", "Fundación, pernos de anclaje, placa base y columna", "1"),
    ("vigas", "Vigas principales, secundarias, de borde y piezas de unión", "1"),
    ("deck", "Chapa colaborante: perfil, máximos y mínimos, colocación, malla y hormigón", "1"),
    ("deck2", "Conector de corte, cenefa de borde y tapa de cierre", "1"),
    ("arr", "Arriostramiento, bulones y soldadura", "1"),
    ("fij", "Fijaciones de la chapa y protección del acero", "1"),
    ("uesq", "Juntas y uniones: esquema general y clasificación", "2"),
    ("u12", "Uniones U1 y U2: base y viga principal-columna", "2"),
    ("u3", "Unión U3: secundaria-principal y cómo trabajan las uniones", "2"),
    ("u47", "Uniones U4 a U7: losa-viga, chapas, borde de losa, arriostramiento", "2"),
    ("u810", "Uniones U8 a U10: cerramientos a la estructura y cubierta", "2"),
    ("maq", "Grúa, plataformas y soldadora de pernos", "3"),
    ("maq2", "Llaves, fijadora y otros equipos", "3"),
    ("plan", "Planificación: alquiler, armado y acceso a obra", "3"),
    ("cw", "Muro cortina: elevación y corte vertical", "4"),
    ("cw2", "Muro cortina: corte horizontal y elementos", "4"),
    ("panel", "Panel sándwich 80 mm (integral opaco)", "4"),
    ("comp", "Comparación CW vs. panel y justificación", "4"),
]
NUM = {k: i + 1 for i, (k, t, p) in enumerate(ORDEN)}
LAMINAS = [(NUM[k], t, p) for k, t, p in ORDEN]


def lam(k):
    return f"{NUM[k]:02d}"
