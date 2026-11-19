# Arma Carpeta_Instalaciones_II.pdf: tapa, carátulas, memorias y cálculos, con numeración al pie.
import io, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('LS','/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
U='/root/.claude/uploads/14df2116-8de2-54f6-8942-50f1368fca3c'; S='/tmp/claude-0/-home-user-Arquitectura-/14df2116-8de2-54f6-8942-50f1368fca3c/scratchpad'; D='/home/user/Arquitectura-/entregables/CARPETA_INSTALACIONES_II'
c=PdfReader(S+'/caratulas.pdf')
R=PdfReader
san=R(U+'/7439b1b7-Instalacion_Sanitaria_Calculos.pdf'); esc=R(U+'/2fc101c3-Balance_Termico_Escuela.pdf'); viv=R(U+'/76acc24a-Balance_Termico_Psicrometria_Vivienda.pdf')
tv=R(U+'/d48f380b-Calculos_Transporte_Vertical_Vivienda.pdf'); me=R(U+'/8e6483f8-Memoria_descriptiva_-_Acondicionamiento_termico.pdf')
mv=R(U+'/7b579e55-Memoria_descriptiva_-_AA__-_CALEFACCION_vivienda.pdf'); ie=R(U+'/ab1de566-MEMORIA_I.E._EDIFICIO_PUBLICO.pdf')
mel=R(D+'/memorias/memoria_electricidad_transporte_vertical.pdf'); minc=R(D+'/memorias/memoria_incendio_sanitarias.pdf'); anx=R(D+'/memorias/anexo_plano_ie.pdf')
w=PdfWriter(); mask=set()
def add(pages,m=False):
    for p in pages:
        if m: mask.add(len(w.pages))
        w.add_page(p)
def mark(t,parent=None): return w.add_outline_item(t,len(w.pages),parent=parent)
mark('Tapa'); add([c.pages[0]])
o=mark('01 Instalación sanitaria e incendio'); add([c.pages[1]])
mark('Memoria proyectual · Incendio e instalaciones sanitarias',o); add(minc.pages)
mark('Cálculos · Instalación sanitaria',o); add(san.pages)
o=mark('02 Acondicionamiento térmico · Escuela'); add([c.pages[2]])
mark('Memoria descriptiva',o); add(me.pages[1:],True)
mark('Balance térmico verano – invierno',o); add(esc.pages)
o=mark('03 Acondicionamiento térmico · Vivienda'); add([c.pages[3]])
mark('Memoria descriptiva',o); add(mv.pages[1:],True)
mark('Balance térmico y psicrometría',o); add(viv.pages)
o=mark('04 Electricidad y transporte vertical · Vivienda'); add([c.pages[4]])
mark('Memoria descriptiva',o); add(mel.pages)
mark('Cálculo de transporte vertical',o); add(tv.pages)
o=mark('05 Instalación eléctrica · Escuela'); add([c.pages[5]])
mark('Memoria descriptiva',o); add(ie.pages[1:4],True)
mark('Anexo · Plano de la instalación',o); add(anx.pages)
w.add_metadata({'/Title':'Instalaciones II · Memorias y cálculos'})
mm=72/25.4
for i,p in enumerate(w.pages):
    W=float(p.mediabox.width);H=float(p.mediabox.height)
    buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(W,H))
    if i in mask:
        cv.setFillColorRGB(1,1,1); cv.rect(W-90,30,50,26,stroke=0,fill=1)
    cv.setFillColorRGB(0x6a/255,0x77/255,0x87/255); cv.setFont('LS',7.5)
    cv.drawCentredString(W/2,5.5*mm+1,str(i+1)); cv.save()
    buf.seek(0); p.merge_page(PdfReader(buf).pages[0])
w.write(D+'/Carpeta_Instalaciones_II.pdf'); print(len(w.pages))
