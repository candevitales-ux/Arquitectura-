# Genera la capa de color del corte (PNG RGBA) por relleno de regiones sobre una máscara de contornos.
# Uso: python3 paint_mask.py original.pdf seeds.py salida.png [preview.png]
import sys, pymupdf, numpy as np
from PIL import Image
from scipy import ndimage

src, seeds_file, out = sys.argv[1], sys.argv[2], sys.argv[3]
prev = sys.argv[4] if len(sys.argv) > 4 else None
K = 72 / 25.4; MM = 1 / K
X0, Y0, X1, Y1 = 33.0, 25.0, 157.0, 372.0          # zona del corte (mm, en el PDF original)
DPI = 300; S = DPI / 25.4
p = pymupdf.open(src)[0]

def key(d): return (d['type'], tuple(round(v, 2) for v in (d.get('fill') or ())), tuple(round(v, 2) for v in (d.get('color') or ())), round(d.get('width') or 0, 2))
HATCH = {('fs', (0.45,) * 3, (0.45,) * 3, 0), ('s', (), (0.39, 0.39, 0.4), 0), ('s', (), (0.45,) * 3, 0.36),
         ('s', (), (0.5, 0.5, 0.5), 0.72), ('s', (), (0.0, 0.0, 0.0), 0), ('s', (), (0.57, 0.58, 0.6), 0.24)}
ns = {}
exec(open(seeds_file).read(), ns)
EXTRA_EXCL = ns.get("EXCL", set())

doc = pymupdf.open(); pg = doc.new_page(width=p.rect.width, height=p.rect.height); sh = pg.new_shape()
for d in p.get_drawings():
    if key(d) in HATCH or key(d) in EXTRA_EXCL: continue
    r = d['rect']
    if r.x0 * MM > X1 or r.x1 * MM < X0 or r.y0 * MM > Y1 or r.y1 * MM < Y0: continue
    for it in d['items']:
        if it[0] == 'l': sh.draw_line(it[1], it[2])
        elif it[0] == 'c': sh.draw_bezier(*it[1:])
        elif it[0] == 're': sh.draw_rect(it[1])
        elif it[0] == 'qu': sh.draw_quad(it[1])
    sh.finish(color=(0, 0, 0), width=0.25, closePath=False)
for (a, b, c, e) in ns.get("WALLS", []):                        # cierres auxiliares (mm)
    sh.draw_line((a * K, b * K), (c * K, e * K)); sh.finish(color=(0, 0, 0), width=0.3)
sh.commit()
pix = pg.get_pixmap(dpi=DPI, clip=pymupdf.Rect(X0 * K, Y0 * K, X1 * K, Y1 * K), colorspace=pymupdf.csGRAY)
B = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width) < 200      # True = contorno
free = ~B
lab, n = ndimage.label(free)
H, W = free.shape
rgba = np.zeros((H, W, 4), np.uint8)
def px(x, y): return int((y - Y0) * S), int((x - X0) * S)
sizes = ndimage.sum(free, lab, range(n + 1)) / (S * S)            # área de cada región (mm²)
BIG = sizes > ns.get("BIG_MM2", 1500)
assigned = np.zeros_like(free)
def rectmask(lim):
    L = np.zeros_like(free)
    for (a, b, c, e) in lim:
        i0, j0 = px(a, b); i1, j1 = px(c, e); L[max(i0, 0):i1, max(j0, 0):j1] = True
    return L
for entry in ns["MAT"]:
    mode, color = entry[0], entry[1]
    col = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    if mode == "flood":
        pts, lim = entry[2], entry[3]
        m = np.zeros_like(free)
        for (x, y) in pts:
            i, j = px(x, y)
            l = lab[i, j]
            if l == 0: print("semilla sobre línea", color, (x, y)); continue
            m |= lab == l
        if lim: m &= rectmask(lim)
    else:                                   # "rest": todo lo libre dentro de los rectángulos, salvo aire/ambientes
        big = BIG if len(entry) < 4 else sizes > entry[3]
        m = free & rectmask(entry[2]) & ~big[lab]
    m &= ~assigned
    assigned |= m
    m = ndimage.binary_dilation(m, iterations=2) & ~(rgba[..., 3] > 0)      # cubre el ancho de las líneas
    rgba[m] = col + (255,)
# globos de referencia: el interior queda blanco (sin color)
yy, xx = np.mgrid[0:H, 0:W]
for d in p.get_drawings():
    r = d['rect']; w, h = r.width * MM, r.height * MM
    if d['type'] == 's' and 3.0 < w < 6.5 and abs(w - h) < 0.4 and any(it[0] == 'c' for it in d['items']):
        cx, cy, rad = (r.x0 + r.x1) / 2 * MM, (r.y0 + r.y1) / 2 * MM, w / 2
        i, j = px(cx, cy); R = rad * S
        i0, i1, j0, j1 = max(int(i - R - 2), 0), min(int(i + R + 2), H), max(int(j - R - 2), 0), min(int(j + R + 2), W)
        sub = (yy[i0:i1, j0:j1] - i) ** 2 + (xx[i0:i1, j0:j1] - j) ** 2 <= R * R
        rgba[i0:i1, j0:j1][sub] = 0
Image.fromarray(rgba, "RGBA").save(out)
if prev:
    pix2 = p.get_pixmap(dpi=DPI, clip=pymupdf.Rect(X0 * K, Y0 * K, X1 * K, Y1 * K))
    base = np.frombuffer(pix2.samples, np.uint8).reshape(pix2.height, pix2.width, 3).astype(float)
    a = rgba[..., 3:4] / 255.0
    comp = base / 255.0 * (rgba[..., :3] * a + 255 * (1 - a))
    Image.fromarray(comp.astype(np.uint8)).save(prev)
