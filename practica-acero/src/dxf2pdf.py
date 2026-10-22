# -*- coding: utf-8 -*-
"""DXF (mm de papel, hoja A4 1:1) -> PDF vectorial a tamaño real y PNG de vista previa."""
import sys
import ezdxf
from ezdxf import bbox
from ezdxf.addons.drawing import RenderContext, Frontend, layout, pymupdf
from ezdxf.addons.drawing.config import Configuration, LineweightPolicy, BackgroundPolicy, ColorPolicy

src, pdf, png = sys.argv[1:4]
doc = ezdxf.readfile(src); msp = doc.modelspace()
# Arial no está en este equipo: se dibuja con Liberation Sans (mismas métricas); el DWG sigue pidiendo Arial.
for st in doc.styles:
    f = st.dxf.font.lower()
    if f.startswith("arialbd"): st.dxf.font = "LiberationSans-Bold.ttf"
    elif f.startswith("arial"): st.dxf.font = "LiberationSans-Regular.ttf"
ext0 = bbox.extents(msp.query("LWPOLYLINE[layer=='0-MARCO']"))
W, H = round(ext0.size.x), round(ext0.size.y)
cfg = Configuration(lineweight_policy=LineweightPolicy.ABSOLUTE, background_policy=BackgroundPolicy.WHITE,
                    color_policy=ColorPolicy.COLOR, lineweight_scaling=1.0, min_lineweight=0.09)
be = pymupdf.PyMuPdfBackend()
Frontend(RenderContext(doc), be, config=cfg).draw_layout(msp)
page = layout.Page(W, H, layout.Units.mm, margins=layout.Margins.all(0))
ext = bbox.BoundingBox([(0, 0), (W, H)])
settings = layout.Settings(fit_page=True, max_stroke_width=0.01, min_stroke_width=0.0)
open(pdf, "wb").write(be.get_pdf_bytes(page, settings=settings, render_box=ext))
if png != "-":
    open(png, "wb").write(be.get_pixmap_bytes(page, fmt="png", dpi=int(sys.argv[4]) if len(sys.argv) > 4 else 130, settings=settings, render_box=ext))
