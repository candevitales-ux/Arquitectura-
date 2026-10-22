# -*- coding: utf-8 -*-
"""Geometría de los elementos del sistema (mm reales), coherente con el TP final (corte integral 1:20 y nudos).
Modulación adoptada: luz VP (perpendicular a fachada) 15,00 m · luz VL / TT (paralela a fachada) 10,00 m · 2 niveles."""

LUZ_X, LUZ_Y = 10000, 15000          # paralela a fachada (VL, TT) / perpendicular (VP)
NIV = {"fund": -2150, "cuello": -510, "pb": 0, "ent": 4500, "cub": 9090}
COL = 400                              # columna 40x40
COL_BOT, COL_TOP = -1300, 8915          # columna premoldeada: empotrada 0,79 m en el cáliz
ENT_TT, CUB_TT = 4415, 8915            # cara superior del TT (entrepiso / cubierta)

# colores por familia (isometrías)
C_COL, C_VL, C_L, C_VP, C_TT, C_FUND, C_CAPA = "#c4cad0", "#a9bccf", "#d3b9b9", "#b9cdb0", "#e3dccb", "#d8cfbd", "#ece6d6"
C_NEO, C_STEEL, C_GROUT = "#262626", "#5a5a5a", "#9a9a9a"


def perfil_VL(x0=0, y0=0):
    """VL doble T 40x70 pretensada (alas 40, alma 12)"""
    P = [(0, 0), (400, 0), (400, 150), (280, 210), (260, 210), (260, 510), (280, 510), (400, 570), (400, 700),
         (0, 700), (0, 570), (120, 510), (140, 510), (140, 210), (120, 210), (0, 150)]
    return [(x0 + x, y0 + y) for x, y in P]


def perfil_L(x0=0, y0=0, flip=False):
    """viga L de borde: talón 40 x 15 + alma 15 x 26 (total)"""
    P = [(0, 0), (400, 0), (400, 150), (150, 150), (150, 260), (0, 260)]
    if flip: P = [(400 - x, y) for x, y in P]
    return [(x0 + x, y0 + y) for x, y in P]


def perfil_VP(x0=0, y0=0):
    """VP T invertida h 75: alma 40, talones 15 x 15 (ancho total 70)"""
    P = [(0, 0), (700, 0), (700, 150), (550, 150), (550, 750), (150, 750), (150, 150), (0, 150)]
    return [(x0 + x, y0 + y) for x, y in P]


def perfil_TT(x0=0, y0=0, dap=0):
    """panel TT 2,40 x 0,65: ala 5 cm, nervios 18/12 a 1,20 entre ejes (x0 = borde izq., y0 = fondo de nervio).
    dap: rebaje del nervio en el apoyo (extremo del panel)"""
    b = dap
    P = [(0, 600), (510, 600), (540 + b * 0.05, b), (660 - b * 0.05, b), (690, 600), (1710, 600), (1740 + b * 0.05, b), (1860 - b * 0.05, b),
         (1890, 600), (2400, 600), (2400, 650), (0, 650)]
    return [(x0 + x, y0 + y) for x, y in P]


def mensula_pts(side=1, alto_raiz=470, frente=160, saliente=330):
    """ménsula corta con diagonal, en el plano (u = saliente desde la cara de columna, v relativo a la cara superior)"""
    return [(0, 0), (side * saliente, 0), (side * saliente, -frente), (0, -alto_raiz)]


# ------------------------------------------------------------------ escena isométrica de la estructura
def estructura(S, nx=2, ny=1, niveles=("ent", "cub"), quitar=(), fund=True, tt_parcial=None, vl_y=(0,), cortar_cub=False):
    """columnas en grilla (x = i*LUZ_X, y = j*LUZ_Y), z arriba. Fachada principal en y = 0 (VL + muro)."""
    import itertools
    cols = [(i * LUZ_X, j * LUZ_Y) for i in range(nx + 1) for j in range(ny + 1)]
    h = COL / 2
    for (cx, cy) in cols:
        if fund:
            S.box(cx - 1000, cx + 1000, cy - 1000, cy + 1000, -2050, -1750, C_FUND)
            S.box(cx - 525, cx + 525, cy - 525, cy + 525, -1750, -510, C_FUND)
        S.box(cx - h, cx + h, cy - h, cy + h, -510, COL_TOP, C_COL)
    for nv in niveles:
        yt = ENT_TT if nv == "ent" else CUB_TT
        # VP (eje y) en cada línea de columnas: T invertida, cara superior = yt, alma centrada en columna
        for i in range(nx + 1):
            cx = i * LUZ_X
            for j in range(ny):
                y0, y1 = j * LUZ_Y + h + 10, (j + 1) * LUZ_Y - h - 10
                if ("VP", i, j, nv) in quitar: continue
                tal = [(-350, 0), (350, 0), (350, 150), (200, 150), (200, 750), (-200, 750), (-200, 150), (-350, 150)]
                if i == 0: tal = [(-200, 0), (350, 0), (350, 150), (200, 150), (200, 750), (-200, 750)]
                if i == nx: tal = [(-350, 0), (200, 0), (200, 750), (-200, 750), (-200, 150), (-350, 150)]
                S.prism([(cx + u, yt - 750 + v) for u, v in tal], "y", y0, y1, C_VP)
                # ménsulas VP
                for (yy, sd) in ((j * LUZ_Y + h, 1), ((j + 1) * LUZ_Y - h, -1)):
                    S.prism([(yy + u * sd / abs(sd), yt - 760 + v) for u, v in mensula_pts(1, saliente=350)], "x", cx - h, cx + h, C_COL)
        # VL + viga L en fachada(s)
        for j in vl_y:
            cy = j * LUZ_Y
            for i in range(nx):
                x0, x1 = i * LUZ_X + h + 10, (i + 1) * LUZ_X - h - 10
                if ("VL", i, j, nv) in quitar: continue
                S.prism([(cy - h + u, yt - 910 + v) for u, v in perfil_VL()], "x", x0, x1, C_VL)
                lp = perfil_L(flip=(j > 0))
                S.prism([(cy - h + u, yt - 210 + v) for u, v in lp], "x", x0, x1, C_L)
                for (xx, sd) in ((i * LUZ_X + h, 1), ((i + 1) * LUZ_X - h, -1)):
                    S.prism([(xx + u * sd, yt - 920 + v) for u, v in mensula_pts(1)], "y", cy - h, cy + h, C_COL)
        # paneles TT (luz en x, ancho 2,40 en y)
        for i in range(nx):
            x0, x1 = i * LUZ_X + 210, (i + 1) * LUZ_X - 210
            for j in range(ny):
                ya = j * LUZ_Y - h + 170
                k = 0
                yy = ya
                while yy + 2400 <= (j + 1) * LUZ_Y + 50:
                    if ("TT", i, j, k, nv) not in quitar and not (tt_parcial and tt_parcial(i, j, k, nv)):
                        S.prism([(yy + u, yt - 650 + v) for u, v in perfil_TT()], "x", x0 + 150, x1 - 150, C_TT)
                        for (a, b_) in ((x0, x0 + 150), (x1 - 150, x1)):
                            S.prism([(yy + u, yt - 650 + v) for u, v in perfil_TT(dap=50)], "x", a, b_, C_TT)
                    yy += 2410; k += 1
    return cols
