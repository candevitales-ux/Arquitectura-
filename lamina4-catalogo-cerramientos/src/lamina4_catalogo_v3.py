# -*- coding: utf-8 -*-
"""Lámina 4 (versión 3: estructura común SHAP) - Catálogo de cerramientos VIDRIADOS Y OPACOS en una sola hoja A3 vertical.
A: muro cortina stick (corte integral muro cortina, losa SHAP). B: panel liso de H°A con alma de EPS,
vertical, Astori, e = 20 cm (lámina 1 opaco). Un único DXF en mm de papel (escala 1:1 de la hoja);
cada detalle se dibuja en mm reales y se lleva a la hoja con su escala. Del DXF salen el DWG y el PDF."""
import math, sys, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)
W, H = 297.0, 420.0

doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
LAY = {"0-MARCO": 7, "1-CONTORNO": 7, "1-CHAPA": 7, "1-NUCLEO-PUR": 8, "1-ACERO": 7, "1-HORMIGON": 8, "1-SUELO": 8,
       "1-SELLADOS": 250, "1-TORNILLERIA": 7, "1-RAYADOS": 8, "1-VISTA": 8, "1-OCULTAR": 7, "2-COTAS": 7,
       "3-REFERENCIAS": 7, "3-TEXTOS": 7, "3-TITULOS": 7, "3-TABLAS": 7}
for n, c in LAY.items(): doc.layers.add(n, color=c)
doc.layers.get("1-RAYADOS").dxf.color = 8

# ------------------------------------------------------------------ primitivas en mm de papel
def pl(pts, layer="1-CONTORNO", lw=25, close=False, lt=None):
    a = {"layer": layer, "lineweight": lw}
    if lt: a["linetype"] = lt
    return msp.add_lwpolyline(pts, close=close, dxfattribs=a)

def hatch(pts, pat="SOLID", sc=1.0, ang=0, layer="1-RAYADOS", rgb=None, color=8):
    h = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    if pat == "SOLID":
        h.set_solid_fill(color=color, rgb=rgb)
    else:
        h.set_pattern_fill(pat, color=color, scale=sc, angle=ang)
    h.paths.add_polyline_path(pts, is_closed=True)
    return h

def txt(s, x, y, h=2.5, align=TA.LEFT, layer="3-TEXTOS", bold=False, rot=0):
    t = msp.add_text(s, height=h, rotation=rot,
                     dxfattribs={"layer": layer, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "width": 0.9})
    t.set_placement((x, y), align=align)
    return t

def mtxt(s, x, y, h=2.2, width=100, layer="3-TEXTOS", spacing=1.35):
    m = msp.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL", "char_height": h, "width": width,
                                     "line_spacing_factor": spacing})
    m.set_location((x, y), attachment_point=1)
    return m

def circle(c, r, layer="1-CONTORNO", lw=18):
    return msp.add_circle(c, r, dxfattribs={"layer": layer, "lineweight": lw})

def globo(n, at, cpos, r=2.4):
    """Referencia numerada: círculo en cpos, línea hasta el punto 'at' con punto final."""
    dx, dy = at[0] - cpos[0], at[1] - cpos[1]; d = math.hypot(dx, dy) or 1
    s = (cpos[0] + dx / d * r, cpos[1] + dy / d * r)
    pl([s, at], "3-REFERENCIAS", 13)
    msp.add_circle(at, 0.35, dxfattribs={"layer": "3-REFERENCIAS"})
    hh = msp.add_hatch(color=256, dxfattribs={"layer": "3-REFERENCIAS"}); hh.set_solid_fill(color=256)
    hh.paths.add_edge_path().add_arc(at, 0.35, 0, 360)
    circle(cpos, r, "3-REFERENCIAS", 18)
    txt(str(n), cpos[0], cpos[1], 2.4, TA.MIDDLE_CENTER, "3-REFERENCIAS")

class V:
    """Ventana de dibujo: coordenadas reales (mm) -> papel (mm) con escala 1:s y origen (ox, oy)."""
    def __init__(self, s, ox, oy): self.s, self.ox, self.oy = s, ox, oy
    def p(self, x, y): return (self.ox + x / self.s, self.oy + y / self.s)
    def P(self, pts): return [self.p(*q) for q in pts]
    def rect(self, x0, y0, x1, y1): return self.P([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    def dim(self, a, b, off, vertical=False, text=None):
        """Cota lineal asociativa (DIMENSION) mostrando mm reales: dimlfac = escala."""
        pa, pb = self.p(*a), self.p(*b)
        if vertical:
            base = (pa[0] + off, pa[1]); ang = 90
        else:
            base = (pa[0], pa[1] + off); ang = 0
        d = msp.add_linear_dim(base=base, p1=pa, p2=pb, angle=ang, dimstyle="CATALOGO", text=text or "<>",
                               override={"dimlfac": self.s}, dxfattribs={"layer": "2-COTAS"})
        d.render()

ds = doc.dimstyles.new("CATALOGO")
ds.dxf.dimtxt = 2.0; ds.dxf.dimasz = 1.4; ds.dxf.dimblk = "ARCHTICK"; ds.dxf.dimexe = 1.0; ds.dxf.dimexo = 0.8
ds.dxf.dimgap = 0.6; ds.dxf.dimtad = 1; ds.dxf.dimdec = 0; ds.dxf.dimtxsty = "ARIAL"; ds.dxf.dimtih = 0; ds.dxf.dimtoh = 0
ds.dxf.dimclrd = 7; ds.dxf.dimclre = 7; ds.dxf.dimclrt = 7; ds.dxf.dimtmove = 0

def titulo_detalle(num, t1, esc, x, y, w=60):
    """Título tipo catálogo: número en círculo negro + nombre + escala, subrayado."""
    circle((x + 3, y + 1.2), 3, "3-TITULOS", 35)
    txt(num, x + 3, y + 1.2, 2.8, TA.MIDDLE_CENTER, "3-TITULOS", True)
    txt(t1, x + 8, y + 0.2, 2.8, TA.LEFT, "3-TITULOS", True)
    if esc: txt(esc, x + w, y + 0.2, 2.4, TA.RIGHT, "3-TITULOS")
    pl([(x, y - 2), (x + w, y - 2)], "3-TITULOS", 35)

def corte_rotura(v, a, b, layer="1-CONTORNO"):
    """Línea de corte con zigzag entre a y b (coords reales)."""
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L; nx, ny = -uy, ux; k = 6 * v.s / 5
    pts = [(x0 - ux * k, y0 - uy * k), (mx - ux * k, my - uy * k), (mx - ux * k * .4 + nx * k, my - uy * k * .4 + ny * k),
           (mx + ux * k * .4 - nx * k, my + uy * k * .4 - ny * k), (mx + ux * k, my + uy * k), (x1 + ux * k, y1 + uy * k)]
    pl(v.P(pts), layer, 13)

for n, c in {"1-ALUMINIO": 7, "1-VIDRIO": 7, "1-EPDM": 250, "1-AISLACION": 8}.items(): doc.layers.add(n, color=c)

ALU = (205, 208, 212)      # aluminio cortado
VID = (222, 234, 240)      # vidrio
ESM = (150, 150, 150)      # vidrio esmaltado (spandrel)

def caja(v, x0, y0, x1, y1, layer="1-ALUMINIO", fill=ALU, lw=25, pat=None, sc=1.0, ang=0):
    p = v.rect(x0, y0, x1, y1)
    if fill: hatch(p, "SOLID", layer=layer, rgb=fill, color=7 if fill == (255, 255, 255) else 9)
    if pat: hatch(p, pat, sc, ang, layer, color=8)
    pl(p, layer, lw, True)
    return p

def poly(v, pts, layer="1-ALUMINIO", fill=ALU, lw=25):
    p = v.P(pts)
    if fill: hatch(p, "SOLID", layer=layer, rgb=fill, color=9)
    pl(p, layer, lw, True)

def epdm(v, x0, y0, x1, y1):
    p = v.rect(x0, y0, x1, y1)
    hatch(p, "SOLID", layer="1-EPDM", color=250); pl(p, "1-EPDM", 13, True)

def tubo(v, x0, y0, x1, y1, e=2.5, cortado=True):
    """Perfil tubular de aluminio cortado: pared e, interior blanco."""
    caja(v, x0, y0, x1, y1, fill=ALU if cortado else None, lw=35)
    if cortado: caja(v, x0 + e, y0 + e, x1 - e, y1 - e, fill=(255, 255, 255), lw=13)

def tornillo(v, a, b, d=5.0):
    """Tornillo/bulón de a hacia b (coords reales) con roscas."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    pl(v.P([(x0, y0), (x1, y1)]), "1-TORNILLERIA", 35)
    k = 0.3
    while k < 0.95:
        cx, cy = x0 + ux * L * k, y0 + uy * L * k
        pl(v.P([(cx - nx * d / 2, cy - ny * d / 2), (cx + nx * d / 2 + ux * 2, cy + ny * d / 2 + uy * 2)]), "1-TORNILLERIA", 9)
        k += 4 / L
    hd = [(x0 - nx * d, y0 - ny * d), (x0 + nx * d, y0 + ny * d), (x0 + nx * d - ux * 3, y0 + ny * d - uy * 3),
          (x0 - nx * d - ux * 3, y0 - ny * d - uy * 3)]
    pl(v.P(hd), "1-TORNILLERIA", 25, True)

# ------------------------------------------------------------------ geometría del sistema (mm reales)
MW, MD = 50.0, 150.0               # montante (mullion) 50 x 150
TD = 120.0                         # travesaño 50 x 120
L_INT, CAM, L_EXT = 6.76, 12.0, 6.0  # DVH: 3+3 laminado PVB (int) + cámara 12 + templado 6 (ext)
E_DVH = L_INT + CAM + L_EXT        # 24,76
G_INT = 4.0                        # burlete interior (entre perfil y vidrio)
Y_V0 = G_INT                       # cara interior del DVH (medida hacia el exterior desde la cara del perfil)
Y_V1 = G_INT + E_DVH               # cara exterior del DVH
Y_P0 = Y_V1 + 3.0                  # presor
Y_P1 = Y_P0 + 6.0
Y_T1 = Y_P0 + 20.0                 # frente de la tapa

def dvh_sec(v, a0, a1, axis="x", flip=1):
    """DVH en sección: 'axis' es la dirección del canto (largo del paño), y la profundidad va en la otra.
    a0..a1: extensión del paño. flip=+1 profundidad hacia +, -1 hacia -."""
    capas = [(Y_V0, Y_V0 + L_INT, True), (Y_V0 + L_INT + CAM, Y_V1, True)]
    for d0, d1, vid in capas:
        if axis == "x": caja(v, a0, flip * d0, a1, flip * d1, "1-VIDRIO", VID, 25)
        else: caja(v, flip * d0, a0, flip * d1, a1, "1-VIDRIO", VID, 25)
    # interlámina PVB del laminado
    m = Y_V0 + 3.38
    if axis == "x": pl(v.P([(a0, flip * m), (a1, flip * m)]), "1-VIDRIO", 9)
    else: pl(v.P([(flip * m, a0), (flip * m, a1)]), "1-VIDRIO", 9)

def separador(v, borde, sentido, axis="x", flip=1):
    """Separador de aluminio c/ desecante + sellado secundario, en la cámara, junto al canto del DVH."""
    c0, c1 = Y_V0 + L_INT, Y_V0 + L_INT + CAM
    s0, s1 = borde, borde + sentido * 3.0           # sellado secundario (silicona estructural)
    p0, p1 = s1, s1 + sentido * 9.0                 # perfil separador
    for (q0, q1), col in (((s0, s1), 250), ((p0, p1), 9)):
        a, b = min(q0, q1), max(q0, q1)
        pts = v.rect(a, flip * c0, b, flip * c1) if axis == "x" else v.rect(flip * c0, a, flip * c1, b)
        hatch(pts, "SOLID", layer="1-EPDM" if col == 250 else "1-ALUMINIO", color=col, rgb=None if col == 250 else ALU)
        pl(pts, "1-CONTORNO", 9, True)


def g(n, v, at, pos, r=2.1):
    """Globo de referencia chico: 'at' en coords reales de la ventana v, 'pos' en mm de papel."""
    a = v.p(*at) if v else at
    dx, dy = a[0] - pos[0], a[1] - pos[1]; d = math.hypot(dx, dy) or 1
    pl([(pos[0] + dx / d * r, pos[1] + dy / d * r), a], "3-REFERENCIAS", 9)
    hh = msp.add_hatch(color=256, dxfattribs={"layer": "3-REFERENCIAS"}); hh.set_solid_fill(color=256)
    hh.paths.add_edge_path().add_arc(a, 0.3, 0, 360)
    circle(pos, r, "3-REFERENCIAS", 18)
    txt(str(n), pos[0], pos[1], 2.0, TA.MIDDLE_CENTER, "3-REFERENCIAS")

H_A = (225, 225, 225)      # hormigón cortado
EPS = (252, 243, 205)      # EPS
TAPA = (236, 237, 239)

def ficha(x0, x1, x2, ytop, filas, rh=3.3):
    pl([(x0, ytop), (x2, ytop)], "3-TABLAS", 35)
    for i, (a, b) in enumerate(filas):
        y = ytop - (i + 1) * rh
        if i % 2 == 0: hatch([(x0, y), (x2, y), (x2, y + rh), (x0, y + rh)], "SOLID", layer="3-TABLAS", rgb=(238, 238, 238), color=254)
        txt(a, x0 + 1, y + 0.75, 2.0, TA.LEFT, "3-TABLAS", True)
        txt(b, x1 + 1, y + 0.75, 2.0, TA.LEFT, "3-TABLAS")
    yb = ytop - len(filas) * rh
    pl([(x0, yb), (x2, yb)], "3-TABLAS", 35); pl([(x1, ytop), (x1, yb)], "3-TABLAS", 13)
    return yb

def banda(letra, titulo, sub, y):
    hatch([(15, y), (W - 15, y), (W - 15, y + 6), (15, y + 6)], "SOLID", layer="3-TITULOS", rgb=(215, 215, 215), color=254)
    pl([(15, y), (W - 15, y)], "3-TITULOS", 50)
    txt(f"{letra}  ·  {titulo}", 17, y + 3, 3.4, TA.MIDDLE_LEFT, "3-TITULOS", True)
    txt(sub, W - 17, y + 3, 2.2, TA.MIDDLE_RIGHT, "3-TITULOS")

def referencias(titulo, refs, ytop, ncol=5):
    txt(titulo, 15, ytop, 2.4, TA.LEFT, "3-TITULOS", True)
    pl([(15, ytop - 1.4), (W - 15, ytop - 1.4)], "3-TITULOS", 18)
    nrow = math.ceil(len(refs) / ncol); cw = (W - 30) / ncol
    for i, r in enumerate(refs):
        col, row = divmod(i, nrow)
        x, y = 15 + col * cw, ytop - 5 - row * 2.8
        txt(f"{i + 1}", x + 2.6, y, 2.0, TA.RIGHT, "3-REFERENCIAS", True)
        txt(r, x + 3.8, y, 2.0)

def ajustar(raw, cx, cy, wmax, hmax):
    xs = [p[0] for p in raw]; ys = [p[1] for p in raw]
    s = min(wmax / (max(xs) - min(xs)), hmax / (max(ys) - min(ys)))
    return s, cx - (min(xs) + max(xs)) / 2 * s, cy - (min(ys) + max(ys)) / 2 * s

# ==================================================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO DE CERRAMIENTOS", 15, 399, 7.0, TA.LEFT, "3-TITULOS", True)
txt("VIDRIADOS Y OPACOS  |  ESTRUCTURA COMÚN: COLUMNAS H°A 40x40 · VL 40x70 · VIGA L DE BORDE · LOSA SHAP h 16 · BASES C/ CUELLO + VIGA DE FUNDACIÓN", 15, 392, 2.4, TA.LEFT, "3-TITULOS")
pl([(15, 389.5), (W - 15, 389.5)], "3-TITULOS", 70)

# #################################################################################### A · VIDRIADO
banda("A", "CERRAMIENTO VIDRIADO - MURO CORTINA DE ALUMINIO TIPO STICK", "corte integral muro cortina · refs. 30 a 39", 380)

# ---------------------------------------------------------------- A1 AXONOMETRÍA
titulo_detalle("A1", "AXONOMETRÍA", "S/E", 15, 373, 63)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
NMOD, MOD, HS, HT, DZ = 3, 1500.0, 900.0, 2600.0, -700.0
def iso0(x, y, z): return ((x + z) * C30, y + (z - x) * S30)
_raw = [iso0(x, y, z) for x in (-40, NMOD * MOD + 40) for y in (0, HT) for z in (DZ - 300, MD)]
AS, AX0, AY0 = ajustar(_raw, 47, 338, 58, 60)
def iso(x, y, z): q = iso0(x, y, z); return (AX0 + q[0] * AS, AY0 + q[1] * AS)

def bloque(x0, x1, y0, y1, z0, z1, fill, layer="1-ALUMINIO", lw=13, pat=None, sc=1.0, ang=0):
    """Prisma: caras visibles superior (y1), lateral derecha (x1) y exterior (z0)."""
    caras = [[iso(x0, y1, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x0, y1, z1)],
             [iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)],
             [iso(x0, y0, z0), iso(x1, y0, z0), iso(x1, y1, z0), iso(x0, y1, z0)]]
    for i, f in enumerate(caras):
        hatch(f, "SOLID", layer="1-OCULTAR", rgb=fill, color=9)
        if pat and i == 2: hatch(f, pat, sc, ang, layer, color=8)
        pl(f, layer, lw, True)

ZM0, ZM1, ZV0, ZV1, ZT0, ZT1 = 0.0, MD, -Y_V1, -Y_V0, -Y_T1, -Y_P0
ys_t = [0.0, HS, HT]
bloque(-MW / 2, MW / 2, 0, HT, ZM0, ZM1, ALU)
for k in range(NMOD):
    for yt in ys_t: bloque(k * MOD + MW / 2, (k + 1) * MOD - MW / 2, yt - MW / 2, min(yt + MW / 2, HT), ZM0, TD, ALU)
    bloque((k + 1) * MOD - MW / 2, (k + 1) * MOD + MW / 2, 0, HT, ZM0, ZM1, ALU)
for k in range(NMOD):
    bloque(k * MOD + 12, (k + 1) * MOD - 12, 12, HS - 12, ZV0, ZV1, ESM, "1-VIDRIO", 9)
    bloque(k * MOD + 12, (k + 1) * MOD - 12, HS + 12, HT - 12, ZV0, ZV1, VID, "1-VIDRIO", 9, "GLASS", 2.0, 0)
for k in range(NMOD):
    for yt in ys_t: bloque(k * MOD + MW / 2, (k + 1) * MOD - MW / 2, yt - MW / 2, min(yt + MW / 2, HT), ZT0, ZT1, TAPA)
    bloque(k * MOD - MW / 2, k * MOD + MW / 2, 0, HT, ZT0, ZT1, TAPA)
XL = NMOD * MOD
for zz in (ZT0, ZT1): pl([iso(XL + MW / 2, HT, zz), iso(XL + MW / 2, HT, zz + DZ - 300)], "1-VISTA", 9, lt="DASHED")
bloque(XL - MW / 2, XL + MW / 2, 500, HT, -Y_P1 + DZ, -Y_P0 + DZ, ALU)
bloque(XL - MW / 2, XL + MW / 2, 500, HT, ZT0 + DZ - 300, -Y_P1 + DZ - 300, TAPA)
g(1, None, iso(MOD * 0.6, HS + 1200, ZV0), (19, 356)); g(2, None, iso(MOD * 0.5, HS * 0.45, ZV0), (19, 330))
g(5, None, iso(MOD * 1.5, HS, ZT0), (19, 316)); g(3, None, iso(XL + MW / 2, HT * 0.6, ZM1 * 0.5), (76, 344))
g(6, None, iso(XL, 1300, -Y_P1 + DZ), (76, 326)); g(4, None, iso(MOD * 2.5, HT, TD / 2), (76, 360))
txt("módulo 1,50 m", 19, 309.5, 2.0)

# ---------------------------------------------------------------- A2 FICHA TÉCNICA + DVH
titulo_detalle("A2", "FICHA TÉCNICA", "", 82, 373, 100)
yb = ficha(82, 116, 182, 369, [
    ("Sistema", "muro cortina stick, montantes + travesaños"),
    ("Montante", "aluminio 6063-T6, 50 x 150 mm"),
    ("Travesaño", "aluminio 6063-T6, 50 x 120 mm"),
    ("Vidrio visión", "DVH 6 templ. + 12 + 3+3 lam. PVB"),
    ("Spandrel", "templado 6 esmaltado + lana mineral 50"),
    ("Fijación vidrio", "presor + tapa + burletes EPDM"),
    ("Transmit. DVH", "U ≈ 2,8 W/m²·K · Rw ≈ 36 dB"),
    ("Modulación", "1,50 m · spandrel 0,90 m frente a losa"),
    ("Montante colgado", "1 piso (4,50 m) desde cada entrepiso"),
    ("Anclaje", "grapa regulable al riel de la viga L"),
    ("Dilatación", "junta 20 mm c/ manguito por piso")])
v = V(1, 90, yb - 28)
caja(v, 0, 0, 6, 26, "1-VIDRIO", VID, 18); caja(v, 18, 0, 24.76, 26, "1-VIDRIO", VID, 18)
pl(v.P([(21.38, 0), (21.38, 26)]), "1-VIDRIO", 9)
caja(v, 6, 14, 18, 23, layer="1-ALUMINIO", fill=ALU, lw=9); hatch(v.rect(6, 23, 18, 26), "SOLID", layer="1-EPDM", color=250)
for i, (t, xx, yy) in enumerate([("Templado 6 mm (ext.)", 3, 6), ("Cámara 12 mm aire deshidratado", 12, 5),
                                 ("Laminado 3+3 c/ PVB (int.)", 21.4, 4), ("Separador c/ desecante + sellado", 12, 20)]):
    y = v.oy + 23 - i * 4.2
    pl([v.p(xx, yy), (118, y + 0.7), (120, y + 0.7)], "3-REFERENCIAS", 9)
    txt(t, 121, y, 2.0)
txt("DVH esc. 1:1 · e = 24,8 mm", 121, v.oy + 2, 2.0, bold=True)

# ---------------------------------------------------------------- A3 REMATE SUPERIOR 1:10
titulo_detalle("A3", "REMATE", "1:10", 186, 373, 47)
v = V(10, 197, 342)
caja(v, 0, -280, MD, 0, fill=ALU, lw=25)
caja(v, -Y_V1, -280, -Y_V1 + 6, -30, "1-VIDRIO", ESM, 18)
caja(v, -Y_T1, -280, -Y_P0, -30, fill=TAPA, lw=13)
caja(v, MD + 4, -280, MD + 54, -40, "1-AISLACION", (255, 255, 255), 13, "INSUL", 0.05, 90)
zo = [(MD + 60, -280), (MD + 180, -280), (MD + 180, -45), (MD + 60, -45)]
hatch(v.P(zo), "ANSI31", 0.25, 0, "1-HORMIGON", color=8); pl(v.P(zo), "1-HORMIGON", 25, True)
corte_rotura(v, (-Y_T1 - 10, -280), (MD + 190, -280))
pl(v.P([(-Y_T1 - 4, -30), (-Y_T1 - 4, 8), (MD + 2, 8), (MD + 2, -12)]), "1-ALUMINIO", 35)
pl(v.P([(-Y_T1 - 22, -70), (-Y_T1 - 14, -62), (-Y_T1 - 14, 28), (MD + 196, 18), (MD + 196, -50), (MD + 204, -58)]), "1-CHAPA", 40)
g(12, v, (100, 23), (210, 352)); g(13, v, (60, 8), (195, 352)); g(2, v, (-Y_V1 + 3, -150), (190, 316))
g(14, v, (MD + 120, -200), (231, 318)); g(10, v, (MD + 30, -220), (214, 312))

# ---------------------------------------------------------------- A4 ARRANQUE 1:10
titulo_detalle("A4", "ARRANQUE", "1:10", 237, 373, 45)
v = V(10, 252, 330)
ba = [(-60, -150), (MD + 110, -150), (MD + 110, -60), (-60, -60)]
hatch(v.P(ba), "ANSI31", 0.25, 0, "1-HORMIGON", color=8); pl(v.P(ba), "1-HORMIGON", 25, True)
pi = [(MD + 20, -60), (MD + 110, -60), (MD + 110, 0), (MD + 20, 0)]
hatch(v.P(pi), "AR-SAND", 0.02, 0, "1-HORMIGON", color=8); pl(v.P(pi), "1-HORMIGON", 13, True)
ve = [(-130, -150), (-62, -150), (-62, -75), (-130, -78)]
hatch(v.P(ve), "AR-CONC", 0.03, 0, "1-HORMIGON", color=8); pl(v.P(ve), "1-HORMIGON", 13, True)
gu = [(-4, -60), (MD + 4, -60), (MD + 4, 20), (MD + 1, 20), (MD + 1, -57), (-1, -57), (-1, 20), (-4, 20)]
poly(v, gu, fill=ALU, lw=18)
pl(v.P([(MD / 2, -55), (MD / 2, -130)]), "1-TORNILLERIA", 25)
caja(v, 1, -37, MD - 1, 230, fill=ALU, lw=25)
caja(v, -Y_V1, 0, -Y_V1 + 6, 230, "1-VIDRIO", ESM, 18); caja(v, -Y_T1, 0, -Y_P0, 230, fill=TAPA, lw=13)
corte_rotura(v, (-Y_T1 - 6, 230), (MD + 6, 230))
pl(v.P([(-Y_T1 - 2, 30), (-Y_T1 - 2, -2), (-48, -40), (-64, -40), (-64, -78)]), "1-CHAPA", 35)
hatch(v.P([(-4, -60), (-4, -45), (-20, -60)]), "SOLID", layer="1-SELLADOS", color=250)
g(21, v, (MD + 2, -20), (280, 336)); g(22, v, (MD / 2, -110), (280, 320)); g(23, v, (-56, -40), (241, 336))
g(15, v, (-12, -52), (241, 324)); g(3, v, (MD / 2, 150), (280, 350)); g(25, v, (100, -120), (262, 312))

# ---------------------------------------------------------------- A5 MONTANTE - CORTE HORIZONTAL 1:3
titulo_detalle("A5", "MONTANTE", "1:3", 15, 301, 61)
v = V(3, 47, 280)
caja(v, -MW / 2, -100, MW / 2, 0, fill=ALU, lw=25)
caja(v, -MW / 2 + 2.5, -100, MW / 2 - 2.5, -14, fill=(255, 255, 255), lw=9)
caja(v, -MW / 2 + 2.5, -11.5, -4, -2.5, fill=(255, 255, 255), lw=9); caja(v, 4, -11.5, MW / 2 - 2.5, -2.5, fill=(255, 255, 255), lw=9)
caja(v, -3, -12, 3, 0, fill=(255, 255, 255), lw=9)
corte_rotura(v, (-MW / 2 - 4, -100), (MW / 2 + 4, -100))
caja(v, -8, 0, 8, Y_P0, layer="1-AISLACION", fill=(120, 120, 120), lw=9)
for s in (-1, 1):
    a0, a1 = s * 12, s * 70
    dvh_sec(v, min(a0, a1), max(a0, a1), "x", 1)
    separador(v, a0, s, "x", 1)
    epdm(v, min(s * 13, s * 24), 0, max(s * 13, s * 24), Y_V0)
    epdm(v, min(s * 13, s * 24), Y_V1, max(s * 13, s * 24), Y_P0)
    corte_rotura(v, (s * 70, -4), (s * 70, Y_V1 + 4))
caja(v, -MW / 2, Y_P0, MW / 2, Y_P1, fill=ALU, lw=18)
pl(v.P([(-MW / 2, Y_P0 + 0.5), (-MW / 2 - 1, Y_T1), (MW / 2 + 1, Y_T1), (MW / 2, Y_P0 + 0.5)]), "1-ALUMINIO", 35)
tornillo(v, (0, Y_P1), (0, -12), 4)
v.dim((MW / 2, -100), (MW / 2, 0), 5, vertical=True, text="150")
txt("EXT.", v.p(-58, 0)[0], v.p(0, 50)[1], 2.0, TA.MIDDLE_CENTER); txt("INT.", v.p(-58, 0)[0], v.p(0, -40)[1], 2.0, TA.MIDDLE_CENTER)
g(5, v, (8, Y_T1), (34, 297)); g(6, v, (-22, (Y_P0 + Y_P1) / 2), (19, 292)); g(7, v, (-18.5, Y_V0 / 2), (19, 282))
g(8, v, (4, 6), (60, 297)); g(1, v, (55, Y_V0 + 3), (74, 292)); g(9, v, (16, 17), (74, 282))
g(3, v, (0, -60), (19, 258))

# ---------------------------------------------------------------- A6 TRAVESAÑO 1:3
titulo_detalle("A6", "TRAVESAÑO", "1:3", 80, 301, 72)
v = V(3, 113, 272)
tubo(v, 0, -MW / 2, TD, MW / 2)
caja(v, -Y_P0, -8, 0, 8, layer="1-AISLACION", fill=(120, 120, 120), lw=9)
caja(v, -Y_P1, -MW / 2, -Y_P0, MW / 2, fill=ALU, lw=18)
pl(v.P([(-Y_P0 - 0.5, -MW / 2), (-Y_T1, -MW / 2 - 1), (-Y_T1, MW / 2 + 1), (-Y_P0 - 0.5, MW / 2)]), "1-ALUMINIO", 35)
tornillo(v, (-Y_P1, 0), (12, 0), 4)
dvh_sec(v, 12, 70, "y", -1); separador(v, 12, 1, "y", -1)
caja(v, -Y_V1, 8, -Y_V0, 12, layer="1-EPDM", fill=(80, 80, 80), lw=9)
for s in (1, -1):
    epdm(v, -Y_V0, min(s * 13, s * 24), 0, max(s * 13, s * 24))
    epdm(v, -Y_P0, min(s * 13, s * 24), -Y_V1, max(s * 13, s * 24))
caja(v, -Y_V1, -70, -Y_V1 + 6, -12, "1-VIDRIO", ESM, 18)
caja(v, -Y_V1 + 6, -24, -Y_V0, -12, "1-EPDM", (80, 80, 80), 9)
caja(v, 12, -70, 62, -MW / 2 - 4, "1-AISLACION", (255, 255, 255), 13, "INSUL", 0.04, 90)
pl(v.P([(TD - 30, -MW / 2), (TD - 30, -MW / 2 - 4), (63, -MW / 2 - 4), (63, -70)]), "1-CHAPA", 25)
for yy in (70, -70): corte_rotura(v, (-Y_T1 - 4, yy), (TD + 4, yy))
v.dim((0, MW / 2), (TD, MW / 2), 6, text="120")
v.dim((TD, -MW / 2), (TD, MW / 2), 3, vertical=True, text="50")
txt("EXT.", v.p(-45, 0)[0], v.p(0, 64)[1], 2.0, TA.MIDDLE_RIGHT)
g(1, v, (-15, 50), (86, 292)); g(11, v, (-16, 10), (86, 279)); g(2, v, (-Y_V1 + 3, -50), (86, 254))
g(4, v, (60, 0), (148, 290)); g(10, v, (37, -50), (148, 254)); g(7, v, (-Y_V0 / 2 - 2, -18), (86, 266))

# ---------------------------------------------------------------- A7 ANCLAJE Y JUNTA EN ENTREPISO 1:5
titulo_detalle("A7", "ANCLAJE Y JUNTA DE DILATACIÓN EN ENTREPISO", "1:5", 156, 301, 126)
v = V(5, 182, 268)
caja(v, 0, -100, MD, 120, fill=ALU, lw=25); caja(v, 0, 140, MD, 150, fill=ALU, lw=25)
pl(v.P([(6, 30), (6, 150), (MD - 6, 150), (MD - 6, 30), (6, 30)]), "1-VISTA", 13, lt="DASHED")
pl(v.P([(-Y_T1, 130), (-Y_T1 + 6, 130)]), "1-SELLADOS", 40)
caja(v, -Y_V1, -100, -Y_V1 + 6, 150, "1-VIDRIO", ESM, 18); caja(v, -Y_T1, -100, -Y_P0, 150, fill=TAPA, lw=13)
caja(v, MD + 4, -100, MD + 54, 150, "1-AISLACION", (255, 255, 255), 13, "INSUL", 0.08, 90)
pl(v.P([(MD + 55, -100), (MD + 55, 150)]), "1-CHAPA", 25)
lo = [(MD + 80, -100), (MD + 220, -100), (MD + 220, -40), (MD + 80, -40)]
hatch(v.P(lo), "ANSI31", 0.3, 0, "1-HORMIGON", color=8); pl(v.P(lo), "1-HORMIGON", 25, True)
cp = [(MD + 80, -40), (MD + 220, -40), (MD + 220, 0), (MD + 80, 0)]
hatch(v.P(cp), "AR-SAND", 0.025, 0, "1-HORMIGON", color=8); pl(v.P(cp), "1-HORMIGON", 13, True)
corte_rotura(v, (MD + 220, -110), (MD + 220, 10))
bc = [(MD + 56, -90), (MD + 80, -90), (MD + 80, -4), (MD + 56, -4)]
hatch(v.P(bc), "INSUL", 0.04, 90, "1-AISLACION", color=8); pl(v.P(bc), "1-AISLACION", 9, True)
hatch(v.P([(MD + 56, -4), (MD + 80, -4), (MD + 80, 0), (MD + 56, 0)]), "SOLID", layer="1-SELLADOS", color=250)
hatch(v.P([(MD + 110, -40), (MD + 140, -40), (MD + 140, -20), (MD + 110, -20)]), "SOLID", layer="1-ACERO", color=8)
pl(v.P([(MD - 2, -36), (MD + 190, -36), (MD + 190, -30), (MD + 4, -30), (MD + 4, 40), (MD - 2, 40)]), "1-ACERO", 35, True)
tornillo(v, (MD + 125, -26), (MD + 125, -46), 5); tornillo(v, (MD + 10, 15), (60, 15), 5)
for yy in (-100, 150): corte_rotura(v, (-Y_T1 - 6, yy), (MD + 60, yy))
v.dim((-Y_T1, 120), (-Y_T1, 140), -3, vertical=True, text="20")
txt("+4,50", v.p(MD + 160, 8)[0], v.p(0, 8)[1] + 0.8, 2.0)
txt("EXT.", v.p(-80, 0)[0], v.p(0, -40)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
g(16, v, (MD + 160, -33), (262, 252)); g(17, v, (MD + 125, -40), (248, 250)); g(18, v, (MD + 7, 15), (232, 286))
g(19, v, (MD / 2, 130), (250, 297)); g(20, v, (MD + 68, -60), (262, 264)); g(24, v, (MD + 200, -70), (274, 252))
g(2, v, (-Y_V1 + 3, -60), (168, 252)); g(10, v, (MD + 30, 100), (262, 292)); g(3, v, (MD / 2, 0), (232, 275))

referencias("REFERENCIAS · VIDRIADO", [
    "DVH 6+12+3+3 (ref. 32)", "Spandrel templ. 6 esmaltado (ref. 33)", "Montante alum. 50x150 (ref. 30)", "Travesaño alum. 50x120 (31)",
    "Tapa exterior de aluminio (ref. 31)", "Presor de aluminio (ref. 31)", "Burletes EPDM int. / ext. (31)", "Aislador (ruptura puente térm.)",
    "Separador c/ desecante + sellado", "Lana 50 mm en bandeja (ref. 34)", "Calzo / suplemento EPDM",
    "Cupertina chapa galv. N°22 (ref. 1)", "Perfil de cierre sup. (ref. 2)", "Agregado H°A s/ viga L (ref. 8)",
    "Sellador silicona neutra (ref. 39)", "Grapa acero galv. regulable (ref. 36)", "Riel de anclaje + bulón T (ref. 19)",
    "Bulón M12 inox (ref. 36)", "Junta 20 mm + manguito (ref. 37)", "Cortafuego lana + sellador (ref. 35)",
    "Perfil guía de arranque (ref. 38)", "Broca c/ prisionero Ø9,5 (ref. 59)", "Babeta chapa galv. (ref. 49)",
    "Viga L de borde / losa SHAP (13-14)", "Viga de fundación (común)"], 241)

# #################################################################################### B · OPACO
banda("B", "CERRAMIENTO OPACO - PANEL H°A + EPS VERTICAL · ASTORI · e = 20 cm", "misma estructura · cambian juntas y uniones", 217)
EXT_, ALM, INT_ = 50.0, 100.0, 50.0    # hoja ext. H°A / alma EPS / hoja int. H°A (mm)
X1, X2, X3 = EXT_, EXT_ + ALM, EXT_ + ALM + INT_
JS = X3 + 20.0                          # cara de la estructura (junta panel-estructura 20 mm)

def hormigon(v, pts, lw=18, sc=0.03):
    p = v.P(pts); hatch(p, "SOLID", layer="1-HORMIGON", rgb=H_A, color=9)
    hatch(p, "AR-CONC", sc, 0, "1-HORMIGON", color=8); pl(p, "1-HORMIGON", lw, True)

def ha_rayado(v, pts, lw=25, sc=0.3):
    """H°A premoldeado (vigas): relleno gris + rayado ANSI31."""
    p = v.P(pts); hatch(p, "SOLID", layer="1-HORMIGON", rgb=(215, 215, 215), color=9)
    hatch(p, "ANSI31", sc, 0, "1-HORMIGON", color=8); pl(p, "1-HORMIGON", lw, True)

def panel_v(v, y0, y1, cortes=(), lw=25):
    """Panel en corte vertical (exterior a la izquierda, x = 0 cara exterior)."""
    hormigon(v, [(0, y0), (X1, y0), (X1, y1), (0, y1)], 13)
    hormigon(v, [(X2, y0), (X3, y0), (X3, y1), (X2, y1)], 13)
    p = v.rect(X1, y0, X2, y1); hatch(p, "SOLID", layer="1-AISLACION", rgb=EPS, color=9); pl(p, "1-AISLACION", 9, True)
    pl(v.P([(0, y0), (0, y1)]), "1-CONTORNO", lw); pl(v.P([(X3, y0), (X3, y1)]), "1-CONTORNO", lw)
    for c in cortes: corte_rotura(v, (-10, c), (X3 + 10, c))

def sellador(v, x0, y0, x1, y1):
    hatch(v.P([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), "SOLID", layer="1-SELLADOS", color=250)

def viga_vp(v, ytop, x0=JS + 5, b=400.0, corte_inf=None, corte_der=None):
    """Viga VP-70 doble T (h 700, b 400) en corte: alas, cartelas y alma (esquemáticas, como en el corte)."""
    xa, xb = x0, x0 + b; xc = x0 + b / 2
    pts = [(xa, ytop), (xb, ytop), (xb, ytop - 140), (xc + 60, ytop - 240), (xc + 60, ytop - 460), (xb, ytop - 560),
           (xb, ytop - 700), (xa, ytop - 700), (xa, ytop - 560), (xc - 60, ytop - 460), (xc - 60, ytop - 240), (xa, ytop - 140)]
    if corte_inf is not None:                            # recorta la viga en una horizontal
        pts = [(x, max(y, corte_inf)) for x, y in pts]
        pts = [p for i, p in enumerate(pts) if p != pts[i - 1]]
    ha_rayado(v, pts, 25, 0.3)
    return xa, xb, xc

# ---------------------------------------------------------------- B1 AXONOMETRÍA DEL PANEL
titulo_detalle("B1", "AXONOMETRÍA", "S/E", 15, 210, 63)
HP, LP = 2600.0, 1250.0                 # trozo de panel vertical: alto x ancho dibujados
def isoB0(x, y, z): return ((z - x) * C30, y + (x + z) * S30)
_raw = [isoB0(x, y, z) for x in (-20, X3) for y in (0, HP + 150) for z in (0, LP)]
BS, BX0, BY0 = ajustar(_raw, 47, 176, 56, 58)
def isoB(x, y, z): q = isoB0(x, y, z); return (BX0 + q[0] * BS, BY0 + q[1] * BS)
def prismaB(poly, z0, z1, fill, layer="1-CONTORNO", pat=None):
    """Extrusión del perfil (x espesor, y alto) entre z0 y z1; caras visibles -x, +y y tapa z0."""
    n = len(poly); caras = []
    for i in range(n):
        (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
        nx, ny = (yb - ya, xa - xb)
        if -nx + ny > 1e-9:
            caras.append(((-(xa + xb) / 2 + (ya + yb) / 2), [isoB(xa, ya, z0), isoB(xb, yb, z0), isoB(xb, yb, z1), isoB(xa, ya, z1)]))
    for _, f in sorted(caras, key=lambda c: c[0]):
        hatch(f, "SOLID", layer="1-OCULTAR", rgb=fill, color=9); pl(f, layer, 13, True)
    cap = [isoB(x, y, z0) for x, y in poly]
    hatch(cap, "SOLID", layer="1-OCULTAR", rgb=fill, color=9)
    if pat: hatch(cap, pat[0], pat[1], 0, "1-HORMIGON", color=8)
    pl(cap, layer, 18, True)
    return cap
cw_ = lambda x0, x1: [(x0, 0), (x0, HP), (x1, HP), (x1, 0)]
prismaB(cw_(X2, X3), 0, LP, H_A, pat=("AR-CONC", 0.02))
# gancho de fijación sobre el borde superior de la hoja interior
pl([isoB(X2 + 25, HP, 420), isoB(X2 + 25, HP + 130, 420), isoB(X2 + 25, HP + 130, 560), isoB(X2 + 25, HP, 560)], "1-TORNILLERIA", 35)
prismaB(cw_(X1, X2), 200, LP, EPS)
prismaB(cw_(0, X1), 400, LP, H_A, pat=("AR-CONC", 0.02))
g(1, None, isoB(0, 1300, 800), (76, 160)); g(2, None, isoB((X1 + X2) / 2, 1800, 200), (19, 188))
g(3, None, isoB(X3, 400, 80), (19, 160)); g(4, None, isoB(X2 + 25, HP + 130, 490), (76, 200))
txt("vertical · alto de piso a piso", 19, 147.5, 2.0)

# ---------------------------------------------------------------- B2 FICHA TÉCNICA + COMPOSICIÓN
titulo_detalle("B2", "FICHA TÉCNICA", "", 82, 210, 100)
yb = ficha(82, 116, 182, 206, [
    ("Sistema", "panel liso H°A c/ alma EPS, vertical"),
    ("Proveedor", "ASTORI - PL-20 (ficha a confirmar)"),
    ("Espesor", "20 cm: 5 H°A + 10 EPS + 5 H°A"),
    ("Aislación", "EPS ~100 mm · K ≈ 0,33 W/m²·K"),
    ("Peso propio", "≈ 250 kg/m²"),
    ("Estructura", "común: columnas, VL, viga L, losa SHAP"),
    ("Fijación", "grapa regulable al riel de la viga L"),
    ("Remate", "parapeto del panel + cupertina + babeta"),
    ("Arranque", "viga de fundación + neopreno + pasador"),
    ("Juntas", "20 mm: fondo + sellador PU / MS"),
    ("Junta c/ losa", "lana mineral cortafuego + sellador")])
v = V(5, 92, yb - 26)
for x0, x1, f in ((0, X1, H_A), (X2, X3, H_A), (X1, X2, EPS)):
    p = v.rect(x0, 0, x1, 90); hatch(p, "SOLID", layer="1-HORMIGON", rgb=f, color=9)
    if f == H_A: hatch(p, "AR-CONC", 0.025, 0, "1-HORMIGON", color=8)
    pl(p, "1-HORMIGON", 18, True)
v.dim((0, 90), (X1, 90), 2.5, text="5"); v.dim((X1, 90), (X2, 90), 2.5, text="10"); v.dim((X2, 90), (X3, 90), 2.5, text="5")
for i, (t, xx, yy) in enumerate([("Hoja ext. H°A 5 cm", 25, 45), ("Alma EPS 10 cm", 100, 45), ("Hoja int. H°A 5 cm", 175, 45)]):
    y = v.oy + 12 - i * 4.4
    pl([v.p(xx, yy), (134, y + 0.7), (136, y + 0.7)], "3-REFERENCIAS", 9)
    txt(t, 137, y, 2.0)
txt("composición esc. 1:5 (cm)", 137, v.oy + 20.5, 2.0, bold=True)

# ---------------------------------------------------------------- B3 REMATE: PARAPETO DEL PANEL SOBRE CUBIERTA SHAP 1:20
titulo_detalle("B3", "REMATE", "1:20", 186, 210, 47)
v = V(20, 192, 200)    # origen: cara ext. del panel, borde superior del panel
YT = -600              # cubierta terminada (membrana)
panel_v(v, -1100, 0, cortes=(-1100,))
p = v.rect(X3 - 12, -320, X3, -300); hatch(p, "SOLID", layer="1-OCULTAR", rgb=(255, 255, 255), color=7)   # buña
pl(v.P([(-25, -110), (-25, 18), (X3 + 30, 18), (X3 + 30, -50), (X3 + 40, -62)]), "1-CHAPA", 40)       # cupertina
pl(v.P([(100, 18), (100, -60)]), "1-TORNILLERIA", 25)                                                    # tornillo
vl_ = [(JS, -1100), (JS + 150, -1100), (JS + 150, -910), (JS + 250, -910), (JS + 250, -1100)]           # viga L de borde
ha_rayado(v, [(JS, -1100), (JS + 250, -1100), (JS + 250, -910), (JS + 150, -910), (JS + 150, -750), (JS, -750)], 25, 0.3)
shap = [(JS + 150, -910), (JS + 470, -910), (JS + 470, -750), (JS + 150, -750)]                          # losa SHAP h 16
ha_rayado(v, shap, 18, 0.25)
for cx in (JS + 245, JS + 375):
    circle(v.p(cx, -830), 55 / 20, "1-HORMIGON", 18)
    hatch(v.P([(cx + 55 * math.cos(t / 12 * 2 * math.pi), -830 + 55 * math.sin(t / 12 * 2 * math.pi)) for t in range(12)]),
          "SOLID", layer="1-OCULTAR", rgb=(255, 255, 255), color=7)
cap_ = [(JS, -750), (JS + 470, -750), (JS + 470, -700), (JS, -700)]                                       # capa de compresión
hormigon(v, cap_, 13, 0.02)
ce = [(X3, -700), (JS + 470, -700), (JS + 470, -615), (X3, -608)]                                         # contrapiso EPS c/ pend.
hatch(v.P(ce), "SOLID", layer="1-AISLACION", rgb=EPS, color=9); hatch(v.P(ce), "AR-SAND", 0.02, 0, "1-HORMIGON", color=8)
pl(v.P(ce), "1-HORMIGON", 13, True)
hatch(v.P([(X3, YT - 8), (X3 + 60, YT - 8), (X3, YT + 52)]), "SOLID", layer="1-HORMIGON", rgb=H_A, color=9)   # media caña
pl(v.P([(X3 + 2, -310), (X3 + 2, YT + 52), (X3 + 60, YT - 6), (JS + 470, YT - 13)]), "1-CHAPA", 35)        # membrana
pl(v.P([(X3 - 10, -302), (X3 + 26, -302), (X3 + 26, -380)]), "1-CHAPA", 25)                                # babeta en buña
lm = [(X3, -1100), (JS, -1100), (JS, -700), (X3, -700)]                                                   # junta c/ lana mineral
hatch(v.P(lm), "INSUL", 0.03, 90, "1-AISLACION", color=8); pl(v.P(lm), "1-AISLACION", 9, True)
corte_rotura(v, (JS + 470, -1110), (JS + 470, -600)); corte_rotura(v, (JS - 10, -1100), (JS + 260, -1100))
txt("pend. 2 %", v.p(JS + 330, -560)[0], v.p(0, -560)[1], 2.0, TA.MIDDLE_CENTER)
g(10, v, (100, 18), (199, 205.3)); g(11, v, (100, -40), (224, 205.3)); g(12, v, (X3 + 20, -330), (231, 197))
g(13, v, (X3 + 2, -450), (231, 187)); g(14, v, (JS + 300, -660), (231, 177)); g(15, v, (JS + 400, -800), (231, 166))
g(16, v, (JS + 60, -1000), (231, 155)); g(8, v, (X3 + 10, -900), (205, 148)); g(1, v, (25, -800), (189, 160))

# ---------------------------------------------------------------- B4 ARRANQUE SOBRE VIGA PORTAPANEL 1:20
titulo_detalle("B4", "ARRANQUE", "1:20", 237, 210, 45)
v = V(20, 256, 172)    # origen: cara ext. del panel, cara superior de la viga de fundación (±0,00)
pp = [(0, -500), (220, -500), (220, 0), (0, 0)]                                                          # viga de fundación (común)
ha_rayado(v, pp, 25, 0.3); corte_rotura(v, (-10, -500), (230, -500))
hatch(v.P([(20, 0), (180, 0), (180, 15), (20, 15)]), "SOLID", layer="1-EPDM", color=250)                # neopreno + anclaje
panel_v(v, 15, 620, cortes=(620,))
pl(v.P([(100, -300), (100, 300)]), "1-TORNILLERIA", 35)                                                  # pasador en vaina
pl(v.P([(90, -300), (90, 300), (110, 300), (110, -300), (90, -300)]), "1-VISTA", 9, lt="DASHED")
sellador(v, -8, 0, 0, 15)
ve = [(-330, -280), (-10, -280), (-10, -150), (-330, -150)]                                              # vereda
hormigon(v, ve, 13, 0.03); corte_rotura(v, (-330, -140), (-330, -290))
pl(v.P([(-330, -150), (-10, -150)]), "1-CONTORNO", 25)
hatch(v.P([(-10, -280), (0, -280), (0, -150), (-10, -150)]), "SOLID", layer="1-AISLACION", rgb=EPS, color=9)  # junta EPS 10
pl(v.P([(-2, -500), (-2, -280)]), "1-SELLADOS", 35)                                                      # pintura asfáltica
hatch(v.P([(-330, -500), (-12, -500), (-12, -282), (-330, -282)]), "EARTH", 0.3, 45, "1-SUELO", color=8)
fi = [(230, -190), (420, -190), (420, 0), (230, 0)]                                                       # piso interior
hormigon(v, fi, 13, 0.03); corte_rotura(v, (420, -200), (420, 10))
txt("-0,15", v.p(-325, -140)[0], v.p(0, -140)[1] + 0.6, 2.0)
txt("±0,00", v.p(240, 10)[0], v.p(0, 10)[1] + 0.6, 2.0)
g(21, v, (110, -400), (279, 152)); g(22, v, (150, 8), (279, 178)); g(23, v, (100, 150), (279, 190))
g(24, v, (-5, -200), (241, 150)); g(25, v, (-2, -400), (262, 144)); g(26, v, (-200, -210), (241, 158))
g(9, v, (-4, 8), (241, 180)); g(1, v, (25, 450), (241, 196))

# ---------------------------------------------------------------- B5 JUNTA VERTICAL - PLANTA 1:5
titulo_detalle("B5", "JUNTA VERTICAL · PLANTA", "1:5", 15, 138, 84)
v = V(5, 58, 125)     # x a lo largo de la fachada, y = 0 cara exterior, interior hacia -y
for s in (-1, 1):
    a, b = s * 10, s * 165
    lo_, hi_ = min(a, b), max(a, b)
    hormigon(v, [(lo_, 0), (hi_, 0), (hi_, -X1), (lo_, -X1)], 13)
    p = v.rect(lo_, -X1, hi_, -X2); hatch(p, "SOLID", layer="1-AISLACION", rgb=EPS, color=9); pl(p, "1-AISLACION", 9, True)
    hormigon(v, [(lo_, -X2), (hi_, -X2), (hi_, -X3), (lo_, -X3)], 13)
    corte_rotura(v, (b, 10), (b, -X3 - 10))
for y0 in (0, -X3):
    sg = -1 if y0 == 0 else 1
    hatch(v.P([(-10, y0), (10, y0), (10, y0 + sg * 12), (-10, y0 + sg * 12)]), "SOLID", layer="1-SELLADOS", color=250)
    circle(v.p(0, y0 + sg * 22), 10 / 5, "1-SELLADOS", 13)
v.dim((-10, 0), (10, 0), 5, text="20"); v.dim((165, 0), (165, -X3), 4, vertical=True, text="200")
txt("EXT.", v.p(-125, 0)[0], v.p(0, 12)[1], 2.0, TA.MIDDLE_CENTER); txt("INT.", v.p(-125, 0)[0], v.p(0, -X3 - 10)[1], 2.0, TA.MIDDLE_CENTER)
g(9, v, (0, -6), (46, 133.5)); g(1, v, (-100, -25), (19, 131)); g(2, v, (-70, -100), (19, 116))
g(3, v, (-100, -175), (19, 100)); g(9, v, (0, -X3 + 6), (72, 89))
txt("Junta abierta 20 mm entre paneles:", 102, 116, 2.0, bold=True)
txt("fondo de junta + sellador elástico", 102, 112.4, 2.0); txt("(poliuretano / MS) en ambas caras.", 102, 108.8, 2.0)
txt("Ancho del panel según fabricante", 102, 103.6, 2.0); txt("(Astori, a confirmar).", 102, 100, 2.0)

# ---------------------------------------------------------------- B6 FIJACIÓN A LA VIGA L DE BORDE Y JUNTA DE ENTREPISO 1:15
titulo_detalle("B6", "FIJACIÓN A LA VIGA L Y JUNTA EN ENTREPISO", "1:15", 152, 138, 130)
v = V(15, 160, 118)    # origen: cara ext. del panel, nivel de piso terminado (+4,50)
panel_v(v, -560, 150, cortes=(-560, 150))
# viga L de borde (común): pata exterior + talón que recibe la losa SHAP; apoya sobre la VL
ha_rayado(v, [(JS, -560), (JS + 260, -560), (JS + 260, -420), (JS + 160, -420), (JS + 160, -130), (JS, -130)], 25, 0.3)
shap = [(JS + 160, -420), (JS + 560, -420), (JS + 560, -260), (JS + 160, -260)]                          # losa SHAP h 16
ha_rayado(v, shap, 18, 0.25)
for cx in (JS + 260, JS + 390, JS + 520):
    hatch(v.P([(cx + 50 * math.cos(t / 12 * 2 * math.pi), -340 + 50 * math.sin(t / 12 * 2 * math.pi)) for t in range(12)]),
          "SOLID", layer="1-OCULTAR", rgb=(255, 255, 255), color=7)
    circle(v.p(cx, -340), 50 / 15, "1-HORMIGON", 18)
cc = [(JS + 160, -260), (JS + 560, -260), (JS + 560, -130), (JS + 160, -130)]                              # capa de compresión
hormigon(v, cc, 13, 0.02)
cp = [(JS, -130), (JS + 560, -130), (JS + 560, 0), (JS, 0)]                                                # contrapiso + carpeta + solado
hatch(v.P(cp), "AR-SAND", 0.02, 0, "1-HORMIGON", color=8); pl(v.P(cp), "1-HORMIGON", 13, True)
pl(v.P([(JS, -15), (JS + 560, -15)]), "1-HORMIGON", 9)
corte_rotura(v, (JS + 560, -430), (JS + 560, 10)); corte_rotura(v, (JS - 10, -560), (JS + 270, -560))
hatch(v.P([(X3 + 4, 0), (X3 + 12, 0), (X3 + 12, 100), (X3 + 4, 100)]), "SOLID", layer="1-ACERO", color=8)   # zócalo
lm = [(X3, -540), (JS, -540), (JS, -15), (X3, -15)]                                                       # lana mineral
hatch(v.P(lm), "INSUL", 0.03, 90, "1-AISLACION", color=8); pl(v.P(lm), "1-AISLACION", 9, True)
sellador(v, X3, -15, JS, 0)
# riel de anclaje embutido en la pata de la viga L + grapa regulable + inserto del panel (igual que el muro cortina)
hatch(v.P([(JS, -300), (JS + 30, -300), (JS + 30, -260), (JS, -260)]), "SOLID", layer="1-ACERO", color=8)       # riel
hatch(v.P([(X3 - 15, -310), (X3, -310), (X3, -250), (X3 - 15, -250)]), "SOLID", layer="1-ACERO", color=8)       # inserto
pl(v.P([(X3 - 8, -280), (JS + 70, -280)]), "1-TORNILLERIA", 50)                                          # grapa + bulón T
pl(v.P([(X3 + 4, -320), (X3 + 14, -320), (X3 + 14, -240), (X3 + 4, -240), (X3 + 4, -320)]), "1-ACERO", 35)
pl(v.P([(JS + 50, -300), (JS + 70, -300), (JS + 70, -260), (JS + 50, -260), (JS + 50, -300)]), "1-TORNILLERIA", 25)
txt("NPT +4,50", v.p(JS + 330, 15)[0], v.p(0, 15)[1] + 0.6, 2.0)
g(5, v, (X3 - 8, -280), (155, 98)); g(6, v, (X3 + 9, -320), (170, 88)); g(7, v, (JS + 15, -290), (192, 88))
g(8, v, (X3 + 10, -450), (155, 110)); g(9, v, (X3 + 10, -8), (172, 131)); g(20, v, (X3 + 8, 60), (155, 128))
g(16, v, (JS + 100, -500), (210, 86)); g(15, v, (JS + 450, -380), (226, 96)); g(18, v, (JS + 450, -200), (228, 108))
g(19, v, (JS + 450, -60), (228, 120)); g(1, v, (25, -100), (155, 119))
txt("Mismo anclaje que el muro cortina:", 238, 118, 2.0, bold=True)
txt("riel embutido en la viga L de borde", 238, 114.4, 2.0); txt("+ grapa regulable al inserto del panel.", 238, 110.8, 2.0)
txt("Junta panel-estructura 20 mm con", 238, 105.6, 2.0); txt("lana mineral (cortafuego) y sellador.", 238, 102, 2.0)
txt("Losa SHAP h 16 s/ talón de la viga L;", 238, 96.8, 2.0); txt("la viga L apoya sobre la VL 40x70.", 238, 93.2, 2.0)

referencias("REFERENCIAS · OPACO", [
    "Hoja ext. H°A 5 cm (panel)", "Alma de EPS ~100 mm", "Hoja int. H°A 5 cm (panel)", "Gancho de izaje inserto",
    "Inserto canal de anclaje del panel", "Grapa galv. regulable (= vidriado)", "Riel embutido + bulón T (común)",
    "Lana mineral cortafuego", "Fondo de junta + sellador PU / MS", "Cupertina chapa galv. c/ goterón",
    "Tornillo c/ arandela de neopreno", "Babeta chapa galv. en buña", "Membrana asfáltica + media caña",
    "Contrapiso H° EPS pend. 2 % (común)", "Losa hueca SHAP h 16 (común)", "Viga L de borde (común)",
    "Viga VL doble T 40x70 (común)", "Capa de compresión 5 cm (común)", "Contrapiso + carpeta + solado",
    "Zócalo 10 x 100 mm", "Viga de fundación perimetral (común)", "Neopreno + anclaje inferior",
    "Pasador en vaina c/ grout", "Junta vereda EPS 10 mm + sellador", "Pintura asfáltica", "Vereda / contrapiso armado (común)"], 78)

# ---------------------------------------------------------------- SISTEMA COMÚN: QUÉ CAMBIA EN CADA CERRAMIENTO
txt("SISTEMA CONSTRUCTIVO COMÚN · UNIONES Y JUNTAS DE CADA CERRAMIENTO", 15, 53.5, 2.6, TA.LEFT, "3-TITULOS", True)
pl([(15, 52), (W - 15, 52)], "3-TITULOS", 25)
tx = [15, 38, 160, 282]; th = 3.4; ty = 51
filas_c = [("", "A · VIDRIADO (muro cortina)", "B · OPACO (panel H°A + EPS)"),
           ("Entrepiso", "montante colgado: grapa + bulón M12 al riel de la viga L; junta 20 mm c/ manguito",
                         "panel apoyado abajo: grapa regulable al riel de la viga L; junta 20 mm c/ lana mineral"),
           ("Cubierta", "perfil de cierre + cupertina s/ agregado H°A sobre la viga L",
                        "el panel sube como parapeto: cupertina + membrana c/ babeta en buña"),
           ("Fundación", "perfil guía deslizante anclado c/ broca a la viga de fundación",
                         "panel apoyado s/ la viga de fundación: neopreno + pasador en vaina"),
           ("Juntas", "burletes EPDM + presor; sellado de silicona neutra",
                      "20 mm: fondo de junta + sellador PU / MS en ambas caras")]
for i, (a_, b_, c_) in enumerate(filas_c):
    y = ty - (i + 1) * th
    if i == 0: hatch([(tx[0], y), (tx[3], y), (tx[3], y + th), (tx[0], y + th)], "SOLID", layer="3-TABLAS", rgb=(225, 225, 225), color=254)
    elif i % 2 == 0: hatch([(tx[0], y), (tx[3], y), (tx[3], y + th), (tx[0], y + th)], "SOLID", layer="3-TABLAS", rgb=(242, 242, 242), color=254)
    txt(a_, tx[0] + 1, y + 0.8, 2.0, TA.LEFT, "3-TABLAS", True)
    txt(b_, tx[1] + 1, y + 0.8, 2.0, TA.LEFT, "3-TABLAS", i == 0)
    txt(c_, tx[2] + 1, y + 0.8, 2.0, TA.LEFT, "3-TABLAS", i == 0)
yb_ = ty - len(filas_c) * th
for x in tx: pl([(x, ty), (x, yb_)], "3-TABLAS", 13)
for y in (ty, ty - th, yb_): pl([(tx[0], y), (tx[3], y)], "3-TABLAS", 25)
txt("Estructura y fundación iguales para ambos (detalle en el corte SHAP, en desarrollo). "
    "Valores de catálogo: verificar con el fabricante.", 15, yb_ - 3.8, 2.0)

# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 26
xs = [15, 41, 170, 237, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 20.4, 3.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 05/11/2026", (xs[0] + xs[1]) / 2, 15.0, 2.0, TA.MIDDLE_CENTER)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 22.6, 2.4)
txt("ALUMNA: Candelaria Vitale", xs[1] + 2, 19.0, 2.4)
txt("GRUPO: 13", xs[1] + 2, 15.4, 2.4)
txt("NIVEL:", xs[2] + 2, 22.6, 2.4); txt("OBS:", xs[2] + 2, 19.0, 2.4)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 21.0, 2.6, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 17.0, 2.6, TA.MIDDLE_CENTER)

doc.saveas(f"{OUT}/Lamina4_Catalogo_Vidriado_y_Opaco_v3_A3.dxf")
print("ok")
