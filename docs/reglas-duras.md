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

*Última actualización: 2026-08-09 — bloque METODOLOGIA.3*
