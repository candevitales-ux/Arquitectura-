"""Genera un clip de video de un porcentaje de batería subiendo de 0% a 100%.

Uso:
    python3 generar_video_bateria.py [--transparente] [--vertical] [--salida archivo.mp4]

Requiere Pillow y ffmpeg.
"""
import argparse
import subprocess

from PIL import Image, ImageDraw, ImageFont

FPS = 30
DURACION_SUBIDA = 8.0   # segundos que tarda en ir de 0% a 100%
PAUSA_INICIO = 0.5
PAUSA_FINAL = 1.5
SS = 2                  # supersampling para bordes suaves

FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

ROJO = (235, 64, 52)
AMARILLO = (245, 190, 40)
VERDE = (52, 199, 89)


def mezclar(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def color_para(pct):
    # rojo por debajo de 20%, transición a amarillo hasta 50%, luego a verde
    if pct <= 20:
        return ROJO
    if pct <= 50:
        return mezclar(ROJO, AMARILLO, (pct - 20) / 30)
    if pct <= 80:
        return mezclar(AMARILLO, VERDE, (pct - 50) / 30)
    return VERDE


def suavizado(t):
    # ease-in-out: arranca y termina más lento
    return t * t * (3 - 2 * t)


def dibujar_rayo(draw, cx, cy, h, color):
    w = h * 0.55
    puntos = [
        (cx + w * 0.15, cy - h / 2),
        (cx - w * 0.45, cy + h * 0.05),
        (cx - w * 0.02, cy + h * 0.05),
        (cx - w * 0.15, cy + h / 2),
        (cx + w * 0.45, cy - h * 0.05),
        (cx + w * 0.02, cy - h * 0.05),
    ]
    draw.polygon(puntos, fill=color)


def cuadro(pct, ancho, alto, fondo, tiempo):
    W, H = ancho * SS, alto * SS
    img = Image.new("RGBA", (W, H), fondo + (255,) if fondo else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    escala = min(W / 1920, H / 1080) if W > H else W / 1080 * 0.9
    bw, bh = int(760 * escala), int(340 * escala)    # cuerpo de la batería
    borde = int(22 * escala)
    radio = int(56 * escala)
    cx, cy = W // 2, int(H * (0.40 if W > H else 0.42))
    x0, y0 = cx - bw // 2, cy - bh // 2
    x1, y1 = cx + bw // 2, cy + bh // 2

    blanco = (240, 240, 240)
    # cuerpo y terminal
    d.rounded_rectangle((x0, y0, x1, y1), radius=radio, outline=blanco, width=borde)
    tw, th = int(40 * escala), int(130 * escala)
    d.rounded_rectangle((x1 + int(14 * escala), cy - th // 2, x1 + int(14 * escala) + tw, cy + th // 2),
                        radius=int(16 * escala), fill=blanco)

    # relleno
    m = borde + int(16 * escala)
    fx0, fy0, fx1, fy1 = x0 + m, y0 + m, x1 - m, y1 - m
    largo = int((fx1 - fx0) * pct / 100)
    color = color_para(pct)
    if largo > 0:
        r = min(int(30 * escala), largo // 2)
        d.rounded_rectangle((fx0, fy0, fx0 + largo, fy1), radius=r, fill=color)
        # brillo sutil en la parte superior
        brillo = mezclar(color, (255, 255, 255), 0.25)
        d.rounded_rectangle((fx0, fy0, fx0 + largo, fy0 + (fy1 - fy0) // 4), radius=r, fill=brillo)

    # rayo de carga que late mientras carga
    if pct < 100:
        alfa = 0.75 + 0.25 * abs(((tiempo * 1.5) % 2) - 1)
    else:
        alfa = 1.0
    color_rayo = mezclar(fondo or (18, 18, 22), (255, 255, 255), alfa)
    dibujar_rayo(d, cx, cy, int(200 * escala), color_rayo)

    # porcentaje
    fuente = ImageFont.truetype(FUENTE, int(190 * escala))
    texto = f"{int(round(pct))}%"
    caja = d.textbbox((0, 0), texto, font=fuente)
    tx = cx - (caja[2] - caja[0]) // 2 - caja[0]
    ty = y1 + int(70 * escala)
    d.text((tx, ty), texto, font=fuente, fill=color)

    return img.resize((ancho, alto), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transparente", action="store_true",
                    help="fondo transparente (ProRes 4444 .mov, para superponer en el editor)")
    ap.add_argument("--vertical", action="store_true")
    ap.add_argument("--salida", default="bateria_subiendo.mp4")
    args = ap.parse_args()

    ancho, alto = (1080, 1920) if args.vertical else (1920, 1080)
    fondo = None if args.transparente else (18, 18, 22)
    if args.transparente:
        codec = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"]
    else:
        codec = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                 "-movflags", "+faststart"]

    total = int((PAUSA_INICIO + DURACION_SUBIDA + PAUSA_FINAL) * FPS)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{ancho}x{alto}", "-r", str(FPS), "-i", "-",
         *codec, args.salida],
        stdin=subprocess.PIPE,
    )
    for i in range(total):
        t = i / FPS
        avance = min(max((t - PAUSA_INICIO) / DURACION_SUBIDA, 0), 1)
        pct = 100 * suavizado(avance)
        ff.stdin.write(cuadro(pct, ancho, alto, fondo, t).tobytes())
    ff.stdin.close()
    ff.wait()


if __name__ == "__main__":
    main()
