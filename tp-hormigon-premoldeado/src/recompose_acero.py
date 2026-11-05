# Reorganiza la lámina TP_INTEGRADOR_ACERO_VIDRIADO sin redibujar nada: cada bloque del PDF original
# se recorta (rectángulo, o círculo + rótulos para los detalles) y se traslada como vector.
import sys, re, pymupdf
from shapely.geometry import Point, box
from shapely.ops import unary_union
from shapely.affinity import translate
src, out = sys.argv[1], sys.argv[2]
K = 72 / 25.4
S = pymupdf.open(src); W, H = S[0].rect.width, S[0].rect.height
D = pymupdf.open(); pg = D.new_page(width=W, height=H)
pg.show_pdf_page(pg.rect, S, 0)                       # crea el XObject con la página original
xo = re.search(rb"/(\w+) Do", D.xref_stream(pg.get_contents()[0])).group(1).decode()

def pp(x, y): return (x * K, H - y * K)               # mm (y abajo) -> pt PDF (y arriba)
def path(geom):
    ops = []
    for ring in [geom.exterior] + list(geom.interiors):
        c = list(ring.coords)[:-1]
        ops.append("%.3f %.3f m " % pp(*c[0]) + " ".join("%.3f %.3f l" % pp(*q) for q in c[1:]) + " h")
    return "\n".join(ops)
def block(geoms, dx, dy, rule="W"):
    clip_ops = "\n".join(path(translate(g, dx, dy)) for g in geoms)      # recorte en la posición de destino
    return f"q\n{clip_ops}\n{rule} n\n1 0 0 1 {dx*K:.3f} {-dy*K:.3f} cm\n/{xo} Do\nQ\n"

# ---- detalles (círculo + rótulos que asoman fuera del círculo)
C = [(143.7, 62.3, 22.2), (140.6, 163.1, 21.5), (138.05, 242.25, 19.55)]
LAB = [[(116.7, 58.7, 128.6, 81.5)], [(121.2, 174.1, 130.4, 183.8)],
       [(115.6, 219.5, 132.9, 235.4), (149.8, 226.9, 166.4, 245.1)]]
DET = [unary_union([Point(cx, cy).buffer(r + 0.7, 64)] + [box(*b) for b in LAB[i]]) for i, (cx, cy, r) in enumerate(C)]

ops = ""
# bordes del papel y rótulo: sin mover
for b in [(0, 0, 297, 3), (0, 417, 297, 420.2), (0, 0, 3, 420.2), (294, 0, 297, 420.2), (3, 384, 294, 417)]:
    ops += block([box(*b)], 0, 0)
# corte integral -> a la derecha
DXC = float(sys.argv[3]) if len(sys.argv) > 3 else 137.0
CORTE = box(33, 25, 157, 372).difference(unary_union(DET))
ops += block(list(getattr(CORTE, "geoms", [CORTE])), DXC, 0)
# título y referencias -> arriba a la izquierda, en una columna
X0 = 10.0
REFS = [(188.5, 28.2, 270.7, 41.4), (187.0, 58.0, 259.4, 114.6), (186.8, 124.3, 290.5, 240.9), (186.8, 257.2, 290.5, 364.0)]
y = 15.0
for i, (x0, y0, x1, y1) in enumerate(REFS):
    ops += block([box(x0, y0, x1, y1)], X0 - x0 + 1.0, y - y0)
    y += (y1 - y0) + 5.0
ytop = y
# detalles -> abajo a la izquierda, en fila
bbs = [g.bounds for g in DET]
row_h = max(b[3] - b[1] for b in bbs)
row_c = ytop + row_h / 2
gap = (168.0 - X0 - sum(b[2] - b[0] for b in bbs)) / 2
xs = X0
for g, b in zip(DET, bbs):
    ops += block([g], xs - b[0], row_c - (b[1] + b[3]) / 2)
    xs += (b[2] - b[0]) + gap
print("refs hasta y=%.1f  fila detalles %.1f-%.1f  gap %.1f" % (ytop, row_c - row_h / 2, row_c + row_h / 2, gap))
D.update_stream(pg.get_contents()[0], ops.encode())
D.save(out, garbage=3, deflate=True)
D[0].get_pixmap(dpi=150).save(out.replace(".pdf", ".png"))
