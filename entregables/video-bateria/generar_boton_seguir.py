"""Genera un clip de un cursor haciendo click en un botón "Seguir" que pasa a "Siguiendo".

Genera:
  - .mp4 con fondo verde liso (fácil de borrar en el editor)
  - .mov ProRes 4444 con fondo transparente

Uso:
    python3 generar_boton_seguir.py

Requiere Pillow y ffmpeg.
"""
import math
import subprocess

from PIL import Image, ImageDraw, ImageFont

FPS = 30
DURACION = 4.0
ANCHO, ALTO = 1920, 1080
SS = 2               # supersampling para bordes suaves

FUENTE = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

FONDO_VERDE = (0, 177, 64)
AZUL = (0, 149, 246)
GRIS = (239, 239, 239)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

BOTON_W, BOTON_H = 560, 150
RADIO = 30

# tiempos (segundos)
T_LLEGA_INI, T_LLEGA_FIN = 0.4, 1.3     # el cursor viaja hasta el botón
T_PRESIONA = 1.45                       # el botón se hunde
T_SUELTA = 1.55                         # se suelta y cambia a "Siguiendo"
T_REBOTE = 1.9
T_SALE_INI, T_SALE_FIN = 2.4, 3.1       # el cursor se aleja


def suave(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)


def tramo(t, a, b):
    return min(max((t - a) / (b - a), 0), 1)


def boton(siguiendo):
    w, h = BOTON_W * SS, BOTON_H * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=RADIO * SS, fill=GRIS if siguiendo else AZUL)
    fuente = ImageFont.truetype(FUENTE, 64 * SS)
    texto = "Siguiendo" if siguiendo else "Seguir"
    color = NEGRO if siguiendo else BLANCO
    tw = d.textlength(texto, font=fuente)
    chevron = 34 * SS if siguiendo else 0
    hueco = 22 * SS if siguiendo else 0
    x = (w - tw - hueco - chevron) / 2
    d.text((x, h / 2), texto, font=fuente, fill=color, anchor="lm")
    if siguiendo:
        cx = x + tw + hueco + chevron / 2
        cy = h / 2 + 2 * SS
        a = chevron / 2
        d.line([(cx - a, cy - a / 2), (cx, cy + a / 2), (cx + a, cy - a / 2)],
               fill=color, width=7 * SS, joint="curve")
    return img


def cursor():
    """Flecha de mouse clásica: blanca con borde negro."""
    s = 4 * SS
    pts = [(0, 0), (0, 34), (8, 26), (14, 40), (19, 38), (13, 25), (24, 25)]
    pts = [(x * s + 8 * SS, y * s + 8 * SS) for x, y in pts]
    img = Image.new("RGBA", (int(40 * s), int(50 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=BLANCO, outline=NEGRO, width=3 * SS)
    return img


def escala_boton(t):
    if t < T_LLEGA_FIN:
        return 1.0
    if t < T_PRESIONA:
        return 1 - 0.08 * suave(tramo(t, T_LLEGA_FIN, T_PRESIONA))
    if t < T_SUELTA:
        return 0.92
    if t < T_REBOTE:
        # vuelve con un pequeño rebote
        p = tramo(t, T_SUELTA, T_REBOTE)
        return 1 - 0.08 * (1 - p) ** 2 * math.cos(p * math.pi * 2)
    return 1.0


def posicion_cursor(t, cx, cy):
    inicio = (cx + 520, cy + 380)
    destino = (cx + 60, cy + 10)
    final = (cx + 380, cy + 300)
    if t < T_SALE_INI:
        p = suave(tramo(t, T_LLEGA_INI, T_LLEGA_FIN))
        a, b = inicio, destino
    else:
        p = suave(tramo(t, T_SALE_INI, T_SALE_FIN))
        a, b = destino, final
    return a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p


def cuadro(t, fondo, img_seguir, img_siguiendo, img_cursor):
    W, H = ANCHO * SS, ALTO * SS
    lienzo = Image.new("RGBA", (W, H), fondo + (255,) if fondo else (0, 0, 0, 0))
    cx, cy = W // 2, H // 2

    b = img_siguiendo if t >= T_SUELTA else img_seguir
    e = escala_boton(t)
    bw, bh = int(b.width * e), int(b.height * e)
    lienzo.alpha_composite(b.resize((bw, bh), Image.LANCZOS), (cx - bw // 2, cy - bh // 2))

    # onda del click
    if T_PRESIONA <= t < T_PRESIONA + 0.45:
        p = tramo(t, T_PRESIONA, T_PRESIONA + 0.45)
        px, py = posicion_cursor(T_PRESIONA, cx / SS, cy / SS)
        r = (20 + 70 * suave(p)) * SS
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(capa).ellipse((px * SS - r, py * SS - r, px * SS + r, py * SS + r),
                                     outline=(255, 255, 255, int(220 * (1 - p))), width=6 * SS)
        lienzo.alpha_composite(capa)

    # cursor (se achica un poco al presionar)
    px, py = posicion_cursor(t, cx / SS, cy / SS)
    ec = 0.88 if T_LLEGA_FIN <= t < T_SUELTA and t >= T_PRESIONA - 0.05 else 1.0
    c = img_cursor if ec == 1 else img_cursor.resize((int(img_cursor.width * ec), int(img_cursor.height * ec)), Image.LANCZOS)
    # el punto de la flecha queda en (px, py)
    lienzo.alpha_composite(c, (int(px * SS - 8 * SS * ec), int(py * SS - 8 * SS * ec)))

    return lienzo.resize((ANCHO, ALTO), Image.LANCZOS)


def exportar(salida, fondo):
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
    imgs = boton(False), boton(True), cursor()
    for i in range(int(DURACION * FPS)):
        ff.stdin.write(cuadro(i / FPS, fondo, *imgs).tobytes())
    ff.stdin.close()
    ff.wait()


def main():
    exportar("boton_seguir_siguiendo_fondo_verde.mp4", FONDO_VERDE)
    exportar("boton_seguir_siguiendo_transparente.mov", None)


if __name__ == "__main__":
    main()
