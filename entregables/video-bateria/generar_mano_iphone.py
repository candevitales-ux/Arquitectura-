"""Genera un clip ilustrado de una mano mostrando un iPhone 13: entra, muestra el frente,
lo gira para mostrar el dorso y vuelve al frente.

Genera:
  - .mp4 con fondo verde liso (fácil de borrar en el editor)
  - .mov ProRes 4444 con fondo transparente

Uso:
    python3 generar_mano_iphone.py

Requiere Pillow y ffmpeg.
"""
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 30
DURACION = 7.0
ANCHO, ALTO = 1920, 1080
SS = 2

FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FUENTE_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FONDO_VERDE = (0, 177, 64)

# iPhone 13 (146,7 x 71,5 mm), color azul
TEL_W, TEL_H = 340, 698
MARCO = (52, 92, 132)
MARCO_BRILLO = (88, 128, 168)
DORSO = (36, 78, 120)
NEGRO = (8, 8, 10)

PIEL = (234, 186, 152)
PIEL_SOMBRA = (205, 152, 118)
UNA = (246, 214, 196)

# lienzo de la mano + teléfono (en coordenadas sin supersampling)
LW, LH = 760, 1240
TX, TY = (LW - TEL_W) // 2, 90          # esquina del teléfono dentro del lienzo


def s(v):
    return int(v * SS)


def caja(x0, y0, x1, y1):
    return (s(x0), s(y0), s(x1), s(y1))


def capsula(d, p0, p1, grosor, color):
    """Dedo: un segmento con extremos redondeados."""
    d.line((s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])), fill=color, width=s(grosor))
    for x, y in (p0, p1):
        r = grosor / 2
        d.ellipse(caja(x - r, y - r, x + r, y + r), fill=color)


def una(d, punta, base, grosor):
    """Uña cerca de la punta del dedo, orientada según el dedo."""
    dx, dy = punta[0] - base[0], punta[1] - base[1]
    largo = math.hypot(dx, dy)
    ux, uy = dx / largo, dy / largo
    cx, cy = punta[0] - ux * grosor * 0.35, punta[1] - uy * grosor * 0.35
    r = grosor * 0.28
    d.ellipse(caja(cx - r, cy - r, cx + r, cy + r), fill=UNA)


def telefono_frente():
    img = Image.new("RGBA", (s(TEL_W), s(TEL_H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radio = 58
    d.rounded_rectangle(caja(0, 0, TEL_W - 1, TEL_H - 1), radius=s(radio), fill=MARCO)
    d.rounded_rectangle(caja(3, 3, TEL_W - 4, TEL_H - 4), radius=s(radio - 3), outline=MARCO_BRILLO, width=s(2))
    d.rounded_rectangle(caja(7, 7, TEL_W - 8, TEL_H - 8), radius=s(radio - 7), fill=NEGRO)

    # pantalla de bloqueo con fondo degradado
    bx0, by0, bx1, by1 = 18, 18, TEL_W - 19, TEL_H - 19
    pw, ph = s(bx1 - bx0), s(by1 - by0)
    fondo = Image.new("RGBA", (pw, ph))
    fd = ImageDraw.Draw(fondo)
    for y in range(ph):
        t = y / ph
        c = (int(40 + 90 * t), int(70 + 20 * t), int(170 - 40 * t), 255)
        fd.line((0, y, pw, y), fill=c)
    mascara = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=s(radio - 18), fill=255)
    img.paste(fondo, (s(bx0), s(by0)), mascara)

    # notch
    nw, nh = 130, 30
    d.rounded_rectangle(caja((TEL_W - nw) / 2, 10, (TEL_W + nw) / 2, 18 + nh), radius=s(16), fill=NEGRO)
    d.ellipse(caja(TEL_W / 2 + 34, 22, TEL_W / 2 + 44, 32), fill=(30, 34, 50))

    # hora y fecha
    d.text((s(TEL_W / 2), s(150)), "9:41", font=ImageFont.truetype(FUENTE_BOLD, s(84)),
           fill=(255, 255, 255), anchor="mm")
    d.text((s(TEL_W / 2), s(92)), "lunes 26 de octubre", font=ImageFont.truetype(FUENTE, s(19)),
           fill=(235, 235, 245), anchor="mm")
    # barra de inicio
    d.rounded_rectangle(caja(TEL_W / 2 - 62, TEL_H - 36, TEL_W / 2 + 62, TEL_H - 30), radius=s(3),
                        fill=(255, 255, 255))
    return img


def telefono_dorso():
    img = Image.new("RGBA", (s(TEL_W), s(TEL_H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radio = 58
    d.rounded_rectangle(caja(0, 0, TEL_W - 1, TEL_H - 1), radius=s(radio), fill=MARCO)
    d.rounded_rectangle(caja(7, 7, TEL_W - 8, TEL_H - 8), radius=s(radio - 7), fill=DORSO)
    # reflejo diagonal suave del vidrio
    brillo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(brillo).polygon([(s(TEL_W * 0.55), 0), (s(TEL_W), 0), (s(TEL_W), s(TEL_H * 0.25)),
                                    (s(TEL_W * 0.1), s(TEL_H * 0.75)), (0, s(TEL_H * 0.75)), (0, s(TEL_H * 0.6))],
                                   fill=(255, 255, 255, 18))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(caja(7, 7, TEL_W - 8, TEL_H - 8), radius=s(radio - 7), fill=255)
    img.paste(Image.alpha_composite(img, brillo), (0, 0), m)
    d = ImageDraw.Draw(img)

    # módulo de cámaras arriba a la izquierda, lentes en diagonal
    mx, my, mt = 24, 24, 150
    d.rounded_rectangle(caja(mx, my, mx + mt, my + mt), radius=s(36), fill=(60, 102, 145),
                        outline=(80, 120, 160), width=s(2))
    for cx, cy in ((mx + 44, my + 44), (mx + mt - 44, my + mt - 44)):
        d.ellipse(caja(cx - 33, cy - 33, cx + 33, cy + 33), fill=(28, 30, 36))
        d.ellipse(caja(cx - 24, cy - 24, cx + 24, cy + 24), fill=NEGRO)
        d.ellipse(caja(cx - 14, cy - 14, cx + 14, cy + 14), fill=(22, 30, 58))
        d.ellipse(caja(cx - 9, cy - 11, cx - 1, cy - 3), fill=(120, 140, 200))
    # flash y micrófono
    fx, fy = mx + mt - 40, my + 40
    d.ellipse(caja(fx - 13, fy - 13, fx + 13, fy + 13), fill=(240, 232, 205))
    d.ellipse(caja(mx + 40, my + mt - 42, mx + 48, my + mt - 34), fill=(25, 30, 40))
    return img


def antebrazo(d, x):
    """Antebrazo que sale por abajo del cuadro; x es el centro de la muñeca."""
    d.polygon([(s(x - 95), s(TY + 600)), (s(x + 95), s(TY + 600)),
               (s(x + 125), s(LH)), (s(x - 115), s(LH))], fill=PIEL_SOMBRA)


def mano_detras():
    """Partes de la mano que quedan detrás del teléfono (vista de frente): antebrazo y palma."""
    img = Image.new("RGBA", (s(LW), s(LH)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    antebrazo(d, TX + TEL_W * 0.62)
    # palma detrás de la mitad baja; asoma un poco por la izquierda, donde nacen los dedos
    d.rounded_rectangle(caja(TX - 46, TY + 290, TX + TEL_W + 20, TY + 690), radius=s(110), fill=PIEL)
    return img


def mano_delante():
    """Dedos que rodean el borde izquierdo y pulgar sobre el borde derecho (vista de frente)."""
    img = Image.new("RGBA", (s(LW), s(LH)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, y in enumerate((318, 378, 438, 498)):
        g = 50 - i * 3
        base = (TX - 30, TY + y + 12)
        punta = (TX + 16, TY + y)
        capsula(d, base, punta, g, PIEL)
        una(d, punta, base, g)
    # pliegues entre dedos
    for y in (348, 408, 468):
        d.line(caja(TX - 50, TY + y, TX - 8, TY + y - 4), fill=PIEL_SOMBRA, width=s(3))
    # pulgar: nace en la base de la mano (abajo a la derecha) y se apoya sobre el borde
    d.ellipse(caja(TX + TEL_W - 60, TY + 520, TX + TEL_W + 60, TY + 720), fill=PIEL)
    base = (TX + TEL_W + 10, TY + 590)
    punta = (TX + TEL_W - 26, TY + 430)
    capsula(d, base, punta, 58, PIEL)
    una(d, punta, base, 58)
    d.arc(caja(TX + TEL_W - 50, TY + 560, TX + TEL_W + 30, TY + 680), 110, 200, fill=PIEL_SOMBRA, width=s(3))
    return img


def mano_dorso_delante():
    """Vista de atrás: la palma y los dedos quedan delante del dorso del teléfono."""
    img = Image.new("RGBA", (s(LW), s(LH)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    antebrazo(d, TX + TEL_W * 0.38)
    # dedos: salen de la palma y cruzan hacia el borde derecho, donde lo rodean
    for i, y in enumerate((318, 378, 438, 498)):
        g = 54 - i * 3
        # contorno apenas más oscuro para separar un dedo del otro
        capsula(d, (TX + 150, TY + y + 70), (TX + TEL_W + 8, TY + y + 10), g + 4, PIEL_SOMBRA)
        capsula(d, (TX + 150, TY + y + 70), (TX + TEL_W + 8, TY + y + 10), g, PIEL)
    # palma y eminencia del pulgar abajo a la izquierda
    d.rounded_rectangle(caja(TX - 20, TY + 470, TX + TEL_W - 40, TY + 700), radius=s(110), fill=PIEL)
    d.ellipse(caja(TX - 60, TY + 500, TX + 90, TY + 720), fill=PIEL)
    d.arc(caja(TX + 30, TY + 500, TX + 240, TY + 660), 200, 330, fill=PIEL_SOMBRA, width=s(4))
    return img


def mano_dorso_detras():
    """Vista de atrás: el pulgar queda del lado de la pantalla, no se ve."""
    return Image.new("RGBA", (s(LW), s(LH)), (0, 0, 0, 0))


def componer(detras, telefono, delante):
    img = Image.new("RGBA", (s(LW), s(LH)), (0, 0, 0, 0))
    # sombra suave para que se lea sobre cualquier fondo
    silueta = detras.copy()
    silueta.alpha_composite(telefono, (s(TX), s(TY)))
    silueta.alpha_composite(delante)
    sombra = Image.new("RGBA", silueta.size, (0, 0, 0, 0))
    sombra.putalpha(silueta.getchannel("A").point(lambda v: v * 70 // 255))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(s(14))), (s(8), s(12)))
    img.alpha_composite(silueta)
    return img


def suave(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t) ** 3


def angulo_giro(t):
    """0 = frente, 180 = dorso, 360 = frente de nuevo."""
    if t < 2.4:
        return 0
    if t < 3.4:
        return 180 * suave((t - 2.4) / 1.0)
    if t < 4.8:
        return 180
    if t < 5.8:
        return 180 + 180 * suave((t - 4.8) / 1.0)
    return 360


def cuadro(t, fondo, frente, dorso):
    W, H = s(ANCHO), s(ALTO)
    lienzo = Image.new("RGBA", (W, H), fondo + (255,) if fondo else (0, 0, 0, 0))

    ang = math.radians(angulo_giro(t))
    vista = frente if math.cos(ang) >= 0 else dorso
    ex = max(abs(math.cos(ang)), 0.02)
    img = vista.resize((max(int(vista.width * ex), 1), vista.height), Image.LANCZOS)
    if ex < 0.999:
        # se oscurece un poco al quedar de canto
        oscuro = Image.new("RGBA", img.size, (0, 0, 0, int(90 * (1 - ex))))
        oscuro.putalpha(img.getchannel("A").point(lambda v: v * int(90 * (1 - ex)) // 255))
        img.alpha_composite(oscuro)

    # entra desde abajo y después se balancea apenas
    entrada = ease_out(t / 1.0)
    dy = (1 - entrada) * s(1100)
    inclinacion = 2.0 * math.sin(t * 1.6) * entrada
    flote = math.sin(t * 2.1) * s(6) * entrada
    img = img.rotate(inclinacion, resample=Image.BICUBIC, expand=True)

    x = (W - img.width) // 2
    y = int(H - img.height + s(150) + dy + flote)
    lienzo.alpha_composite(img, (x, y))
    return lienzo.resize((ANCHO, ALTO), Image.LANCZOS)


def exportar(salida, fondo, frente, dorso):
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
        ff.stdin.write(cuadro(i / FPS, fondo, frente, dorso).tobytes())
    ff.stdin.close()
    ff.wait()


def vistas():
    frente = componer(mano_detras(), telefono_frente(), mano_delante())
    dorso = componer(mano_dorso_detras(), telefono_dorso(), mano_dorso_delante())
    return frente, dorso


def main():
    frente, dorso = vistas()
    exportar("mano_iphone13_fondo_verde.mp4", FONDO_VERDE, frente, dorso)
    exportar("mano_iphone13_transparente.mov", None, frente, dorso)


if __name__ == "__main__":
    main()
