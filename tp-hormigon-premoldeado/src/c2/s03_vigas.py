# -*- coding: utf-8 -*-
"""E3 viga VL doble T + E4 viga L de borde (una lámina) y E5 viga VP T invertida (otra lámina)."""
from lib import Sheet, Iso, page, spec, heading, breakline, REB, TB, TS, TD, TT
from s02_fundacion_columna import legend
import geo

VISTA = "#eceeef"


def elev_col(v, x, y_top_m, side, frente=160, raiz=470, sal=330):
    v.rect(x - 400 if side > 0 else x, y_top_m - 1300, x if side > 0 else x + 400, y_top_m + 1300, fill=VISTA, sw=0.2)
    v.poly([(x, y_top_m), (x + side * sal, y_top_m), (x + side * sal, y_top_m - frente), (x, y_top_m - raiz)], fill=VISTA, sw=0.2)


@page("E3 · Viga VL doble T + E4 · Viga L de borde")
def vl(num, total):
    sh = Sheet(num, total, "E3 · Viga VL + E4 · Viga L de borde", escalas="elevación 1:100 · sección 1:10 · isometría 1:50", fname="E3_E4_Viga_VL_y_L")
    heading(sh, "1º ELEMENTOS · E3 VIGA VL DOBLE T + E4 VIGA L DE BORDE", "Viga perimetral de fachada pretensada y viga L premoldeada montada encima (recibe el borde del panel TT)")
    sh.title_drawing(12, 32, "ELEVACIÓN", "esc. 1:100", TT)
    v = sh.view(24, 60, 100)
    L = 9580
    elev_col(v, 0, 0, 1); elev_col(v, L + 20, 0, -1)
    v.rect(10, 10, L + 10, 710, fill="#dfe6ee", sw=0.3)
    v.rect(10, 710, L + 10, 970, fill="#ecdede", sw=0.3)
    v.line(10, 160, L + 10, 160, sw=0.1); v.line(10, 560, L + 10, 560, sw=0.1)
    v.line(10, 55, L + 10, 55, stroke=REB, sw=0.15, dash="1 0.5")
    v.dim((10, 970), (L + 10, 970), 3.5, "9,58")
    v.dim((L + 400, 10), (L + 400, 710), -4.0, "0,70")
    v.dim((L + 400, 710), (L + 400, 970), -4.0, "0,26")
    sh.note(v.P(3000, 55), (40, 78), "cordones de pretensado (VL)")
    sh.note(v.P(6000, 840), (80, 42), "viga L de borde (E4)")
    # isometría
    S = Iso((1, -1, 1))
    S.prism(geo.perfil_VL(), "x", 0, 1500, geo.C_VL, sw=0.12)
    S.prism(geo.perfil_L(0, 708), "x", 0, 1500, geo.C_L, sw=0.12)
    ox, oy = S.fit((146, 40, 200, 82), 50); S.draw(sh, ox, oy, 50)
    sh.text(146, 32, "ISOMETRÍA", TT, bold=True); sh.text(146, 37, "esc. 1:50 · tramo 1,50 m", TS)
    # sección 1:10
    sh.title_drawing(12, 88, "SECCIÓN TRANSVERSAL", "esc. 1:10", TT)
    s = sh.view(26, 197, 10)
    s.poly(geo.perfil_VL(), mat="HA", sw=0.4)
    s.rect(0, 700, 400, 708, mat="grout", sw=0.1)
    s.poly(geo.perfil_L(0, 708), mat="HA", sw=0.4)
    for x in (45, 125, 200, 275, 355): s.dot(x, 45, 0.7, "#000")
    for x in (160, 240): s.dot(x, 100, 0.7, "#000")
    for x in (45, 200, 355): s.dot(x, 655, 0.55)
    s.pline([(150, 30), (150, 670)], stroke=REB, sw=0.15); s.pline([(250, 30), (250, 670)], stroke=REB, sw=0.15)
    for x in (80, 270): s.line(x, 580, x, 830, stroke=REB, sw=0.4)
    s.pline([(70, 800), (70, 990), (390, 990)], stroke=REB, sw=0.3)
    s.poly([(0, 384), (42, 384), (42, 436), (0, 436), (0, 428), (34, 428), (34, 392), (0, 392)], mat="acero", sw=0.05)
    s.rect(0, -10, 400, 0, mat="neo", stroke=None)
    s.dim((0, 0), (400, 0), -4.0, "0,40")
    s.dim((0, 0), (0, 700), 6.0, "0,70")
    s.dim((400, 708), (400, 858), -3.0, "0,15")
    s.dim((0, 968), (150, 968), 3.0, "0,15")
    s.dim((0, 708), (0, 968), 6.0, "0,26")
    s.dim((140, 330), (260, 330), 0, "0,12")
    R = [("1", (300, 350), "VL doble T 40x70 pretensada (E3)"), ("2", (200, 45), "Cordones Ø12,7 (7 inf. + 2 sup.)"),
         ("3", (300, 800), "Viga L de borde: talón 40x15 + alma 15x26 (E4)"), ("4", (300, 704), "Junta VL / L c/ mortero 8 mm"),
         ("5", (80, 800), "Barras de vinculación Ø12 (en grout)"), ("6", (230, 990), "Estribos salientes 2Ø10 (anclan la capa)"),
         ("7", (20, 410), "Riel embutido (grapas del muro cortina)"), ("8", (200, -5), "Neopreno 10 mm s/ ménsula")]
    for i, (lab, tgt, txt) in enumerate(R):
        at = (82, 102 + i * 11)
        sh.callout(s.P(*tgt), at, lab)
        sh.para(87, at[1] + 0.9, 112, txt, TB, 1.25)
    y = 210
    y = spec(sh, 12, y, 186, "E3 · VIGA VL DOBLE T 40x70", [
        ("Función:", "viga perimetral de fachada: ata las columnas y recibe la viga L y el cerramiento (riel p/ grapas o bulones del panel)."),
        ("Medidas / peso:", "0,40 x 0,70 · alas 0,15 · alma 0,12 · L 9,58 m · ≈ 4,4 t · catálogo h 0,50-1,20 p/ luces de 6-18 m."),
        ("Colocación:", "izado c/ balancín a L/5; apoyo ≥ 15 cm s/ neopreno + 2 pernos Ø20 en vainas c/ grout (antivuelco)."),
    ], size=TB, tsize=2.9)
    spec(sh, 12, y + 2, 186, "E4 · VIGA L DE BORDE", [
        ("Función:", "completa la altura hasta la losa, recibe el ala del TT en su talón y confina la capa en el borde."),
        ("Medidas / colocación:", "talón 0,40 x 0,15 + alma 0,15 x 0,26 · ≈ 1,8 t · s/ la VL con cama de mortero y barras Ø12 en grout."),
    ], size=TB, tsize=2.9)
    return sh


@page("E5 · Viga VP T invertida")
def vp(num, total):
    sh = Sheet(num, total, "E5 · Viga VP T invertida", escalas="elevación 1:100 · sección 1:10 · isometría 1:50", fname="E5_Viga_VP")
    heading(sh, "1º ELEMENTOS · E5 VIGA VP T INVERTIDA h 0,75", "Viga portante principal pretensada (perpendicular a la fachada): recibe los paneles TT en sus talones")
    sh.title_drawing(12, 32, "ELEVACIÓN", "esc. 1:100 · en trazos: nervios de los TT apoyados en los talones", TT)
    v = sh.view(18, 64, 100)
    L2 = 14580
    elev_col(v, 0, 0, 1, sal=350); elev_col(v, L2 + 20, 0, -1, sal=350)
    v.rect(10, 10, L2 + 10, 760, fill="#e2ecdc", sw=0.3)
    v.line(10, 160, L2 + 10, 160, sw=0.1)
    v.line(10, 55, L2 + 10, 55, stroke=REB, sw=0.15, dash="1 0.5")
    for x in range(10 + 1200, L2, 2410):
        v.rect(x - 90, 170, x + 90, 760, fill="none", sw=0.1, dash="0.6 0.3")
    v.dim((10, 760), (L2 + 10, 760), 3.5, "14,58 (luz entre ejes 15,00)")
    v.dim((L2 + 420, 10), (L2 + 420, 760), -4.0, "0,75")
    # sección 1:10
    sh.title_drawing(12, 84, "SECCIÓN TRANSVERSAL", "esc. 1:10", TT)
    s = sh.view(52, 172, 10)
    s.poly(geo.perfil_VP(), mat="HA", sw=0.4)
    for x in (40, 110, 590, 660): s.dot(x, 45, 0.7, "#000")
    for x in (200, 280, 350, 420, 500):
        s.dot(x, 45, 0.7, "#000"); s.dot(x, 105, 0.7, "#000")
    for x in (200, 500): s.dot(x, 705, 0.55)
    s.pline([(190, 30), (190, 720), (510, 720), (510, 30)], stroke=REB, sw=0.15)
    s.pline([(25, 120), (25, 30), (675, 30), (675, 120)], stroke=REB, sw=0.15)
    for xs in (0, 550): s.rect(xs + 10, 150, xs + 140, 160, mat="neo", stroke=None)
    for sd, xe, xf in ((-1, 140, -280), (1, 560, 980)):
        s.poly([(xf, 750), (xe, 750), (xe, 160), (xe + sd * 150, 160), (xe + sd * 150, 100), (xf, 100)], fill="none", sw=0.2, dash="1 0.5")
        breakline(sh, s.P(xf, 80), s.P(xf, 770))
    s.rect(-280, 750, 980, 800, mat="HAis", sw=0.2)
    s.dim((0, 0), (700, 0), -4.0, "0,70")
    s.dim((150, 800), (550, 800), 3.5, "0,40")
    s.dim((980, 0), (980, 750), -4.0, "0,75")
    s.dim((0, 0), (0, 150), 7.0, "0,15")
    R = [("1", (350, 400), "VP T invertida h 0,75 pretensada (E5)"), ("2", (350, 45), "Cordones Ø12,7 (14) en talón y alma"),
         ("3", (75, 155), "Talones 15x15: apoyo de los nervios TT"), ("4", (620, 155), "Neopreno 10 mm (nervio TT / talón)"),
         ("5", (-200, 400), "Extremo del TT: nervio c/ rebaje (dap)"), ("6", (800, 775), "Capa de compresión in situ (continuidad)")]
    for lab, tgt, at in zip("123456", [r[1] for r in R], [(160, 132), (160, 170), (30, 170), (160, 158), (22, 120), (160, 96)]):
        sh.callout(s.P(*tgt), at, lab)
    y = legend(sh, 12, 182, [f"{a} {c}" for a, b, c in R])
    # isometría
    S = Iso((1, -1, 1))
    S.prism(geo.perfil_VP(), "x", 0, 1500, geo.C_VP, sw=0.12)
    ox, oy = S.fit((166, 100, 200, 150), 50); S.draw(sh, ox, oy, 50)
    sh.text(166, 92, "ISOMETRÍA", TT, bold=True); sh.text(166, 97, "1:50", TS)
    y = spec(sh, 12, y + 3, 186, "ESPECIFICACIÓN", [
        ("Función:", "viga PORTANTE principal: recibe los TT en sus talones y descarga en las ménsulas de las columnas."),
        ("Medidas / peso:", "ancho 0,70 (alma 0,40) · h 0,75 · L 14,58 m · ≈ 12,6 t (pieza más pesada de la obra)."),
        ("Especificación:", "H-45, 23 cordones Ø12,7; contraflecha ≈ L/500; neopreno + perno Ø20 en cada apoyo."),
        ("Colocación:", "llega en carretón (> 12 m); izado c/ balancín; se montan los TT simétricos a ambos lados (evita torsión)."),
    ], size=TB, tsize=2.9)
    rows = [("Rango de catálogo", "h (m)", "Luz usual", "Peso"), ("VL doble T", "0,50-1,20", "6-18 m", "0,45 t/m"),
            ("Viga L de borde", "0,26-0,60", "5-12 m", "0,19 t/m"), ("VP T invertida", "0,60-1,40", "8-20 m", "0,86 t/m")]
    sh.table(12, y + 2, [60, 40, 40, 46], rows, size=TS, rowh=4.6)
    return sh


PAGES = [vl, vp]
