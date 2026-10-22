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

LAMINAS = [
    (1, "Sistema adoptado: memoria, planta estructural y corte transversal", "-"),
    (2, "Axonometría estructural: elementos del sistema y referencias", "1"),
    (3, "Elementos 1: fundación, pernos de anclaje, placa base y columna", "1"),
    (4, "Elementos 2: vigas principales, secundarias, de borde y piezas de unión", "1"),
    (5, "Elementos 3: chapa colaborante, conectores, malla, cenefa y cierres", "1"),
    (6, "Elementos 4: arriostramientos, bulones, soldadura, fijaciones y protección", "1"),
    (7, "Juntas y uniones: esquema general y clasificación", "2"),
    (8, "Uniones U1 a U3: base, viga principal-columna, secundaria-principal", "2"),
    (9, "Uniones U4 a U7: losa-viga, chapas, borde de losa, arriostramiento", "2"),
    (10, "Uniones U8 a U10: cerramientos a la estructura y junta de cubierta", "2"),
    (11, "Máquinas y herramientas de montaje, moldeo y anclaje", "3"),
    (12, "Planificación: alquiler, armado y acceso a obra", "3"),
    (13, "Muro exterior vidriado: muro cortina (CW) stick", "4"),
    (14, "Muro exterior opaco: integral panel sándwich 80 mm", "4"),
    (15, "Comparación CW vs. panel y justificación de la elección", "4"),
]
