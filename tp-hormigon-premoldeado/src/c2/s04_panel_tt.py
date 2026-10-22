# -*- coding: utf-8 -*-
"""E6 panel TT + E7 capa de compresión (una lámina) y E8 apoyos y conectores (otra lámina)."""
from lib import Sheet, Iso, page, spec, heading, breakline, REB, TB, TS, TD, TT
from s02_fundacion_columna import legend
import geo

VISTA = "#eceeef"


@page("E6 · Panel TT + E7 · Capa de compresión")
def tt(num, total):
    sh = Sheet(num, total, "E6 · Panel TT + E7 · Capa de compresión", escalas="sección 1:20 · elevación y planta 1:100 · isometría 1:75",
               fname="E6_E7_Panel_TT_Capa")
    heading(sh, "1º ELEMENTOS · E6 PANEL TT h 0,65 + E7 CAPA", "Losa pretensada de doble nervio para entrepiso y cubierta, completada con capa de compresión in situ")
    sh.title_drawing(12, 32, "SECCIÓN TRANSVERSAL", "esc. 1:20", TT)
    s = sh.view(40, 82, 20)
    s.poly(geo.perfil_TT(), mat="HA", sw=0.4)
    s.rect(0, 650, 2400, 700, mat="HAis", sw=0.3)
    s.pline([(20, 675), (2380, 675)], stroke=REB, sw=0.2, dash="1.6 0.4")
    for x in range(75, 2400, 150): s.dot(x, 675, 0.35)
    s.pline([(20, 625), (2380, 625)], stroke=REB, sw=0.15)
    for xc in (600, 1800):
        for y in (40, 90, 140): s.dot(xc, y, 0.6, "#000")
        s.line(xc, 30, xc, 620, stroke=REB, sw=0.15)
    s.dim((0, 0), (600, 0), -4.0, "0,60"); s.dim((600, 0), (1800, 0), -4.0, "1,20"); s.dim((1800, 0), (2400, 0), -4.0, "0,60")
    s.dim((0, 0), (2400, 0), -10.0, "2,40")
    s.dim((2400, 0), (2400, 650), -4.0, "0,65")
    s.dim((510, 600), (690, 600), 0, "0,18")
    for lab, tgt, at in (("1", (1200, 625), (115, 38)), ("2", (1800, 90), (165, 70)), ("3", (900, 675), (95, 38)),
                         ("4", (300, 690), (60, 38)), ("5", (600, 400), (24, 70))):
        sh.callout(s.P(*tgt), at, lab)
    y = legend(sh, 12, 104, ["1 Ala 5 cm c/ malla Ø6 c/20, superficie rugosa p/ adherir la capa", "2 Nervio 18/12 c/ 3 cordones Ø12,7 pretensados",
                             "3 Capa de compresión H-25 in situ e = 5 cm (E7)", "4 Malla soldada Ø6 c/15 x 15", "5 Conectores salientes Ø6 en nervios"])
    sh.title_drawing(12, 140, "ELEVACIÓN Y PLANTA", "esc. 1:100 · VP en trazos a ambos extremos", TT)
    v = sh.view(20, 160, 100)
    L = 9580
    v.poly([(0, 650), (L, 650), (L, 50), (L - 150, 50), (L - 150, 0), (150, 0), (150, 50), (0, 50)], fill=VISTA, sw=0.3)
    v.line(0, 600, L, 600, sw=0.1)
    v.rect(-200, -300, -10, 700, fill="#e2ecdc", sw=0.15, dash="0.6 0.3"); v.rect(L + 10, -300, L + 200, 700, fill="#e2ecdc", sw=0.15, dash="0.6 0.3")
    for x in (2000, L - 2000): v.circle(x, 600, 60, sw=0.15)
    v.dim((0, 650), (L, 650), 3.0, "9,58")
    sh.note(v.P(2000, 600), (90, 148), "insertos de izaje (4, a L/5)")
    p = sh.view(20, 192, 100)
    p.rect(0, 0, L, 2400, fill=VISTA, sw=0.3)
    for y in (540, 660, 1740, 1860): p.line(150, y, L - 150, y, sw=0.1, dash="0.6 0.3")
    p.dim((L, 0), (L, 2400), -3.5, "2,40")
    sh.note(v.P(L - 75, 25), (90, 172), "rebaje (dap) s/ talón de la VP")
    S = Iso((1, -1, 1))
    S.prism(geo.perfil_TT(), "x", 150, 3000, geo.C_TT, sw=0.12)
    S.prism(geo.perfil_TT(dap=50), "x", 0, 150, geo.C_TT, sw=0.12)
    ox, oy = S.fit((132, 150, 200, 198), 75); S.draw(sh, ox, oy, 75)
    sh.text(150, 140, "ISOMETRÍA", TT, bold=True); sh.text(150, 145, "esc. 1:75 (extremo c/ rebaje)", TS)
    y = spec(sh, 12, 206, 186, "E6 · PANEL TT", [
        ("Función / medidas:", "losa de gran luz sin apuntalar · 2,40 x 0,65, ala 5 cm, nervios 18/12 a 1,20 · L 9,58 m · ≈ 7,2 t."),
        ("Máx./mín.:", "luces de catálogo 6 a 18 m (h 0,40 a 0,80); apoyo ≥ 10 cm; sobrecarga útil ≈ 500 kg/m²."),
        ("Colocación:", "izado por 4 insertos con balancín; apoyo s/ neopreno 10 mm; se sueldan las chapas de borde entre paneles."),
    ], size=TB, tsize=2.9)
    spec(sh, 12, y + 2, 186, "E7 · CAPA DE COMPRESIÓN", [
        ("Función:", "monolitizar los paneles (diafragma rígido), repartir cargas y tomar el momento negativo sobre los apoyos."),
        ("Medidas / colocación:", "e = 5 cm (usual 5-8) H-25, malla Ø6 c/15; limpiar y humedecer el ala, hormigonar c/ bomba y curar 7 días."),
    ], size=TB, tsize=2.9)
    return sh


@page("E8 · Apoyos y conectores")
def accesorios(num, total):
    sh = Sheet(num, total, "E8 · Apoyos y conectores", escalas="neopreno 1:5 · perno y vaina 1:10 · riel 1:2 · inserto 1:5", fname="E8_Apoyos_Conectores")
    heading(sh, "1º ELEMENTOS · E8 APOYOS Y CONECTORES", "Piezas que materializan las uniones entre los elementos premoldeados (ver juntas J1 a J8)")
    # a) neopreno 1:5
    sh.title_drawing(12, 34, "a) NEOPRENO ZUNCHADO", "esc. 1:5", TT)
    n = sh.view(20, 80, 5)
    n.rect(0, 0, 300, 150, fill="#3a3a3a", sw=0.3)
    for y in (40, 75, 110): n.line(5, y, 295, y, stroke="#aaa", sw=0.15)
    n.dim((0, 0), (300, 0), -4.0, "0,30 (≈ ancho de la viga)")
    n.dim((300, 0), (300, 150), -4.0, "0,15")
    sh.para(12, 98, 88, "Placa dureza 60 Shore A, e = 10 mm, con chapas de acero interiores; σ adm ≈ 7-10 MPa.", TS, 1.25)
    # b) perno 1:10
    sh.title_drawing(108, 34, "b) PERNO Ø20 + VAINA Ø40", "esc. 1:10", TT)
    q = sh.view(130, 68, 10)
    q.rect(-120, -150, 120, 0, mat="HA", sw=0.25); q.rect(-120, 10, 120, 200, mat="HA", sw=0.25)
    q.rect(-120, 0, 120, 10, mat="neo", stroke=None)
    q.rect(-20, 10, 20, 190, mat="grout", sw=0.1)
    q.rect(-10, -140, 10, 170, mat="acero", sw=0.05)
    q.line(-40, -140, 40, -140, sw=0.5)
    sh.note(q.P(0, 100), (150, 54), "vaina rellena c/ grout")
    sh.note(q.P(0, 5), (150, 67), "neopreno")
    sh.note(q.P(0, -60), (150, 78), "perno anclado en la ménsula")
    sh.para(108, 98, 92, "Viga arriba / ménsula abajo: impide vuelco y deslizamiento sin trabar el giro.", TS, 1.25)
    # c) riel 1:2
    sh.title_drawing(12, 112, "c) RIEL DE ANCLAJE EMBUTIDO", "esc. 1:2", TT)
    r = sh.view(30, 150, 2)
    r.rect(0, -60, 90, 60, mat="HA", stroke=None)
    r.poly([(0, -26), (42, -26), (42, 26), (0, 26), (0, 18), (34, 18), (34, -18), (0, -18)], mat="acero", sw=0.1)
    for dy in (-22, 22): r.line(42, dy, 90, dy, sw=0.6)
    r.rect(8, -8, 34, 8, fill="#666", sw=0.1); r.line(-30, 0, 20, 0, sw=0.9)
    r.dim((0, 26), (0, -26), 5.0, "52 mm")
    sh.para(12, 186, 88, "Perfil C 52/34 galvanizado + bulón T M12: regulación lateral de la grapa ± 25 mm.", TS, 1.25)
    # d) inserto 1:5
    sh.title_drawing(108, 112, "d) INSERTO DE IZAJE", "esc. 1:5", TT)
    z = sh.view(140, 152, 5)
    z.rect(-100, -150, 100, 0, mat="HA", stroke=None)
    z.rect(-12, -120, 12, 0, mat="acero", sw=0.05)
    z.rect(-30, -130, 30, -120, mat="acero", sw=0.05)
    z.circle(0, 25, 22, sw=0.4); z.line(0, 0, 0, 47, sw=0.4)
    sh.note(z.P(0, -60), (162, 162), "manguito roscado / ancla")
    sh.note(z.P(0, 35), (162, 136), "argolla giratoria")
    sh.para(108, 186, 92, "Capacidad s/ catálogo: 2,5 a 10 t por inserto; se usan siempre de a pares o de a cuatro.", TS, 1.25)
    spec(sh, 12, 202, 186, "ESPECIFICACIÓN", [
        ("Neopreno:", "placas zunchadas e = 10 mm bajo VL, VP y TT: reparten la carga y permiten giros y dilataciones (apoyo articulado)."),
        ("Pernos:", "Ø20 anclados en la ménsula; entran en vainas Ø40 de la viga que se rellenan con grout."),
        ("Grout:", "mortero cementicio fluido sin retracción ≥ 40 MPa para vainas, juntas y cáliz."),
        ("Riel / insertos:", "embutidos en fábrica: riel C p/ grapas del muro cortina, insertos de izaje y placas de soldadura."),
    ], size=TB, tsize=2.9)
    return sh


PAGES = [tt, accesorios]
