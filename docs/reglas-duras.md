# Reglas duras del proyecto

Reglas transversales acumuladas a partir de incidentes reales. No son
preferencias de estilo: cada una existe porque su ausencia ya rompió algo o hizo
perder tiempo en el diagnóstico de un problema. Este documento es acumulativo —
se agregan reglas, no se renegocian sin un incidente nuevo que lo justifique.

Se consulta **antes** de proponer un enfoque, no después de romper algo.

Cada regla se escribe con la misma estructura:

- **Enunciado** — qué se hace y qué no, en una frase verificable.
- **Justificación** — el incidente concreto que la motivó. Una regla sin el
  incidente que la explica se renegocia al primer apuro.

La diferencia con [metodologia-de-trabajo.md](metodologia-de-trabajo.md): allá
van las reglas de **proceso** (cómo se trabaja, quién hace qué, en qué orden);
acá van las reglas **técnicas** que salen de haberse quemado con algo concreto.

---

## Un hook de seguridad no vale hasta que se lo ve disparar

**Enunciado.** Cuando se instala un control automático que debe bloquear algo
(un hook, una validación, un chequeo), no se lo da por activo hasta haberlo
visto actuar. Se prueba de dos formas: que rechace el caso que tiene que
rechazar, y que deje pasar el caso normal. Un control que solo se probó en el
caso que bloquea puede estar bloqueando todo.

Además, todo control de este tipo se escribe **fail-closed**: si no puede
ejecutarse o no entiende lo que recibe, bloquea. Un control que ante la duda
deja pasar es un control que se apaga solo el día que más falta hace.

**Justificación:** el 2026-08-09 se corrió la skill `/freeze` de gstack para
aislar este proyecto de `patti-erp`. La skill informó éxito y escribió su
archivo de estado, pero el hook que debía leerlo no estaba enganchado en ningún
`settings.json` — no bloqueaba absolutamente nada. Encima comparaba rutas en
formato POSIX contra las rutas de Windows que iba a recibir, así que tampoco
habría funcionado estando cableado. Durante ese rato el proyecto se creía
protegido y no lo estaba. Se detectó solo porque se fue a leer el código del
hook en vez de confiar en el mensaje de éxito.

**Corolario que también salió de ahí:** una prueba que falla puede estar
delatando un error en la prueba, no en lo que se prueba. En la primera corrida
del hook nuevo el caso "bloquear" no bloqueaba; la causa era que el JSON de
prueba estaba mal armado (`printf` se había comido las barras invertidas de la
ruta de Windows) y el hook lo estaba rechazando con razón. Antes de tocar el
código que se está probando, se verifica que el caso de prueba sea válido.

**Verificado en vivo el 2026-08-09** (bloque METODOLOGIA.3), en la primera sesión
que arrancó con la carpeta `.claude/` ya existente. Cinco casos de punta a punta:
bloquea escribir un archivo nuevo dentro de `patti-erp`, bloquea una ruta que se
escapa con `..`, bloquea editar un archivo que ya existe afuera, y deja pasar
tanto la landing como el scratchpad. Hasta esa fecha el candado estaba escrito
pero nunca se lo había visto actuar.

**Segundo corolario — un intento cuenta como prueba solo si aparece el mensaje
del control.** En la primera vuelta de esa verificación, dos de cuatro intentos
no probaron nada: uno murió porque el texto a reemplazar no existía en el
archivo, el otro porque el archivo no existía. Claude Code valida la entrada de
`Edit` **antes** de correr el hook, así que esos intentos se rechazan sin que el
candado llegue a opinar. Los dos se veían iguales a "la edición no ocurrió" y
ninguno demostraba nada — leídos mal, habrían justificado reportar que el candado
no cubre las ediciones. El criterio de aprobado es que aparezca el texto del
propio control (acá, `[limite de proyecto] Bloqueado`), nunca la ausencia de un
cambio.

**Cómo se prueba el caso "editar un archivo que ya existe afuera".** Hace falta
un archivo real fuera del límite, y **nunca es un archivo de otro proyecto**: se
crea un centinela descartable (por ejemplo en el Escritorio), se intenta
editarlo, se verifica que su contenido quedó intacto y se lo borra. Ese centinela
se crea por consola, que es justamente lo que el candado no vigila — así que la
prueba deja demostrado, de paso, el agujero declarado en la Regla 1.

---

## PowerShell 5.1, no 7

**Enunciado.** Todo comando de PowerShell que se le entrega a Marcos tiene que
funcionar en **PowerShell 5.1**, que es la versión real de su máquina. Un cmdlet
o un flag que solo existe en PowerShell 7 falla sin avisar con claridad.

Consecuencias concretas ya conocidas:

- No existen los operadores `&&`, `||`, `?:` ni `??`.
- `Set-Content` y `Add-Content` escriben en la codificación del sistema; para un
  archivo que van a leer otras herramientas hay que pasar `-Encoding utf8`
  explícito.
- Para texto de varias líneas se usa un here-string de comillas simples con el
  `'@` de cierre pegado al margen izquierdo, o mejor: el texto va a un archivo y
  el comando lo lee de ahí.

**Justificación:** heredada de `patti-erp`, donde costó varios incidentes. Se
adopta acá de entrada en vez de esperar a repetirlos.

---

## Los archivos de este proyecto se leen en Git Bash y en Windows

**Enunciado.** Cualquier script o comparación de rutas que se escriba para este
proyecto tiene que entender los dos formatos: `C:\Users\...` (Windows) y
`/c/Users/...` (Git Bash), y comparar sin distinguir mayúsculas de minúsculas.

**Justificación:** la máquina de Marcos corre las dos cosas a la vez — la
terminal de Claude Code usa Git Bash, y las herramientas de edición reportan
rutas de Windows. El hook de la Regla 1 tuvo que contemplar ambos formatos
justamente por esto; un control que solo entiende uno de los dos no bloquea
nada o bloquea todo.

---

## Los fines de línea se fijan en `.gitattributes`, no en la máquina

**Enunciado.** El proyecto guarda todos los archivos de texto con fin de línea
LF, declarado en [.gitattributes](../.gitattributes) con `* text=auto eol=lf`.
Las imágenes y demás binarios se marcan `binary` para que git no los toque
nunca.

No se resuelve cambiando `core.autocrlf` en la máquina: esa configuración es
por computadora y por usuario, así que el mismo repositorio se comportaría
distinto en otra máquina. `.gitattributes` viaja adentro del repositorio.

**Justificación:** el 2026-08-09, el primer `git add` del proyecto devolvió once
advertencias de conversión de fin de línea. No rompieron nada, pero Marcos tuvo
que frenar el cierre y preguntar qué eran. La configuración que las produce
(`core.autocrlf = true`) es la default de Git para Windows y estaba puesta en la
máquina, no en el proyecto.

---

## Las skills de diseño deciden cómo se ve la página, nunca qué dice

**Enunciado.** Las skills de diseño instaladas (`impeccable`, `ui-ux-pro-max`,
`design-taste-frontend`, `redesign-existing-projects`) mandan sobre la forma:
jerarquía visual, tipografías, color, espaciado, movimiento, estructura. **No
mandan sobre el contenido.** Todo texto visible sigue saliendo de la Fuente
Maestra, y lo que no está confirmado sigue siendo `[CONFIRMAR]`. Si una skill
pide un dato para completar un bloque de diseño —un teléfono para el botón, una
cifra para un contador, un testimonio, una fecha— el dato no se inventa: se deja
el hueco marcado y se le pregunta a Marcos.

**Por qué.** Ninguna de estas skills sabe nada de T3RZO, y varias están escritas
para que el resultado se vea vendedor y completo. Un instructivo que premia la
página terminada empuja a rellenar huecos, y la sección 0.3 de la Fuente Maestra
prohíbe exactamente eso: teléfonos, precios, stock, URLs, certificaciones,
garantías y fechas de eventos. Un número de WhatsApp inventado para que el hero
"cierre bien" es un botón que el cliente toca y no llega a nadie.

**Justificación:** no sale de un incidente todavía, y se escribe igual porque el
riesgo es estructural: se instalaron cuatro skills cuyo objetivo declarado es que
la página quede impecable, en un proyecto donde hay cinco datos marcados
`[CONFIRMAR]` y dos ítems BLOQUEANTE en el backlog por datos inventados por una
plantilla. La regla existe para que el conflicto esté resuelto antes de que
aparezca, no después.

---

## El material pesado no entra al repositorio

**Enunciado.** Al repositorio entra únicamente el archivo que **se muestra en la
página**, ya redimensionado y comprimido para web. El resto del material —las
carpetas de fotos y videos originales— se queda afuera, donde está. Los videos
**nunca** entran: se publican en YouTube o Vimeo y la página los incrusta o los
enlaza.

Números de referencia, no criterio:

| Qué | Cuánto |
|---|---|
| Foto de producto o de ambiente para web | 150–300 KB |
| Imagen del hero (la de arriba, a pantalla completa) | hasta 500 KB |
| Logo o gráfico de color plano | PNG; una foto **nunca** va en PNG |
| Video alojado en el repositorio | 0 |

**Por qué.** Git guarda todas las versiones para siempre: una foto de 20 MB que
entra y después se reemplaza sigue pesando 20 MB en el repositorio de por vida, y
se descarga entera cada vez que alguien lo clona. Y hay un límite duro que no es
opinable: **GitHub rechaza cualquier archivo de más de 100 MB** y avisa a partir
de 50 MB. Un `git push` con un video de 222 MB adentro no se sube lento: falla.

**Justificación:** el 2026-08-09 Marcos preguntó si convenía copiar al proyecto
la carpeta `Desktop\imagenes para la pagina de t3rzo`. Se midió antes de
contestar: 828 MB en 75 archivos, con seis videos que suman 536 MB —dos de ellos
de 222 MB y 141 MB, los dos por encima del límite duro de GitHub— y fotos de
mercadería de hasta 31 MB guardadas en PNG, que es el formato equivocado para una
fotografía. El repositorio entero pesa hoy 20 MB. Copiar la carpeta lo habría
multiplicado por cuarenta y el push habría fallado. La pregunta llegó antes del
daño; la regla queda para que la próxima vez no dependa de que alguien pregunte.

---

---

## El recorte de fondo no se automatiza

**Qué pasó.** Marcos aportó fotos de packaging sobre fondo blanco. Se intentó
recortarles el fondo con un algoritmo, dos veces. La primera dejó el gris del
estudio pegado a la caja; la segunda, con el umbral más bajo, le comió pedazos a
la tapa. Mientras tanto Marcos ya tenía los recortes hechos a mano.

**La regla.** Claude Code **no recorta fondos**. Si una imagen necesita fondo
transparente, la trae Marcos ya recortada. Lo único permitido sobre una imagen es
bajarle el peso, sin tocar encuadre ni composición (Regla 4).

**Por qué es estructural y no un problema de parámetros.** El packaging es blanco
sobre fondo blanco. No hay umbral que separe una cosa de la otra sin romper una
de las dos. Medirlo lleva minutos; ajustar parámetros a ciegas, horas.

**Cómo se verifica que un recorte es real.** No alcanza con que el PNG tenga
canal alfa: puede estar entero opaco. Se mide el porcentaje transparente y se
comprueba que las cuatro esquinas lo sean. Un archivo con 48% de transparencia y
esquinas opacas tiene el recorte a medias.

*Incidente: 2026-08-12, bloque LANDING.1.*

---

## `height:auto` en las imágenes, siempre

**Qué pasó.** La caja del cierre se veía completamente deformada: estirada en
vertical. La causa: el `<img>` llevaba `width` y `height` en el HTML, y el CSS le
fijaba solo el ancho. El alto seguía tomándolo del atributo, así que quedaba de
340 píxeles de ancho por 734 de alto.

**La regla.** La regla global de imágenes lleva `height:auto`. Los atributos
`width` y `height` del HTML se conservan —reservan el espacio y evitan que la
página salte al cargar— pero el alto real lo calcula el navegador.

*Incidente: 2026-08-12, bloque LANDING.1.*

---

## Una animación automática no puede pisar el input del usuario

**Qué pasó.** La cinta de productos tenía una animación que le reescribía la
posición en cada cuadro. Cuando el usuario la movía con la rueda del mouse, el
cuadro siguiente le borraba el movimiento. Se veía congelada. La prueba
automatizada no lo detectó porque disparaba el evento y leía el resultado en el
mismo instante, antes de que la animación volviera a correr.

**La regla.** Si un elemento se anima solo **y** el usuario lo puede mover, las
dos cosas tienen que escribir sobre la misma propiedad y la del usuario tiene que
ganar. Ante la duda, se saca la animación automática: el movimiento del usuario
no se negocia.

**Corolario sobre las pruebas.** Un evento sintético leído en el mismo tick no
prueba que algo funcione en vivo. Cuando hay una animación en juego, se verifica
con el ojo o dejando pasar cuadros.

*Incidente: 2026-08-12, bloque LANDING.1.*

---

## Una skill de gstack puede tocar archivos del repositorio

**Qué pasó.** El navegador de pruebas de gstack (`browse`) creó una carpeta
`.gstack/` dentro del proyecto con sus registros, y **se agregó solo al
`.gitignore`**. El cambio era correcto, pero lo hizo una herramienta sin pedirlo.

**La regla.** Después de usar una herramienta de gstack se revisa `git status`
antes de cerrar. Un archivo del repositorio que cambió sin que nadie lo tocara se
declara en el reporte, aunque el cambio esté bien.

*Incidente: 2026-08-12, bloque LANDING.1.*

---

## Un fundido no convierte un fondo claro en transparente

**Enunciado.** Si el material viene sobre fondo **claro** y la página es
**oscura** (o al revés), un degradado hacia el color del fondo **no** va a
parecer un recorte: va a parecer un halo. No es cuestión de ajustar el radio ni
la suavidad, es cómo funciona la luz. Cuando el pedido es "que se vea flotando,
como una foto transparente", las únicas salidas reales son dos: que el material
venga con fondo transparente de verdad, o que venga con el fondo del mismo tono
que la página.

**Y el recorte no lo hace Claude Code** (ver la regla del recorte de fondo, más
arriba). Así que en la práctica la salida es pedir el material de nuevo.

**Antes de proponer un fundido, se compara el brillo de los dos fondos.** Si van
en direcciones opuestas, se dice que no va a funcionar en vez de intentarlo.

**Justificación:** el 2026-08-15 se le ofreció a Marcos un fundido para integrar
un video 360 de la caja, con fondo gris de estudio, sobre la piel azul oscuro de
la página. Eligió esa opción sobre una imagen fija de muestra, se construyó
entera —máscara medida contra la silueta real de la caja en los 282 cuadros,
color calibrado, video comprimido de 25,7 MB a 1,12 MB— y cuando la vio dijo
"queda horrible" y pidió volver a la foto. Tenía razón, y el problema no era la
ejecución: la opción no podía dar lo que él quería y **eso se sabía desde antes
de empezar**. Un catálogo de opciones donde una no puede cumplir el objetivo no
es una opción, es tiempo perdido.

*Incidente: 2026-08-15, bloque LANDING.2.*

---

## Un color que tiene que coincidir con el fondo se mide, no se copia el hex

**Enunciado.** Cuando un archivo lleva grabado adentro el color de fondo de la
página para fundirse con ella, **no alcanza con poner el mismo código de color**:
hay que abrir el archivo generado, leer el píxel de la esquina y compararlo
contra el color de la página. Los compresores mueven los colores. Y **se hace con
cada archivo que se publica**, no solo con el que uno tiene en la cabeza.

**Justificación:** el 2026-08-15, al meter el video de la caja, el compresor de
video corrió el azul `#0B0D24` tres niveles. Se detectó midiendo y se corrigió
calibrando el color de entrada. Pero la **imagen de arranque** del video se
generó a partir de ese mismo cuadro ya calibrado, y una imagen no pasa por el
compresor de video: se quedó con la corrección puesta y salió **cinco niveles más
clara** que la página. Marcos vio un rectángulo pegado y su comentario fue "parece
pegado en Paint". El chequeo existía y decía "las esquinas del video coinciden":
miraba el video y nadie miró el otro archivo.

*Incidente: 2026-08-15, bloque LANDING.2.*

---

## Un dato del sistema se confirma contra el comportamiento, no al revés

**Enunciado.** Cuando se lee una configuración de la máquina (el registro de
Windows, una variable de entorno, un archivo de ajustes) para explicar por qué
algo no funciona, esa lectura es una **hipótesis**, no una prueba. Si el
comportamiento observado la contradice, gana el comportamiento y la lectura está
mal hecha. No se le informa a Marcos una conclusión basada solo en la lectura.

**Justificación:** el 2026-08-15 el video no arrancaba. Se leyó el registro de
Windows para ver si Marcos tenía las animaciones apagadas —lo que haría que el
código, correctamente, no lo reprodujera— y se leyó **el bit equivocado**
(`MenuFade` en vez de `ClientAreaAnimation`). Con eso se le informó "tus
animaciones están activadas, así que no es eso", se descartó la causa real y se
reescribió el arranque del video para nada. Dos entregas seguidas fallaron por
el mismo motivo que se había descartado. El comportamiento ya lo estaba gritando:
la segunda versión mostró los controles del reproductor, y esos controles **solo**
los pone la rama de "menos movimiento".

*Incidente: 2026-08-15, bloque LANDING.2.*

---

## El texto legal se copia, no se redacta

**Enunciado.** Un documento legal que aporta Marcos (política de garantía,
términos, condiciones) se publica **copiado exacto**. No se resume, no se
"mejora" la redacción, no se corrigen inconsistencias por cuenta propia. Cambiar
el formato del título o pasar una lista a `<ul>` está bien; tocar una palabra del
contenido, no.

Si el documento se contradice con la realidad —por ejemplo dice que la versión
vigente está publicada en otro lado—, **se declara y lo corrige Marcos en el
documento original**, no Claude Code en la página.

Un resumen en otra parte de la página está permitido, pero tiene que ser fiel y
no puede borrar las distinciones que el documento hace a propósito. La política
de T3RZO regula la relación con el **comercio**, no con el consumidor final, a
quien lo ampara la Ley 24.240: mezclar las dos cosas en un resumen no es un error
de redacción, es un problema legal.

**Cómo se verifica:** comparando el texto publicado contra el original palabra por
palabra, con especial atención a los números —CUIT, plazos, importes, fechas— y
no leyéndolo por encima.

**Justificación:** no sale de un incidente. Se escribe el 2026-08-15, cuando entró
el primer documento legal al proyecto, porque el riesgo es evidente y el costo de
equivocarse no lo paga la página.

---

## El aire transparente de una imagen recibe los clicks igual

**Qué pasó.** El botón "Pedila por T3RZO" del cierre no llevaba a ningún lado. El
link estaba puesto y era el correcto. Lo que fallaba era otra cosa: la imagen de la
caja mide 920 px de ancho y **el 61% de eso es aire transparente**; el CSS la sube
con un margen negativo, así que el borde invisible de la imagen se metía **33 px
adentro de un botón de 59**. El aire no se ve, pero el navegador se lo cobra igual:
un click en el centro del botón lo recibía la foto. Solo funcionaba la franja de
arriba, que es justo donde nadie apunta.

**La regla.** Una imagen **decorativa** que se superpone a algo clickeable lleva
`pointer-events:none`. Y ojo con el tamaño real de un recorte: el archivo ocupa
todo su rectángulo, no la silueta que se ve. Un margen negativo sobre una imagen
con fondo transparente es exactamente la receta de este bug.

**Cómo se verifica — y esto es lo que faltaba.** No alcanza con mirar la página ni
con medir posiciones: hay que preguntarle al navegador **quién recibe el click** en
cada botón. Se recorren todos los elementos clickeables y en cada uno se consulta
`document.elementFromPoint` sobre su centro; si devuelve algo que no es el propio
botón, está tapado. Se corre en escritorio y en celular, porque los anchos
cambian con `vw` y el solapamiento también.

**Por qué es regla y no un arreglo suelto.** El bug lo introdujo LANDING.2, al
agrandar la caja de 132 a 356 px, y **ese bloque reportó el cierre como
verificado**: se habían medido las dimensiones, los pesos y los colores, pero
nadie probó tocar el botón. Es el mismo mecanismo de la M-9 — una lista de
verificaciones ciertas que omite justamente la que importaba. Marcos lo encontró
abriendo la página, que es el único control que quedaba.

*Incidente: 2026-08-16, bloque AUDITORIA.1.*

---

*Última actualización: 2026-08-16 — bloque AUDITORIA.1*
