# -*- coding: utf-8 -*-
"""Genera src/lamina4_a4.py a partir de src/lamina4_catalogo.py (lámina A3 con vidriado + opaco).
La versión A4 reutiliza el mismo dibujo de cada detalle y sólo lo reubica: cada bloque (A1..A7, B1..B7)
se traslada en la hoja A4 con su desplazamiento (contenido y título), y la letra se agranda un 20 %."""
import re, sys

src = open("src/lamina4_catalogo.py", encoding="utf-8").read()
L = src.split("\n")
def idx(prefix):
    return next(i for i, l in enumerate(L) if l.startswith(prefix))
def seccion(tag):
    """Líneas del bloque que empieza en '# ---... <tag> ' hasta el siguiente encabezado de sección."""
    a = next(i for i, l in enumerate(L) if l.startswith("# ----") and f" {tag} " in l)
    b = next(i for i in range(a + 1, len(L)) if L[i].startswith("# ----") or L[i].startswith("# ####")
             or L[i].startswith("referencias("))
    return "\n".join(L[a:b])

base = "\n".join(L[:idx("# ==================================================================================== HOJA")])
base = base.replace("W, H = 297.0, 420.0", "W, H = 210.0, 297.0\nPAGINA = sys.argv[2] if len(sys.argv) > 2 else 'vidriado'\nF = 1.20   # letra 20 % más grande que en la A3")
base = base.replace('def txt(s, x, y, h=2.5, align=TA.LEFT, layer="3-TEXTOS", bold=False, rot=0):\n',
                    'def txt(s, x, y, h=2.5, align=TA.LEFT, layer="3-TEXTOS", bold=False, rot=0):\n'
                    '    if layer != "3-TITULOS" and h <= 2.25: h *= F\n')
base = base.replace("ds.dxf.dimtxt = 2.0;", "ds.dxf.dimtxt = 2.0 * F;")
base = base.replace("def g(n, v, at, pos, r=2.1):", "def g(n, v, at, pos, r=2.1 * F):")
base = base.replace('"""Lámina 4 - Catálogo de cerramientos VIDRIADOS Y OPACOS en una sola hoja A3 vertical.',
                    '"""Lámina 4 en dos hojas A4 verticales (vidriado / opaco). ARCHIVO GENERADO por src/armar_a4.py:\n'
                    'no editar a mano; los dibujos salen de src/lamina4_catalogo.py.\n')
assert base.count("h *= F") == 1 and base.count("2.0 * F") == 1 and base.count("2.1 * F") == 1

pre_b = "\n".join(L[idx("EXT_, ALM, INT_ ="):idx("# ---------------------------------------------------------------- B1")])

# arranque opaco recortado en altura para que entre en la A4
b4 = seccion("B4")
for a, b in [("hormigon(v, [(0, -300), (X3, -300), (X3, 0), (0, 0)], 25, 0.025)", "hormigon(v, [(0, -150), (X3, -150), (X3, 0), (0, 0)], 25, 0.025)"),
             ("corte_rotura(v, (-10, -300), (X3 + 10, -300))", "corte_rotura(v, (-10, -150), (X3 + 10, -150))"),
             ("panel_v(v, 20, 300, cortes=(300,))", "panel_v(v, 20, 170, cortes=(170,))"),
             ("pl(v.P([(150, -150), (150, 170)])", "pl(v.P([(150, -120), (150, 150)])"),
             ("pl(v.P([(140, -150), (140, 170), (160, 170), (160, -150), (140, -150)])", "pl(v.P([(140, -120), (140, 150), (160, 150), (160, -120), (140, -120)])"),
             ("pl(v.P([(-2, -300), (-2, -150)]), \"1-SELLADOS\", 35)", "pass"),
             ("g(12, v, (100, -200), (277, 160))", "g(12, v, (100, -80), (277, 168))"),
             ("g(14, v, (-2, -250), (262, 148)); ", ""),
             ("g(3, v, (160, 200), (277, 198))", "g(3, v, (160, 120), (277, 190))")]:
    assert b4.count(a) == 1, a
    b4 = b4.replace(a, b)

# desplazamientos (dx, dy) del contenido y, si difiere, del título de cada bloque
VID = {"A1": ((0, -109), None), "A2": ((3, -110), None), "A5": ((0, -116), None), "A6": ((-3, -115), None),
       "A4": ((-85, -171), (-85, -187)), "A7": ((-143, -178), None), "A3": ((-38, -234), (-38, -248))}
OPA = {"B1": ((0, 53), None), "B2": ((3, 53), None), "B5": ((0, 49), None), "B6": ((-1, 49), None),
       "B3": ((-38, -22), (-38, -23)), "B7": ((-143, -17), None), "B4": ((-87, -81), (-86, -91))}

def bloque(tag, code, delta, dtit):
    dt = dtit or delta
    return (f"_n0 = len(msp)\n{code}\n"
            f"for _e in list(msp)[_n0:]:\n"
            f"    _d = {dt} if _e.dxf.layer == '3-TITULOS' else {delta}\n"
            f"    _e.translate(_d[0], _d[1], 0)\n")

TIT = {'titulo_detalle("A5", "MONTANTE", "1:3", 15, 301, 61)': 'titulo_detalle("A5", "MONTANTE", "1:3", 15, 301, 59)',
       'titulo_detalle("A6", "TRAVESAÑO", "1:3", 80, 301, 72)': 'titulo_detalle("A6", "TRAVESAÑO", "1:3", 80, 301, 68)',
       'v.dim((TD, -MW / 2), (TD, MW / 2), 3, vertical=True, text="50")': 'pass',
       'titulo_detalle("B6", "JUNTA HORIZ.", "1:5", 95, 138, 55)': 'titulo_detalle("B6", "JUNTA HORIZ.", "1:5", 95, 138, 51)'}
_sec = seccion
def seccion(tag):
    c = _sec(tag)
    for a, b in TIT.items(): c = c.replace(a, b)
    return c

cuerpo = []
cuerpo.append("C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))")
cuerpo.append("if PAGINA == 'vidriado':")
blk = []
for tag in ("A1", "A2", "A3", "A4", "A5", "A6", "A7"):
    blk.append(bloque(tag, seccion(tag), *VID[tag]))
cuerpo.append("\n".join("    " + l for l in "\n".join(blk).split("\n")))
cuerpo.append("else:")
blk = [pre_b]
for tag in ("B1", "B2", "B3", "B4", "B5", "B6", "B7"):
    blk.append(bloque(tag, b4 if tag == "B4" else seccion(tag), *OPA[tag]))
cuerpo.append("\n".join("    " + l for l in "\n".join(blk).split("\n")))

# listas de referencias y de montaje tal como están en la A3
refs_vid = re.search(r'referencias\("REFERENCIAS · VIDRIADO", (\[.*?\]), 241\)', src, re.S).group(1)
refs_opa = re.search(r'referencias\("REFERENCIAS · OPACO", (\[.*?\]), 78\)', src, re.S).group(1)
mont = re.search(r'for x, tit, pasos in \(\(15, "MONTAJE · VIDRIADO", (\[.*?\])\),\s*\(152, "MONTAJE · OPACO", (\[.*?\])\)\):', src, re.S)

hoja = f'''
# ==================================================================================== HOJA A4
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO DE CERRAMIENTOS", 15, 280, 5.5, TA.LEFT, "3-TITULOS", True)
txt("LÁMINA 4", W - 15, 280, 5.5, TA.RIGHT, "3-TITULOS", True)
if PAGINA == "vidriado":
    txt("A  ·  VIDRIADO - MURO CORTINA DE ALUMINIO TIPO STICK", 15, 273, 3.0, TA.LEFT, "3-TITULOS", True)
    txt("HOJA 1 DE 2", W - 15, 273, 2.6, TA.RIGHT, "3-TITULOS")
else:
    txt("B  ·  OPACO - PANEL SÁNDWICH PREMOLDEADO DE H°A° e = 20 cm", 15, 273, 3.0, TA.LEFT, "3-TITULOS", True)
    txt("HOJA 2 DE 2", W - 15, 273, 2.6, TA.RIGHT, "3-TITULOS")
pl([(15, 270), (W - 15, 270)], "3-TITULOS", 70)

{chr(10).join(cuerpo)}

def referencias4(titulo, refs, ytop, ncol=3, paso=2.75):
    txt(titulo, 15, ytop, 2.6, TA.LEFT, "3-TITULOS", True)
    pl([(15, ytop - 1.4), (W - 15, ytop - 1.4)], "3-TITULOS", 18)
    nrow = math.ceil(len(refs) / ncol); cw = (W - 30) / ncol
    for i, r in enumerate(refs):
        col, row = divmod(i, nrow)
        x, y = 15 + col * cw, ytop - 4.4 - row * paso
        txt(f"{{i + 1}}", x + 2.8, y, 1.85, TA.RIGHT, "3-REFERENCIAS", True)
        txt(r, x + 4.0, y, 1.85)

def montaje4(titulo, pasos, ytop):
    txt(titulo, 15, ytop, 2.6, TA.LEFT, "3-TITULOS", True)
    pl([(15, ytop - 1.4), (W - 15, ytop - 1.4)], "3-TITULOS", 18)
    for i, p in enumerate(pasos):
        col, row = (0, i) if i < 3 else (1, i - 3)
        txt(p, 15 + col * 90, ytop - 4.4 - row * 3.1, 2.0)

if PAGINA == "vidriado":
    montaje4("SECUENCIA DE MONTAJE", {mont.group(1)}, 64.5)
    referencias4("REFERENCIAS", {refs_vid}, 49.6)
else:
    montaje4("SECUENCIA DE MONTAJE", {mont.group(2)}, 60.5)
    referencias4("REFERENCIAS", {refs_opa}, 45.6, paso=2.6)

# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 21
xs = [15, 39, 118, 158, 195]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 17.8, 3.2, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 19/10/2026", (xs[0] + xs[1]) / 2, 13.6, 1.7, TA.MIDDLE_CENTER, "3-TITULOS")
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 1.5, 18.9, 1.8)
txt("ALUMNA: Candelaria Vitale", xs[1] + 1.5, 16.1, 1.8)
txt("GRUPO: 13", xs[1] + 1.5, 13.3, 1.8)
txt("NIVEL:", xs[2] + 1.5, 18.9, 1.8); txt("OBS:", xs[2] + 1.5, 16.1, 1.8)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 17.9, 2.0, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 14.5, 2.0, TA.MIDDLE_CENTER)

doc.saveas(f"{{OUT}}/Lamina4_Catalogo_{{PAGINA.capitalize()}}_A4.dxf")
print("ok", PAGINA)
'''
open("src/lamina4_a4.py", "w", encoding="utf-8").write(base + "\n" + hoja)
print("generado src/lamina4_a4.py")
