import sys, ezdxf
from ezdxf import bbox
from collections import Counter
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace(); c = Counter()
for e in list(msp):
    if e.dxf.layer == "0-MARCO-A3": c['marco'] += 1; continue
    b = bbox.extents([e], fast=True)
    if not b.has_data: c['nodata'] += 1; continue
    x0, x1 = b.extmin.x, b.extmax.x
    if x1 <= 126.5: e.translate(166, 0, 0); c['corte'] += 1
    elif x0 >= 126.5: e.translate(-122, 0, 0); c['der'] += 1
    else: c['straddle'] += 1; print('straddle', e.dxftype(), e.dxf.layer, round(x0,1), round(x1,1))
print(c); doc.saveas(sys.argv[2])
