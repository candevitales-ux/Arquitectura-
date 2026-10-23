# -*- coding: utf-8 -*-
"""DXF (mm de papel) -> PDF vectorial A3 vertical a tamaño real (1 unidad = 1 mm) y PNG de vista previa."""
import sys
import ezdxf
from ezdxf import bbox
from ezdxf.addons.drawing import RenderContext, Frontend, layout, pymupdf
from ezdxf.addons.drawing.config import Configuration, LineweightPolicy, BackgroundPolicy, ColorPolicy
from ezdxf.fonts import fonts

src, pdf, png = sys.argv[1:4]
PW, PH = (210, 297) if len(sys.argv) > 4 and sys.argv[4].upper() == "A4" else (297, 420)   # hoja: A3 (defecto) o A4
doc = ezdxf.readfile(src); msp = doc.modelspace()
# Arial no está en este equipo: se dibuja con Liberation Sans (mismas métricas); el DWG sigue pidiendo Arial.
for st in doc.styles:
    f = st.dxf.font.lower()
    if f.startswith("arialbd"): st.dxf.font = "LiberationSans-Bold.ttf"
    elif f.startswith("arial"): st.dxf.font = "LiberationSans-Regular.ttf"

cfg = Configuration(lineweight_policy=LineweightPolicy.ABSOLUTE, background_policy=BackgroundPolicy.WHITE,
                    color_policy=ColorPolicy.COLOR, lineweight_scaling=1.0, min_lineweight=0.09)
be = pymupdf.PyMuPdfBackend()
Frontend(RenderContext(doc), be, config=cfg).draw_layout(msp)
page = layout.Page(PW, PH, layout.Units.mm, margins=layout.Margins.all(0))
# el contenido se ubica por su recuadro: forzamos que el recuadro sea la hoja completa
ext = bbox.BoundingBox([(0, 0), (PW, PH)])
settings = layout.Settings(fit_page=False, scale=1, max_stroke_width=0.01, min_stroke_width=0.0)
open(pdf, "wb").write(be.get_pdf_bytes(page, settings=settings, render_box=ext))
open(png, "wb").write(be.get_pixmap_bytes(page, fmt="png", dpi=150, settings=settings, render_box=ext))
print("pdf ok")
