import sys, pymupdf
src, out = sys.argv[1], sys.argv[2]
mm = 72 / 25.4
S = pymupdf.open(src); W, H = S[0].rect.width, S[0].rect.height
D = pymupdf.open(); pg = D.new_page(width=W, height=H)
def place(x0, x1, dx, y0=4.5, y1=415.5):
    clip = pymupdf.Rect(x0 * mm, y0 * mm, x1 * mm, y1 * mm)
    pg.show_pdf_page(clip + (dx * mm, 0, dx * mm, 0), S, 0, clip=clip)
place(4.5, 126.5, +166.0)     # corte integral -> derecha
place(126.5, 292.7, -122.0)   # referencias (arriba) + nudos (abajo) + rótulo -> izquierda
pg.draw_rect(pymupdf.Rect(4 * mm, 4 * mm, 293 * mm, 416 * mm), color=(0, 0, 0), width=0.4 * mm)
D.save(out, garbage=4, deflate=True)
pg.get_pixmap(dpi=200).save(out.replace('.pdf', '.png'))
