import sys
sys.path.insert(0, ".")
from figs import F, DEFS

_n = [0]
def fig(k, cap, cls=""):
    _n[0] += 1
    return f'<figure class="fig {cls}">{F[k]}<figcaption><b>Fig. {_n[0]}</b> · {cap}</figcaption></figure>'

def ck(*items):
    return '<ul class="ck">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def ar(*items):
    return '<ul class="ar">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def d(term, body):
    return f'<p class="def"><span class="term">{term}</span> {body}</p>'

def pc(pros, cons, tp="Ventajas", tc="Desventajas"):
    return (f'<div class="pc"><div class="pro"><h5>{tp}</h5>{ar(*pros)}</div>'
            f'<div class="con"><h5>{tc}</h5>{ar(*cons)}</div></div>')

def sec(num, title, sub, color, icon):
    return (f'<section class="sec" style="--c:{color}"><div class="sec-head"><div class="num">{num}</div>'
            f'<div><div class="kicker">{sub}</div><h2>{title}</h2></div><div class="ico">{icon}</div></div>')

I = {
 "sun": '<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><g stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M20 4v5M20 31v5M4 20h5M31 20h5M8.7 8.7l3.5 3.5M27.8 27.8l3.5 3.5M8.7 31.3l3.5-3.5M27.8 12.2l3.5-3.5"/></g></svg>',
 "snow": '<svg viewBox="0 0 40 40"><g stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M20 4v32M6 12l28 16M6 28l28-16M16 6l4 4 4-4M16 34l4-4 4 4"/></g></svg>',
 "fan": '<svg viewBox="0 0 40 40"><g fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="20" cy="20" r="3"/><path d="M20 17c0-8 8-10 10-6s-4 7-10 6M23 20c8 0 10 8 6 10s-7-4-6-10M20 23c0 8-8 10-10 6s4-7 10-6M17 20c-8 0-10-8-6-10s7 4 6 10"/></g></svg>',
 "fire": '<svg viewBox="0 0 40 40"><path d="M20 4c2 8 10 10 10 20a10 10 0 0 1-20 0c0-6 4-8 5-13 2 3 2 6 5 7 0-5-2-9 0-14z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/></svg>',
 "plug": '<svg viewBox="0 0 40 40"><g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4v8M26 4v8M10 12h20v6a10 10 0 0 1-20 0zM20 28v8"/></g></svg>',
 "bolt": '<svg viewBox="0 0 40 40"><path d="M23 3L9 23h10l-3 14 15-21H21z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/></svg>',
 "lift": '<svg viewBox="0 0 40 40"><g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"><rect x="7" y="4" width="26" height="32" rx="2"/><path d="M20 4v32M12 15l3-4 3 4M22 25l3 4 3-4"/></g></svg>',
}

C1, C2, C3, C4, C5, C6, C7 = "#2f6fde", "#0e9aa7", "#6b4fd8", "#e0453a", "#d98a00", "#8a3ffc", "#1f9d6b"

body = []
A = body.append

# ===================== 1 CONFORT + BALANCE VERANO
A(sec("01", "Confort y balance térmico de verano", "Climatización · Aire acondicionado", C1, I["sun"]))
A('<div class="hero-def"><span class="term">Confort</span> = Temp. de bulbo seco, humedad, radiación de sup., movimientos de aire.</div>')
A('<div class="chips"><span>✓ Unidad calor = <b>kcal/h</b></span><span>✓ Temperatura = mide los grados</span></div>')
A(fig(1, "Verano / invierno: el calor entra o se pierde"))
A('<div class="grid2">' +
  '<div class="card">' + ck("En invierno <b>aporto</b> calor", "En verano, <b>saco</b> el calor. <span class='hand'>↓ ¿Cuánto tengo que sacar?</span>") +
  '<p class="mini">✓ 2 fórmulas =</p>' + ar("Ganancia por radiación solar", "Ganancia por transmisión de calor") + '</div>' +
  '<div class="card">' + ck("Ganancia de calor interiores = iluminación, personas, equipos <b>(3 fórmulas)</b>",
     "Hay calor <b>sensible</b> y calor <b>latente</b>.") +
  ar("<b>Sensible</b> ↳ se mide con el termómetro", "<b>Latente</b> ↳ cant. de calor que produce un cambio de estado.") + '</div></div>')
A('<div class="card">' + ck("<b>Psicometría</b> = mide la cantidad de humedad en el aire.",
   "<b>Humedad</b> = cant. de vapor de agua que está contenida en el aire",
   "<b>Humedad relativa</b> = varía con la temperatura",
   "<b>Humedad absoluta</b> = se mide en gramos/kg de aire seco y esa cant. de humedad es fija a menos que se produzca un cambio de estado. ej = humedad (gas) a lluvia (líquido).") + '</div>')
A('<h3>Balance térmico verano <span class="tag">3 aspectos importantes</span></h3>')
A('<div class="three">'
  '<div class="mini-card"><h4>Ganancias externas</h4>' + ar("<b>Transmisión</b> → calor sensible <span class='hand'>↳ cálculo muro int., ext., vidrio y carpintería</span>", "<b>Radiación</b> → calor latente.") + '</div>'
  '<div class="mini-card"><h4>Ganancias internas</h4>' + ar("<b>Personas</b> = calor sensible + latente", "<b>Iluminación</b> = calor sensible", "<b>Equipos</b> = calor sensible (puede aportar latente un equipo especial o cocina).") + '</div>'
  '<div class="mini-card"><h4>Ventilación</h4><p>Aire exterior – calor sensible + calor latente</p><p class="hand">↳ e infiltraciones, considerar aire caliente y húmedo.</p></div></div>')
A('<div class="formula big">Q<sub>T</sub> = Q<sub>S</sub> + Q<sub>L</sub></div>')

A('<h3>Cálculos del equipo</h3>')
A('<div class="grid2">'
  '<div class="formula"><div class="fl">Potencia frigorífica</div>(Volumen (L·L·h) × 70 kcal) / 3024<div class="ex">ej = (141 m³ × 70 kcal) / 3024 = <b>3,2 TR</b></div></div>'
  '<div class="formula"><div class="fl">C.A.M · caudal de aire de mando</div>TR · 600 m³/hora<div class="ex">ej = 3,2 TR · 600 m³/hora = <b>1920 m³/h</b></div></div>'
  '<div class="formula"><div class="fl">C.A.R · caudal de aire de retorno</div>80 % del CAM</div>'
  '<div class="formula"><div class="fl">C.A.E · caudal de aire exterior</div>20 % del CAM</div></div></section>')

# ===================== 2 CICLO + EQUIPOS
A(sec("02", "Ciclo de compresión y equipos de A.A.", "Cómo producir frío", C2, I["fan"]))
A(fig(2, "Ciclo de compresión: ① evaporador → ② compresor → ③ condensador → ④ válvula de expansión"))
A('<h4 class="sub">Componentes = evaporador, compresor, condensador, válvula de expansión.</h4>')
A('<div class="comp4">'
  '<div><b>Evaporador</b><span>Toma el calor (gas)</span><em>↓ Equipo interior, contiene un fluido "Freón"</em></div>'
  '<div><b>Compresor</b><span>Toma el fluido y lo comprime con alta presión y temp.</span><em>Con frío se comprime.</em></div>'
  '<div><b>Condensador</b><span>Paso de gas a líquido</span><em>↑ Equipo exterior</em></div>'
  '<div><b>Válvula de expansión</b><span>Baja la temp. y presión en líquido.</span></div></div>')
A('<h3>Clasificación de equipos de A.A.</h3>')
A('<div class="grid2"><div class="card"><h4>• Individuales</h4><p>Split · De ventana <span class="pill">expansión directa</span></p></div>'
  '<div class="card"><h4>• Centrales</h4><p>→ Rooftop, separados, multisplit, VRV <span class="pill">exp. directa</span></p>'
  '<p>↳ MEL de agua/aire, fancoil (mixtos) <span class="pill alt">exp. indirecta</span></p></div></div>')
A('<div class="eq"><div class="eq-t"><h4>✱ Equipo de ventana <small>(individual)</small></h4>' + ar("Expansión directa", "Condensador enfriado por aire", "Uso = vivienda – oficina.") + '</div>' + fig(3, "Equipo de ventana") + '</div>')
A('<div class="eq"><div class="eq-t"><h4>✱ Equipo split</h4>' + ar("Expansión directa", "Condensador enfriado por aire", "Uso = vivienda, oficina") +
  '<p class="mini">1 unidad interior (evaporador)<br>1 unidad exterior (condensador)</p></div>'
  '<div class="eq-t"><h4>✱ Roof top</h4>' + ar("Expansión directa", "Condensador enfriado por aire", "Ubicado en azotea") + '</div></div>')
A(fig(4, "Roof top"))
A('<div class="eq"><div class="eq-t"><h4>✱ Equipo separado</h4>' + ar("Expansión directa.", "Condensador enfriado por aire") +
  '<p class="mini">1 unidad interior (evaporadora)<br>1 unidad exterior (condensadora)</p>'
  '<h4 style="margin-top:10px">✱ VRV</h4><p>1 condensadora, varias evaporadoras.</p></div>' + fig(5, "VRV") + '</div>')
A('<div class="eq"><div class="eq-t"><h4>✱ Mixto = Fancoil + MEL por aire</h4>' + ar("Expansión indirecta", "Condensador enfriado por aire") + '</div>' + fig(6, "Mixto: fancoil + MEL") + '</div>')
A('<div class="grid2 figs">' + fig(7, "Ubicación en el edificio") + fig(8, "Fancoil + MEL con torre de enfriamiento") + '</div>')
A('<h3>Distribución del aire</h3>')
A('<div class="card">' + ck("En verano mueves el aire <span class='hand'>↳ distribución a baja velocidad y de manera pareja</span>",
   "<b>Instalaciones centrales</b> = el aire se distribuye en conductos de chapa galvanizada, u otros. Luego se incorporan a los locales por medio de difusores.") +
  ar("<b>Mandos</b> = difusores (cada difusor toma una cant. de aire de mando).", "<b>Retornos</b> = rejas") + '</div>')
A('<div class="eq">' + fig(9, "Conducto de mando con 6 difusores") +
  '<div class="eq-t"><div class="formula"><div class="fl">CAM total = 1200 m³/h</div>Si tengo 6 difusores → <b>200 m³/h c/u</b><div class="ex">CAM TOTAL / cant. difusores = CAM DIF.</div></div>'
  '<div class="formula"><div class="fl">1 TR = 600 m³/h</div>Si mi equipo tiene 1200 m³/h<div class="ex">↳ 1200 m³/h / 600 m³ = <b>2 TR</b></div></div></div></div></section>')

# ===================== 3 BALANCE INVIERNO
A(sec("03", "Balance térmico de invierno", "Uso orientaciones", C3, I["snow"]))
A('<div class="card">' + ck("Considero mampostería y carpinterías.") +
  '<p class="mini">✓ Cálculo = <span class="tag">3 aspectos</span></p>' +
  ar("<b>Pérdidas de calor</b> (transmisión) por orientación, aex, infilt.) <span class='hand'>→ tener en cuenta muros, ventanas… sup. y coef. K</span>",
     "<b>Ganancias de calor</b> (personas, equipos, iluminación) → ganancias internas",
     "<b>Ventilación</b> (pérdida) / pérdidas de calor por ventilación e infiltraciones.") + '</div>')
A('<div class="formula big">Q total = Pérdidas – Ganancias <small>(kcal/h)</small></div>')
A('<div class="card">' + ck("<b>Valor índice</b> = relación entre la pérdida o ganancia de calor y el volumen de un local.") +
  '<div class="formula"><div class="fl">Valor índice</div>Carga térmica / Volumen de local</div>'
  '<div class="grid2 tight"><p class="note">↳ Para tener un valor representativo se toman mín. 3 locales y se promedian obteniendo un valor de índice promedio.</p>'
  '<p class="note alt">Con este valor puedo sacar la carga térmica de cualquier local o zona, multiplicándolo por su volumen.</p></div></div></section>')

# ===================== 4 CLIMATIZACIÓN / CALEFACCIÓN
A(sec("04", "Climatización y calefacción", "Sistemas, equipos y terminales", C4, I["fire"]))
A('<div class="card"><h4>Confort</h4><p>→ en invierno <b>16 °C – 24 °C</b> · Humedad entre <b>30 % y 70 %</b>.</p>'
  '<p class="mini">Los valores para el confort dependen de las consideraciones siguientes:</p>' +
  ck("Tipo de espacio (ext. o int.)", "Tipo de tarea a desarrollar", "Época del año a evaluar (invierno o verano)", "Ubicación geográfica", "Características de las personas y/o materiales.") + '</div>')
A('<div class="grid2"><div class="card"><h4>Destinos de climatización</h4>' + ar("Residencias o ambientes de uso para personas", "Edificios institucionales y comerciales (objetos, materiales)") + '</div>'
  '<div class="card"><h4>Sistemas</h4>' + ck("<b>Sistemas centrales</b> → 1 equipo generador de calor (concentración de salas de máquinas, ahorro energético del edificio)",
  "<b>Sistemas individuales</b> → varios equipos generadores de calor (cada ambiente es una sala de máquinas, ahorro energético solo algunos usuarios).") + '</div></div>')
_n[0] += 1
A(f'<figure class="fig"><table class="tbl"><thead><tr><th>Sala de máquinas</th><th>Canalizaciones</th><th>Equipos terminales</th></tr></thead>'
  '<tbody><tr><td>Calderas, equipos calentadores de aire</td><td class="flow r">mando →</td><td>Radiadores, fancoils, piso radiante, caloventiladores, convectores</td></tr>'
  '<tr><td>Planta térmica, generación de calor</td><td class="flow b">← retorno</td><td>Emisión de calor al ambiente</td></tr></tbody></table>'
  f'<figcaption><b>Fig. {_n[0]}</b> · Partes de una instalación de calefacción</figcaption></figure>')
A('<div class="card">' + ar("<b>Sistema por agua caliente</b> = &gt; temperatura del agua c/equipo térmico.",
  "<b>Sistema por paneles radiantes</b> = &lt; temp. del agua sin/equipo térmico.",
  "<b>Sistema por vapor</b> o baja presión caliente.", "<b>Sistema por aire.</b>") +
  '<p class="note">✓ Las ventilaciones se encuentran a 30 cm del piso, 30 cm del techo, 2 rejillas por equipo obligatorios.</p></div>')
A('<h3>Agua caliente</h3><p class="lead">Radiadores, caldera, bombas, convectores de piso, zocaloducto, caloventiladores, convectores, piso radiante</p>')
A(pc(["Calor suave y agradable", "Bajo tostamiento del polvo", "Funcionamiento silencioso en canalizaciones y eq. terminales.",
       "Mayor duración de las cañerías", "Buena regulación en la planta térmica y equipos terminales", "Calor remanente en eq. terminales (inercia térmica).",
       "Respuesta aceptable ante lentas variaciones de temp."],
      ["Lenta puesta en marcha e inercia térmica", "Posibles inconvenientes por pérdida de agua en cañerías", "Posibilidad de congelamiento",
       "Distribución de calor puntual, poco uniforme", "Poca regulación por el usuario", "No ventila el ambiente climatizado."]))
A('<div class="card"><h4>Características</h4>' + ar("<b>Directos</b> = 1 solo fluido caloportador", "<b>Indirectos</b> = 2 o más fluidos caloportadores",
  "<b>Ubicación</b> = sala de máquinas (azotea / subsuelo, PB)", "<b>Forzado</b> (con bomba) o <b>no forzado</b> (circulación natural)", "<b>Distribución</b> = superior o inferior.") + '</div>')
A('<div class="card"><h4>Equipos <span class="hand">↗ sala de máquinas en subsuelo</span></h4><p>Radiadores, caldera, bombas, convectores de piso, zocaloducto, caloventiladores…</p></div>')
A('<h3>• Radiadores <span class="tag">sistema directo</span></h3>')
A('<div class="eq">' + fig(11, "Caldera de 3 pasos") + '<div class="eq-t"><p>→ Cuenta con = mufla, quemador, salida de vapor, retorno, chimenea, regulador de presurización, cámara de retorno.</p><p class="big-note">Son 3 pasos.</p></div></div>')
A('<div class="grid2 figs">' + fig(12, "Instalación de radiadores en el edificio") + fig(121, "Detalles: azotea, radiadores y sala de calderas") + '</div>')
A(fig(15, "Esquema de la solapa: tanque, radiadores por piso, bombas y válvula de limpieza", "w70"))
A('<h3>• Calderas</h3>')
A('<div class="eq">' + fig(13, "Caldera") + '<div class="eq-t">' + ar("Puede ser a gas, eléctrica o a leña.", "Componente de sistema directo", "Ubicada en subsuelo") +
  '<p class="hand">↳ Sumamos 1 conducto de humo por artefacto.</p></div></div>')
A('<h3>• Bombas de recirculación</h3>')
A('<div class="eq">' + fig(14, "Bombas en paralelo") + '<div class="eq-t"><p>→ Se encuentran antes de la entrada desde la cañería de retorno y antes del vaso de expansión (VE)</p></div></div>')
A('<h3>Equipos terminales <span class="tag">sistema directo</span></h3>')
A('<div class="terms">'
  f'<div class="term-c">{fig(16, "Convector de piso")}<h4>• Convectores de piso</h4><p>Contrarrestan el frío de la abertura</p></div>'
  f'<div class="term-c">{fig(17, "Zocaloducto")}<h4>• Zocaloducto</h4><p>Va por dentro del zócalo</p></div>'
  f'<div class="term-c">{fig(18, "Caloventilador")}<h4>• Caloventilador</h4><p>→ Cuenta con alimentación, colector de cobre, ventilador, motor, aletas, persiana regulable y retorno.</p><p>Mucho más chico por el lado del techo</p></div>'
  f'<div class="term-c">{fig(19, "Convector")}<h4>• Convectores</h4><p>→ Cuentan con regulador, grilla de salida de aire, frente, aletas, cabezal, unión, caño de conexión, grilla de entrada de aire.</p><p>Embutido en la pared</p></div></div>')
A('<h3>• Piso radiante <span class="tag">sistema indirecto</span></h3>')
A('<div class="temps"><div><b>35° – 50°</b><span>agua en tuberías plásticas</span></div><div><b>20° – 28°</b><span>suelo</span></div><div><b>18° – 20°</b><span>ambiente</span></div></div>')
A('<div class="eq"><div class="eq-t"><h4>✓ Esquema general</h4>' + ar("Serpentinas de polietileno (continuo o espiral)", "Diám. ext. 20 mm o 16 mm separados a 20/30 cm", "Caldera mural o bajo mesada.") +
  '<p class="hand">↗ El agua caliente entra por las paredes exteriores.</p></div>' + fig(20, "Esquema general de piso radiante") + '</div>')
A('<div class="eq">' + fig(21, "Caja de colectores") + '<div class="eq-t"><h4>Aplicación</h4>' +
  ck("Calefacción en viviendas", "Criaderos de pollos, cerdos…", "Derretimiento de nieve", "Calefacción de piscinas", "Invernaderos", "Calles, estadios de fútbol", "Frigoríficos.") + '</div></div>')
A('<h4 class="sub">Diferencias entre piso radiante y losa radiante</h4>')
A('<div class="grid2 figs">' + '<div>' + fig(22, "Losa radiante") + '<p class="note">→ Losa radiante = cañería en losa</p></div>' +
  '<div>' + fig(23, "Piso radiante") + '<p class="note alt">→ Piso radiante = cañería en capa de H° 1:3</p></div></div>')
A('<div class="card"><p><b>Paneles radiantes</b> = se transporta agua con menor temperatura porque no lleva equipo térmico.</p></div>')
A('<h4 class="sub">✓ Piso radiante</h4>' + pc(["Funcionamiento silencioso", "Gran inercia térmica", "Flexible, sin equipos a la vista", "Calor suave, agradable, uniforme", "Poca pérdida de calor al ventilar"],
   ["Alto costo de uso", "Influye fuertemente en el costo eléctrico", "Posibilidad de congelamiento"]))
A('<h3>Sistemas por vapor o baja presión</h3><p class="lead">Calderas que alimentan únicamente a radiadores. Este sistema no requiere bombas, ya que va y vuelve por sí solo.</p>')
A(pc(["Rápida puesta en marcha", "Sin inconvenientes en zonas frías", "Aprovecha la existencia de vapor de otro equipo."],
     ["Rápida puesta en marcha", "Baja duración de cañerías", "Calor fuerte y alto tostamiento de polvos", "Poca flexibilidad en locales por equipo terminal"]))
A('<h3>Sistemas por aire caliente</h3><p class="lead">El aire se calienta con fuego o agua, dependiendo con qué va a ser la calidad que aporte al espacio. Estas cañerías deben disponerse de un espacio mínimo de 30 cm para que pasen conductos de 20 × 20</p>')
A(pc(["Rápida puesta en marcha", "Calor suave y agradable", "Bajo nivel de ruido", "Ingreso y tratamiento del aire exterior", "Posibilidad de instalar equipos de refrigeración y terminales."],
     ["Más costoso que por agua caliente", "No tiene inercia térmica", "Amplios espacios para la canalización", "Poca flexibilidad."]))
A('<div class="hero-def"><span class="term">Inercia térmica</span> = lo que tarda un equipo en calentarse y enfriarse, depende para qué, es ventaja o desventaja.</div></section>')

# ===================== 5 ELECTRICIDAD
A(sec("05", "Electricidad", "Redes, tableros y fuerza motriz", C5, I["plug"]))
A('<div class="grid2"><div class="card"><h4>Redes de distribución de acuerdo al nivel de tensión</h4>' +
  ar("Redes de <b>MT</b> (13,2 kV)", "Redes de <b>BT</b> (380–220 V)") + '<p class="mini">} Disposición aérea / Disposición subterránea (no se ven tanto)</p></div>'
  '<div class="card"><h4>Distribución al consumo domiciliario</h4>' + ar("La alimentación se hace desde transformadores subterráneos o aéreos",
  "Se alimentan en malla cerrada como seguridad", "Desde esos ramales se efectúan las acometidas a los consumidores.") + '</div></div>')
A('<h4 class="sub">✓ Códigos de colores</h4><div class="wires">'
  '<div><i style="background:#7a4a2a"></i><b>Línea 1</b> (fase R) · L1 · marrón</div>'
  '<div><i style="background:#1b1b1b"></i><b>Línea 2</b> (fase S) · L2 · negro</div>'
  '<div><i style="background:#e0453a"></i><b>Línea 3</b> (fase T) · L3 · rojo</div>'
  '<div><i style="background:#7cc6f2"></i><b>Neutro</b> · N · celeste</div>'
  '<div><i style="background:repeating-linear-gradient(90deg,#2aa84a 0 8px,#f3d02c 8px 16px)"></i><b>Conductor a tierra</b> · PE · verde-amarillo</div>'
  '<p class="mini">L1, L2, L3 } Fase – vivo</p></div>')
A('<div class="eq"><div class="eq-t"><h4>✓ Red eléctrica domiciliaria</h4><p>A la salida del medidor hay un interruptor diferencial o termomagnético y constituye el T.P</p>'
  '<h4 style="margin-top:12px">✓ Componentes básicos en una instalación</h4><div class="chips sm"><span>Acometida</span><span>Caja de toma</span><span>Medidor</span><span>Línea de alimentación</span><span>T.P</span><span>TPSG</span><span>T.S</span><span>Líneas de circuitos terminales</span></div></div>' +
  fig(24, "Red de distribución y responsabilidades") + '</div>')
A('<div class="eq">' + fig(25, "Esquema montante") + '<div class="eq-t"><h4>✓ Esquema montante</h4><p>Hay = un C.T.P que va a la caja, de ahí a los medidores y tableros.</p>' +
  ar("<b>TPD</b> → domicilios", "<b>TPSG</b> → serv. generales") + '<p>y de ahí a los seccionales y sus circuitos.</p></div></div>')
A('<h4 class="sub">✓ Múltiples usuarios, esquema unifilar</h4>')
A(fig(26, "Esquema unifilar para múltiples usuarios", "w80"))
A(fig(27, "Solapa: distribución de tableros en el edificio", "w60"))
A('<div class="card">' + ck("<b>Gabinetes colectivos</b> = tienen cajas superiores con interruptor diferencial y termomagnético (1 por medidor)",
  "<b>Servicios generales</b> = iluminación de pasillos, accesos, cocheras, ext… iluminación de emergencia, iluminación de escaleras, tomas…",
  "<b>Instalación de fuerza motriz</b> = circuitos de instalación fija y uso específico, que realicen la transmisión de energía eléctrica para el accionamiento de motores eléctricos de cierta envergadura, generalmente trifásicos.",
  "<b>Motores eléctricos</b> = máquinas eléctricas rotativas que transforman la energía eléctrica en energía mecánica.",
  "<b>Circuitos de fuerza motriz</b> = “son parte de los servicios generales.”") +
  '<p class="hand">↳ Ascensores, montacargas, bombas de incendio, bombas de agua, accionamiento de portones, equipos de aire acond., compactadores.</p></div></section>')

# ===================== 6 PARARRAYOS
A(sec("06", "Protección contra descargas atmosféricas", "Rayos y SPCR", C6, I["bolt"]))
A('<div class="hero-def"><span class="term">Rayo</span> = descarga eléctrica producida entre una nube cargada de electricidad y la tierra o 2 nubes cargadas con electricidad de distinta polaridad.'
  '<span class="hand">↳ Tensión en la base de la nube respecto a la tierra = 100–1000 millones de volts.</span></div>')
A('<div class="effects">'
  '<div><b>Efectos visuales</b>relámpago</div>'
  '<div><b>Efectos acústicos</b>propagación de una onda de choque mecánica en el aire. Efecto perceptible hasta una docena de km.</div>'
  '<div><b>Efectos térmicos</b>liberaciones de calor por el efecto de Joule en el canal ionizado.</div>'
  '<div><b>Efectos electrodinámicos</b>deformaciones en los materiales que se hallan a su paso.</div>'
  '<div><b>Efectos electroquímicos</b>descomposición electrolítica por aplicación de la ley de Faraday.</div>'
  '<div><b>Efectos de inducción</b>en un campo electromagnético variable, cualquier conductor es proclive a corrientes inducidas.</div>'
  '<div class="wide"><b>Efecto sobre humano o animal</b>durante una corta duración es suficiente para provocar riesgos de electrocución (ataque cardíaco, respiratorio) y riesgo de quemaduras.</div></div>')
A('<p class="note">– Los sistemas de protección no impiden la formación de rayos ↳ reduce en forma significativa el riesgo de los daños producidos.</p>')
A('<h3>Sistema de protección contra el rayo (SPCR) <span class="tag">consta de</span></h3>')
A('<div class="grid2"><div class="card"><h4>↳ Sistema externo</h4><p>Tiene un dispositivo captor (terminal aéreo), las bajadas y puesta a tierra. Su función es interceptar, conducir y dispersar la corriente de descarga a la tierra.</p></div>'
  '<div class="card"><h4>↳ Sistema interno</h4><p>Tiene todos los dispositivos complementarios al anterior con el fin de reducir los efectos electromagnéticos de la corriente del rayo dentro del espacio a proteger.</p><p>Previene chispas en descargas protegiendo a las personas, animales y equipos.</p></div></div>')
A('<p class="note alt">→ En casos particulares un SPCR puede ser solo interno o externo</p>')
A('<h3>Tipos de instalación</h3>')
A('<div class="eq"><div class="eq-t"><h4>✱ Sistema de protección separado del volumen a proteger</h4><p>Los captores y las bajadas están ubicados sin contacto con el volumen a proteger. Evita las descargas laterales.</p></div>' + fig(28, "Sistema separado") + '</div>')
A('<div class="eq"><div class="eq-t"><h4>✱ Sistema de protección parcialmente separado del volumen a proteger</h4><p>Los captores están ubicados para que el trayecto de la descarga atmosférica no tenga ningún contacto con el volumen.</p><p>Impide descargas laterales pero los conductores de las bajadas no están separados del volumen.</p></div>' + fig(29, "Sistema parcialmente separado") + '</div>')
A('<h3>✓ Sistema externo de protección contra el rayo</h3>')
A('<div class="card"><p>✱ <b>Dispositivos captor</b> = la probabilidad de que un rayo penetre el espacio a proteger se reduce considerablemente.</p>'
  '<p>✱ <b>Se pueden formar por cualquier combinación</b> =</p><ol class="num"><li>Varillas con puntas captoras (pararrayos)</li><li>Conductores horizontales tendidos (captores)</li><li>Mallas de conductores captores.</li></ol>'
  '<p>✱ <b>Techo captor</b> → debe haber =</p>' + ar("Continuidad eléctrica entre las chapas.", "Espesor de las chapas 0,5 mm si se acepta perforación o 4 mm para hierro si se pretende que no se perfore.",
  "Las chapas no cubiertas de material aislante.", "Conductos y depósitos deben ser de 2,5 mm si acepta la perforación o 5 mm para hierro si no se acepta.") + '</div>')
A('<div class="eq"><div class="eq-t"><h4>① Varillas con puntas captoras</h4></div>' + fig(30, "Varilla con punta captora") + '</div>')
A('<div class="eq"><div class="eq-t"><h4>• Hilo de guardia</h4><p>Usado en Polonia para protección de viviendas rurales.</p></div>' + fig(31, "Hilo de guardia") + '</div>')
A('<div class="eq"><div class="eq-t"><h4>③ Malla de conductores captores</h4></div>' + fig(32, "Malla captora") + '</div>')
A('<h3>Métodos para la elección del sistema</h3>')
A('<div class="grid2"><div class="card">' + ck("<b>Método del ángulo de protección</b> = se usa en estructuras simples y pequeñas (&lt; 20 m)") + '</div>'
  '<div class="card">' + ck("<b>Método de la esfera rodante o ficticia</b> = estructuras más altas y complejas.") + '</div></div>')
A(fig(33, "Método del ángulo", "w80"))
A('<div class="card"><h4>Consideraciones para la ejecución de bajadas</h4>' + ck("La elección del N° y la posición de los conductores de bajada deberán ser tomadas por el hecho.",
  "Los conductores de bajada deberán ser de manera uniforme ubicadas a lo largo del perímetro de la estructura a proteger.", "Los conductores de bajada deben ser lo más cortos posible.") + '</div></section>')

# ===================== 7 TRANSPORTE VERTICAL
A(sec("07", "Transporte vertical", "Ascensores y escaleras mecánicas", C7, I["lift"]))
A('<h3>✱ Ascensores</h3><div class="three">'
  '<div class="mini-card"><h4>Electromecánicos</h4><p>Necesitan una máquina de tracción con un motor eléctrico trifásico en sala de máquinas sobre o debajo de la instalación.</p></div>'
  '<div class="mini-card"><h4>Hidráulicos</h4><p>Funcionan gracias a una central oleodinámica, tracción a través de un pistón que se mueve por presión de aceite.</p></div>'
  '<div class="mini-card"><h4>Autoportantes</h4><p>(sin sala de máquinas) La máquina de tracción es un conjunto completo que se cuelga en la parte superior, dentro del pasadizo. Tiene un recorrido útil de hasta 45 m (16 paradas) y consume menos que los tradicionales.</p></div></div>')
A('<h3>✱ Aspectos a tener en cuenta</h3><div class="card">' + ck(
  "<b>Dimensiones mín. para una cabina</b> = 1,30 × 1,70 (600 kg) a 1,5 × 2,05 (1000 kg)",
  "<b>Pasadizo</b> = su construcción debe ser incombustible, entre cabina y tabique no debe haber menos de 0,4 m y en PB el tabique divisorio entre 2 ascensores debe llegar a los 2 m.",
  "<b>Claro inferior o foso</b> = allí se encuentran los paragolpes de la cabina y el contrapeso, este contrapeso debe tener el mismo peso que la cabina y un 50 % más.",
  "<b>Cabina</b> = conformada con materiales incombustibles, su superficie y lados mínimos se determina por la cant. de personas, su ventilación debe ser natural y forzada.",
  "<b>Sala de máquinas</b> = contiene los elementos necesarios para el funcionamiento del ascensor, como conjunto motriz (una polea de arrastre que de ellas dependen la carga nominal de carga y marcha), un tablero de comando (que maneja el arranque, las paradas, velocidad, aceleración y sentido de la marcha) y cables (de regulación, accionamiento y compensación).",
  "<b>Sistemas de seguridad</b> = cerraduras eléctricas en puertas de cabina y electromecánicas en puertas de rellano. Interruptor de fin de carrera en claro superior e inferior. Paracaídas en descenso y ascenso es capaz de parar por completo la cabina por presión contra las guías correspondientes, hay instantáneo o progresivo.") + '</div>')
A('<div class="card"><h4>✱ Ascensores hidráulicos</h4><p>Tienen bajo nivel de mantenimiento, suave funcionamiento y arranque, bajo nivel de consumo, pero como desventaja el pistón y el cilindro deben tener la misma longitud de la altura hasta el piso superior y tiene una baja velocidad de operación 30 m/min.</p></div>')
A('<div class="card"><h4>✱ Escaleras mecánicas</h4><p>Contiene un motor eléctrico que impulsa una rueda de transmisión en la parte superior que hace dar vuelta los escalones. En los extremos, el riel se nivela aplanando los escalones, además dispone de dispositivo para evitar que ingresen objetos.</p>'
  '<div class="temps g"><div><b>1 m</b><span>ancho de escalón habitual</span></div><div><b>30° · máx. 35°</b><span>inclinación óptima</span></div><div><b>30 m/min</b><span>velocidad</span></div></div>'
  '<p>– Deben garantizarse espacios libres lo suficientemente grandes a la entrada y a la salida (3 o más escalones)</p></div>')
A('<div class="grid2 figs"><div><h4>• Esquema pasadizo</h4>' + fig(34, "Esquema pasadizo") + '</div><div><h4>• Esquema cabina</h4>' + fig(35, "Esquema cabina (planta)") +
  '<h4 style="margin-top:14px">• Sala de máquinas <small>(h mín = 2 m)</small></h4>' + fig(36, "Sala de máquinas") +
  '<p class="note">← Acceso por lugares comunes. Puerta de acceso c/llave e incombustible con salida de emergencias.</p></div></div></section>')

CSS = open("style.css").read()
html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Resumen Instalaciones</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,800&family=Inter:wght@400;500;600;700&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{DEFS}{"".join(body)}</body></html>'''
open("resumen.html", "w").write(html)
print("figs:", _n[0])
