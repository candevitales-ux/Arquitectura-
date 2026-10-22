# -*- coding: utf-8 -*-
"""Lámina 03 – E3 viga VL doble T, E4 viga L de borde, E5 viga VP T invertida."""
from lib import Sheet, Iso, spec, heading, breakline, REB
import geo

VISTA = "#eceeef"


def elev_col(v, x, y_top_m, side, frente=160, raiz=470, sal=330):
    """tramo de columna con ménsula (vista) en una elevación"""
    v.rect(x - 400 if side > 0 else x, y_top_m - 1300, x if side > 0 else x + 400, y_top_m + 1300, fill=VISTA, sw=0.2)
    v.poly([(x, y_top_m), (x + side * sal, y_top_m), (x + side * sal, y_top_m - frente), (x, y_top_m - raiz)], fill=VISTA, sw=0.2)


def make(num, total):
    sh = Sheet(num, total, "Elementos constructivos 2", "E3 Viga VL doble T · E4 Viga L de borde · E5 Viga VP T invertida",
               "Elevaciones 1:150 · secciones 1:20 · isometrías 1:50")
    heading(sh, "1º ELEMENTOS CONSTRUCTIVOS DEL SISTEMA  ·  2/3", "Vigas premoldeadas pretensadas: VL de fachada (+ viga L de borde) y VP portante principal")

    # ============================================================ ELEVACIONES 1:150
    sh.title_drawing(10, 26, "ELEVACIONES 1:150", None, 2.3)
    # VL + L
    v = sh.view(16, 44, 150)
    L = 9580
    elev_col(v, 0, 0, 1); elev_col(v, L + 20, 0, -1)
    v.rect(10, 10, L + 10, 710, fill="#dfe6ee", sw=0.3)
    v.rect(10, 710, L + 10, 970, fill="#ecdede", sw=0.3)
    v.line(10, 160, L + 10, 160, sw=0.1); v.line(10, 560, L + 10, 560, sw=0.1)
    v.line(10, 55, L + 10, 55, stroke=REB, sw=0.12, dash="1 0.5")
    for x in (170, L - 150): v.line(x, -250, x, 180, sw=0.1, dash="0.6 0.3")
    v.dim((10, 970), (L + 10, 970), 2.5, "9,58 (VL y L)")
    v.dim((L + 10, 10), (L + 10, 710), -6.0, "0,70", size=1.4)
    v.dim((L + 10, 710), (L + 10, 970), -6.0, "0,26", size=1.4)
    sh.text(16 + L / 300, 52.5, "VL doble T 40x70 + viga L de borde (encima)", 1.6, anchor="middle", bold=True)
    sh.note(v.P(3000, 55), (40, 58.5), "cordones de pretensado", 1.35)
    # VP
    v = sh.view(110, 44, 150)
    L2 = 14580
    elev_col(v, 0, 0, 1, sal=350); elev_col(v, L2 + 20, 0, -1, sal=350)
    v.rect(10, 10, L2 + 10, 760, fill="#e2ecdc", sw=0.3)
    v.line(10, 160, L2 + 10, 160, sw=0.1)
    v.line(10, 55, L2 + 10, 55, stroke=REB, sw=0.12, dash="1 0.5")
    for x in (175, L2 - 155): v.line(x, -250, x, 180, sw=0.1, dash="0.6 0.3")
    for x in range(10 + 1200, L2, 2410):
        v.rect(x - 90, 170, x + 90, 760, fill="none", sw=0.08, dash="0.6 0.3")
    v.dim((10, 760), (L2 + 10, 760), 2.5, "14,58 (luz entre ejes 15,00)")
    v.dim((L2 + 10, 10), (L2 + 10, 760), -6.0, "0,75", size=1.4)
    sh.text(110 + L2 / 300, 52.5, "VP T invertida h 0,75 · en trazos: nervios de TT apoyados en los talones", 1.6, anchor="middle", bold=True)
    # columna de rangos (catálogo)
    sh.text(222, 26, "RANGOS DE CATÁLOGO (orientativo)", 2.0, bold=True)
    rows = [("Pieza", "h (m)", "Luz usual", "Peso"),
            ("VL doble T", "0,50-1,20", "6-18 m", "0,45 t/m"),
            ("Viga L borde", "0,26-0,60", "5-12 m", "0,19 t/m"),
            ("VP T invert.", "0,60-1,40", "8-20 m", "0,86 t/m"),
            ("Esbeltez", "h ≈ L/15 a L/20", "", "")]
    sh.table(222, 28.5, [17, 18, 14, 16], rows, size=1.45, rowh=3.1)

    # ============================================================ SECCIONES 1:20
    sh.title_drawing(10, 66, "SECCIONES TRANSVERSALES 1:20", None, 2.3)
    # VL + L
    s = sh.view(18, 128, 20)
    s.poly(geo.perfil_VL(), mat="HA", sw=0.35)
    s.rect(0, 700, 400, 708, mat="grout", sw=0.1)
    s.poly(geo.perfil_L(0, 708), mat="HA", sw=0.35)
    for x in (45, 125, 200, 275, 355): s.dot(x, 45, 0.42, "#000")
    for x in (160, 240): s.dot(x, 100, 0.42, "#000")
    for x in (45, 200, 355): s.dot(x, 655, 0.33)
    s.pline([(150, 30), (150, 670)], stroke=REB, sw=0.12); s.pline([(250, 30), (250, 670)], stroke=REB, sw=0.12)
    for x in (80, 270): s.line(x, 580, x, 830, stroke=REB, sw=0.28)
    s.pline([(70, 800), (70, 990), (390, 990)], stroke=REB, sw=0.22)
    s.poly([(0, 384), (42, 384), (42, 436), (0, 436), (0, 428), (34, 428), (34, 392), (0, 392)], mat="acero", sw=0.05)
    s.rect(0, -10, 400, 0, mat="neo", stroke=None)
    s.dim((0, 0), (400, 0), -2.5, "0,40", size=1.4)
    s.dim((400, 0), (400, 700), -2.5, "0,70", size=1.4)
    s.dim((400, 708), (400, 858), -2.5, "0,15", size=1.3)
    s.dim((0, 968), (150, 968), 2.0, "0,15", size=1.3)
    s.dim((0, 708), (0, 968), 2.5, "0,26", size=1.3)
    s.dim((140, 350), (260, 350), 1.2, "0,12", size=1.2)
    s.dim((0, 560), (0, 700), 6.0, "0,15", size=1.2)
    R = [("1", (300, 350), "VL doble T 40x70 pretensada (E3)"), ("2", (200, 45), "Cordones Ø12,7 (7 inf. + 2)"),
         ("3", (300, 800), "Viga L de borde: talón 40x15 + alma 15x26 (E4)"), ("4", (300, 704), "Junta VL / L c/ mortero"),
         ("5", (80, 800), "Barras de vinculación Ø12 (en grout)"), ("6", (70, 980), "Estribos salientes 2Ø10 (anclan la capa)"),
         ("7", (20, 410), "Riel de anclaje embutido (grapas muro cortina)"), ("8", (200, -5), "Neopreno 10 mm s/ ménsula")]
    for i, (lab, tgt, txt) in enumerate(R):
        at = (50, 84 + i * 4.6)
        sh.callout(s.P(*tgt), at, lab, r=1.5)
        sh.text(53, at[1] + 0.6, txt, 1.45)
    # VP
    s = sh.view(122, 128, 20)
    s.poly(geo.perfil_VP(), mat="HA", sw=0.35)
    for x in (40, 110, 590, 660): s.dot(x, 45, 0.42, "#000")
    for x in (200, 280, 350, 420, 500): s.dot(x, 45, 0.42, "#000")
    for x in (200, 280, 350, 420, 500): s.dot(x, 105, 0.42, "#000")
    for x in (200, 500): s.dot(x, 705, 0.33)
    s.pline([(190, 30), (190, 720), (510, 720), (510, 30)], stroke=REB, sw=0.12)
    s.pline([(25, 120), (25, 30), (675, 30), (675, 120)], stroke=REB, sw=0.12)
    for xs in (0, 550):
        s.rect(xs + 10, 150, xs + 140, 160, mat="neo", stroke=None)
    for sd, xe, xf in ((-1, 140, -480), (1, 560, 1180)):
        s.poly([(xf, 750), (xe, 750), (xe, 160), (xe + sd * 150, 160), (xe + sd * 150, 100), (xf, 100)], fill="#f1efe8", sw=0.12, dash="0.7 0.35")
        s.line(xf, 700, xe, 700, sw=0.08, dash="0.5 0.3")
    s.rect(150, 750, 550, 800, mat="HAis", sw=0.2)
    s.dim((0, 0), (700, 0), -2.5, "0,70", size=1.4)
    s.dim((150, 750), (550, 750), 4.5, "0,40", size=1.3)
    s.dim((700, 0), (700, 750), -2.5, "0,75", size=1.4)
    s.dim((0, 0), (0, 150), 2.5, "0,15", size=1.3)
    s.dim((0, 150), (150, 150), -1.8, "0,15", size=1.2)
    R = [("1", (350, 400), "VP T invertida h 0,75 pretensada (E5)"), ("2", (350, 45), "Cordones Ø12,7 (14) en talón y alma"),
         ("3", (75, 155), "Talón 15x15: apoyo de los nervios TT"), ("4", (620, 155), "Neopreno 10 mm (nervio TT / talón)"),
         ("5", (-250, 400), "Extremo del TT: nervio c/ rebaje s/ talón"), ("6", (350, 775), "Capa de compresión in situ (continuidad)")]
    for i, (lab, tgt, txt) in enumerate(R):
        at = (165, 84 + i * 4.6)
        sh.callout(s.P(*tgt), at, lab, r=1.5)
        sh.text(168, at[1] + 0.6, txt, 1.45)

    # ============================================================ ISOMETRÍAS 1:50
    sh.text(222, 66, "Isometrías 1:50 (tramo de 1,50 m)", 1.7, bold=True)
    S = Iso((1, -1, 1))
    S.prism(geo.perfil_VL(), "x", 0, 1500, geo.C_VL, sw=0.12)
    S.prism(geo.perfil_L(0, 708), "x", 0, 1500, geo.C_L, sw=0.12)
    ox, oy = S.fit((222, 68, 254, 106), 50); S.draw(sh, ox, oy, 50)
    sh.text(238, 109, "E3 VL + E4 L", 1.5, anchor="middle", bold=True)
    S = Iso((1, -1, 1))
    S.prism(geo.perfil_VP(), "x", 0, 1500, geo.C_VP, sw=0.12)
    ox, oy = S.fit((257, 68, 289, 106), 50); S.draw(sh, ox, oy, 50)
    sh.text(273, 109, "E5 VP", 1.5, anchor="middle", bold=True)

    # ============================================================ ESPECIFICACIONES
    y0 = 146
    spec(sh, 10, y0, 88, "E3 · Viga VL doble T 40x70", [
        ("Función:", "viga perimetral de fachada: atar las columnas, recibir la viga L y el cerramiento (riel p/ grapas del muro cortina o bulones del panel)."),
        ("Medidas:", "b 0,40 · h 0,70 · alas 0,15 · alma 0,12 · largo 9,58 m · ≈ 4,4 t."),
        ("Especificación:", "H-45, pretensado c/ 9 cordones Ø12,7; apoyo s/ neopreno 10 mm y 2 pernos Ø20 en vainas c/ grout (antivuelco)."),
        ("Colocación:", "izado c/ balancín por 2 insertos a L/5 de los extremos; apoyo mín. 15 cm en la ménsula."),
    ], size=1.5, tsize=2.0)
    spec(sh, 103, y0, 88, "E4 · Viga L de borde", [
        ("Función:", "completar la altura hasta el nivel de losa, recibir el ala del TT en su talón y confinar la capa de compresión en el borde."),
        ("Medidas:", "talón 0,40 x 0,15 + alma 0,15 x 0,26 · largo 9,58 m · ≈ 1,8 t."),
        ("Especificación:", "H-40 armado; barras de vinculación Ø12 a la VL en grout; estribos salientes 2Ø10."),
        ("Colocación:", "se monta sobre la VL ya fijada, con cama de mortero 8 mm; luego se colocan los TT."),
    ], size=1.5, tsize=2.0)
    spec(sh, 196, y0, 93, "E5 · Viga VP T invertida h 0,75", [
        ("Función:", "viga PORTANTE principal (perpendicular a fachada): recibe los paneles TT en sus talones y descarga en las ménsulas de columna."),
        ("Medidas:", "alma 0,40 · talones 0,15 x 0,15 · ancho 0,70 · h 0,75 · L 14,58 m · ≈ 12,6 t (pieza más pesada de la obra)."),
        ("Especificación:", "H-45, pretensado c/ 23 cordones Ø12,7; contraflecha de pretensado ≈ L/500; neopreno + perno Ø20 en cada apoyo."),
        ("Colocación:", "transporte en carretón (> 12 m); izado c/ balancín y 2 eslingas; montaje simétrico de TT a ambos lados para evitar torsión."),
    ], size=1.5, tsize=2.0)
    return sh
