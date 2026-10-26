"""Genera los recuadros de texto sobre salud de batería como clips de video.

Por cada recuadro genera:
  - .mp4 con fondo azul liso (fácil de borrar en el editor)
  - .mov ProRes 4444 con fondo transparente
  - .png transparente (imagen fija)

Uso:
    python3 generar_recuadros.py

Requiere Pillow y ffmpeg.
"""
import subprocess

from PIL import Image, ImageDraw, ImageFont

FPS = 30
ENTRADA = 0.5        # segundos de la animación de aparición
DURACION = 5.0       # duración total del clip
ANCHO, ALTO = 1920, 1080
SS = 2               # supersampling para bordes suaves

FUENTE_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FONDO_AZUL = (0, 71, 187)
CAJA = (24, 24, 30)
BLANCO = (245, 245, 245)

RECUADROS = [
    ("recuadro_1_arriba_85", "Arriba de 85% de batería", "Te va a andar bien", (52, 199, 89), 92),
    ("recuadro_2_entre_80_85", "Entre 80% y 85% de batería", "Se nota el desgaste", (245, 190, 40), 82),
    ("recuadro_3_debajo_80", "Debajo de 80%", "Apple recomienda cambio", (235, 64, 52), 70),
]


def dibujar_bateria(d, x, y, w, h, pct, color):
    borde = int(h * 0.09)
    d.rounded_rectangle((x, y, x + w, y + h), radius=int(h * 0.22), outline=BLANCO, width=borde)
    tw, th = int(h * 0.14), int(h * 0.42)
    d.rounded_rectangle((x + w + borde, y + (h - th) // 2, x + w + borde + tw, y + (h + th) // 2),
                        radius=tw // 2, fill=BLANCO)
    m = borde * 2
    largo = int((w - 2 * m) * pct / 100)
    d.rounded_rectangle((x + m, y + m, x + m + largo, y + h - m), radius=int(h * 0.1), fill=color)


def recuadro(titulo, texto, color, pct, ancho_texto_min=0):
    """Dibuja el recuadro sobre un lienzo transparente del tamaño justo."""
    f_titulo = ImageFont.truetype(FUENTE_BOLD, 58 * SS)
    f_texto = ImageFont.truetype(FUENTE, 76 * SS)
    pad = 44 * SS
    bat_w, bat_h = 190 * SS, 96 * SS
    sep = 60 * SS

    medir = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bt = medir.textbbox((0, 0), titulo, font=f_titulo)
    bx = medir.textbbox((0, 0), texto, font=f_texto)
    ancho_texto = max(bt[2] - bt[0], bx[2] - bx[0], ancho_texto_min)
    entre = 10 * SS
    # alturas por métrica de la fuente (no por el texto) para que todos los recuadros midan igual
    alto_titulo = sum(f_titulo.getmetrics())
    alto_texto = alto_titulo + entre + sum(f_texto.getmetrics())

    barra = 18 * SS
    w = barra + pad + bat_w + 30 * SS + sep + ancho_texto + pad
    h = max(alto_texto, bat_h) + 2 * pad
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radio = 40 * SS
    # caja con borde de color y franja lateral
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radio, fill=color)
    d.rounded_rectangle((barra, 6 * SS, w - 1 - 6 * SS, h - 1 - 6 * SS), radius=radio - 6 * SS, fill=CAJA)

    x = barra + pad
    dibujar_bateria(d, x, (h - bat_h) // 2, bat_w, bat_h, pct, color)

    tx = x + bat_w + 30 * SS + sep
    ty = (h - alto_texto) // 2
    d.text((tx - bt[0], ty), titulo, font=f_titulo, fill=color, anchor="la")
    d.text((tx - bx[0], ty + alto_titulo + entre), texto, font=f_texto, fill=BLANCO, anchor="la")

    return img.resize((w // SS, h // SS), Image.LANCZOS)


def ease_out_back(t):
    c = 1.4
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def cuadro(caja, t, fondo):
    lienzo = Image.new("RGBA", (ANCHO, ALTO), fondo + (255,) if fondo else (0, 0, 0, 0))
    avance = min(t / ENTRADA, 1)
    escala = max(ease_out_back(avance), 0.01)
    w, h = max(int(caja.width * escala), 1), max(int(caja.height * escala), 1)
    c = caja.resize((w, h), Image.LANCZOS)
    if avance < 1:
        a = c.getchannel("A").point(lambda v: int(v * min(avance * 2, 1)))
        c.putalpha(a)
    lienzo.alpha_composite(c, ((ANCHO - w) // 2, (ALTO - h) // 2))
    return lienzo


def exportar(caja, salida, fondo):
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
    for i in range(int(DURACION * FPS)):
        ff.stdin.write(cuadro(caja, i / FPS, fondo).tobytes())
    ff.stdin.close()
    ff.wait()


def ancho_texto(titulo, texto):
    medir = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    return max(medir.textlength(titulo, font=ImageFont.truetype(FUENTE_BOLD, 58 * SS)),
               medir.textlength(texto, font=ImageFont.truetype(FUENTE, 76 * SS)))


def main():
    # mismo ancho para los tres recuadros, así quedan parejos
    minimo = int(max(ancho_texto(r[1], r[2]) for r in RECUADROS))
    for nombre, titulo, texto, color, pct in RECUADROS:
        caja = recuadro(titulo, texto, color, pct, minimo)
        caja.save(f"{nombre}.png")
        exportar(caja, f"{nombre}_fondo_azul.mp4", FONDO_AZUL)
        exportar(caja, f"{nombre}_transparente.mov", None)


if __name__ == "__main__":
    main()
