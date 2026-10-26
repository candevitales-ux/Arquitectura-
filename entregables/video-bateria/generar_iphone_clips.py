"""Genera clips ilustrados del iPhone 13:
  - sacando una foto
  - siendo veloz (abre apps una tras otra)
  - actualizándose

Cada clip sale en .mp4 con fondo verde liso y en .mov ProRes 4444 con fondo transparente.
En pantalla no se usa verde, para que no se borre junto con el fondo.

Uso:
    python3 generar_iphone_clips.py

Requiere Pillow y ffmpeg. Reutiliza el teléfono de generar_mano_iphone.py.
"""
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from generar_mano_iphone import (
    ALTO, ANCHO, FONDO_VERDE, FPS, FUENTE, FUENTE_BOLD, PANT_H, PANT_W, PANT_X, PANT_Y, SS, TEL_H, TEL_W,
    barra_inicio, caja, ease_out, fondo_degradado, s, suave, telefono_con_pantalla,
)

BLANCO = (255, 255, 255)
AMARILLO = (255, 204, 0)
AZUL_IOS = (0, 122, 255)

# colores de íconos de apps, sin verde
COLORES_APPS = [
    (255, 59, 48), (255, 149, 0), (255, 204, 0), (0, 122, 255), (88, 86, 214), (175, 82, 222),
    (255, 45, 85), (90, 200, 250), (52, 120, 246), (255, 112, 67), (142, 142, 147), (191, 90, 242),
    (255, 159, 10), (10, 132, 255), (230, 60, 90), (100, 110, 240),
]


def mezclar(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def tramo(t, a, b):
    return min(max((t - a) / (b - a), 0), 1)


def ease_out_back(t):
    t = min(max(t, 0), 1)
    c = 1.5
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def fuente(tam, bold=False):
    return ImageFont.truetype(FUENTE_BOLD if bold else FUENTE, s(tam))


def texto_ajustado(d, xy, texto, tam, ancho_max, bold=False, **kw):
    """Escribe el texto achicando la fuente si no entra en ancho_max (coordenadas sin supersampling)."""
    while tam > 8 and d.textlength(texto, font=fuente(tam, bold)) > s(ancho_max):
        tam -= 1
    d.text((s(xy[0]), s(xy[1])), texto, font=fuente(tam, bold), **kw)


def pantalla_vacia(color):
    return Image.new("RGBA", (s(PANT_W), s(PANT_H)), color + (255,))


# ---------------------------------------------------------------- sombra y armado del cuadro

_SOMBRA = None


def sombra_telefono():
    global _SOMBRA
    if _SOMBRA is None:
        m = s(60)
        img = Image.new("RGBA", (s(TEL_W) + 2 * m, s(TEL_H) + 2 * m), (0, 0, 0, 0))
        ImageDraw.Draw(img).rounded_rectangle((m, m, m + s(TEL_W), m + s(TEL_H)), radius=s(58), fill=(0, 0, 0, 80))
        _SOMBRA = img.filter(ImageFilter.GaussianBlur(s(18)))
    return _SOMBRA


def montar(fondo, telefono, escala=1.0, dx=0, dy=0, alfa=1.0, extra=None):
    """Pone el teléfono centrado en el cuadro. `extra` dibuja cosas detrás (líneas de velocidad)."""
    W, H = s(ANCHO), s(ALTO)
    lienzo = Image.new("RGBA", (W, H), fondo + (255,) if fondo else (0, 0, 0, 0))
    if extra:
        extra(lienzo)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sombra = sombra_telefono()
    tel = telefono
    if escala != 1.0:
        sombra = sombra.resize((max(int(sombra.width * escala), 1), max(int(sombra.height * escala), 1)))
        tel = tel.resize((max(int(tel.width * escala), 1), max(int(tel.height * escala), 1)), Image.LANCZOS)
    cx, cy = W // 2 + int(dx), H // 2 + int(dy)
    capa.alpha_composite(sombra, (cx - sombra.width // 2 + s(8), cy - sombra.height // 2 + s(14)))
    capa.alpha_composite(tel, (cx - tel.width // 2, cy - tel.height // 2))
    if alfa < 1:
        capa.putalpha(capa.getchannel("A").point(lambda v: int(v * alfa)))
    lienzo.alpha_composite(capa)
    return lienzo.resize((ANCHO, ALTO), Image.LANCZOS)


def entrada_pop(t, dur=0.5):
    """Escala y opacidad para que el teléfono aparezca con un pequeño rebote."""
    p = tramo(t, 0, dur)
    return 0.6 + 0.4 * ease_out_back(p), min(p * 2.5, 1)


# ---------------------------------------------------------------- 1) sacando una foto

VISOR_Y0, VISOR_Y1 = 70, 500          # zona del visor dentro de la pantalla


def paisaje(w, h):
    """Escena simple para el visor: cielo, sol, montañas y lago (sin verde)."""
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line((0, y, w, y), fill=(int(255 - 60 * t), int(170 + 40 * t), int(120 + 110 * t), 255))
    d.ellipse((w * 0.58, h * 0.16, w * 0.82, h * 0.16 + w * 0.24), fill=(255, 236, 160))
    d.polygon([(0, h * 0.72), (w * 0.3, h * 0.38), (w * 0.62, h * 0.72)], fill=(96, 80, 150))
    d.polygon([(w * 0.35, h * 0.72), (w * 0.7, h * 0.3), (w * 1.05, h * 0.72)], fill=(70, 58, 120))
    d.polygon([(w * 0.62, h * 0.38), (w * 0.7, h * 0.3), (w * 0.78, h * 0.38), (w * 0.72, h * 0.36),
               (w * 0.68, h * 0.4)], fill=(240, 240, 250))
    d.rectangle((0, h * 0.72, w, h), fill=(60, 120, 190))
    for i in range(5):
        y = h * (0.78 + i * 0.045)
        d.line((w * 0.15 + i * 9, y, w * 0.55 - i * 7, y), fill=(140, 190, 235), width=max(h // 160, 1))
    return img


def clip_foto(t, fondo, cache):
    if "visor" not in cache:
        cache["visor"] = paisaje(s(PANT_W), s(VISOR_Y1 - VISOR_Y0))
    visor = cache["visor"]
    T_FOCO, T_DISPARO, T_FLASH = 0.9, 1.9, 2.0

    p = pantalla_vacia((0, 0, 0))
    p.alpha_composite(visor, (0, s(VISOR_Y0)))
    d = ImageDraw.Draw(p)

    # cuadro de enfoque amarillo
    if T_FOCO <= t < T_DISPARO + 0.4:
        q = tramo(t, T_FOCO, T_FOCO + 0.35)
        lado = 120 - 30 * suave(q)
        cx, cy = PANT_W * 0.45, (VISOR_Y0 + VISOR_Y1) / 2 + 20
        alfa = 255 if t < T_DISPARO else int(255 * (1 - tramo(t, T_DISPARO, T_DISPARO + 0.4)))
        capa = Image.new("RGBA", p.size, (0, 0, 0, 0))
        ImageDraw.Draw(capa).rectangle(caja(cx - lado / 2, cy - lado / 2, cx + lado / 2, cy + lado / 2),
                                       outline=AMARILLO + (alfa,), width=s(3))
        p.alpha_composite(capa)

    # modos y botón de disparo
    d.text((s(PANT_W / 2), s(VISOR_Y1 + 26)), "FOTO", font=fuente(15, True), fill=AMARILLO, anchor="mm")
    d.text((s(PANT_W / 2 - 70), s(VISOR_Y1 + 26)), "VIDEO", font=fuente(14), fill=(220, 220, 220), anchor="mm")
    d.text((s(PANT_W / 2 + 74), s(VISOR_Y1 + 26)), "RETRATO", font=fuente(14), fill=(220, 220, 220), anchor="mm")
    bx, by = PANT_W / 2, VISOR_Y1 + 95
    d.ellipse(caja(bx - 38, by - 38, bx + 38, by + 38), outline=BLANCO, width=s(5))
    presion = 1.0
    if T_DISPARO <= t < T_DISPARO + 0.25:
        presion = 1 - 0.18 * math.sin(math.pi * tramo(t, T_DISPARO, T_DISPARO + 0.25))
    r = 30 * presion
    d.ellipse(caja(bx - r, by - r, bx + r, by + r), fill=BLANCO)
    # cambiar cámara
    gx = PANT_W - 60
    d.ellipse(caja(gx - 24, by - 24, gx + 24, by + 24), fill=(50, 50, 52))
    d.arc(caja(gx - 12, by - 12, gx + 12, by + 12), 200, 340, fill=BLANCO, width=s(3))
    d.arc(caja(gx - 12, by - 12, gx + 12, by + 12), 20, 160, fill=BLANCO, width=s(3))

    # miniatura de la última foto (abajo a la izquierda)
    mx, my, ml = 36, by - 24, 48
    d.rounded_rectangle(caja(mx, my, mx + ml, my + ml), radius=s(8), fill=(40, 40, 42))
    if t >= T_FLASH:
        q = suave(tramo(t, T_FLASH + 0.1, T_FLASH + 0.6))
        # la foto vuela desde el visor hasta la miniatura
        w0, h0 = PANT_W, VISOR_Y1 - VISOR_Y0
        x = 0 + (mx - 0) * q
        y = VISOR_Y0 + (my - VISOR_Y0) * q
        w = w0 + (ml - w0) * q
        h = h0 + (ml - h0) * q
        mini = visor.resize((s(w), s(h)), Image.LANCZOS)
        if q < 1:
            borde = Image.new("RGBA", (mini.width + s(6), mini.height + s(6)), BLANCO + (255,))
            borde.alpha_composite(mini, (s(3), s(3)))
            mini = borde
        p.alpha_composite(mini, (s(x), s(y)))

    # destello blanco del disparo
    if T_FLASH <= t < T_FLASH + 0.35:
        a = int(255 * (1 - tramo(t, T_FLASH, T_FLASH + 0.35)))
        p.alpha_composite(Image.new("RGBA", p.size, (255, 255, 255, a)))

    barra_inicio(ImageDraw.Draw(p))
    escala, alfa = entrada_pop(t)
    return montar(fondo, telefono_con_pantalla(p), escala, alfa=alfa)


# ---------------------------------------------------------------- 2) veloz

COLS, FILAS = 4, 5
ICONO, MARGEN_X, ARRIBA, PASO_Y = 54, 24, 70, 86


def pos_icono(i):
    paso_x = (PANT_W - 2 * MARGEN_X - ICONO) / (COLS - 1)
    return MARGEN_X + (i % COLS) * paso_x, ARRIBA + (i // COLS) * PASO_Y


def inicio_apps(cache):
    if "inicio" not in cache:
        p = fondo_degradado()
        d = ImageDraw.Draw(p)
        for i in range(COLS * FILAS):
            x, y = pos_icono(i)
            d.rounded_rectangle(caja(x, y, x + ICONO, y + ICONO), radius=s(13), fill=COLORES_APPS[i % len(COLORES_APPS)])
            d.rounded_rectangle(caja(x + 8, y + ICONO + 7, x + ICONO - 8, y + ICONO + 11), radius=s(2),
                                fill=(225, 215, 240))
        # dock (capa aparte: dibujar con alfa directo dejaría la pantalla transparente)
        capa = Image.new("RGBA", p.size, (0, 0, 0, 0))
        ImageDraw.Draw(capa).rounded_rectangle(caja(10, PANT_H - 108, PANT_W - 10, PANT_H - 30), radius=s(30),
                                               fill=(255, 255, 255, 70))
        p.alpha_composite(capa)
        d = ImageDraw.Draw(p)
        for j, c in enumerate((AZUL_IOS, (255, 59, 48), (255, 149, 0), (88, 86, 214))):
            x = MARGEN_X + j * (PANT_W - 2 * MARGEN_X - ICONO) / 3
            d.rounded_rectangle(caja(x, PANT_H - 96, x + ICONO, PANT_H - 96 + ICONO), radius=s(13), fill=c)
        barra_inicio(d)
        cache["inicio"] = p
    return cache["inicio"]


def app_abierta(color):
    """Contenido genérico de una app: barra de color y renglones."""
    p = pantalla_vacia((248, 248, 250))
    d = ImageDraw.Draw(p)
    d.rectangle(caja(0, 0, PANT_W, 120), fill=color)
    d.rounded_rectangle(caja(20, 70, 170, 96), radius=s(6), fill=mezclar(color, BLANCO, 0.85))
    for k in range(6):
        y = 150 + k * 78
        d.rounded_rectangle(caja(20, y, 76, y + 56), radius=s(10), fill=mezclar(color, BLANCO, 0.6))
        d.rounded_rectangle(caja(90, y + 8, PANT_W - 30, y + 22), radius=s(5), fill=(200, 200, 208))
        d.rounded_rectangle(caja(90, y + 32, PANT_W - 90, y + 44), radius=s(5), fill=(222, 222, 228))
    barra_inicio(d, (30, 30, 30))
    return p


APERTURAS = [(1.0, 5), (1.75, 10), (2.5, 2), (3.25, 13)]   # (momento, ícono)
ABRE, QUEDA, CIERRA = 0.18, 0.32, 0.16


def lineas_velocidad(t, x_tel, alfa):
    def dibujar(lienzo):
        if alfa <= 0:
            return
        capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        W, H = lienzo.size
        for k in range(14):
            y = H / 2 + (k - 6.5) * s(52) + s(9) * math.sin(k * 7.3)
            largo = s(260 + 180 * ((k * 37) % 5) / 4)
            fin = x_tel - s(TEL_W / 2) + s(40) - s(30 * ((k * 13) % 3))
            ini = fin - largo
            d.rounded_rectangle((ini, y - s(4), fin, y + s(4)), radius=s(4),
                                fill=(255, 255, 255, int(200 * alfa)))
        lienzo.alpha_composite(capa)
    return dibujar


def clip_veloz(t, fondo, cache):
    p = inicio_apps(cache).copy()

    for t0, icono in APERTURAS:
        if t0 <= t < t0 + ABRE + QUEDA + CIERRA:
            if t < t0 + ABRE:
                q = suave(tramo(t, t0, t0 + ABRE))
            elif t < t0 + ABRE + QUEDA:
                q = 1.0
            else:
                q = 1 - suave(tramo(t, t0 + ABRE + QUEDA, t0 + ABRE + QUEDA + CIERRA))
            color = COLORES_APPS[icono % len(COLORES_APPS)]
            ix, iy = pos_icono(icono)
            x0, y0 = ix * (1 - q), iy * (1 - q)
            w = ICONO + (PANT_W - ICONO) * q
            h = ICONO + (PANT_H - ICONO) * q
            key = ("app", icono)
            if key not in cache:
                cache[key] = app_abierta(color)
            ventana = cache[key].resize((max(s(w), 1), max(s(h), 1)), Image.LANCZOS)
            # mientras se agranda, se ve el color del ícono que se va transformando en la app
            tapa = Image.new("RGBA", ventana.size, color + (int(255 * (1 - q) ** 0.6),))
            ventana.alpha_composite(tapa)
            m = Image.new("L", ventana.size, 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, ventana.width - 1, ventana.height - 1),
                                                radius=s(13 + 27 * q), fill=255)
            p.paste(ventana, (s(x0), s(y0)), m)

    # entra desde la izquierda a toda velocidad y frena con un rebote
    q = tramo(t, 0, 0.45)
    if q < 1:
        dx = -s(1400) * (1 - ease_out_back(q))
    else:
        dx = 0
    x_tel = s(ANCHO) / 2 + dx
    alfa_lineas = 1 - tramo(t, 0.35, 0.8)
    extra = lineas_velocidad(t, x_tel, alfa_lineas)
    return montar(fondo, telefono_con_pantalla(p), dx=dx, extra=extra)


# ---------------------------------------------------------------- 3) actualizaciones

GRIS_FONDO = (242, 242, 247)


def engranaje(d, cx, cy, r, ang, color, fondo):
    puntos = []
    dientes = 9
    for k in range(dientes * 4):
        a = ang + k * (2 * math.pi / (dientes * 4))
        rad = r if (k % 4) in (1, 2) else r * 0.78
        puntos.append((s(cx + rad * math.cos(a)), s(cy + rad * math.sin(a))))
    d.polygon(puntos, fill=color)
    ri = r * 0.34
    d.ellipse(caja(cx - ri, cy - ri, cx + ri, cy + ri), fill=fondo)


def clip_actualizacion(t, fondo, cache):
    T_INI, T_FIN, T_LISTO = 0.9, 4.0, 4.3
    p = pantalla_vacia(GRIS_FONDO)
    d = ImageDraw.Draw(p)
    texto_ajustado(d, (PANT_W / 2, 66), "Actualización de software", 19, PANT_W - 40, True,
                   fill=(0, 0, 0), anchor="mm")
    d.line(caja(0, 92, PANT_W, 92), fill=(210, 210, 215), width=s(1))

    cx, cy = PANT_W / 2, 250
    progreso = suave(tramo(t, T_INI, T_FIN))
    if t < T_LISTO:
        giro = t * 1.6 if t >= T_INI else 0
        engranaje(d, cx, cy, 72, giro, (142, 142, 147), GRIS_FONDO)
        if t < T_INI:
            estado = "Hay una actualización disponible"
        elif progreso < 0.55:
            estado = "Descargando…"
        else:
            estado = "Instalando…"
        texto_ajustado(d, (PANT_W / 2, 380), estado, 18, PANT_W - 40, True, fill=(30, 30, 30), anchor="mm")
        # barra de progreso
        bx0, bx1, by = 40, PANT_W - 40, 420
        d.rounded_rectangle(caja(bx0, by, bx1, by + 10), radius=s(5), fill=(214, 214, 220))
        if progreso > 0:
            d.rounded_rectangle(caja(bx0, by, bx0 + max((bx1 - bx0) * progreso, 10), by + 10), radius=s(5),
                                fill=AZUL_IOS)
        d.text((s(PANT_W / 2), s(by + 34)), f"{int(round(progreso * 100))}%", font=fuente(16),
               fill=(110, 110, 115), anchor="mm")
    else:
        # tilde azul que aparece con rebote
        e = ease_out_back(tramo(t, T_LISTO, T_LISTO + 0.4))
        r = 70 * e
        d.ellipse(caja(cx - r, cy - r, cx + r, cy + r), fill=AZUL_IOS)
        if e > 0.3:
            k = r / 70
            d.line([(s(cx - 30 * k), s(cy + 2 * k)), (s(cx - 8 * k), s(cy + 24 * k)), (s(cx + 32 * k), s(cy - 22 * k))],
                   fill=BLANCO, width=s(12 * k), joint="curve")
        alfa = int(255 * tramo(t, T_LISTO + 0.15, T_LISTO + 0.45))
        capa = Image.new("RGBA", p.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(capa)
        texto_ajustado(dc, (PANT_W / 2, 380), "Tu iPhone está actualizado", 19, PANT_W - 36, True,
                       fill=(0, 0, 0, alfa), anchor="mm")
        texto_ajustado(dc, (PANT_W / 2, 410), "Ya tenés la última versión de iOS", 15, PANT_W - 36,
                       fill=(110, 110, 115, alfa), anchor="mm")
        p.alpha_composite(capa)

    barra_inicio(ImageDraw.Draw(p), (30, 30, 30))
    escala, alfa = entrada_pop(t)
    return montar(fondo, telefono_con_pantalla(p), escala, alfa=alfa)


# ---------------------------------------------------------------- exportar

def exportar(fn, salida, fondo, duracion):
    if fondo:
        codec = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                 "-movflags", "+faststart"]
    else:
        codec = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"]
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{ANCHO}x{ALTO}", "-r", str(FPS), "-i", "-", *codec, salida],
        stdin=subprocess.PIPE,
    )
    cache = {}
    for i in range(int(duracion * FPS)):
        ff.stdin.write(fn(i / FPS, fondo, cache).tobytes())
    ff.stdin.close()
    ff.wait()


CLIPS = [
    ("iphone13_foto", clip_foto, 4.5),
    ("iphone13_veloz", clip_veloz, 4.5),
    ("iphone13_actualizacion", clip_actualizacion, 6.0),
]


def main():
    for nombre, fn, dur in CLIPS:
        exportar(fn, f"{nombre}_fondo_verde.mp4", FONDO_VERDE, dur)
        exportar(fn, f"{nombre}_transparente.mov", None, dur)


if __name__ == "__main__":
    main()
