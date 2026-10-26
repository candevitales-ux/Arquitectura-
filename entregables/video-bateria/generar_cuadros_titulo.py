"""Genera los cuadros de título "¿Para quién es ideal?" y "¿A quién no le conviene tanto?".

Mismo estilo y animación que generar_recuadros.py. Por cada cuadro genera:
  - .mp4 con fondo azul liso (fácil de borrar en el editor)
  - .mov ProRes 4444 con fondo transparente
  - .png transparente

Uso:
    python3 generar_cuadros_titulo.py

Requiere Pillow y ffmpeg.
"""
from PIL import Image, ImageDraw, ImageFont

from generar_recuadros import BLANCO, CAJA, FONDO_AZUL, FUENTE_BOLD, SS, exportar

VERDE = (52, 199, 89)
ROJO = (235, 64, 52)

CUADROS = [
    ("cuadro_para_quien_es_ideal", "¿Para quién es ideal?", VERDE, "tilde"),
    ("cuadro_a_quien_no_le_conviene", "¿A quién no le conviene tanto?", ROJO, "cruz"),
]


def icono(d, cx, cy, r, color, tipo):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    g = int(r * 0.22)
    if tipo == "tilde":
        d.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.12, cy + r * 0.36), (cx + r * 0.48, cy - r * 0.34)],
               fill=BLANCO, width=g, joint="curve")
    else:
        a = r * 0.38
        d.line([(cx - a, cy - a), (cx + a, cy + a)], fill=BLANCO, width=g)
        d.line([(cx - a, cy + a), (cx + a, cy - a)], fill=BLANCO, width=g)


def cuadro(titulo, color, tipo, ancho_texto_min=0):
    f = ImageFont.truetype(FUENTE_BOLD, 76 * SS)
    medir = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    ancho_texto = max(medir.textlength(titulo, font=f), ancho_texto_min)
    alto_texto = sum(f.getmetrics())

    pad, barra, r, sep = 44 * SS, 18 * SS, 58 * SS, 46 * SS
    w = int(barra + pad + 2 * r + sep + ancho_texto + pad)
    h = max(alto_texto, 2 * r) + 2 * pad
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radio = 40 * SS
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radio, fill=color)
    d.rounded_rectangle((barra, 6 * SS, w - 1 - 6 * SS, h - 1 - 6 * SS), radius=radio - 6 * SS, fill=CAJA)

    icono(d, barra + pad + r, h // 2, r, color, tipo)
    d.text((barra + pad + 2 * r + sep, (h - alto_texto) // 2), titulo, font=f, fill=BLANCO, anchor="la")
    return img.resize((w // SS, h // SS), Image.LANCZOS)


def main():
    f = ImageFont.truetype(FUENTE_BOLD, 76 * SS)
    medir = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    # mismo ancho para los dos cuadros, así quedan parejos
    minimo = max(medir.textlength(c[1], font=f) for c in CUADROS)
    for nombre, titulo, color, tipo in CUADROS:
        caja = cuadro(titulo, color, tipo, minimo)
        caja.save(f"{nombre}.png")
        exportar(caja, f"{nombre}_fondo_azul.mp4", FONDO_AZUL)
        exportar(caja, f"{nombre}_transparente.mov", None)


if __name__ == "__main__":
    main()
