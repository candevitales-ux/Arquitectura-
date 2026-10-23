# -*- coding: utf-8 -*-
"""Genera src/lamina4_a4.py a partir de src/lamina4_catalogo.py (lámina A3 con vidriado + opaco).
Versión A4 (una hoja por sistema) con DIBUJOS MÁS CHICOS Y LETRA MÁS GRANDE:
- cada detalle se dibuja con el código de la A3 y después se reduce con un factor k que lleva su escala
  a otra escala normalizada (1:3 -> 1:5, 1:5 -> 1:10, 1:10 -> 1:15), y se ubica en la hoja A4;
- los textos, globos de referencia y cotas NO se reducen: se rehacen con la letra grande;
- ficha técnica, DVH / composición, montaje, referencias y rótulo se dibujan de nuevo con letra grande."""
import re

src = open("src/lamina4_catalogo.py", encoding="utf-8").read()
L = src.split("\n")
def idx(prefix):
    return next(i for i, l in enumerate(L) if l.startswith(prefix))
def seccion(tag):
    """Código del bloque '# ---... <tag> ...' hasta el siguiente encabezado de sección (sin la línea del título)."""
    a = next(i for i, l in enumerate(L) if l.startswith("# ----") and f" {tag} " in l)
    b = next(i for i in range(a + 1, len(L)) if L[i].startswith("# ----") or L[i].startswith("# ####")
             or L[i].startswith("referencias("))
    return "\n".join(l for l in L[a:b] if not l.startswith("titulo_detalle("))

base = "\n".join(L[:idx("# ==================================================================================== HOJA")])
base = base.replace("W, H = 297.0, 420.0", "W, H = 210.0, 297.0\nPAGINA = sys.argv[2] if len(sys.argv) > 2 else 'vidriado'")
base = base.replace('"""Lámina 4 - Catálogo de cerramientos VIDRIADOS Y OPACOS en una sola hoja A3 vertical.',
                    '"""Lámina 4 en dos hojas A4 verticales (vidriado / opaco). ARCHIVO GENERADO por src/armar_a4.py:\n'
                    'no editar a mano; los dibujos salen de src/lamina4_catalogo.py.\n')

pre_b = "\n".join(L[idx("EXT_, ALM, INT_ ="):idx("# ---------------------------------------------------------------- B1")])

# arranque opaco recortado en altura
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
# las notas de B7 se reescriben aparte con letra grande
b7 = "\n".join(l for l in seccion("B7").split("\n") if not l.startswith('txt("agujero') and not l.startswith('txt("zona'))

# (tag, título, escala nueva, k, x, y_titulo, ancho_titulo)
LAY = {
 "vidriado": [("A1", "AXONOMETRÍA", "S/E", 0.62, 15, 263, 50, 1.1),
              ("A5", "MONTANTE", "1:5", 0.60, 15, 205, 52),
              ("A6", "TRAVESAÑO", "1:5", 0.60, 72, 205, 50),
              ("A7", "ANCLAJE Y JUNTA EN ENTREPISO", "1:10", 0.50, 15, 152, 92),
              ("A3", "REMATE", "1:15", 2 / 3, 113, 152, 38),
              ("A4", "ARRANQUE", "1:15", 2 / 3, 157, 152, 38)],
 "opaco":    [("B1", "AXONOMETRÍA", "S/E", 0.62, 15, 263, 50, 1.1),
              ("B5", "JUNTA VERTICAL", "1:10", 0.50, 15, 199, 50),
              ("B6", "JUNTA HORIZ.", "1:10", 0.50, 71, 199, 40),
              ("B3", "REMATE", "1:15", 2 / 3, 115, 199, 38, 1.1),
              ("B4", "ARRANQUE", "1:15", 2 / 3, 158, 199, 37, 1.1),
              ("B7", "FIJACIÓN A LA VIGA VL · BULÓN M20", "1:15", 2 / 3, 15, 140, 110, 1.15)],
}

def bloque_code(tag, code, tit, esc, k, x, yt, w, s=1.3):
    return f'''_n0 = len(msp)
{code}
colocar(list(msp)[_n0:], {k}, {x}, {yt} - 5.5, {s})
titulo_detalle("{tag}", "{tit}", "{esc}", {x}, {yt}, {w})
'''

def cuerpo(pagina):
    out = ["C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))"]
    if pagina == "opaco": out.append(pre_b)
    for tag, tit, esc, k, x, yt, w, *s in LAY[pagina]:
        code = b4 if tag == "B4" else b7 if tag == "B7" else seccion(tag)
        out.append(bloque_code(tag, code, tit, esc, k, x, yt, w, *s))
    return "\n".join(out)

def indent(s): return "\n".join("    " + l for l in s.split("\n"))

refs_vid = re.search(r'referencias\("REFERENCIAS · VIDRIADO", (\[.*?\]), 241\)', src, re.S).group(1)
refs_opa = re.search(r'referencias\("REFERENCIAS · OPACO", (\[.*?\]), 78\)', src, re.S).group(1)
mont = re.search(r'for x, tit, pasos in \(\(15, "MONTAJE · VIDRIADO", (\[.*?\])\),\s*\(152, "MONTAJE · OPACO", (\[.*?\])\)\):', src, re.S)

hoja = f'''
# ==================================================================================== HOJA A4
from ezdxf.math import Matrix44, Vec2
from ezdxf import bbox as _bbox
T_TXT, T_GLO, R_GLO, T_DIM = 2.6, 2.5, 2.75, 2.5     # letra grande de la A4 (mm)
ds.dxf.dimtxt = T_DIM; ds.dxf.dimasz = 1.6

def colocar(ents, k, x, ytop, s=1.3):
    """Reduce el detalle (geometría) con factor k y lo ubica con su esquina sup. izq. en (x, ytop).
    Textos, globos y cotas mantienen la letra grande; los globos se separan del dibujo (factor s)
    para que no se amontonen al achicarlo."""
    caja = _bbox.extents([e for e in ents if e.dxftype() not in ("TEXT", "DIMENSION")])
    M = Matrix44.chain(Matrix44.translate(-caja.extmin.x, -caja.extmax.y, 0), Matrix44.scale(k, k, 1),
                       Matrix44.translate(x, ytop, 0))
    dib = _bbox.extents([e for e in ents if e.dxf.layer not in ("3-REFERENCIAS", "2-COTAS", "3-TEXTOS")
                         and e.dxftype() not in ("TEXT", "DIMENSION")])
    cen = Vec2(M.transform(dib.center))
    globos, lideres, cotas, numeros = [], [], [], []
    for e in ents:
        t = e.dxftype()
        if t == "DIMENSION":
            cotas.append(e); continue
        if t == "TEXT":
            h = e.dxf.height
            e.transform(M)
            e.dxf.height = T_GLO if e.dxf.layer == "3-REFERENCIAS" else (T_TXT if h <= 2.2 else h)
            if e.dxf.layer == "3-REFERENCIAS": numeros.append(e)
            continue
        e.transform(M)
        if t == "CIRCLE" and e.dxf.layer == "3-REFERENCIAS" and e.dxf.radius > 0.5 * k:
            globos.append(e)
        elif t == "LWPOLYLINE" and e.dxf.layer == "3-REFERENCIAS" and len(e) == 2:
            lideres.append(e)
    centros = []
    for c in globos:                       # separar el globo del centro del dibujo y agrandarlo
        c0 = Vec2(c.dxf.center); c1 = cen + (c0 - cen) * s
        for n in numeros:
            if Vec2(n.dxf.align_point).distance(c0) < 0.5: n.dxf.align_point = (c1.x, c1.y, 0)
        for p in lideres:
            if Vec2(p[0][:2]).distance(c0) < 3: p.tag_ = c1
        c.dxf.center = (c1.x, c1.y, 0); c.dxf.radius = R_GLO; centros.append(c1)
    for p in lideres:                      # el líder arranca en el borde del globo
        c = getattr(p, "tag_", None)
        if c is None: continue
        b = Vec2(p[1][:2]); d = (b - c).normalize()
        p[0] = (*(c + d * R_GLO), 0, 0, 0)
    for e in cotas:                        # las cotas se rehacen con la letra grande
        p1, p2, base = (M.transform(e.dxf.defpoint2), M.transform(e.dxf.defpoint3), M.transform(e.dxf.defpoint))
        ang, texto = e.dxf.get("angle", 0), e.dxf.get("text", "<>")
        msp.delete_entity(e)
        nd = msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=ang, dimstyle="CATALOGO", text=texto,
                                dxfattribs={{"layer": "2-COTAS"}})
        nd.render(); ents.append(nd.dimension)
    vivos = [e for e in ents if e.is_alive]
    tot = _bbox.extents(vivos)             # reubicar todo (incluidos globos) en la esquina pedida
    for e in vivos: e.translate(x - tot.extmin.x, ytop - tot.extmax.y, 0)

def ficha4(x0, x1, x2, ytop, filas, rh=4.1):
    pl([(x0, ytop), (x2, ytop)], "3-TABLAS", 35)
    for i, (a, b) in enumerate(filas):
        y = ytop - (i + 1) * rh
        if i % 2 == 0: hatch([(x0, y), (x2, y), (x2, y + rh), (x0, y + rh)], "SOLID", layer="3-TABLAS", rgb=(238, 238, 238), color=254)
        txt(a, x0 + 1, y + 1.0, T_TXT, TA.LEFT, "3-TABLAS", True)
        txt(b, x1 + 1, y + 1.0, T_TXT, TA.LEFT, "3-TABLAS")
    yb = ytop - len(filas) * rh
    pl([(x0, yb), (x2, yb)], "3-TABLAS", 35); pl([(x1, ytop), (x1, yb)], "3-TABLAS", 13)
    return yb

def lista(titulo, items, ytop, ncol, paso, numerada=True, h=T_TXT):
    txt(titulo, 15, ytop, 3.0, TA.LEFT, "3-TITULOS", True)
    pl([(15, ytop - 1.6), (W - 15, ytop - 1.6)], "3-TITULOS", 18)
    nrow = -(-len(items) // ncol); cw = (W - 30) / ncol
    for i, r in enumerate(items):
        col, row = divmod(i, nrow)
        x, y = 15 + col * cw, ytop - 5.6 - row * paso
        if numerada:
            txt(f"{{i + 1}}", x + 3.6, y, h, TA.RIGHT, "3-REFERENCIAS", True); txt(r, x + 5, y, h)
        else:
            txt(r, x, y, h)
    return ytop - 5.6 - (nrow - 1) * paso

pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO DE CERRAMIENTOS", 15, 280, 5.5, TA.LEFT, "3-TITULOS", True)
txt("LÁMINA 4", W - 15, 280, 5.5, TA.RIGHT, "3-TITULOS", True)
pl([(15, 270), (W - 15, 270)], "3-TITULOS", 70)

if PAGINA == "vidriado":
    txt("A  ·  VIDRIADO - MURO CORTINA DE ALUMINIO TIPO STICK", 15, 273, 3.2, TA.LEFT, "3-TITULOS", True)
    txt("HOJA 1 DE 2", W - 15, 273, 2.8, TA.RIGHT, "3-TITULOS")
{indent(cuerpo("vidriado"))}
    titulo_detalle("A2", "FICHA TÉCNICA", "", 70, 263, 125)
    yb = ficha4(70, 104, 195, 259, [
        ("Sistema", "muro cortina stick"), ("Montante", "aluminio 6063-T6, 50 x 150 mm"),
        ("Travesaño", "aluminio 6063-T6, 50 x 120 mm"), ("Vidrio visión", "DVH 6 templ. + 12 + 3+3 lam. PVB"),
        ("Spandrel", "templado 6 esmaltado + lana min. 50"), ("Fijación vidrio", "presor + tapa + burletes EPDM"),
        ("Transmitancia", "DVH U ≈ 2,8 W/m²·K · Rw ≈ 36 dB"), ("Modulación", "1,50 m · spandrel 0,90 m"),
        ("Montante", "colgado, 1 piso (4,50 m)"), ("Anclaje", "grapa galv. regulable + bulón M12"),
        ("Dilatación", "junta 20 mm c/ manguito por piso")])
    # composición del DVH 1:1
    titulo_detalle("A8", "COMPOSICIÓN DEL DVH", "1:1", 126, 205, 69)
    v = V(1, 128, 171)
    caja(v, 0, 0, 6, 26, "1-VIDRIO", VID, 18); caja(v, 18, 0, 24.76, 26, "1-VIDRIO", VID, 18)
    pl(v.P([(21.38, 0), (21.38, 26)]), "1-VIDRIO", 9)
    caja(v, 6, 14, 18, 23, layer="1-ALUMINIO", fill=ALU, lw=9); hatch(v.rect(6, 23, 18, 26), "SOLID", layer="1-EPDM", color=250)
    for i, (t, xx, yy) in enumerate([("templado 6 mm (ext.)", 3, 6), ("cámara 12 mm", 12, 4),
                                     ("laminado 3+3 PVB (int.)", 21.4, 2), ("separador + desecante", 12, 20)]):
        y = 195 - i * 5.2
        pl([v.p(xx, yy), (157, y + 0.9), (158.5, y + 0.9)], "3-REFERENCIAS", 9)
        txt(t, 159, y, 2.4)
    txt("e = 24,8 mm", 159, 173.5, 2.6, bold=True)
    yy = lista("SECUENCIA DE MONTAJE", {mont.group(1)}, 104, 1, 3.6, numerada=False)
    lista("REFERENCIAS", {refs_vid}, yy - 6, 2, 3.45)
else:
    txt("B  ·  OPACO - PANEL SÁNDWICH PREMOLDEADO DE H°A° e = 20 cm", 15, 273, 3.2, TA.LEFT, "3-TITULOS", True)
    txt("HOJA 2 DE 2", W - 15, 273, 2.8, TA.RIGHT, "3-TITULOS")
{indent(cuerpo("opaco"))}
    titulo_detalle("B2", "FICHA TÉCNICA", "", 70, 263, 125)
    yb = ficha4(70, 104, 195, 259, [
        ("Sistema", "panel sándwich premoldeado H°A°"), ("Espesor", "20 cm: 6 ext. + 6 EPS + 8 int."),
        ("Hormigón", "H-30, malla en cada hoja"), ("Aislación", "EPS 6 cm + conectores fibra vidrio"),
        ("Módulo", "2,40 m x 1 piso (4,50 m)"), ("Peso propio", "≈ 340 kg/m²"),
        ("Transmitancia", "K ≈ 0,5 W/m²·K"), ("Fijación", "bulón pasante M20 al ala de la VL"),
        ("Dilatación", "agujero ovalado vertical 40x60"), ("Apoyo inferior", "viga portapanel + mortero + Ø16"),
        ("Juntas", "20 mm, fondo + sellador PU")])
    # composición del panel 1:10 y notas de la fijación
    titulo_detalle("B8", "COMPOSICIÓN", "1:10", 135, 138, 60)
    v = V(10, 137, 115)
    for x0, x1, f in ((0, X1, H_A), (X2, X3, H_A), (X1, X2, EPS)):
        p = v.rect(x0, 0, x1, 160); hatch(p, "SOLID", layer="1-HORMIGON", rgb=f, color=9)
        if f == H_A: hatch(p, "AR-CONC", 0.02, 0, "1-HORMIGON", color=8)
        pl(p, "1-HORMIGON", 18, True)
    for yy_ in (40, 120): pl(v.P([(X1 - 20, yy_), (X2 + 25, yy_)]), "1-TORNILLERIA", 25)
    for i, (t, xx, yy_) in enumerate([("hoja ext. 6 cm", 30, 80), ("alma EPS 6 cm", 90, 140),
                                      ("hoja int. 8 cm", 160, 100), ("conector fibra vidrio", 110, 40)]):
        y = 130 - i * 5.0
        pl([v.p(xx, yy_), (160, y + 0.9), (161.5, y + 0.9)], "3-REFERENCIAS", 9)
        txt(t, 162, y, 2.4)
    txt("agujero ovalado vertical 40x60:", 135, 105, 2.4); txt("el panel dilata sin trabar la viga.", 135, 101.6, 2.4)
    txt("zona maciza 30x30 sin EPS", 135, 96.6, 2.4); txt("en cada anclaje.", 135, 93.2, 2.4)
    yy = lista("SECUENCIA DE MONTAJE", {mont.group(2)}, 85.5, 2, 3.5, numerada=False, h=2.25)
    lista("REFERENCIAS", {refs_opa}, yy - 6, 2, 3.3)

# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 22
xs = [15, 41, 118, 158, 195]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 18.4, 3.6, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 19/10/2026", (xs[0] + xs[1]) / 2, 14.0, 1.9, TA.MIDDLE_CENTER, "3-TITULOS")
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 1.5, 19.3, 2.1, layer="3-TITULOS")
txt("ALUMNA: Candelaria Vitale", xs[1] + 1.5, 16.2, 2.1, layer="3-TITULOS")
txt("GRUPO: 13", xs[1] + 1.5, 13.1, 2.1, layer="3-TITULOS")
txt("NIVEL:", xs[2] + 1.5, 19.3, 2.1, layer="3-TITULOS"); txt("OBS:", xs[2] + 1.5, 16.2, 2.1, layer="3-TITULOS")
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 18.6, 2.3, TA.MIDDLE_CENTER, "3-TITULOS")
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 14.8, 2.3, TA.MIDDLE_CENTER, "3-TITULOS")

doc.saveas(f"{{OUT}}/Lamina4_Catalogo_{{PAGINA.capitalize()}}_A4.dxf")
print("ok", PAGINA)
'''
open("src/lamina4_a4.py", "w", encoding="utf-8").write(base + "\n" + hoja)
print("generado src/lamina4_a4.py")
