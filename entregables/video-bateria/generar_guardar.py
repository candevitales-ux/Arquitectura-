"""Genera un clip de un cursor haciendo click en el ícono de guardar (marcador) que se rellena.

Genera:
  - .mp4 con fondo verde liso (fácil de borrar en el editor)
  - .mov ProRes 4444 con fondo transparente

Uso:
    python3 generar_guardar.py

Requiere Pillow y ffmpeg. Reutiliza el cursor y los tiempos de generar_boton_seguir.py.
"""
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter

from generar_boton_seguir import (
    ALTO, ANCHO, BLANCO, DURACION, FONDO_VERDE, FPS, SS,
    T_PRESIONA, T_SUELTA, T_LLEGA_FIN, cursor, posicion_cursor, suave, tramo,
)

ICONO_W, ICONO_H = 200, 254
GROSOR = 20
T_REBOTE = 2.0


def marcador(relleno):
    """Ícono de guardar (marcador) blanco, con sombra suave para que se lea sobre cualquier fondo."""
    m = 40 * SS
    w, h = ICONO_W * SS, ICONO_H * SS
    g = GROSOR * SS
    pts = [(m, m), (m + w, m), (m + w, m + h), (m + w / 2, m + h - w * 0.42), (m, m + h), (m, m)]
    img = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))

    def trazar(d, color):
        if relleno:
            d.polygon(pts[:-1], fill=color)
        d.line(pts + [pts[1]], fill=color, width=g, joint="curve")
        for x, y in pts[:-1]:
            d.ellipse((x - g / 2, y - g / 2, x + g / 2, y + g / 2), fill=color)

    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    trazar(ImageDraw.Draw(sombra), (0, 0, 0, 90))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(10 * SS)), (0, 4 * SS))
    trazar(ImageDraw.Draw(img), BLANCO + (255,))
    return img


def escala_icono(t):
    if t < T_LLEGA_FIN:
        return 1.0
    if t < T_PRESIONA:
        return 1 - 0.15 * suave(tramo(t, T_LLEGA_FIN, T_PRESIONA))
    if t < T_SUELTA:
        return 0.85
    if t < T_REBOTE:
        # salta más grande y se asienta, como el "pop" de la app
        p = tramo(t, T_SUELTA, T_REBOTE)
        return 1 - 0.15 * (1 - p) ** 2 * math.cos(p * math.pi * 2.2) + 0.1 * math.sin(p * math.pi) * (1 - p)
    return 1.0


def cuadro(t, fondo, vacio, lleno, img_cursor):
    W, H = ANCHO * SS, ALTO * SS
    lienzo = Image.new("RGBA", (W, H), fondo + (255,) if fondo else (0, 0, 0, 0))
    cx, cy = W // 2, H // 2

    ic = lleno if t >= T_SUELTA else vacio
    e = escala_icono(t)
    iw, ih = int(ic.width * e), int(ic.height * e)
    lienzo.alpha_composite(ic.resize((iw, ih), Image.LANCZOS), (cx - iw // 2, cy - ih // 2))

    # onda del click
    if T_PRESIONA <= t < T_PRESIONA + 0.45:
        p = tramo(t, T_PRESIONA, T_PRESIONA + 0.45)
        px, py = posicion_cursor(T_PRESIONA, cx / SS, cy / SS)
        r = (20 + 70 * suave(p)) * SS
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(capa).ellipse((px * SS - r, py * SS - r, px * SS + r, py * SS + r),
                                     outline=(255, 255, 255, int(220 * (1 - p))), width=6 * SS)
        lienzo.alpha_composite(capa)

    px, py = posicion_cursor(t, cx / SS, cy / SS)
    ec = 0.88 if T_PRESIONA - 0.05 <= t < T_SUELTA else 1.0
    c = img_cursor if ec == 1 else img_cursor.resize(
        (int(img_cursor.width * ec), int(img_cursor.height * ec)), Image.LANCZOS)
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
    imgs = marcador(False), marcador(True), cursor()
    for i in range(int(DURACION * FPS)):
        ff.stdin.write(cuadro(i / FPS, fondo, *imgs).tobytes())
    ff.stdin.close()
    ff.wait()


def main():
    exportar("guardar_video_fondo_verde.mp4", FONDO_VERDE)
    exportar("guardar_video_transparente.mov", None)


if __name__ == "__main__":
    main()
