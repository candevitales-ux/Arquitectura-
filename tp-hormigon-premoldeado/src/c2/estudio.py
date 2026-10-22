# -*- coding: utf-8 -*-
"""Recuadro 'PARA ESTUDIAR · IDEAS CLAVE' de cada lámina (se ubica solo en el espacio libre; si no entra, se recorta)."""
NOTAS = {
    "Sistema_Axonometria": [
        "El sistema se arma como un mecano: piezas fabricadas en planta (columnas, vigas, paneles) que en obra sólo se apoyan y se vinculan.",
        "Recorrido de cargas: panel TT → viga VP (o viga L) → ménsula → columna → cáliz → suelo.",
        "Las vigas apoyan ARTICULADAS (neopreno); la estabilidad la dan las columnas EMPOTRADAS en el cáliz y la capa de compresión, que convierte el piso en un diafragma rígido.",
        "Los cerramientos (muro cortina y panel sándwich) no son estructura: cuelgan de la viga perimetral VL.",
    ],
    "E1_Fundacion_Caliz": [
        "El cáliz es una 'cavidad' de hormigón donde se encastra la columna: se hace IN SITU, antes de que llegue la estructura premoldeada.",
        "Empotra la columna: la profundidad de encastre (≥ 1,5 a 2 veces el lado) y las llaves de corte transmiten el momento al suelo.",
        "La holgura (5 a 8 cm) permite aplomar con cuñas; después se llena con grout sin retracción, que es el que materializa la unión.",
        "Secuencia: excavación → H° de limpieza → base y cuello → montaje de columna → aplomado → grout → retiro de cuñas.",
    ],
    "E2_Columna": [
        "Columna de UNA pieza para los dos niveles: menos juntas y montaje más rápido (limita el largo: transporte y volteo).",
        "Las ménsulas cortas reciben las vigas: la carga baja por la diagonal (biela comprimida) y el tensor superior la equilibra.",
        "Pretensada: los cordones tesados comprimen la pieza y controlan la fisuración durante el izaje y el uso.",
        "Se monta con grúa, se aploma con puntales y recién cuando fragua el grout del cáliz se le apoyan vigas.",
    ],
    "E3_E4_Viga_VL_y_L": [
        "La VL es la viga de fachada: ata las columnas en el perímetro y es el soporte de los cerramientos (riel para el muro cortina o bulones del panel).",
        "Forma doble T: el material está en las alas, lejos del eje, donde más trabaja a flexión → más rigidez con menos peso.",
        "La viga L completa la altura hasta el piso y recibe el borde del panel TT en su talón; se vincula a la VL con barras en grout.",
        "Apoyo: neopreno (permite giro) + 2 pernos (evitan vuelco y deslizamiento).",
    ],
    "E5_Viga_VP": [
        "La VP es la viga PORTANTE principal: salva la luz mayor (15 m) y recibe los paneles TT.",
        "T invertida: los talones inferiores sirven de apoyo a los TT, así el piso queda a la altura de la cara superior de la viga (menos altura total).",
        "Es la pieza más pesada (≈ 12,6 t): define la grúa, el transporte y el plan de montaje.",
        "Se montan los TT simétricos a ambos lados para que la viga no se torsione.",
    ],
    "E6_E7_Panel_TT_Capa": [
        "El TT es una losa con dos nervios: los nervios trabajan como vigas y el ala como losa; cubre grandes luces sin apuntalar.",
        "El extremo del nervio tiene un rebaje (dap) que se apoya en el talón de la VP sobre neopreno.",
        "La capa de compresión (5 cm in situ con malla) une todos los paneles: reparte cargas y forma el diafragma rígido que estabiliza el edificio.",
        "El ala rugosa y los conectores salientes hacen que capa y panel trabajen juntos.",
    ],
    "E8_Apoyos_Conectores": [
        "Neopreno: apoyo elástico que reparte la carga y deja girar y dilatar la viga → unión articulada.",
        "Perno + vaina con grout: traba la pieza en el plano (no se cae ni se desliza) sin impedir el giro.",
        "Grout: mortero fluido sin retracción que rellena cálices, vainas y juntas (une sin dejar huecos).",
        "Riel e insertos: piezas metálicas que se dejan embutidas en fábrica para fijar cerramientos e izar las piezas.",
    ],
    "Juntas_1_Ubicacion": [
        "Una UNIÓN transmite esfuerzos entre piezas; una JUNTA las separa para permitir movimientos.",
        "Las juntas aparecen en cada encuentro entre piezas distintas: estructura / estructura, estructura / cerramiento y cerramiento / cerramiento.",
        "Para estudiar: ubicar cada J en planta y corte y relacionarla con su detalle (láminas 11 a 14).",
    ],
    "Juntas_2_Clasificacion": [
        "Seca = abulonada, soldada o apoyada: montaje inmediato y desmontable. Húmeda = grout u hormigón en obra: monolítica, necesita fragüe.",
        "Articulada = transmite corte y deja girar (vigas s/ neopreno). Rígida o empotrada = transmite también momento (columna en el cáliz).",
        "Juntas de movimiento: se calculan por dilatación térmica + tolerancias y se sellan con material elástico, nunca rígido.",
    ],
    "Juntas_3_Detalles_J1_J4": [
        "J1 es la única unión que empotra: por eso el cáliz es profundo y lleva llaves de corte.",
        "J2 y J3 son apoyos articulados: neopreno + pernos. La viga puede girar, pero no caerse ni deslizarse.",
        "J4 es una unión húmeda rígida: la viga L queda solidaria con la VL gracias a las barras en grout.",
    ],
    "Juntas_4_Detalles_J5_J8": [
        "J5: el rebaje del nervio TT (dap) apoya en el talón de la VP; la armadura de suspensión evita que el diente se fisure.",
        "J6 y J7: los paneles se apoyan en sus bordes y se traban entre sí con llaves de corte llenas de grout y chapas soldadas.",
        "J8: la capa de compresión con barras de negativo da continuidad sobre las vigas y une todo el piso.",
    ],
    "Juntas_5_Detalles_J9_J12": [
        "J9: el piso se separa de la columna con EPS para que sus movimientos no se transmitan a la estructura.",
        "J10: la grapa regulable absorbe las tolerancias del premoldeado (± 25 mm) y fija el muro cortina a la VL.",
        "J11: el montante se divide por nivel con un manguito que desliza: absorbe flechas de vigas y dilataciones.",
        "J12: el arranque es deslizante y con babeta/sellado para que el agua no entre por la base.",
    ],
    "Juntas_6_Detalles_J13_J15": [
        "J13: el bulón pasa por un agujero ovalado vertical: sostiene el panel contra el viento pero lo deja dilatar.",
        "J14: el peso del panel baja a la viga portapanel por el mortero de asiento; el pasador lo traba horizontalmente.",
        "J15: junta de 20 mm con fondo de junta y sellador elástico (relación ancho/profundidad 2:1).",
    ],
    "M1_Grua_Telescopica": [
        "La grúa se elige por CARGA x RADIO: la pieza más pesada a la mayor distancia del eje de giro (no por su capacidad nominal).",
        "Siempre trabaja sobre estabilizadores extendidos y placas de reparto sobre suelo firme.",
        "Se usa como máximo el 75 % de la tabla de carga; a la carga de la pieza se suman balancín y eslingas.",
        "Un señalero (rigger) coordina por radio con el operador y se aísla la zona bajo la carga.",
    ],
    "M2_M3_Carreton_Balancin": [
        "El carretón extensible transporta piezas largas; las de más de 12 m requieren permiso y escolta.",
        "Las piezas llegan en el orden de montaje y se izan directo del camión (menos acopio y manipuleo).",
        "El balancín cuelga la pieza con tiros verticales: no la comprime ni la flexiona de forma imprevista.",
        "Eslingas, grilletes y ganchos deben estar certificados para la carga.",
    ],
    "M4_Moldeo_Pista_Pretensado": [
        "Pretensado con armadura pretesa: se tesan los cordones ANTES de hormigonar, entre dos cabezales fijos.",
        "Cuando el hormigón alcanza resistencia se cortan los cordones: al querer acortarse, comprimen la pieza.",
        "Los moldes metálicos se reutilizan cientos de veces: piezas iguales, precisas y de buena terminación.",
        "El curado a vapor acelera el fragüe y permite desmoldar en el día.",
    ],
    "M5_M8_Anclaje": [
        "Puntales: sostienen la columna aplomada hasta que el grout del cáliz endurece.",
        "Plataforma elevadora: permite trabajar en altura en la fachada (vidrios, sellados, juntas).",
        "Equipo de grouteo: rellena cálices, vainas y juntas desde abajo, sin aire atrapado.",
        "Herramientas: llave dinamométrica (torque de bulones) y nivel láser / estación total (replanteo y aplomado).",
    ],
    "M9_Implantacion_Acceso_Obra": [
        "Antes de alquilar la grúa se verifica que el equipo y el camión PUEDAN ENTRAR: ancho, giro, pendiente, altura libre y suelo firme.",
        "Montaje en retroceso: la grúa empieza en el fondo y retrocede hacia el acceso, así nunca queda encerrada.",
        "El camión se ubica al alcance de la grúa y se iza directo; el acopio es mínimo y ordenado.",
    ],
    "M10_Planificacion_Alquiler": [
        "Pasos: relevar piezas → elegir equipo con la tabla de carga → contratar → pedir permisos → preparar suelo y acceso → coordinar entregas.",
        "La grúa se alquila por jornada con operador y SOLO las semanas de montaje pesado (acá 2 semanas).",
        "Los equipos menores (plataforma, grouteo, puntales) se alquilan aparte y por más tiempo.",
    ],
    "E9_Muro_Cortina_Croquis": [
        "Muro cortina stick: montantes verticales y travesaños horizontales de aluminio armados en obra, con vidrio DVH.",
        "No es portante: cuelga de la VL por grapas y sólo resiste su peso y el viento.",
        "El spandrel (vidrio opaco + lana) tapa el frente de losa; detrás va la barrera cortafuego.",
        "El sistema presor + tapa aprieta el vidrio contra burletes: estanqueidad al agua y al aire.",
    ],
    "E9_Muro_Cortina_Especificacion": [
        "Ventajas: luz natural, visuales, liviano (≈ 50 kg/m²), absorbe tolerancias con las grapas.",
        "Desventajas: aísla poco (K 2,8), no resiste fuego, gana calor (requiere control solar) y necesita mantenimiento de sellos.",
        "Stick vs. unitizado: el stick conviene en edificios bajos (2 niveles); el unitizado en torres con mucha repetición.",
    ],
    "E10_Panel_Sandwich_Croquis": [
        "Panel sándwich: hoja exterior + aislación EPS + hoja interior portante, en una sola pieza premoldeada.",
        "La hoja interior lleva los anclajes; los conectores de fibra de vidrio unen las hojas sin puente térmico.",
        "Cuelga de la VL con bulones (ojal vertical) y apoya abajo en la viga portapanel.",
    ],
    "E10_E11_Especificacion": [
        "El panel aísla mucho mejor que el vidrio (K ≈ 0,5), resiste fuego (F120) e impactos y casi no requiere mantenimiento.",
        "Es pesado (≈ 350 kg/m²): se monta con grúa, un panel por izaje.",
        "La viga portapanel recibe el peso de los paneles y lo lleva a los cuellos de las bases.",
    ],
    "Comparacion_1_Cortes": [
        "Los dos cerramientos se fijan al MISMO nudo (VL + viga L): la estructura no cambia, sólo la piel.",
        "Muro cortina: piel liviana delante de la estructura, con barrera cortafuego en la losa.",
        "Panel sándwich: piel pesada y aislante, abulonada a la VL y apoyada en la viga portapanel.",
    ],
    "Comparacion_2_Cuadro_Justificacion": [
        "Vidrio donde se necesita luz y visuales (fachada principal); panel opaco donde se necesita aislación y fuego (resto).",
        "Ambos son industrializados y en seco: se montan rápido y con los mismos equipos que la estructura.",
        "Para el parcial: saber explicar función, ventajas, desventajas y cómo se fija cada uno.",
    ],
}
