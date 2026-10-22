# -*- coding: utf-8 -*-
"""Lámina 04 – E6 panel TT, E7 capa de compresión, E8 apoyos y conectores."""
from lib import Sheet, Iso, spec, heading, breakline, REB
import geo

VISTA = "#eceeef"


def make(num, total):
    sh = Sheet(num, total, "Elementos constructivos 3", "E6 Panel TT h 0,65 · E7 Capa de compresión · E8 Apoyos y conectores",
               "Sección TT 1:20 · elevación y planta 1:100 · accesorios 1:5 a 1:20 · isometría 1:75")
    heading(sh, "1º ELEMENTOS CONSTRUCTIVOS DEL SISTEMA  ·  3/3", "Panel TT pretensado de entrepiso y cubierta, capa de compresión in situ y piezas de apoyo / vinculación")

    # ============================================================ SECCIÓN TT 1:20
    sh.title_drawing(10, 26, "E6 · PANEL TT 2,40 x 0,65  +  E7 CAPA", "Sección transversal 1:20", 2.3)
    s = sh.view(16, 72, 20)
    s.poly(geo.perfil_TT(), mat="HA", sw=0.35)
    s.rect(0, 650, 2400, 700, mat="HAis", sw=0.3)
    s.pline([(20, 675), (2380, 675)], stroke=REB, sw=0.14, dash="1.6 0.4")
    for x in range(75, 2400, 150): s.dot(x, 675, 0.2)
    s.pline([(20, 625), (2380, 625)], stroke=REB, sw=0.1)
    for xc in (600, 1800):
        for y in (40, 90, 140): s.dot(xc, y, 0.4, "#000")
        s.line(xc, 30, xc, 620, stroke=REB, sw=0.1)
    s.dim((0, 0), (2400, 0), -6.0, "2,40")
    s.dim((0, 0), (600, 0), -2.5, "0,60", size=1.4); s.dim((600, 0), (1800, 0), -2.5, "1,20", size=1.4); s.dim((1800, 0), (2400, 0), -2.5, "0,60", size=1.4)
    s.dim((2400, 0), (2400, 650), -3.0, "0,65", size=1.4)
    s.dim((2400, 600), (2400, 650), -7.0, "0,05", size=1.2)
    s.dim((2400, 650), (2400, 700), -7.0, "0,05", size=1.2)
    s.dim((510, 600), (690, 600), 1.5, "0,18", size=1.2)
    for lab, tgt, at in (("1", (1200, 625), (78, 31)), ("2", (1800, 90), (98, 52)), ("3", (900, 675), (60, 31)),
                         ("4", (300, 690), (40, 31)), ("5", (600, 400), (26, 52))):
        sh.callout(s.P(*tgt), at, lab, r=1.5)
    yy = 80
    for t in ("1 Ala 5 cm c/ malla Ø6 c/20 (superficie rugosa p/ adherir la capa)", "2 Nervio 18/12 c/ 3 cordones Ø12,7 pretensados",
              "3 Capa de compresión H-25 in situ e = 5 cm (E7)", "4 Malla soldada Ø6 c/15 x 15", "5 Estribos / conectores salientes Ø6 en nervios"):
        sh.text(12, yy, t, 1.5); yy += 2.6

    # ============================================================ ELEVACIÓN Y PLANTA 1:100
    sh.text(12, 98, "Elevación longitudinal y planta 1:100", 1.6, bold=True)
    v = sh.view(14, 110, 100)
    L = 9580
    v.poly([(0, 650), (L, 650), (L, 50), (L - 150, 50), (L - 150, 0), (150, 0), (150, 50), (0, 50)], fill=VISTA, sw=0.3)
    v.line(0, 600, L, 600, sw=0.1)
    v.rect(-200, -300, 0 - 10, 700, fill="#e2ecdc", sw=0.15, dash="0.6 0.3"); v.rect(L + 10, -300, L + 200, 700, fill="#e2ecdc", sw=0.15, dash="0.6 0.3")
    for x in (2000, L - 2000):
        v.circle(x, 600, 60, sw=0.12)
    v.dim((0, 650), (L, 650), 2.0, "9,58 (luz de cálculo ≈ 9,40)")
    v.dim((0, 0), (150, 0), -2.0, "0,15", size=1.2)
    sh.note(v.P(2000, 600), (40, 103), "inserto de izaje (4 por panel, a L/5)", 1.3)
    sh.note(v.P(L - 75, 25), (100, 117.5), "rebaje (dap) s/ talón VP", 1.3)
    p = sh.view(14, 143, 100)
    p.rect(0, 0, L, 2400, fill=VISTA, sw=0.3)
    for y in (540, 660, 1740, 1860): p.line(150, y, L - 150, y, sw=0.08, dash="0.6 0.3")
    p.dim((L, 0), (L, 2400), -2.0, "2,40", size=1.3)
    sh.text(12, 147, "VP en trazos a ambos extremos · nervios en trazos (vista desde arriba)", 1.3, ital=True, color="#333")

    # ============================================================ ISOMETRÍA TT
    S = Iso((1, -1, 1))
    S.prism(geo.perfil_TT(), "x", 150, 3000, geo.C_TT, sw=0.12)
    S.prism(geo.perfil_TT(dap=50), "x", 0, 150, geo.C_TT, sw=0.12)
    ox, oy = S.fit((116, 84, 170, 140), 75); S.draw(sh, ox, oy, 75)
    sh.text(143, 147, "Isometría 1:75 (extremo c/ rebaje)", 1.45, anchor="middle", bold=True)

    # ============================================================ E8 ACCESORIOS
    sh.title_drawing(176, 26, "E8 · APOYOS Y CONECTORES", None, 2.3)
    # neopreno 1:10
    sh.text(176, 32.5, "a) Neopreno zunchado 1:10", 1.55, bold=True)
    n = sh.view(180, 53, 10)
    n.rect(0, 0, 300, 150, fill="#3a3a3a", sw=0.25)
    for y in (40, 75, 110): n.line(5, y, 295, y, stroke="#aaa", sw=0.1)
    n.dim((0, 0), (300, 0), -2.0, "0,30 (≈ ancho de la viga)", size=1.3)
    n.dim((300, 0), (300, 150), -2.0, "0,15", size=1.3)
    sh.text(176, 60.5, "Placa dureza 60 Shore A, e = 10 mm,", 1.35); sh.text(176, 62.8, "c/ chapas de acero; σ adm ≈ 7-10 MPa", 1.35)
    # perno y vaina 1:10
    sh.text(234, 32.5, "b) Perno Ø20 + vaina Ø40 1:20", 1.55, bold=True)
    q = sh.view(246, 52, 20)
    q.rect(-120, -150, 120, 0, mat="HA", sw=0.2); q.rect(-120, 10, 120, 200, mat="HA", sw=0.2)
    q.rect(-120, 0, 120, 10, mat="neo", stroke=None)
    q.rect(-20, 10, 20, 190, mat="grout", sw=0.1)
    q.rect(-10, -140, 10, 170, mat="acero", sw=0.05)
    q.line(-40, -140, 40, -140, sw=0.4)
    sh.note(q.P(0, 100), (256, 39), "vaina rellena c/ grout", 1.3)
    sh.note(q.P(0, -60), (256, 57), "perno anclado en ménsula", 1.3)
    sh.text(282, 57.5, "", 1.3)
    # riel embutido 1:5
    sh.text(176, 74, "c) Riel de anclaje embutido 1:5", 1.55, bold=True)
    r = sh.view(186, 92, 5)
    r.rect(0, -60, 70, 60, mat="HA", stroke=None)
    r.poly([(0, -26), (42, -26), (42, 26), (0, 26), (0, 18), (34, 18), (34, -18), (0, -18)], mat="acero", sw=0.06)
    for dy in (-22, 22): r.line(42, dy, 100, dy, sw=0.3)
    r.rect(8, -8, 34, 8, fill="#666", sw=0.08); r.line(-25, 0, 20, 0, sw=0.5)
    r.dim((0, 26), (0, -26), 2.0, "52 mm", size=1.2)
    sh.text(176, 109, "Perfil C 52/34 galv. + bulón T M12;", 1.35); sh.text(176, 111.3, "regulación lateral de la grapa ± 25 mm", 1.35)
    # inserto de izaje 1:5
    sh.text(234, 74, "d) Inserto de izaje 1:10", 1.55, bold=True)
    z = sh.view(244, 92, 10)
    z.rect(-80, -120, 80, 0, mat="HA", stroke=None)
    z.rect(-12, -100, 12, 0, mat="acero", sw=0.05)
    z.rect(-30, -110, 30, -100, mat="acero", sw=0.05)
    z.circle(0, 20, 18, sw=0.3); z.line(0, 0, 0, 38, sw=0.3)
    sh.note(z.P(0, -50), (254, 96), "manguito roscado / ancla", 1.3)
    sh.note(z.P(0, 30), (254, 85), "argolla giratoria (s/ carga)", 1.3)
    sh.text(234, 111.3, "Capacidad s/ catálogo: 2,5 - 10 t c/u", 1.35)

    # ============================================================ ESPECIFICACIONES
    y0 = 154
    spec(sh, 10, y0, 88, "E6 · Panel TT h 0,65 x 2,40", [
        ("Función:", "losa de entrepiso y cubierta de gran luz sin apuntalar; apoya sus nervios en los talones de las VP."),
        ("Medidas:", "2,40 x 0,65; ala 5 cm; nervios 18/12 a 1,20; largo 9,58 m · ≈ 0,30 m²/m · 7,2 t."),
        ("Máx./mín.:", "luces de catálogo 6 a 18 m (h 0,40 a 0,80); apoyo mín. 10 cm; sobrecarga útil ≈ 500 kg/m²."),
        ("Colocación:", "izado por 4 insertos con balancín; se apoya s/ neopreno 10 mm, se alinea y se sueldan las chapas de borde entre paneles."),
    ], size=1.5, tsize=2.0)
    spec(sh, 103, y0, 88, "E7 · Capa de compresión", [
        ("Función:", "monolitizar los paneles (diafragma rígido), repartir cargas y absorber el momento negativo sobre apoyos."),
        ("Medidas:", "e = 5 cm (mín. 5, usual 5-8) sobre el ala, H-25; malla Ø6 c/15 + barras de continuidad sobre las VP."),
        ("Colocación:", "limpiar y humedecer el ala rugosa, colocar malla c/ separadores, hormigonar con bomba y curar 7 días; el TT actúa de encofrado perdido."),
    ], size=1.5, tsize=2.0)
    spec(sh, 196, y0, 93, "E8 · Apoyos y conectores", [
        ("Neopreno:", "placas zunchadas e = 10 mm bajo VL, VP y TT: reparten carga y permiten giros y dilataciones (apoyo articulado)."),
        ("Pernos:", "Ø20 anclados en la ménsula, entran en vainas Ø40 de la viga que se rellenan c/ grout: impiden vuelco y desplazamiento."),
        ("Grout:", "mortero cementicio fluido sin retracción ≥ 40 MPa p/ vainas, juntas y cáliz."),
        ("Riel / insertos:", "embutidos en fábrica (riel C p/ grapas del muro cortina, insertos de izaje y placas de soldadura)."),
    ], size=1.5, tsize=2.0)
    return sh
