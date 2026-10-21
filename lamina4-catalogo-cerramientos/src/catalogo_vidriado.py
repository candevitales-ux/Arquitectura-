# -*- coding: utf-8 -*-
"""Lámina 4 - Catálogo de cerramientos: VIDRIADO (muro cortina stick del corte integral muro cortina).
Mismo método que el catálogo opaco: un único DXF en mm de papel (A3 vertical, escala 1:1 de la hoja);
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

# ==================================================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CATÁLOGO DE CERRAMIENTOS", 15, 398, 7.5, TA.LEFT, "3-TITULOS", True)
txt("VIDRIADOS  |  MURO CORTINA DE ALUMINIO TIPO STICK", 15, 389.5, 4.2, TA.LEFT, "3-TITULOS")
txt("LÁMINA 4", W - 15, 398, 7.5, TA.RIGHT, "3-TITULOS", True)
txt("CORTE INTEGRAL MURO CORTINA - REFS. 25 A 34", W - 15, 389.5, 2.6, TA.RIGHT, "3-TITULOS")
pl([(15, 386), (W - 15, 386)], "3-TITULOS", 70)

# ---------------------------------------------------------------- 01 AXONOMETRÍA DEL SISTEMA (S/E)
titulo_detalle("1", "EL SISTEMA - AXONOMETRÍA", "S/E", 15, 378, 128)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
NMOD, MOD, HS, HT = 3, 1500.0, 900.0, 2600.0     # módulos dibujados, módulo, alto spandrel, alto dibujado
AS = 1 / 66.0
DZ = -700.0                                       # despiece de presor y tapa hacia el exterior
_raw = [((x + z) * C30, y + (z - x) * S30) for x in (-40, NMOD * MOD + 40) for y in (0, HT) for z in (DZ - 300, MD)]
AX0 = 79 - (min(p[0] for p in _raw) + max(p[0] for p in _raw)) / 2 * AS
AY0 = 337 - (min(p[1] for p in _raw) + max(p[1] for p in _raw)) / 2 * AS
# vista desde el exterior, de frente-derecha y desde arriba: se ven las caras -z (exterior), +y (arriba) y +x (derecha)
def iso(x, y, z): return (AX0 + (x + z) * C30 * AS, AY0 + (y + (z - x) * S30) * AS)

def bloque(x0, x1, y0, y1, z0, z1, fill, layer="1-ALUMINIO", lw=18, pat=None, sc=1.0, ang=0):
    """Prisma recto: se dibujan las caras visibles superior (y1), lateral derecha (x1) y exterior (z0)."""
    caras = [[iso(x0, y1, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x0, y1, z1)],
             [iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)],
             [iso(x0, y0, z0), iso(x1, y0, z0), iso(x1, y1, z0), iso(x0, y1, z0)]]
    for i, f in enumerate(caras):
        hatch(f, "SOLID", layer="1-OCULTAR", rgb=fill, color=9)
        if pat and i == 2: hatch(f, pat, sc, ang, layer, color=8)
        pl(f, layer, lw, True)

ZM0, ZM1 = 0.0, MD                      # montantes: de la cara exterior del perfil hacia el interior
ZV0, ZV1 = -Y_V1, -Y_V0                 # vidrio
ZT0, ZT1 = -Y_T1, -Y_P0                 # tapa
TAPA = (236, 237, 239)
ys_t = [0.0, HS, HT]
# 1) estructura (atrás), de izquierda a derecha para que cada montante tape el extremo del travesaño
bloque(-MW / 2, MW / 2, 0, HT, ZM0, ZM1, ALU)
for k in range(NMOD):
    for yt in ys_t: bloque(k * MOD + MW / 2, (k + 1) * MOD - MW / 2, yt - MW / 2, min(yt + MW / 2, HT), ZM0, TD, ALU)
    bloque((k + 1) * MOD - MW / 2, (k + 1) * MOD + MW / 2, 0, HT, ZM0, ZM1, ALU)
# 2) paños: spandrel (abajo) y visión (arriba)
for k in range(NMOD):
    bloque(k * MOD + 12, (k + 1) * MOD - 12, 12, HS - 12, ZV0, ZV1, ESM, "1-VIDRIO", 13)
    bloque(k * MOD + 12, (k + 1) * MOD - 12, HS + 12, HT - 12, ZV0, ZV1, VID, "1-VIDRIO", 13, "GLASS", 2.5, 0)
# 3) tapas exteriores: horizontales primero, después verticales; la del último montante va en despiece
for k in range(NMOD):
    for yt in ys_t: bloque(k * MOD + MW / 2, (k + 1) * MOD - MW / 2, yt - MW / 2, min(yt + MW / 2, HT), ZT0, ZT1, TAPA)
    if k < NMOD: bloque(k * MOD - MW / 2, k * MOD + MW / 2, 0, HT, ZT0, ZT1, TAPA)
XL = NMOD * MOD
for zz in (ZT0, ZT1):
    pl([iso(XL + MW / 2, HT, zz), iso(XL + MW / 2, HT, zz + DZ - 300)], "1-VISTA", 9, lt="DASHED")
bloque(XL - MW / 2, XL + MW / 2, 500, HT, -Y_P1 + DZ, -Y_P0 + DZ, ALU)                 # presor
bloque(XL - MW / 2, XL + MW / 2, 500, HT, ZT0 + DZ - 300, -Y_P1 + DZ - 300, TAPA)     # tapa
def gax(n, P, x, dy=0): globo(n, P, (x, P[1] + dy))
gax(1, iso(MOD * 0.6, HS + 1200, ZV0), 22, 6)
gax(2, iso(MOD * 0.5, HS * 0.45, ZV0), 22)
gax(4, iso(MOD * 1.5, HS, ZT0), 22, -14)
gax(3, iso(XL + MW / 2, HT * 0.6, ZM1 * 0.5), 138, 4)
gax(5, iso(XL, 1300, -Y_P1 + DZ), 138, 0)
gax(6, iso(XL, 900, ZT0 + DZ - 300), 138, -4)
gax(7, iso(MOD * 2.5, HT, TD / 2), 138, 4)
txt("módulo 1,50 m · 3 módulos", 17, 302, 2.2)

# ---------------------------------------------------------------- 02 FICHA TÉCNICA
titulo_detalle("2", "FICHA TÉCNICA", "", 152, 378, 130)
filas = [("Sistema", "Muro cortina stick (montantes + travesaños)"),
         ("Uso en el corte", "Fachada vidriada (refs. 25 a 34) s/ estructura H°A°"),
         ("Montante (mullion)", "aluminio 6063-T6, 50 x 150 mm (ref. 25)"),
         ("Travesaño", "aluminio 6063-T6, 50 x 120 mm"),
         ("Fijación del vidrio", "presor + tapa a presión + burletes EPDM"),
         ("Vidrio visión (DVH)", "6 templado + 12 cámara + 3+3 lam. PVB"),
         ("Espesor DVH", "24,8 mm (ref. 27)"),
         ("Spandrel", "vidrio templado 6 mm esmaltado (ref. 28)"),
         ("Aislación spandrel", "lana mineral 50 mm + bandeja chapa galv."),
         ("Transmitancia DVH U", "≈ 2,8 W/m²·K"),
         ("Factor solar g", "≈ 0,70 (incoloro)"),
         ("Aislación acústica Rw", "≈ 36 dB"),
         ("Módulo horizontal", "1,50 m entre ejes de montantes"),
         ("Altura de montante", "1 piso: 4,50 m (colgado del entrepiso)"),
         ("Anclaje", "grapa acero galv. regulable + bulón M12 inox"),
         ("Dilatación vertical", "junta 20 mm c/ manguito en cada piso"),
         ("Estanqueidad", "drenaje y ventilación por travesaños"),
         ("Terminación perfiles", "anodizado natural o pintura poliéster"),
         ("Tolerancias montaje", "±2 mm en plomo y nivel por módulo")]
fx0, fx1, fx2, fy = 152, 196, 282, 373
rh = 3.6
pl([(fx0, fy), (fx2, fy)], "3-TABLAS", 35)
for i, (a, b) in enumerate(filas):
    y = fy - (i + 1) * rh
    if i % 2 == 0: hatch([(fx0, y), (fx2, y), (fx2, y + rh), (fx0, y + rh)], "SOLID", layer="3-TABLAS", rgb=(238, 238, 238), color=254)
    txt(a, fx0 + 1.2, y + 0.9, 2.1, TA.LEFT, "3-TABLAS", True)
    txt(b, fx1 + 1.2, y + 0.9, 2.1, TA.LEFT, "3-TABLAS")
yb = fy - len(filas) * rh
pl([(fx0, yb), (fx2, yb)], "3-TABLAS", 35); pl([(fx1, fy), (fx1, yb)], "3-TABLAS", 13)
txt("Valores de referencia de catálogo: verificar con el fabricante elegido.", fx0, yb - 3.5, 2.0)

# ---------------------------------------------------------------- 03 MONTANTE - CORTE HORIZONTAL 1:3
titulo_detalle("3", "MONTANTE - CORTE HORIZ.", "ESC. 1:3", 15, 294, 86)
v3 = V(3, 58, 263)     # origen: eje del montante, cara exterior del perfil; +y hacia el exterior
caja(v3, -MW / 2, -MD, MW / 2, 0, fill=ALU, lw=35)
caja(v3, -MW / 2 + 2.5, -MD + 2.5, MW / 2 - 2.5, -14, fill=(255, 255, 255), lw=13)
caja(v3, -MW / 2 + 2.5, -11.5, -4, -2.5, fill=(255, 255, 255), lw=13); caja(v3, 4, -11.5, MW / 2 - 2.5, -2.5, fill=(255, 255, 255), lw=13)
caja(v3, -3, -12, 3, 0, fill=(255, 255, 255), lw=9)                                 # canal de tornillo
caja(v3, -8, 0, 8, Y_P0, layer="1-AISLACION", fill=(120, 120, 120), lw=13)           # aislador / RPT
for s in (-1, 1):
    a0, a1 = s * 12, s * 100
    dvh_sec(v3, min(a0, a1), max(a0, a1), "x", 1)
    separador(v3, a0, s, "x", 1)
    epdm(v3, min(s * 13, s * 24), 0, max(s * 13, s * 24), Y_V0)                    # burlete interior
    epdm(v3, min(s * 13, s * 24), Y_V1, max(s * 13, s * 24), Y_P0)                  # burlete exterior
    corte_rotura(v3, (s * 100, -4), (s * 100, Y_V1 + 4))
caja(v3, -MW / 2, Y_P0, MW / 2, Y_P1, fill=ALU, lw=25)                              # presor
pl(v3.P([(-MW / 2, Y_P0 + 0.5), (-MW / 2 - 1, Y_T1), (MW / 2 + 1, Y_T1), (MW / 2, Y_P0 + 0.5)]), "1-ALUMINIO", 35)  # tapa
pl(v3.P([(-MW / 2 + 2, Y_P1 + 1), (-MW / 2 + 1, Y_T1 - 2), (MW / 2 - 1, Y_T1 - 2), (MW / 2 - 2, Y_P1 + 1)]), "1-ALUMINIO", 13)
tornillo(v3, (0, Y_P1), (0, -12), 4)
v3.dim((-MW / 2, -MD), (MW / 2, -MD), -3.5, text="50")
v3.dim((MW / 2, -MD), (MW / 2, 0), 6, vertical=True, text="150")
v3.dim((100, Y_V0), (100, Y_V1), 5, vertical=True, text="24,8")
txt("EXT.", v3.p(-88, 0)[0], v3.p(0, 42)[1], 2.0, TA.MIDDLE_CENTER)
txt("INT.", v3.p(-88, 0)[0], v3.p(0, -32)[1], 2.0, TA.MIDDLE_CENTER)
def g3(n, at, dx, dy, v=None): globo(n, (v or v3).p(*at), ((v or v3).ox + dx, (v or v3).oy + dy))
g3(9, (8, Y_T1), -22, 22); g3(10, (-22, (Y_P0 + Y_P1) / 2), -36, 18); g3(13, (-18.5, (Y_V1 + Y_P0) / 2), -38, 9)
g3(11, (-18.5, Y_V0 / 2), -38, -2); g3(12, (4, 6), 16, 22); g3(15, (60, Y_V0 + 3), 30, 17)
g3(14, (16, 17), 30, -9); g3(16, (0, -6), -38, -13); g3(8, (0, -100), -22, -38)

# ---------------------------------------------------------------- 04 TRAVESAÑO VISIÓN / SPANDREL - CORTE 1:3
titulo_detalle("4", "TRAVESAÑO", "ESC. 1:3", 105, 294, 86)
v4 = V(3, 146, 252)    # origen: cara exterior del perfil (x=0, exterior hacia -x), eje del travesaño
tubo(v4, 0, -MW / 2, TD, MW / 2)
caja(v4, -Y_P0, -8, 0, 8, layer="1-AISLACION", fill=(120, 120, 120), lw=13)
caja(v4, -Y_P1, -MW / 2, -Y_P0, MW / 2, fill=ALU, lw=25)
pl(v4.P([(-Y_P0 - 0.5, -MW / 2), (-Y_T1, -MW / 2 - 1), (-Y_T1, MW / 2 + 1), (-Y_P0 - 0.5, MW / 2)]), "1-ALUMINIO", 35)
tornillo(v4, (-Y_P1, 0), (12, 0), 4)
dvh_sec(v4, 12, 85, "y", -1)                                                       # DVH (visión) arriba
separador(v4, 12, 1, "y", -1)
caja(v4, -Y_V1, 8, -Y_V0, 12, layer="1-EPDM", fill=(80, 80, 80), lw=13)            # calzo de apoyo
for s in (1, -1):
    epdm(v4, -Y_V0, min(s * 13, s * 24), 0, max(s * 13, s * 24))
    epdm(v4, -Y_P0, min(s * 13, s * 24), -Y_V1, max(s * 13, s * 24))
caja(v4, -Y_V1, -85, -Y_V1 + 6, -12, "1-VIDRIO", ESM, 25)                         # spandrel esmaltado
caja(v4, -Y_V1 + 6, -24, -Y_V0, -12, "1-EPDM", (80, 80, 80), 13)                  # suplemento EPDM
caja(v4, 12, -85, 62, -MW / 2 - 4, "1-AISLACION", (255, 255, 255), 18, "INSUL", 0.05, 90)
pl(v4.P([(TD - 30, -MW / 2), (TD - 30, -MW / 2 - 4), (63, -MW / 2 - 4), (63, -85)]), "1-CHAPA", 35)   # bandeja
for yy in (85, -85): corte_rotura(v4, (-Y_T1 - 4, yy), (TD + 4, yy))
v4.dim((0, MW / 2), (TD, MW / 2), 10, text="120")
v4.dim((TD, -MW / 2), (TD, MW / 2), 4, vertical=True, text="50")
txt("EXT.", v4.p(-62, 0)[0], v4.p(0, 74)[1], 2.0, TA.MIDDLE_CENTER)
txt("INT.", v4.p(150, 0)[0], v4.p(0, 74)[1], 2.0, TA.MIDDLE_CENTER)
g3(1, (-15, 60), -34, 26, v4); g3(36, (-16, 10), -34, 10, v4); g3(37, (-Y_T1 + 3, -MW / 2 - 2), -34, -4, v4)
g3(20, (-12, -18), -34, -14, v4); g3(2, (-Y_V1 + 3, -60), -34, -24, v4); g3(17, (60, 0), 30, 13, v4)
g3(18, (37, -60), 14, -30, v4); g3(19, (63, -70), 38, -18, v4)

# ---------------------------------------------------------------- 05 MODULACIÓN (S/E)
titulo_detalle("5", "MODULACIÓN", "S/E", 196, 294, 86)
mx0, my0, mw, mh = 211, 222, 56, 62
nm = 4
esc = mh / 9.47
for y0, y1 in ((0, 0.9), (4.5, 5.4), (9.0, 9.47)):
    hatch([(mx0, my0 + y0 * esc), (mx0 + mw, my0 + y0 * esc), (mx0 + mw, my0 + y1 * esc), (mx0, my0 + y1 * esc)],
          "ANSI31", 0.25, 0, "1-VIDRIO", color=8)
for y0, y1 in ((0.9, 4.5), (5.4, 9.0)):
    for k in range(nm):
        x = mx0 + mw * k / nm
        pl([(x + 2, my0 + y1 * esc - 3), (x + 6, my0 + y1 * esc - 7)], "1-VIDRIO", 9)
        pl([(x + 2, my0 + y1 * esc - 6), (x + 9, my0 + y1 * esc - 13)], "1-VIDRIO", 9)
for y in (0.0, 0.90, 4.50, 5.40, 9.0, 9.47):
    pl([(mx0, my0 + y * esc), (mx0 + mw, my0 + y * esc)], "1-ALUMINIO", 25)
for k in range(nm + 1):
    x = mx0 + mw * k / nm
    pl([(x - 0.6, my0), (x - 0.6, my0 + mh)], "1-ALUMINIO", 25); pl([(x + 0.6, my0), (x + 0.6, my0 + mh)], "1-ALUMINIO", 25)
for y, t in ((0, "±0,00"), (4.5, "+4,50"), (9.47, "+9,47")):
    pl([(mx0 - 3.5, my0 + y * esc), (mx0, my0 + y * esc)], "2-COTAS", 13)
    txt(t, mx0 - 4, my0 + y * esc, 1.9, TA.MIDDLE_RIGHT)
pl([(mx0, my0 + mh + 1.5), (mx0 + mw / nm, my0 + mh + 1.5)], "2-COTAS", 13)
txt("1,50", mx0 + mw / nm / 2, my0 + mh + 3, 2.0, TA.MIDDLE_CENTER)
for y, t in ((2.7, "visión"), (0.45, "spandrel"), (4.95, "spandrel"), (7.2, "visión")):
    txt(t, mx0 + mw + 1.5, my0 + y * esc, 1.9, TA.MIDDLE_LEFT)
txt("Spandrel 0,90 m frente a cada losa.", 196, 216, 2.0)

# ---------------------------------------------------------------- 06 REMATE SUPERIOR (CORTE 1:5)
titulo_detalle("6", "REMATE SUPERIOR", "ESC. 1:5", 15, 203, 86)
v6 = V(5, 34, 186)    # origen: cara ext. del perfil, borde superior del montante; exterior hacia -x
caja(v6, 0, -280, MD, 0, fill=ALU, lw=35)
pl(v6.P([(2.5, -280), (2.5, -2.5), (MD - 2.5, -2.5), (MD - 2.5, -280)]), "1-ALUMINIO", 9)
caja(v6, -Y_V1, -280, -Y_V1 + 6, -30, "1-VIDRIO", ESM, 25)                         # spandrel
caja(v6, -Y_T1, -280, -Y_P0, -30, fill=TAPA, lw=18)                               # tapa (vista)
caja(v6, MD + 4, -280, MD + 54, -40, "1-AISLACION", (255, 255, 255), 18, "INSUL", 0.1, 90)
zo = [(MD + 60, -280), (MD + 180, -280), (MD + 180, -45), (MD + 60, -45)]           # zócalo sup. H°A°
hatch(v6.P(zo), "ANSI31", 0.35, 0, "1-HORMIGON", color=8); pl(v6.P(zo), "1-HORMIGON", 35, True)
corte_rotura(v6, (-Y_T1 - 10, -280), (MD + 190, -280))
pl(v6.P([(-Y_T1 - 4, -30), (-Y_T1 - 4, 8), (MD + 2, 8), (MD + 2, -12)]), "1-ALUMINIO", 40)   # perfil de cierre
hatch(v6.P([(-Y_V1, -30), (-Y_V1 + 6, -30), (-Y_V1 + 6, -22), (-Y_V1, -22)]), "SOLID", layer="1-SELLADOS", color=250)
pl(v6.P([(-Y_T1 - 22, -70), (-Y_T1 - 14, -62), (-Y_T1 - 14, 28), (MD + 196, 18), (MD + 196, -50), (MD + 204, -58)]), "1-CHAPA", 50)
pl(v6.P([(MD + 70, -45), (MD + 70, 21.5)]), "1-VISTA", 13); pl(v6.P([(MD + 170, -45), (MD + 170, 19)]), "1-VISTA", 13)
tornillo(v6, (MD + 120, 20), (MD + 120, -40), 6)
v6.dim((0, -280), (MD, -280), -5, text="150")
txt("i = 5%", v6.p(MD + 120, 40)[0], v6.p(0, 40)[1], 2.0, TA.MIDDLE_CENTER)
txt("EXT.", v6.p(-100, -150)[0], v6.p(0, -150)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
g3(21, (30, 26), 10, 11, v6); g3(22, (MD / 2, 8), -15, 11, v6); g3(24, (-Y_V1 + 3, -26), -14, -8, v6)
g3(2, (-Y_V1 + 3, -180), -14, -40, v6); g3(8, (MD / 2, -200), 15, -26, v6); g3(18, (MD + 30, -240), 34, -26, v6)
g3(23, (MD + 120, -200), 64, -30, v6)

# ---------------------------------------------------------------- 07 ANCLAJE AL ENTREPISO + JUNTA DE DILATACIÓN (CORTE 1:5)
titulo_detalle("7", "ANCLAJE Y JUNTA EN ENTREPISO", "ESC. 1:5", 105, 203, 86)
v7 = V(5, 119, 150)   # origen: cara ext. del perfil, nivel de piso terminado (+4,50); exterior hacia -x
caja(v7, 0, -150, MD, 140, fill=ALU, lw=35)
caja(v7, 0, 160, MD, 230, fill=ALU, lw=35)
for xx in (2.5, MD - 2.5):
    pl(v7.P([(xx, -150), (xx, 140)]), "1-ALUMINIO", 9); pl(v7.P([(xx, 160), (xx, 230)]), "1-ALUMINIO", 9)
pl(v7.P([(6, 40), (6, 225), (MD - 6, 225), (MD - 6, 40), (6, 40)]), "1-VISTA", 18, lt="DASHED")   # manguito
hatch(v7.P([(-Y_T1, 140), (0, 140), (0, 160), (-Y_T1, 160)]), "SOLID", layer="1-SELLADOS", rgb=(255, 255, 255), color=7)
pl(v7.P([(-Y_T1, 150), (-Y_T1 + 6, 150)]), "1-SELLADOS", 50)
caja(v7, -Y_V1, -150, -Y_V1 + 6, 230, "1-VIDRIO", ESM, 25)                          # spandrel frente a la losa
caja(v7, -Y_T1, -150, -Y_P0, 230, fill=TAPA, lw=18)
caja(v7, MD + 4, -150, MD + 54, 230, "1-AISLACION", (255, 255, 255), 18, "INSUL", 0.1, 90)
pl(v7.P([(MD + 55, -150), (MD + 55, 230)]), "1-CHAPA", 35)
lo = [(MD + 80, -150), (MD + 220, -150), (MD + 220, -40), (MD + 80, -40)]            # viga de borde H°A°
hatch(v7.P(lo), "ANSI31", 0.35, 0, "1-HORMIGON", color=8); pl(v7.P(lo), "1-HORMIGON", 35, True)
cp = [(MD + 80, -40), (MD + 220, -40), (MD + 220, 0), (MD + 80, 0)]                   # carpeta + solado
hatch(v7.P(cp), "AR-SAND", 0.03, 0, "1-HORMIGON", color=8); pl(v7.P(cp), "1-HORMIGON", 18, True)
corte_rotura(v7, (MD + 220, -160), (MD + 220, 10))
bc = [(MD + 56, -120), (MD + 80, -120), (MD + 80, -4), (MD + 56, -4)]               # barrera cortafuego
hatch(v7.P(bc), "INSUL", 0.05, 90, "1-AISLACION", color=8); pl(v7.P(bc), "1-AISLACION", 13, True)
hatch(v7.P([(MD + 56, -4), (MD + 80, -4), (MD + 80, 0), (MD + 56, 0)]), "SOLID", layer="1-SELLADOS", color=250)
hatch(v7.P([(MD + 110, -40), (MD + 140, -40), (MD + 140, -20), (MD + 110, -20)]), "SOLID", layer="1-ACERO", color=8)  # riel
gr = [(MD - 2, -36), (MD + 190, -36), (MD + 190, -30), (MD + 4, -30), (MD + 4, 40), (MD - 2, 40)]          # grapa L
pl(v7.P(gr), "1-ACERO", 35, True)
tornillo(v7, (MD + 125, -26), (MD + 125, -46), 6)
tornillo(v7, (MD + 10, 15), (60, 15), 6)
for yy in (-150, 230): corte_rotura(v7, (-Y_T1 - 6, yy), (MD + 60, yy))
v7.dim((-Y_T1, 140), (-Y_T1, 160), -3, vertical=True, text="20")
txt("+4,50", v7.p(MD + 160, 8)[0], v7.p(0, 8)[1] + 0.8, 2.0, TA.LEFT)
g3(25, (MD + 150, -33), 60, -26, v7); g3(26, (MD + 125, -45), 50, -24, v7); g3(27, (MD + 7, 15), 52, 14, v7)
g3(28, (-Y_T1 + 3, 150), -10, 40, v7); g3(29, (MD / 2, 190), 52, 36, v7); g3(30, (MD + 68, -80), 66, -12, v7)
g3(31, (MD + 68, -2), 66, 26, v7); g3(2, (-Y_V1 + 3, -100), -10, -24, v7)

# ---------------------------------------------------------------- 08 ARRANQUE (CORTE 1:5)
titulo_detalle("8", "ARRANQUE DESLIZANTE", "ESC. 1:5", 196, 203, 86)
v8 = V(5, 227, 150)    # origen: cara ext. del perfil, nivel ±0,00; exterior hacia -x
ba = [(-60, -150), (MD + 110, -150), (MD + 110, -60), (-60, -60)]
hatch(v8.P(ba), "ANSI31", 0.35, 0, "1-HORMIGON", color=8); pl(v8.P(ba), "1-HORMIGON", 35, True)
pi = [(MD + 20, -60), (MD + 110, -60), (MD + 110, 0), (MD + 20, 0)]
hatch(v8.P(pi), "AR-SAND", 0.03, 0, "1-HORMIGON", color=8); pl(v8.P(pi), "1-HORMIGON", 18, True)
ve = [(-130, -150), (-62, -150), (-62, -75), (-130, -78)]
hatch(v8.P(ve), "AR-CONC", 0.04, 0, "1-HORMIGON", color=8); pl(v8.P(ve), "1-HORMIGON", 18, True)
corte_rotura(v8, (-130, -70), (-130, -160)); corte_rotura(v8, (-70, -150), (MD + 120, -150))
corte_rotura(v8, (MD + 110, -160), (MD + 110, 10))
gu = [(-4, -60), (MD + 4, -60), (MD + 4, 20), (MD + 1, 20), (MD + 1, -57), (-1, -57), (-1, 20), (-4, 20)]   # guía U
poly(v8, gu, fill=ALU, lw=25)
tornillo(v8, (MD / 2, -55), (MD / 2, -130), 5)
caja(v8, 1, -37, MD - 1, 230, fill=ALU, lw=35)                                     # montante colgado (no apoya)
pl(v8.P([(3.5, -37), (3.5, 230)]), "1-ALUMINIO", 9); pl(v8.P([(MD - 3.5, -37), (MD - 3.5, 230)]), "1-ALUMINIO", 9)
v8.dim((MD + 4, -57), (MD + 4, -37), 5, vertical=True, text="20")
caja(v8, -Y_V1, 0, -Y_V1 + 6, 230, "1-VIDRIO", ESM, 25)
caja(v8, -Y_T1, 0, -Y_P0, 230, fill=TAPA, lw=18)
corte_rotura(v8, (-Y_T1 - 6, 230), (MD + 6, 230))
pl(v8.P([(-Y_T1 - 2, 30), (-Y_T1 - 2, -2), (-48, -40), (-64, -40), (-64, -78)]), "1-CHAPA", 40)    # babeta
hatch(v8.P([(-Y_V1, 0), (-Y_V1 + 6, 0), (-Y_V1 + 6, 8), (-Y_V1, 8)]), "SOLID", layer="1-SELLADOS", color=250)
hatch(v8.P([(-4, -60), (-4, -45), (-20, -60)]), "SOLID", layer="1-SELLADOS", color=250)
txt("±0,00", v8.p(MD + 30, 6)[0], v8.p(0, 6)[1] + 0.8, 2.0, TA.LEFT)
g3(32, (MD + 2, -20), 44, 15, v8); g3(33, (MD / 2, -110), 44, -26, v8); g3(34, (-56, -40), -26, -2, v8)
g3(24, (-Y_V1 + 3, 4), -26, 12, v8); g3(35, (-12, -52), -26, -16, v8); g3(8, (MD / 2, 150), 44, 30, v8)
g3(2, (-Y_V1 + 3, 160), -26, 36, v8)

# ---------------------------------------------------------------- 09 COMPOSICIÓN DEL DVH + MONTAJE
titulo_detalle("9", "COMPOSICIÓN DEL DVH", "ESC. 1:1", 15, 112, 128)
v9 = V(1, 30, 79)
caja(v9, 0, 0, 6, 26, "1-VIDRIO", VID, 25); caja(v9, 18, 0, 24.76, 26, "1-VIDRIO", VID, 25)
pl(v9.P([(21.38, 0), (21.38, 26)]), "1-VIDRIO", 9)
caja(v9, 6, 14, 18, 23, layer="1-ALUMINIO", fill=ALU, lw=13)
hatch(v9.rect(6, 23, 18, 26), "SOLID", layer="1-EPDM", color=250)
for i, (t, xx, yy) in enumerate([("Templado 6 mm (exterior)", 3, 8), ("Cámara 12 mm - aire deshidratado", 12, 6),
                                 ("Laminado 3+3 c/ PVB 0,38 (interior)", 21.4, 4),
                                 ("Separador de aluminio c/ desecante", 12, 18), ("Sellado secundario (silicona)", 12, 24.5)]):
    y = 104 - i * 4.4
    pl([v9.p(xx, yy), (66, y + 0.8), (68, y + 0.8)], "3-REFERENCIAS", 9)
    msp.add_circle(v9.p(xx, yy), 0.35, dxfattribs={"layer": "3-REFERENCIAS"})
    txt(t, 69, y, 2.0)
txt("e total = 24,8 mm  ·  U ≈ 2,8 W/m²·K", 69, 82, 2.0, bold=True)
txt("EXT.", v9.p(3, -3)[0], v9.p(0, -1.5)[1], 2.0, TA.TOP_CENTER)
txt("INT.", v9.p(21.4, -3)[0], v9.p(0, -1.5)[1], 2.0, TA.TOP_CENTER)

txt("SECUENCIA DE MONTAJE", 152, 110.2, 2.8, TA.LEFT, "3-TITULOS", True)
pl([(152, 108), (282, 108)], "3-TITULOS", 25)
pasos = ["1. Replantear ejes y embutir los rieles de anclaje en la viga de borde (26).",
         "2. Fijar las grapas regulables (25) y colgar los montantes de cada piso (8).",
         "3. Unir montantes con manguito (29), con junta de dilatación de 20 mm (28).",
         "4. Colocar la guía de arranque (32) y los travesaños (17); nivelar y aplomar.",
         "5. Barrera cortafuego (30, 31), lana mineral y bandeja del spandrel (18, 19).",
         "6. Colocar DVH sobre calzos (36), burletes (11, 13), presor (10) y tapas (9).",
         "7. Remate superior (21, 22), babeta inferior (34) y sellados (24, 35)."]
yy = 104
for p in pasos:
    txt(p, 152, yy, 2.0); yy -= 3.4

# ---------------------------------------------------------------- REFERENCIAS
txt("REFERENCIAS", 15, 70, 2.6, TA.LEFT, "3-TITULOS", True)
pl([(15, 68.5), (W - 15, 68.5)], "3-TITULOS", 25)
refs = ["DVH visión 6+12+3+3 (ref. 27)", "Spandrel templado 6 esmaltado (ref. 28)", "Montante (estructura del sistema)",
        "Tapa exterior a presión", "Presor (despiece)", "Tapa exterior (despiece)", "Travesaño (estructura del sistema)",
        "Montante alum. 50x150 (ref. 25)", "Tapa exterior de aluminio", "Presor de aluminio", "Burlete EPDM interior",
        "Aislador / ruptura de puente térmico", "Burlete EPDM exterior", "Separador c/ desecante + sellado", "Laminado 3+3 c/ PVB",
        "Canal de tornillo del montante", "Travesaño alum. 50x120", "Lana mineral 50 mm (ref. 29)", "Bandeja chapa galv. (ref. 29)",
        "Suplemento EPDM del spandrel", "Cupertina chapa galv. N°22 (ref. 1)", "Perfil de cierre superior (ref. 2)",
        "Zócalo superior H°A° (ref. 8)", "Sellador silicona neutra (ref. 34)", "Grapa acero galv. regulable (ref. 31)",
        "Riel de anclaje + bulón T (ref. 18)", "Bulón M12 inox (ref. 31)", "Junta de dilatación 20 mm (ref. 32)",
        "Manguito de unión (ref. 32)", "Barrera cortafuego lana mineral (ref. 30)", "Sellador intumescente (ref. 30)",
        "Perfil guía de arranque (ref. 33)", "Broca c/ prisionero Ø9,5 (ref. 55)", "Babeta chapa galv. c/ goterón (ref. 44)",
        "Sellador s/ fondo de junta", "Calzo de apoyo del DVH (neopreno)", "Drenaje del travesaño"]
ncol = 4; nrow = math.ceil(len(refs) / ncol); cw = (W - 30) / ncol
for i, r in enumerate(refs):
    col, row = divmod(i, nrow)
    x, y = 15 + col * cw, 64.5 - row * 3.4
    txt(f"{i + 1}", x + 2.6, y, 2.0, TA.RIGHT, "3-REFERENCIAS", True)
    txt(r, x + 4, y, 2.0)


# ---------------------------------------------------------------- RÓTULO (formato TP FINAL)
ry0, ry1 = 12, 26
xs = [15, 41, 170, 237, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("TP FINAL", (xs[0] + xs[1]) / 2, 20.4, 3.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 19/10/2026", (xs[0] + xs[1]) / 2, 15.2, 1.8, TA.MIDDLE_CENTER)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 22.6, 2.4)
txt("ALUMNA: Candelaria Vitale", xs[1] + 2, 19.0, 2.4)
txt("GRUPO: 13", xs[1] + 2, 15.4, 2.4)
txt("NIVEL:", xs[2] + 2, 22.6, 2.4); txt("OBS:", xs[2] + 2, 19.0, 2.4)
txt("CONSTRUCCIONES II", (xs[3] + xs[4]) / 2, 21.0, 2.6, TA.MIDDLE_CENTER)
txt("CATEDRA: ARQ. TUCCI", (xs[3] + xs[4]) / 2, 17.0, 2.6, TA.MIDDLE_CENTER)

doc.saveas(f"{OUT}/Lamina4_Catalogo_Vidriado_A3.dxf")
print("ok")
