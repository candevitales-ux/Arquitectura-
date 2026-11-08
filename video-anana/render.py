import json, math, os, subprocess, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(BASE, 'fonts')
SRC = os.path.join(BASE, 'dl', 'v2.mov')
W, H, FPS = 1080, 1920, 30
DUR = 34.25

# ---------------- palette (classic / beige) ----------------
WHITE = (255, 253, 248)
CREAM = (244, 236, 222)
BEIGE = (226, 208, 176)
SAND = (200, 178, 140)
BROWN = (62, 46, 34)
EMBER = (232, 176, 110)

# ---------------- fonts ----------------
_fc = {}
def font(name, size, wght=None):
    k = (name, size, wght)
    if k not in _fc:
        f = ImageFont.truetype(os.path.join(FD, name), size)
        if wght:
            f.set_variation_by_axes([wght])
        _fc[k] = f
    return _fc[k]

SANS = lambda s, w=800: font('Montserrat.ttf', s, w)
SERIF_I = lambda s, w=600: font('PlayfairDisplay-Italic.ttf', s, w)
SERIF = lambda s, w=600: font('PlayfairDisplay.ttf', s, w)
CORM_I = lambda s, w=500: font('CormorantGaramond-Italic.ttf', s, w)

# ---------------- easing ----------------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_inout(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def ease_back(x, s=1.7):
    x = clamp(x); x -= 1
    return x * x * ((s + 1) * x + s) + 1
def prog(t, t0, d): return clamp((t - t0) / d)

# ---------------- sprites ----------------
def add_shadow(img, radius=9, offset=(0, 4), opacity=0.8, pad=30):
    w, h = img.size
    out = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    a = img.split()[3]
    sh = Image.new('L', out.size, 0)
    sh.paste(a, (pad + offset[0], pad + offset[1]))
    sh = sh.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * opacity))
    out.paste(Image.new('RGBA', out.size, (20, 14, 8, 255)), (0, 0), sh)
    out.alpha_composite(img, (pad, pad))
    return out

_tc = {}
def text_sprite(txt, f, fill, tracking=0, shadow=True):
    k = (txt, id(f), fill, tracking, shadow)
    if k in _tc: return _tc[k]
    if tracking:
        widths = [f.getlength(c) for c in txt]
        tw = int(sum(widths) + tracking * (len(txt) - 1)) + 4
    else:
        tw = int(f.getlength(txt)) + 4
    asc, desc = f.getmetrics()
    img = Image.new('RGBA', (tw + 20, asc + desc + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if tracking:
        x = 10
        for c, wd in zip(txt, widths):
            d.text((x, 10), c, font=f, fill=fill)
            x += wd + tracking
    else:
        d.text((10, 10), txt, font=f, fill=fill)
    if shadow:
        img = add_shadow(img)
    _tc[k] = img
    return img

def place(canvas, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if alpha <= 0.01 or scale <= 0.01: return
    s = spr
    if abs(scale - 1) > 0.005:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BICUBIC)
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = s.split()[3].point(lambda v: int(v * alpha))
        s = s.copy(); s.putalpha(a)
    x, y = int(cx - s.width / 2), int(cy - s.height / 2)
    canvas.alpha_composite(s, (max(0, x), max(0, y)),
                           (max(0, -x), max(0, -y)))

# ---------------- line icons ----------------
def arc(cx, cy, r, a0, a1, n=40, rx=None):
    rx = rx or r
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def circle(cx, cy, r, n=48): return arc(cx, cy, r, -90, 270, n)

def rrect(x0, y0, x1, y1, r):
    p = []
    p += arc(x1 - r, y0 + r, r, -90, 0, 8)
    p += arc(x1 - r, y1 - r, r, 0, 90, 8)
    p += arc(x0 + r, y1 - r, r, 90, 180, 8)
    p += arc(x0 + r, y0 + r, r, 180, 270, 8)
    p.append(p[0])
    return p

ICONS = {}
ICONS['pin'] = [arc(0, -0.3, 0.55, 145, 395, 50) + [(0, 0.85)] + [arc(0, -0.3, 0.55, 145, 395, 50)[0]],
                circle(0, -0.3, 0.2)]
def _basilica():
    P = []
    P.append([(-0.95, 0.9), (0.95, 0.9)])
    for sx in (-1, 1):
        x0, x1 = sx * 0.33, sx * 0.72
        P.append([(x0, 0.9), (x0, -0.05), (x1, -0.05), (x1, 0.9)])
        xm = (x0 + x1) / 2
        P.append([(x0, -0.05), (xm, -0.85), (x1, -0.05)])
        P.append([(xm, -0.85), (xm, -1.0)])
        P.append([(xm - 0.06, -0.94), (xm + 0.06, -0.94)])
        P.append([(xm - 0.06, 0.45), (xm - 0.06, 0.25)] + arc(xm, 0.25, 0.06, 180, 360, 8) + [(xm + 0.06, 0.45)])
    P.append([(-0.33, 0.12), (0, -0.3), (0.33, 0.12)])
    P.append(circle(0, 0.22, 0.13, 30))
    P.append([(-0.13, 0.9), (-0.13, 0.66)] + arc(0, 0.66, 0.13, 180, 360, 12) + [(0.13, 0.9)])
    return P
ICONS['basilica'] = _basilica()
ICONS['expand'] = []
for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
    ICONS['expand'].append([(sx * 0.2, sy * 0.2), (sx * 0.85, sy * 0.85)])
    ICONS['expand'].append([(sx * 0.45, sy * 0.85), (sx * 0.85, sy * 0.85), (sx * 0.85, sy * 0.45)])
def person(cx, cy, s):
    return [circle(cx, cy - 0.45 * s, 0.22 * s, 30), arc(cx, cy + 0.55 * s, 0.45 * s, 180, 360, 20)]
ICONS['family'] = person(-0.48, 0.1, 0.9) + person(0.48, 0.1, 0.9) + person(0, 0.38, 0.6)
def glass(cx, ang):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def T(x, y): return (cx + x * c - y * s, 0.1 + x * s + y * c)
    bowl = [T(*p) for p in [(-0.22, -0.7)] + arc(0, -0.45, 0.25, 180, 360, 16)[::-1][::-1] ]
    bowl = [T(-0.24, -0.75)] + [T(0.24 * math.cos(math.radians(a)), -0.42 + 0.3 * math.sin(math.radians(a))) for a in range(180, -1, -15)][::-1][::-1]
    cup = [T(-0.24, -0.78), T(-0.24, -0.45)] + [T(0.24 * math.cos(math.radians(a)), -0.45 + 0.28 * math.sin(math.radians(a))) for a in range(180, -1, -12)] + [T(0.24, -0.78), T(-0.24, -0.78)]
    return [cup, [T(0, -0.17), T(0, 0.6)], [T(-0.18, 0.6), T(0.18, 0.6)]]
ICONS['cheers'] = glass(-0.32, 14) + glass(0.32, -14) + [[(-0.12, -0.95), (-0.05, -0.8)], [(0, -1.0), (0, -0.84)], [(0.12, -0.95), (0.05, -0.8)]]
def heart(s=0.55, cx=0, cy=0.05):
    pts = []
    for i in range(81):
        t = math.pi * 2 * i / 80
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x / 17 * s * 1.6, cy - y / 17 * s * 1.6))
    return pts
ICONS['heart'] = [heart()]
def flame():
    pts = []
    for i in range(61):
        t = i / 60 * 2 * math.pi
        r = 0.55
        x = r * math.sin(t) * (1 - 0.15 * math.cos(t))
        y = 0.3 - 0.65 * math.cos(t) * (1 if math.cos(t) > 0 else 0.6)
        pts.append((x, y))
    outer = [(0, -0.95)] + [(0.18, -0.6), (0.5, -0.25), (0.62, 0.2)] + arc(0, 0.25, 0.62, 0, 180, 20)[1:] + [(-0.5, -0.2), (-0.28, -0.45), (-0.2, -0.15), (-0.05, -0.55), (0, -0.95)]
    inner = [(0, -0.2), (0.22, 0.15)] + arc(0, 0.38, 0.25, -20, 200, 14) + [(-0.22, 0.15), (0, -0.2)]
    return [outer, inner]
ICONS['flame'] = flame()
ICONS['plate'] = [circle(0, 0, 0.62), circle(0, 0, 0.44),
                  [(-0.88, -0.75), (-0.88, 0.8)], [(-0.98, -0.75), (-0.98, -0.4)], [(-0.78, -0.75), (-0.78, -0.4)],
                  [(-0.98, -0.4)] + arc(-0.88, -0.4, 0.1, 180, 0, 8)[::-1][::-1],
                  [(0.88, 0.8), (0.88, -0.75)] + [(0.96, -0.55), (0.96, -0.1), (0.88, -0.1)]]
ICONS['qmark'] = [arc(0, -0.35, 0.42, 190, 400, 40) + [(0.0, 0.05), (0.0, 0.3)], circle(0, 0.62, 0.06, 16)]
ICONS['one'] = person(0, 0.15, 1.1)
ICONS['two'] = person(-0.38, 0.15, 0.95) + person(0.38, 0.15, 0.95)
ICONS['burger'] = [arc(0, -0.15, 0.62, 180, 360, 30, rx=0.85) + [(-0.85, -0.15)],
                   [(-0.9, 0.05), (-0.6, 0.15), (-0.3, 0.03), (0, 0.15), (0.3, 0.03), (0.6, 0.15), (0.9, 0.05)],
                   rrect(-0.85, 0.28, 0.85, 0.42, 0.07),
                   rrect(-0.85, 0.55, 0.85, 0.78, 0.11),
                   [(-0.3, -0.45), (-0.24, -0.42)], [(0.05, -0.55), (0.11, -0.52)], [(0.35, -0.4), (0.41, -0.37)]]
ICONS['calendar'] = [rrect(-0.85, -0.7, 0.85, 0.85, 0.12), [(-0.85, -0.3), (0.85, -0.3)],
                     [(-0.45, -0.88), (-0.45, -0.55)], [(0.45, -0.88), (0.45, -0.55)]]
ICONS['bookmark'] = [[(-0.5, -0.85), (0.5, -0.85), (0.5, 0.85), (0, 0.45), (-0.5, 0.85), (-0.5, -0.85)]]
ICONS['check'] = [[(-0.6, 0.0), (-0.15, 0.45), (0.65, -0.45)]]

def _lens(paths):
    L = []
    for p in paths:
        l = 0
        for a, b in zip(p, p[1:]):
            l += math.hypot(b[0] - a[0], b[1] - a[1])
        L.append(l)
    return L

_ic = {}
def icon_sprite(name, size, color=CREAM, width=6, p=1.0, shadow=True):
    pq = round(clamp(p) * 40) / 40
    k = (name, size, color, width, pq, shadow)
    if k in _ic: return _ic[k]
    SS = 3
    S = size * SS
    m = width * SS * 2
    img = Image.new('RGBA', (S + 2 * m, S + 2 * m), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    paths = ICONS[name]
    lens = _lens(paths)
    total = sum(lens) * pq
    wpx = width * SS
    def tr(pt): return (m + (pt[0] + 1) / 2 * S, m + (pt[1] + 1) / 2 * S)
    for path, l in zip(paths, lens):
        if total <= 0: break
        pts = [tr(path[0])]
        rem = total
        for a, b in zip(path, path[1:]):
            seg = math.hypot(b[0] - a[0], b[1] - a[1])
            if seg <= rem:
                pts.append(tr(b)); rem -= seg
            else:
                f = rem / seg if seg else 0
                pts.append(tr((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))); rem = 0
                break
        total -= l
        if len(pts) > 1:
            d.line(pts, fill=color + (255,), width=wpx, joint='curve')
        for q in (pts[0], pts[-1]):
            d.ellipse([q[0] - wpx / 2, q[1] - wpx / 2, q[0] + wpx / 2, q[1] + wpx / 2], fill=color + (255,))
    img = img.resize((img.width // SS, img.height // SS), Image.LANCZOS)
    if shadow: img = add_shadow(img, radius=8, opacity=0.6)
    _ic[k] = img
    return img

def draw_icon(canvas, name, cx, cy, size, t, t0, draw_d=0.6, color=CREAM, width=6, t_out=None, pop=True):
    if t < t0: return
    p = ease_inout(prog(t, t0, draw_d))
    a = 1.0
    sc = ease_back(prog(t, t0, 0.35)) if pop else 1
    sc = 0.6 + 0.4 * sc
    if t_out is not None:
        if t > t_out + 0.25: return
        if t > t_out:
            a = 1 - prog(t, t_out, 0.25); sc *= 1 - 0.15 * prog(t, t_out, 0.25)
    place(canvas, icon_sprite(name, size, color, width, p), cx, cy, sc, a)

# ---------------- cards / shapes ----------------
_cc = {}
def card_sprite(w, h, fill=(245, 238, 226, 240), outline=None, r=28, ow=3):
    k = (w, h, fill, outline, r, ow)
    if k in _cc: return _cc[k]
    SS = 2
    img = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], r * SS, fill=fill,
                        outline=outline, width=ow * SS if outline else 0)
    img = img.resize((w, h), Image.LANCZOS)
    img = add_shadow(img, radius=14, offset=(0, 8), opacity=0.45, pad=40)
    _cc[k] = img
    return img

def composite_card(w, h, items, fill=(245, 238, 226, 238), outline=None):
    """items: list of (sprite, cx, cy) relative to card center"""
    base = card_sprite(w, h, fill, outline).copy()
    ox, oy = base.width / 2, base.height / 2
    for spr, x, y in items:
        base.alpha_composite(spr, (int(ox + x - spr.width / 2), int(oy + y - spr.height / 2)))
    return base

# ---------------- words / captions ----------------
words = json.load(open(os.path.join(BASE, 'words.json')))
FIX = {3: 'Pará,', 58: '¿Sos', 74: 'querés', 85: 'Somos', 95: 'parrilla.', 115: 'sabés:',
       123: 'Guardá', 127: 'etiquetá'}
tokens = []
for i, (s, e, w) in enumerate(words):
    w = FIX.get(i, w)
    tokens.append([s, e, w])

def clean(w):
    return w.rstrip('.,:;')

GROUPS = [
    ("¿Venís a Luján?", ""),
    ("Pará,", "no te vayas"),
    ("sin venir", "a comer acá"),
    ("Estamos a solo", "600 metros de la basílica"),
    ("Bienvenidos a", "Anana"),
    ("Mirá", "este salón"),
    ("¿Lugar?", "Sobra"),
    ("Vení con toda", "la familia"),
    ("amigos", "o pareja"),
    ("Acá la carne se hace", "a las brasas"),
    ("como tiene", "que ser"),
    ("Parrillada", "para compartir"),
    ("y no te va", "a sobrar nada"),
    ("¿Sos más", "de milanesa?"),
    ("Tenemos milanesa", "con papas fritas"),
    ("para compartir", "o la individual"),
    ("si no querés", "compartir con nadie"),
    ("Y esto es", "lo que nadie tiene"),
    ("Somos el único", "lugar en Luján"),
    ("con hamburguesas", "a la parrilla"),
    ("Sí,", "a la parrilla"),
    ("Y ojo,", ""),
    ("porque todos", "los jueves"),
    ("tenemos promo", "en pizzas o hamburguesas"),
    ("Así que", "ya sabés"),
    ("después de", "la basílica"),
    ("venite", "a Anana"),
    ("Guardá", "este video"),
    ("y etiquetá", "a esa persona"),
    ("que se viene", "para acá"),
]
groups = []
ti = 0
for l1, l2 in GROUPS:
    g = {'l1': [], 'l2': []}
    for key, line in (('l1', l1), ('l2', l2)):
        for w in line.split():
            tw = tokens[ti]
            if clean(tw[2]).lower().strip('¿?¡!') != clean(w).lower().strip('¿?¡!'):
                print('MISMATCH', ti, tw, w); sys.exit(1)
            g[key].append((w, tw[0], tw[1]))
            ti += 1
    groups.append(g)
assert ti == len(tokens), (ti, len(tokens))
for i, g in enumerate(groups):
    allw = g['l1'] + g['l2']
    g['start'] = allw[0][1]
    last_end = allw[-1][2]
    nxt = groups[i + 1]['l1'][0][1] if i + 1 < len(groups) else DUR
    g['end'] = min(nxt - 0.02, last_end + 0.7)
    if i + 1 == len(groups): g['end'] = DUR
SKIP_GROUPS = {4}  # brand reveal handled by custom graphic

CAP_Y1, CAP_Y2 = 1000, 1092
HL_WORDS = {'600', 'metros', 'Anana', 'brasas', 'único', 'jueves', 'Sobra', 'nadie', 'parrilla', 'individual', 'promo'}

def layout_line(ws, f, color_fn, maxw=960):
    sprites = [text_sprite(clean(w) if not w.endswith('?') else w, f, color_fn(w)) for w, _, _ in ws]
    space = f.getlength(' ')
    widths = [s.width - 60 - 24 for s in sprites]  # minus shadow pad & text pad
    total = sum(widths) + space * (len(ws) - 1)
    scale = min(1.0, maxw / total) if total else 1
    x = W / 2 - total * scale / 2
    out = []
    for s, wd in zip(sprites, widths):
        out.append((s, x + wd * scale / 2, scale))
        x += (wd + space) * scale
    return out

_band = {}
def band_sprite(a):
    k = round(a * 10)
    if k not in _band:
        h = 480
        y = np.linspace(-1, 1, h)
        prof = np.exp(-(y / 0.55) ** 2) * 0.32 * (k / 10)
        al = (prof * 255).astype(np.uint8)[:, None].repeat(W, 1)
        img = Image.new('RGBA', (W, h), (18, 12, 6, 0))
        img.putalpha(Image.fromarray(al))
        _band[k] = img
    return _band[k]

_lc = {}
def draw_captions(canvas, t):
    for gi, g in enumerate(groups):
        if gi in SKIP_GROUPS: continue
        if not (g['start'] - 0.01 <= t < g['end']): continue
        if gi not in _lc:
            f1 = SANS(92, 800)
            f2 = SERIF_I(84, 600)
            c1 = lambda w: (BEIGE if clean(w).strip('¿?') in HL_WORDS else WHITE)
            c2 = lambda w: BEIGE
            L1 = layout_line(g['l1'], f1, c1)
            L2 = layout_line(g['l2'], f2, c2) if g['l2'] else []
            _lc[gi] = (L1, L2)
        L1, L2 = _lc[gi]
        ga = clamp(prog(t, g['start'] - 0.05, 0.15)) * (1 - prog(t, g['end'] - 0.08, 0.08))
        canvas.alpha_composite(band_sprite(ga), (0, CAP_Y1 - 190))
        single = not L2
        y1 = (CAP_Y1 + CAP_Y2) / 2 if single else CAP_Y1
        exit_a = 1 - prog(t, g['end'] - 0.08, 0.08)
        for (spr, x, sc), (w, ws, we) in list(zip(L1, g['l1'])) + list(zip(L2, g['l2'])):
            if t < ws - 0.04: continue
            isl2 = (spr, x, sc) in L2
            y = CAP_Y2 if isl2 else y1
            p = prog(t, ws - 0.04, 0.2)
            s = sc * (0.75 + 0.25 * ease_back(p))
            place(canvas, spr, x, y + 14 * (1 - ease_out(p)), s, ease_out(p * 1.6) * exit_a)

# ---------------- headline (top) ----------------
def headline(canvas, txt, t, t0, t1, y=300, size=64, sub=None):
    if not (t0 <= t < t1 + 0.3): return
    p = ease_out(prog(t, t0, 0.5))
    a = p * (1 - prog(t, t1, 0.3))
    track = 26 - 12 * p
    spr = text_sprite(txt, SERIF(size, 600), CREAM, tracking=round(track))
    place(canvas, spr, W / 2, y, 1.0, a)
    # thin rules either side
    lw = int(90 * ease_out(prog(t, t0 + 0.15, 0.5)))
    if lw > 2:
        d = ImageDraw.Draw(canvas)
        half = (spr.width - 60) / 2 + 30
        col = CREAM + (int(220 * a),)
        d.line([(W / 2 - half - lw, y + 4), (W / 2 - half, y + 4)], fill=col, width=3)
        d.line([(W / 2 + half, y + 4), (W / 2 + half + lw, y + 4)], fill=col, width=3)
    if sub:
        s2 = text_sprite(sub, CORM_I(46, 500), BEIGE)
        place(canvas, s2, W / 2, y + 62, 1.0, a * ease_out(prog(t, t0 + 0.25, 0.4)))

# ---------------- graphics ----------------
GY = 1400  # graphics band center

def dotted_line(canvas, x0, x1, y, p, a=1.0, col=CREAM):
    d = ImageDraw.Draw(canvas)
    xe = x0 + (x1 - x0) * p
    x = x0
    while x < xe:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col + (int(255 * a),))
        x += 26

def route(canvas, t, t0, t1, labels=('BASÍLICA', 'ANANA'), mid='600 m', t_line=None, t_pin=None):
    if not (t0 <= t < t1 + 0.3): return
    out = t1
    a = 1 - prog(t, out, 0.3)
    t_line = t_line or t0 + 0.5
    t_pin = t_pin or t_line + 0.6
    draw_icon(canvas, 'basilica', 250, GY, 200, t, t0, 0.8, t_out=out)
    lp = ease_inout(prog(t, t_line, t_pin - t_line))
    if lp > 0: dotted_line(canvas, 380, 720, GY + 40, lp, a)
    if mid and t >= t_line + 0.2:
        q = ease_back(prog(t, t_line + 0.2, 0.35))
        place(canvas, text_sprite(mid, SERIF_I(64, 600), BEIGE), 550, GY - 30, 0.6 + 0.4 * q, a * clamp(q))
    draw_icon(canvas, 'pin', 820, GY - 10, 170, t, t_pin, 0.5, t_out=out)
    for lab, x, tt in ((labels[0], 250, t0 + 0.4), (labels[1], 820, t_pin + 0.2)):
        if t >= tt:
            q = ease_out(prog(t, tt, 0.35))
            place(canvas, text_sprite(lab, SANS(30, 600), CREAM, tracking=6), x, GY + 150, 1, a * q)

def brand(canvas, t, t0=5.06, t1=6.05):
    if not (t0 <= t < t1 + 0.25): return
    a = 1 - prog(t, t1, 0.25)
    q = ease_out(prog(t, t0, 0.45))
    place(canvas, text_sprite('Bienvenidos a', CORM_I(80, 500), BEIGE), W / 2, 905 + 20 * (1 - q), 1, a * q)
    t2 = 5.62
    if t >= t2 - 0.08:
        q2 = ease_out(prog(t, t2 - 0.08, 0.45))
        tr = round(40 - 18 * q2)
        place(canvas, text_sprite('ANANA', SERIF(150, 700), WHITE, tracking=tr), W / 2, 1040, 0.9 + 0.1 * q2, a * q2)
    lw = int(240 * ease_inout(prog(t, t0 + 0.2, 0.6)))
    if lw > 2:
        d = ImageDraw.Draw(canvas)
        col = BEIGE + (int(230 * a),)
        for y in (835, 1150):
            d.line([(W / 2 - lw, y), (W / 2 + lw, y)], fill=col, width=3)
        for x in (W / 2 - lw - 14, W / 2 + lw + 14):
            for y in (835, 1150):
                d.polygon([(x, y - 7), (x + 7, y), (x, y + 7), (x - 7, y)], fill=col)

def viewfinder(canvas, t, t0=6.1, t1=7.95):
    if not (t0 <= t < t1 + 0.2): return
    p = ease_out(prog(t, t0, 0.4))
    a = 1 - prog(t, t1, 0.2)
    m = 150 - 80 * p
    x0, y0, x1, y1 = m, 230 + (1 - p) * 60, W - m, 1640 - (1 - p) * 60
    L = 90
    d = ImageDraw.Draw(canvas)
    col = CREAM + (int(235 * a * p),)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(x, y + sy * L), (x, y), (x + sx * L, y)], fill=col, width=6, joint='curve')
    # rec dot + label
    if (t * 2) % 1 < 0.6:
        d.ellipse([x0 + 30, y0 + 30, x0 + 52, y0 + 52], fill=(214, 120, 96, int(220 * a * p)))
    place(canvas, text_sprite('EL SALÓN', SANS(28, 600), CREAM, tracking=6), x0 + 150, y0 + 42, 1, a * p)

def chips(canvas, t, specs, t_out, y=GY, size=120):
    n = len(specs)
    gap = 300
    for i, (ic, lab, t0) in enumerate(specs):
        if t < t0 or t > t_out + 0.3: continue
        x = W / 2 + (i - (n - 1) / 2) * gap
        q = ease_back(prog(t, t0, 0.35))
        a = clamp(q * 1.5) * (1 - prog(t, t_out, 0.3))
        spr = chip_sprite(ic, lab, size)
        place(canvas, spr, x, y + 30 * (1 - clamp(q)), 0.7 + 0.3 * q, a)

_chc = {}
def chip_sprite(ic, lab, size):
    k = (ic, lab, size)
    if k in _chc: return _chc[k]
    icon = icon_sprite(ic, size, BROWN, 6, 1.0, shadow=False)
    txt = text_sprite(lab, SANS(28, 700), BROWN, tracking=4, shadow=False)
    spr = composite_card(max(250, txt.width + 30), 250, [(icon, 0, -25), (txt, 0, 85)])
    _chc[k] = spr
    return spr

def sparks(canvas, t, t0, t1, n=60, seed=1, y0=1750, rise=900):
    if not (t0 <= t < t1): return
    rnd = random.Random(seed)
    d = ImageDraw.Draw(canvas)
    env = clamp(prog(t, t0, 0.4)) * (1 - prog(t, t1 - 0.4, 0.4))
    for i in range(n):
        b = t0 - 1.5 + rnd.random() * (t1 - t0 + 1.5)
        life = 1.2 + rnd.random() * 1.2
        x = rnd.random() * W
        sp = rnd.random()
        sway = rnd.random() * 6
        r = 2 + rnd.random() * 3.5
        age = (t - b) / life
        if not (0 <= age <= 1): continue
        yy = y0 - age * rise * (0.6 + 0.6 * sp)
        xx = x + math.sin(age * 5 + sway) * 30
        al = math.sin(age * math.pi) * env
        d.ellipse([xx - r * 2.2, yy - r * 2.2, xx + r * 2.2, yy + r * 2.2], fill=EMBER + (int(60 * al),))
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 226, 180, int(230 * al)))

def option_cards(canvas, t):
    t0a, t0b, tsel, tout = 17.9, 18.45, 19.3, 20.1
    if not (t0a <= t < tout + 0.3): return
    a_out = 1 - prog(t, tout, 0.3)
    sel = ease_out(prog(t, tsel, 0.3))
    for (ic, lab, x, t0, is_b) in (('two', 'PARA COMPARTIR', 300, t0a, False), ('one', 'INDIVIDUAL', 780, t0b, True)):
        if t < t0: continue
        q = ease_back(prog(t, t0, 0.35))
        k = ('opt', lab)
        if k not in _chc:
            icon = icon_sprite(ic, 130, BROWN, 6, 1, shadow=False)
            txt = text_sprite(lab, SANS(30, 700), BROWN, tracking=3, shadow=False)
            _chc[k] = composite_card(400, 290, [(icon, 0, -30), (txt, 0, 95)])
        spr = _chc[k]
        dim = 1.0
        sc = 0.7 + 0.3 * q
        if is_b: sc *= 1 + 0.06 * sel
        else: dim = 1 - 0.45 * sel
        place(canvas, spr, x, GY + 20, sc, clamp(q * 1.5) * a_out * dim)
        if is_b and sel > 0:
            ck = icon_sprite('check', 70, BROWN, 9, sel, shadow=False)
            cb = card_sprite(90, 90, (226, 208, 176, 255), None, r=45)
            place(canvas, cb, x + 170, GY - 110, 0.5 + 0.5 * ease_back(prog(t, tsel, 0.3)), a_out)
            place(canvas, ck, x + 170, GY - 110, 0.7, a_out)

_seal = None
def seal_sprite():
    global _seal
    if _seal: return _seal
    S = 440
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = S / 2
    d.ellipse([c - 200, c - 200, c + 200, c + 200], fill=(245, 238, 226, 235))
    d.ellipse([c - 186, c - 186, c + 186, c + 186], outline=BROWN + (255,), width=3)
    d.ellipse([c - 118, c - 118, c + 118, c + 118], outline=BROWN + (255,), width=2)
    txt = 'ÚNICOS EN LUJÁN  •  HAMBURGUESAS A LA PARRILLA  •  '
    f = SANS(25, 700)
    n = len(txt)
    for i, ch in enumerate(txt):
        ang = 360 * i / n
        ci = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        ImageDraw.Draw(ci).text((20, 20), ch, font=f, fill=BROWN, anchor='mm')
        ci = ci.rotate(-ang, resample=Image.BICUBIC)
        r = 152
        x = c + r * math.sin(math.radians(ang)); y = c - r * math.cos(math.radians(ang))
        img.alpha_composite(ci, (int(x - 20), int(y - 20)))
    _seal = add_shadow(img, radius=14, offset=(0, 8), opacity=0.45, pad=30)
    return _seal

def seal(canvas, t, t0=22.4, t1=25.1):
    if not (t0 <= t < t1 + 0.3): return
    q = ease_back(prog(t, t0, 0.45))
    a = clamp(q * 1.5) * (1 - prog(t, t1, 0.3))
    place(canvas, seal_sprite(), W / 2, GY + 10, (0.5 + 0.5 * q) * 0.95, a, rot=-(t - t0) * 18)
    draw_icon(canvas, 'burger', W / 2, GY + 10, 150, t, t0 + 0.15, 0.7, color=BROWN, width=6, t_out=t1)

def calendar(canvas, t, t0=26.4, t1=28.95):
    if not (t0 <= t < t1 + 0.3): return
    q = ease_back(prog(t, t0, 0.4))
    a = clamp(q * 1.5) * (1 - prog(t, t1, 0.3))
    k = 'cal'
    if k not in _chc:
        base = card_sprite(420, 330, (245, 238, 226, 240)).copy()
        d = ImageDraw.Draw(base)
        ox, oy = 40, 40
        d.rounded_rectangle([ox, oy, ox + 420, oy + 95], 28, fill=BROWN)
        d.rectangle([ox, oy + 60, ox + 420, oy + 95], fill=BROWN)
        jt = text_sprite('JUEVES', SANS(46, 700), CREAM, tracking=10, shadow=False)
        base.alpha_composite(jt, (int(ox + 210 - jt.width / 2), int(oy + 48 - jt.height / 2)))
        pt = text_sprite('Promo', SERIF_I(110, 600), BROWN, shadow=False)
        base.alpha_composite(pt, (int(ox + 210 - pt.width / 2), int(oy + 210 - pt.height / 2)))
        for rx in (ox + 110, ox + 310):
            d.rounded_rectangle([rx - 9, oy - 22, rx + 9, oy + 26], 9, fill=(176, 150, 112))
        _chc[k] = base
    place(canvas, _chc[k], W / 2, GY - 30, 0.6 + 0.4 * q, a)
    for lab, x, tt in (('PIZZA', W / 2 - 150, 27.95), ('HAMBURGUESA', W / 2 + 120, 28.75)):
        if t >= tt:
            qq = ease_back(prog(t, tt, 0.3))
            kk = ('pill', lab)
            if kk not in _chc:
                ts = text_sprite(lab, SANS(30, 700), BROWN, tracking=4, shadow=False)
                _chc[kk] = composite_card(ts.width + 40, 70, [(ts, 0, 2)], fill=(226, 208, 176, 250))
            place(canvas, _chc[kk], x, GY + 190, 0.6 + 0.4 * qq, clamp(qq * 1.5) * (1 - prog(t, t1 + 0.4, 0.3)))

def cta(canvas, t):
    specs = (('bookmark', 'GUARDAR', 31.62, 360), (None, 'ETIQUETAR', 32.7, 720))
    for ic, lab, t0, x in specs:
        if t < t0: continue
        q = ease_back(prog(t, t0, 0.4))
        k = ('cta', lab)
        if k not in _chc:
            if ic:
                isp = icon_sprite(ic, 110, BROWN, 7, 1, shadow=False)
            else:
                isp = text_sprite('@', SANS(130, 600), BROWN, shadow=False)
            lsp = text_sprite(lab, SANS(28, 700), BROWN, tracking=5, shadow=False)
            _chc[k] = composite_card(260, 260, [(isp, 0, -22), (lsp, 0, 90)])
        place(canvas, _chc[k], x, GY + 20, 0.6 + 0.4 * q, clamp(q * 1.5))
    # little tap pulse
    for t0, x in ((31.9, 360), (32.95, 720)):
        if t0 <= t < t0 + 0.5:
            p = prog(t, t0, 0.5)
            d = ImageDraw.Draw(canvas)
            r = 40 + 120 * ease_out(p)
            d.ellipse([x + 90 - r, GY + 120 - r, x + 90 + r, GY + 120 + r], outline=CREAM + (int(200 * (1 - p)),), width=4)

def big_q(canvas, t, t0=15.2, t1=16.3):
    if not (t0 <= t < t1 + 0.25): return
    draw_icon(canvas, 'qmark', W / 2, GY, 230, t, t0, 0.55, color=CREAM, width=9, t_out=t1)

def stamp(canvas, t, txt, t0, t1, y=GY, size=120):
    if not (t0 <= t < t1 + 0.2): return
    p = prog(t, t0, 0.22)
    sc = 1.6 - 0.6 * ease_out(p)
    a = clamp(p * 2) * (1 - prog(t, t1, 0.2))
    place(canvas, text_sprite(txt, SERIF_I(size, 700), CREAM), W / 2, y, sc, a, rot=-4)

def draw_overlay(t):
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # 0-2.7 hook
    headline(cv, 'LUJÁN', t, 0.05, 2.65, y=290, size=70, sub='Buenos Aires')
    draw_icon(cv, 'pin', W / 2, 175, 80, t, 0.1, 0.5, t_out=2.65, width=5)
    # 2.78-4.9 route basilica -> anana
    route(cv, t, 2.75, 4.95, mid='600 m', t_line=3.3, t_pin=4.3)
    brand(cv, t)
    viewfinder(cv, t)
    draw_icon(cv, 'expand', W / 2, GY, 170, t, 6.75, 0.45, t_out=7.95, width=7)
    chips(cv, t, [('family', 'FAMILIA', 8.75), ('cheers', 'AMIGOS', 9.38), ('heart', 'PAREJA', 9.78)], t_out=10.32)
    sparks(cv, t, 10.4, 13.0, n=70, seed=3)
    draw_icon(cv, 'flame', W / 2, GY, 190, t, 11.4, 0.6, t_out=12.9, width=7)
    draw_icon(cv, 'plate', W / 2, GY, 220, t, 13.3, 0.7, t_out=15.15, width=6)
    if 14.9 <= t < 15.2:
        pass
    big_q(cv, t)
    chips(cv, t, [('plate', 'PAPAS FRITAS', 16.55)], t_out=17.85, size=130)
    option_cards(cv, t)
    headline(cv, 'LO QUE NADIE TIENE', t, 20.16, 21.82, y=300, size=60)
    seal(cv, t)
    sparks(cv, t, 24.2, 25.4, n=40, seed=7)
    headline(cv, 'TODOS LOS JUEVES', t, 25.9, 28.9, y=300, size=60)
    calendar(cv, t)
    route(cv, t, 29.9, 31.5, labels=('BASÍLICA', 'ANANA'), mid='', t_line=30.6, t_pin=31.1)
    cta(cv, t)
    draw_captions(cv, t)
    return cv

# ---------------- camera moves ----------------
CUTS = [0, 2.7, 4.83, 6.0, 6.7, 7.37, 8.77, 9.57, 10.3, 12.77, 13.4, 14.13, 14.7, 15.17, 16.37, 17.12,
        17.74, 18.41, 19.08, 19.62, 20.16, 21.83, 22.28, 22.66, 22.95, 23.37, 23.66, 24.08, 24.45, 24.78,
        25.16, 27.83, 28.33, 28.49, 28.93, 31.46, 99]
PUNCH = [(7.30, 7.95, 1.10), (21.08, 21.83, 1.10), (24.2, 24.45, 1.08), (1.0, 1.32, 1.07), (25.4, 25.75, 1.08)]
def zoom_at(t):
    for a, b in zip(CUTS, CUTS[1:]):
        if a <= t < b: break
    # gentle push in through each shot + small settle at cut
    z = 1.0 + 0.035 * clamp((t - a) / max(0.5, (b - a if b < 90 else 3)))
    z += 0.04 * (1 - ease_out(prog(t, a, 0.35))) if a > 0 else 0
    for s, e, k in PUNCH:
        if s <= t < e: z *= k
    return z

def apply_zoom(img, z):
    if z <= 1.001: return img
    cw, ch = W / z, H / z
    x0, y0 = (W - cw) / 2, (H - ch) / 2
    return img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))

# vignette
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
VIG = np.clip(1 - 0.38 * np.clip(r - 0.55, 0, 1) ** 1.4, 0, 1).astype(np.float32)[..., None]

def main(out_path, t_start=0.0, t_end=DUR, only=None):
    grade = ("eq=saturation=0.74:contrast=1.04:brightness=0.005:gamma=1.02,"
             "colorbalance=rs=0.045:gs=0.02:bs=-0.05:rm=0.04:gm=0.015:bm=-0.04:rh=0.02:bh=-0.03,"
             "curves=all='0/0.035 0.5/0.51 1/0.97'")
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(t_start), '-i', SRC, '-t', str(t_end - t_start),
                            '-vf', 'scale=in_color_matrix=bt709:in_range=tv,format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                            '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-color_primaries', 'smpte432', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv', out_path], stdin=subprocess.PIPE)
    n = 0
    fsz = W * H * 3
    rng = np.random.default_rng(0)
    while True:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz: break
        t = t_start + n / FPS
        arr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        img = Image.fromarray(arr)
        img = apply_zoom(img, zoom_at(t))
        img = img.convert('RGBA')
        img.alpha_composite(draw_overlay(t))
        enc.stdin.write(img.convert('RGB').tobytes())
        n += 1
        if n % 60 == 0: print('frame', n, round(t, 2), flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()

def stills(ts, outdir):
    os.makedirs(outdir, exist_ok=True)
    for t in ts:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', SRC, '-frames:v', '1', '-f', 'rawvideo',
                              '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        img = Image.fromarray(np.frombuffer(raw, np.uint8).reshape(H, W, 3))
        img = apply_zoom(img, zoom_at(t)).convert('RGBA')
        img.alpha_composite(draw_overlay(t))
        img.convert('RGB').resize((360, 640)).save(os.path.join(outdir, f's_{t:05.2f}.jpg'))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        stills([float(x) for x in sys.argv[2].split(',')], sys.argv[3])
    else:
        main(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0, float(sys.argv[4]) if len(sys.argv) > 4 else DUR)
