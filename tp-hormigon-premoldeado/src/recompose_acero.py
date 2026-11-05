# -*- coding: utf-8 -*-
"""Lámina TP_INTEGRADOR_ACERO_VIDRIADO en el formato de las láminas de hormigón:
corte integral (sin cambios, vectorial) a la derecha; título + referencias en 2 columnas (Liberation Sans,
mismos tamaños que src/tp_corte.py) arriba a la izquierda; los 3 detalles ampliados abajo a la izquierda,
con sus rótulos reescritos en Liberation Sans. El dibujo del corte y de los detalles no se modifica."""
import sys, re, pymupdf
from shapely.geometry import Point, box
from shapely.ops import unary_union
from shapely.affinity import affine_transform

src, out = sys.argv[1], sys.argv[2]
COLOR = sys.argv[3] if len(sys.argv) > 3 else None    # capa de color del corte (PNG de paint_mask.py, zona 33-157 x 25-372 mm)
K = 72 / 25.4
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
fR, fB = pymupdf.Font(fontfile=FR), pymupdf.Font(fontfile=FB)

# ------------------------------------------------------------------ rótulos de los detalles (trazos SHX)
# líneas medidas en el PDF original (mm): (x0, y0, x1, y1, texto)
LBL = [
    (117.05, 59.32, 126.11, 60.86, "COLUMNA"), (117.05, 61.64, 120.57, 62.99, "HEB"),
    (117.05, 68.62, 122.68, 69.93, "UNION"), (117.05, 70.71, 126.53, 72.43, "COLUMNA,"),
    (117.14, 73.02, 123.32, 74.34, "PGU Y"), (117.14, 75.27, 122.98, 76.58, "PANEL"),
    (117.14, 77.34, 128.02, 78.66, "ESTRUCTURA"), (117.14, 79.54, 126.83, 80.90, "PRINCIPAL"),
    (150.20, 68.20, 161.37, 69.55, "PANEL PUR"),
    (149.99, 160.66, 153.63, 161.97, "EXT."),
    (121.75, 174.62, 127.55, 175.94, "JUNTA"), (121.75, 176.73, 132.12, 178.24, "HERMETICA"),
    (121.71, 179.00, 129.41, 180.83, "(con un"), (121.71, 181.29, 129.88, 183.33, "sellador)"),
    (116.16, 222.04, 121.96, 223.35, "JUNTA"), (116.16, 224.14, 126.58, 225.65, "HERMETICA"),
    (116.08, 231.31, 125.10, 232.66, "PIEZA DE"), (116.08, 233.45, 122.72, 234.97, "CIERRE"),
    (149.14, 227.33, 155.02, 228.68, "PANEL"),
    (153.59, 238.84, 160.65, 240.20, "REMATE"), (153.59, 240.97, 165.95, 242.52, "INFERIOR DE"),
    (153.50, 243.29, 161.84, 244.64, "FACHADA"),
]
S0 = pymupdf.open(src)
S = pymupdf.open(); S.insert_pdf(S0)
sp = S[0]
for x0, y0, x1, y1, _ in LBL:
    sp.add_redact_annot(pymupdf.Rect((x0 - 0.6) * K, (y0 - 0.4) * K, (x1 + 0.4) * K, (y1 + 0.4) * K), fill=False)
sp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                    text=pymupdf.PDF_REDACT_TEXT_NONE)
W, H = sp.rect.width, sp.rect.height

D = pymupdf.open(); pg = D.new_page(width=W, height=H)
pg.show_pdf_page(pg.rect, S, 0)
xo = re.search(rb"/(\w+) Do", D.xref_stream(pg.get_contents()[0])).group(1).decode()

def pp(x, y): return (x * K, H - y * K)
def path(g):
    o = []
    for ring in [g.exterior] + list(g.interiors):
        c = list(ring.coords)[:-1]
        o.append("%.3f %.3f m " % pp(*c[0]) + " ".join("%.3f %.3f l" % pp(*q) for q in c[1:]) + " h")
    return "\n".join(o)
def block(geoms, s=1.0, ax=0.0, ay=0.0):
    """dibuja la página original transformada (x' = s x + ax, y' = s y + ay, en mm) recortada a geoms (coords de origen)"""
    clip = "\n".join(path(affine_transform(g, [s, 0, 0, s, ax, ay])) for g in geoms)
    return f"q\n{clip}\nW n\n{s:.5f} 0 0 {s:.5f} {ax*K:.3f} {H*(1-s) - ay*K:.3f} cm\n/{xo} Do\nQ\n"

ops = ""
for b in [(0, 0, 297, 3), (0, 417, 297, 420.2), (0, 0, 3, 420.2), (294, 0, 297, 420.2), (3, 384, 294, 417)]:
    ops += block([box(*b)])                                           # bordes del papel y rótulo, sin mover

C = [(143.7, 62.3, 22.2), (140.6, 163.1, 21.5), (138.05, 242.25, 19.55)]
LAB = [[(116.7, 58.7, 128.6, 81.5)], [(121.2, 174.1, 132.6, 183.8)],
       [(116.12, 219.5, 132.9, 235.4), (148.6, 226.9, 166.4, 245.1)]]
DET = [unary_union([Point(cx, cy).buffer(r + 0.7, 64)] + [box(*b) for b in LAB[i]]) for i, (cx, cy, r) in enumerate(C)]
CORTE = box(33, 25, 157, 372).difference(unary_union(DET))
ops += block(list(getattr(CORTE, "geoms", [CORTE])), 1.0, 137.0, 0.0)   # corte integral -> derecha

# ------------------------------------------------------------------ textos
TXT = []   # (x, y_baseline, texto, size_mm, bold, align)
def T(x, y, s, size=2.8, bold=False, a="start"): TXT.append((x, y, s, size, bold, a))
T(16, 31.9, "CORTE INTEGRAL", 7.4)
T(16, 39.9, "CERRAMIENTO VIDRIADO", 7.4)
T(16, 47.7, "ESCALA 1:20", 4.7)
T(16, 65.8, "REFERENCIAS", 5.0)

LEG = [
("NUDO: FUNDACION ZAPATA AISLADA DE H°A° Y CERRAMIENTO VERTICAL OPACO", None),
(1, "Suelo tosca compactada"), (2, "As inferior de la base"), (3, "H° de limpieza e: 0.05m"), (4, "As de tronco de base"),
(5, "Tronco de base H°A° IN SITU"), (6, "Armadura principal de cabezal."), (7, "Estribos Ø10 s/calculo"),
(8, "Perchas Ø10 s/calculo"), (9, "Cabezal H°A° h: 0.80m"), (10, "Mortero fluido para anclajes tipo \"Grout\" e: 0.03m"),
(11, "Perno roscado de anclaje"), (12, "Placa de anclaje de base columna metalica e: 0.012m"),
(13, "Doble tuerca roscada y contra tuerca con arandela"), (14, "Cartelas metalicas soldadas."),
(15, "Columna metalica HEB 400 s/corte."), (16, "Film de polietileno 200u."),
(17, "Contrapiso de H° pobre de cascote e: 0.08m"), (18, "Carpeta hidrofuga MCI e: 0.02m"),
(19, "Carpeta niveladora e: 0.02m"), (20, "Adhesivo cementicio para porcelanato e: 0.01m"),
(21, "Mortero de junta e: 0.01m"), (22, "Solado de terminacion: porcelanato 60x60cm e: 0.01m"),
(23, "Carpeta niveladora MHR"), (24, "Contrapiso HRP 1:1/4:3:6 e: 0.08m"),
(25, "Remate inferior de panel en fachada (Acero prelacado) e: 0.06cm"),
("NUDO: ENTREPISO STEEL DECK Y CERRAMIENTO SISTEMA PANEL SANDWICH", None),
(26, "Viga metalica HEB400 (40X30cm) Luz: 6.00mts"), (27, "Cartela angular vinculacion viga–columna"),
(28, "Perno conector de corte Steel Deck (placa colaborante) h: 0.13mts"),
(29, "Tuerca abulonada para vinculacion viga–columna"),
(30, "Moldura frontera ALCOR de borde \"L\" galvanizada + sujetador de borde"),
(31, "Solado de terminacion: porcelanato 60x60cm e: 0.01m"), (32, "Carpeta MHR 1:1/4:3 e: 0.02m"),
(33, "Contrapiso liviano EPS e: 0.04m"), (34, "Malla electrosoldada c/0.15m s/calculo"),
(35, "Capa de compresion H°A° e: 0.03m"), (36, "Placa colaborante Steel Deck ALCOR h: 0.11m"),
(37, "Viga entrepiso secundaria HEB300 (30x30cm) Luz: 6.00m"),
(38, "Angulo \"L\" perimetral para cierre de cielorraso tecnico"),
(39, "Placa roca yeso para cielorraso tecnico e: 0.02m"), (40, "Perfil larguero"), (41, "Perfil travesaño"),
(42, "Placa soldada a viga para fijacion de cielorraso tecnico"), (43, "Cuelgue de esctructura de cielorraso tecnico"),
(44, "Perfil PGU 100"), (45, "Tornillo de union perfil PGU–Columna metalica"), (46, "Lamina interior de acero galvanizado"),
(47, "Aislacion termica: panel poliuretano (PUR) e: 80mm"), (48, "Lamina exterior de acero galvanizado"),
(49, "Tornillo autoperforante de union oculta entre Paneles y PGU"),
(50, "Encuentro entre paneles con fijacion oculta y encastre"), (51, "Cerramiento integral en muro panel sandwich"),
("NUDO: CUBIERTA PLANA Y CERRAMIENTO PANEL SANDWICH", None),
(52, "Barrera de vapor: pintura asfaltica"), (53, "Contrapiso liviano EPS con pendiente e: 0.04mts"),
(54, "Mortero impermeable MCI e: 0.05mts"), (55, "Carpeta niveladora"), (56, "Membrana asfaltica de aluminio"),
(57, "Losa de H°A° sobre encofrado perdido h: 0.11mts"), (58, "Malla de reparticion"),
(59, "Tornillo autoperforante para fijaciones cupertina"), (60, "Aislacion termica EPS para cierre superior"),
(61, "Cupertina de chapa galvanizada"), (62, "Moldura tapa ALCOR"), (63, "Soporte de Malla"),
]
def wrap(txt, width, font, size):
    words, lines, cur = txt.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.text_length(t, size * K) / K <= width or not cur: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]
COLS = [(18.6, 66.0), (90.4, 77.0)]          # (x de los números, ancho del texto)
y0, dy = 70.4, 3.25
def rows_of(entries, width):                  # (texto, es_titulo, n)
    rows = []
    for n, txt in entries:
        if txt is None:
            if rows: rows.append(("", False, None))
            rows += [(l, True, None) for l in wrap(n, width + 4, fB, 2.8)]
        else:
            rows += [(l, False, n if i == 0 else None) for i, l in enumerate(wrap(txt, width, fR, 2.8))]
    return rows
# corte de columnas que equilibra la cantidad de renglones (sin partir una referencia)
best = min(range(1, len(LEG)), key=lambda k: max(len(rows_of(LEG[:k], COLS[0][1])), len(rows_of(LEG[k:], COLS[1][1]))))
cols = [rows_of(LEG[:best], COLS[0][1]), rows_of(LEG[best:], COLS[1][1])]
for c, rr in enumerate(cols):
    xn = COLS[c][0]
    for r, (l, head, n) in enumerate(rr):
        y = y0 + r * dy
        if head: T(xn - 2.6, y, l, 2.8, True)
        elif l:
            if n is not None: T(xn, y, str(n), 2.8, True, "end")
            T(xn + 1.3, y, l, 2.8)
ref_end = y0 + max(len(rr) for rr in cols) * dy
print("referencias: filas", [len(rr) for rr in cols], "fin y =", round(ref_end, 1))

# ------------------------------------------------------------------ detalles ampliados
SD = 1.65
TIT = ["DETALLE 1 · CUBIERTA Y PANEL SANDWICH", "DETALLE 2 · ENTREPISO Y PANEL SANDWICH", "DETALLE 3 · FUNDACIÓN Y REMATE DE FACHADA"]
bb = [g.bounds for g in DET]
ytop = ref_end + 10.0
row1_h = max(SD * (b[3] - b[1]) for b in bb[:2])
w1, w2 = SD * (bb[0][2] - bb[0][0]), SD * (bb[1][2] - bb[1][0])
gap = (168.0 - 10.0 - w1 - w2)
place = [(10.0, ytop + 6.0), (10.0 + w1 + gap, ytop + 6.0)]
y2 = ytop + 6.0 + row1_h + 12.0
w3 = SD * (bb[2][2] - bb[2][0])
place.append(((10.0 + 168.0 - w3) / 2, y2 + 6.0))
for i, (g, b, (px, py)) in enumerate(zip(DET, bb, place)):
    ax, ay = px - SD * b[0], py - SD * b[1]
    ops += block([g], SD, ax, ay)
    T(px, py - 3.0, TIT[i], 3.2, True)
    for x0, yy0, x1, yy1, s in LBL:
        if g.contains(Point((x0 + x1) / 2, (yy0 + yy1) / 2)) or g.distance(Point(x0, yy0)) < 1:
            T(SD * x0 + ax, SD * (yy0 + 1.33) + ay, s, 2.8)
print("detalles: fila 1 hasta", round(ytop + 6 + row1_h, 1), " detalle 3 hasta", round(y2 + 6 + SD * (bb[2][3] - bb[2][1]), 1))

D.update_stream(pg.get_contents()[0], ops.encode())
if COLOR:   # colores por debajo de las líneas del corte (mismo desplazamiento que el corte)
    pg.insert_image(pymupdf.Rect((33 + 137) * K, 25 * K, (157 + 137) * K, 372 * K), filename=COLOR, overlay=False)
pg.insert_font(fontname="LibSans", fontfile=FR); pg.insert_font(fontname="LibSansB", fontfile=FB)
for x, y, s, size, bold, a in TXT:
    f = fB if bold else fR
    w = f.text_length(s, size * K)
    xx = x * K - (w if a == "end" else w / 2 if a == "middle" else 0)
    pg.insert_text((xx, y * K), s, fontsize=size * K, fontname="LibSansB" if bold else "LibSans", color=(0, 0, 0))
D.save(out, garbage=3, deflate=True)
D[0].get_pixmap(dpi=150).save(out.replace(".pdf", ".png"))
