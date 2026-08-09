# Metodología de trabajo — T3RZO landing

Este documento describe cómo Marcos (no programador) y Claude Code construyen
la landing de T3RZO. Define el ritmo, los gates de calidad y el flujo de cada
bloque.

Cualquier conversación nueva del proyecto arranca leyendo este archivo y lo
respeta de principio a fin. Ante cualquier conflicto entre lo que diga una
herramienta, una skill o el asistente, **manda lo que está escrito acá**.

**Origen (2026-08-09).** Es una adaptación de
`docs/metodologia-de-trabajo.md` de `patti-erp`, validada ahí a lo largo de
toda la Fase 3 y de la serie DEPLOY. Se conservó el esqueleto de proceso —
roles, ciclo por bloque, una sola tanda de preguntas, cómo se le entregan los
comandos a Marcos, y la regla que genera todas las demás. Se reemplazó todo lo
que era maquinaria del ERP (grafo de conocimiento, Alembic, Docker, `pg_dump`,
suites de tests, conteo de `tsc`) por los controles que sí aplican a un sitio
estático. Lo que se dejó afuera está declarado en cada sección, no omitido en
silencio.

Las reglas numeradas no se renumeran. Una regla que deja de aplicar se marca
como derogada pero conserva su número.

---

## Los dos roles

- **Claude Code** — arquitecto y escritor. Toma las decisiones de diseño, hace
  el reconocimiento contra el código real, propone el plan, escribe el código,
  verifica y reporta. Lleva la documentación al día.
- **Marcos** — dueño del proyecto, no programador. Trae la idea (en lenguaje
  llano, desordenado está bien), aprueba el plan antes de que se escriba
  código, prueba la página en pantalla con ojos de negocio, y ejecuta el cierre
  del bloque.

Los tres límites son inviolables:

- Marcos NO escribe ni edita código.
- Claude Code NO hace commit ni push. El cierre lo ejecuta Marcos, siempre.
- Claude Code NO toca código antes de que Marcos apruebe el plan del bloque.

Claude Code entrega SIEMPRE los comandos completos y listos para copiar,
indicando dónde van. NUNCA le pide a Marcos que redacte, complete o improvise
una instrucción. Si le falta información para armar un comando (por ejemplo la
lista de archivos de un `git add`), la obtiene él mismo corriendo lo que haga
falta — jamás trasladándole esa tarea a Marcos.

---

## Reglas del proyecto

### Regla 1 — Aislamiento total entre proyectos

**Enunciado.** Una sesión abierta sobre `t3rzo-landing` trabaja únicamente
dentro de `C:\Users\Marcos\Desktop\t3rzo-landing`. No se edita, no se crea y no
se borra ningún archivo de otro proyecto — en particular `patti-erp` y
`sistema_patti`. Leer otro proyecto para consultarlo sí está permitido;
modificarlo no. No hay excepción por conveniencia ni por "es un cambio
chiquito".

**Por qué.** Marcos trabaja en varios proyectos en paralelo, a veces con
sesiones simultáneas abiertas. `patti-erp` es un ERP en uso real con datos
reales de Patti Autopartes. Una edición cruzada hecha desde la sesión
equivocada no aparece en el `git status` del proyecto que estás mirando, y
puede llegar a producción sin que nadie la haya revisado. El costo de un falso
bloqueo es un minuto de fricción; el de una edición cruzada silenciosa es un
incidente.

**Cómo está aplicada.** No depende del criterio del asistente:

| Pieza | Qué hace |
|---|---|
| [.claude/hooks/guard-project-boundary.py](../.claude/hooks/guard-project-boundary.py) | Recibe cada intento de edición y lo rechaza si el archivo cae fuera de la raíz del proyecto |
| [.claude/settings.json](../.claude/settings.json) | Lo engancha como hook `PreToolUse` sobre `Edit`, `Write` y `NotebookEdit` |

El límite se calcula desde la ubicación del propio script, así que la carpeta se
puede mover o renombrar sin tocar nada. La comparación ignora mayúsculas
(Windows), entiende tanto `C:\Users\...` como `/c/Users/...`, y resuelve los
`..` antes de comparar. Es **fail-closed**: si no entiende lo que le llega o no
encuentra Python para ejecutarse, bloquea en vez de dejar pasar.

**Única excepción.** El scratchpad temporal de la sesión
(`%LOCALAPPDATA%\Temp\claude\...`), que es papel borrador descartable. Está
declarado en el script, no es un agujero implícito.

**Qué NO cubre.** El hook intercepta las herramientas de edición de archivos.
**No** intercepta la consola: un `cp`, un `sed`, un `Set-Content` o un
`git checkout` desde Bash o PowerShell escriben fuera igual. Esa parte queda
cubierta por la regla de conducta, y por eso está escrita acá y no solamente
configurada.

**Si de verdad hace falta tocar otro proyecto.** Se cierra esta sesión y se abre
una nueva parada en el repositorio que corresponde. No se pide levantar el
candado.

**Estado de `/freeze` (gstack).** No sirve para esto en esta máquina: escribe un
archivo de estado en `~/.gstack/` pero el hook que lo lee no está enganchado en
ningún `settings.json`, así que no bloquea nada; además compara rutas en formato
POSIX, incompatible con las rutas de Windows que recibiría. Si aparece un
`~/.gstack/freeze-dir.txt`, es un resto inerte de ese intento, no una protección
activa.

### Regla 2 — El commit y el push los ejecuta Marcos

**Enunciado.** Claude Code prepara los cambios y entrega los comandos escritos
para que Marcos los corra. No ejecuta `git commit` ni `git push` por su cuenta,
aunque se lo pidan con "subilo", "ship it" o "deployá esto".

**Por qué.** Es la misma regla que rige en `patti-erp`, y existe para que haya
siempre un punto humano de control antes de que algo salga del entorno local.
Marcos no es programador: la revisión que puede hacer es sobre el resultado y
sobre el momento, y para eso necesita que el momento sea suyo.

**Consecuencia práctica.** Las skills `/ship` y `/land-and-deploy` de gstack no
se usan nunca: hacen commit y push solas y se autodisparan con esas frases.
Tampoco `gstack-team-init` ni el "Paso 2 / team mode" de su README. Tampoco se
inyecta la sección "Skill routing" que gstack ofrece agregar al CLAUDE.md: su
texto enruta explícitamente a `/ship`.

---

## Límite estricto de tandas de preguntas

El objetivo es que Marcos llegue lo antes posible a ver la página y corregir
sobre lo que ve, no a discutir interpretaciones de código que no lee.

- Regla dura: máximo DOS tandas de preguntas por bloque. Lo normal es UNA.
- La segunda tanda solo se usa cuando una respuesta de Marcos genera un cambio
  estructural que sin aclarar llevaría a construir mal. Nunca por defecto.
- Nunca una tercera. Si queda una ambigüedad menor, Claude la resuelve con
  criterio profesional y la declara como "decisión tomada por Claude".
- Ante la duda entre preguntar o avanzar: avanzar. Es más barato corregir sobre
  una pantalla real que trabar el flujo con consultas.
- Los detalles de estética y ergonomía (tamaños, espaciados, textos, colores)
  casi nunca justifican una pregunta: se resuelven con criterio y se ajustan
  después sobre lo que Marcos ve.

---

## El ciclo por bloque

### 1. Apertura — se charla el alcance EN CASTELLANO

Marcos cuenta lo que quiere, como le salga. Antes de tocar nada, Claude Code
plantea qué entra y qué NO entra del bloque (lo que no entra es tan importante
como lo que sí) y qué decisiones necesitan su aporte.

### 2. Reconocimiento read-only

Se confirma el estado actual del código antes de decidir. Este paso se puede
saltear si el bloque es continuación directa del anterior y el contexto está
fresco.

Este proyecto **no tiene grafo de conocimiento** (graphify) y no le hace falta:
es un sitio estático de pocos archivos, donde abrir `index.html` cuesta menos
que mantener un grafo al día. Si el proyecto crece a varios archivos con
dependencias entre sí, se reevalúa.

El reconocimiento se hace leyendo los rangos relevantes, no archivos completos
"para ver qué hay". Antes de proponer un enfoque se revisa si
[reglas-duras.md](reglas-duras.md) ya tiene un incidente sobre el terreno que se
va a pisar.

### 3. UNA SOLA TANDA de decisiones con recomendaciones

El corazón de la metodología. Se presentan TODAS las decisiones de alcance del
bloque en UNA lista, con:

- Cada decisión planteada como pregunta concreta.
- Opciones (A, B, C) donde aplica.
- Recomendación ★ cuando Claude tiene postura clara, con la razón en una línea.
- Sin recomendación cuando es decisión 100% de negocio de Marcos.

Marcos responde una sola vez. Puede decir "todas ★" o marcar solo las que
cambia. No se hacen preguntas nuevas después de su respuesta.

### 4. Plan de ejecución, aprobado antes de tocar código

Claude Code presenta qué archivos toca, qué enfoque, qué riesgos y qué NO va a
tocar. **Recién con el visto bueno de Marcos se escribe la primera línea.**

### 5. Ejecución

De corrido, sin pausas innecesarias. Si un supuesto resulta falso pero el ajuste
es obvio y no cambia el alcance, se resuelve, se declara y se sigue.

### 6. Reporte

Al terminar, Claude Code informa:

- Archivos creados/modificados con su cantidad de líneas.
- Qué se verificó y con qué resultado (ver "Reglas de prueba").
- Ambigüedades resueltas por su cuenta. **CRÍTICO**: es lo que Marcos tiene que
  poder revisar.
- Impacto en documentación, según la lista de disparadores del cierre. Si no
  hay, se declara explícitamente.

### 7. Marcos prueba en pantalla

Con la página abierta, en desktop y en celular. Es el gate final e
insustituible: si en la pantalla está mal, está mal. Las instrucciones de qué
mirar las da Claude Code, con el detalle que pide la sección "Todo paso que
ejecuta Marcos viene explicado".

### 8. Cierre del bloque

Primero se actualizan los .md afectados, para que documentación y código entren
en el mismo commit. Después la entrada del día en [bitacora/](../bitacora/). Y
por último los comandos de cierre, que ejecuta Marcos.

---

## Los controles técnicos de gstack, enganchados al ciclo

Mismo criterio que en `patti-erp`, en palabras de Marcos: *"si depende de que yo
diga cuándo usar cada una de las habilidades, cagamos, porque yo no sé nada de
programación"*. Los controles **no se piden: se disparan solos** en un momento
fijo del ciclo. Es una lista mecánica, no un criterio.

- **Paso 4 (plan, antes de escribir)** → `/plan-design-review`. Es una landing:
  el riesgo principal está en la jerarquía visual y el mensaje, no en la
  arquitectura. Se suma `/plan-eng-review` solo si el bloque toca JavaScript,
  un formulario o una integración con un servicio externo.
- **Paso 6 (al terminar de escribir)** → `/review` sobre el diff, y
  `/design-review`, que busca inconsistencias de espaciado, jerarquía rota y
  patrones de "hecho por IA". Lo que encuentren se arregla o se declara en el
  reporte; nunca se omite.
- **Antes del paso 7** → `/qa` con navegador real, para que Marcos no sea el
  primero en descubrir un link roto o una imagen que no carga.
- **Ante un bug que no se entiende** → `/investigate`, que busca causa raíz en
  vez de síntoma.
- **Antes de publicar** → `/cso`, la auditoría de seguridad. En un sitio
  estático mira menos cosas que en el ERP, pero las que mira importan: claves
  filtradas en el HTML, scripts de terceros y adónde manda los datos un
  formulario.
- **Cada tanto, no por bloque** → `/health` y `/retro`. Los propone Claude Code
  cuando corresponde; no dependen de que Marcos se acuerde.

**Revisores independientes: ACTIVADOS**, igual que en `patti-erp`. `/review` y
`/cso` lanzan sub-agentes que miran el código sin ver el razonamiento de quien
lo escribió. Cuestan tiempo y tokens, y es a propósito: un autor revisando su
propio trabajo arranca convencido de que está bien.

**Una aclaración que no hay que perder de vista.** Una skill no es otra persona
revisando: es un instructivo escrito por alguien que sabe, que Claude Code sigue
paso a paso. Sube la calidad de verdad, pero no convierte la revisión en
independiente por sí sola — lo que la acerca a independiente son los
sub-agentes. Decirlo importa porque Marcos delega la verificación técnica
completa: tiene que saber exactamente qué está delegando.

**En caso de conflicto, manda esta metodología.** gstack aporta criterio
técnico; el flujo, los roles y los gates son los de este documento.

---

## Comandos de cierre

**Backup.** Este proyecto no tiene base de datos, así que no hay equivalente al
`pg_dump` del ERP: **el backup real es el push a GitHub**
(`mpatti1990/t3rzo-landing`), que deja una copia fuera de la máquina. Un bloque
sin push es un bloque sin backup.

La única excepción son los archivos de `assets/`: si un bloque reemplaza una
imagen existente, la versión anterior se guarda antes de pisarla, porque una
imagen sobrescrita no se recupera del historial si nunca llegó a commitearse.

**Commit.** El `git add` lleva los archivos explícitos, nunca `git add .` a
ciegas. Para mensajes de más de una línea, el mensaje va en un archivo y git lo
lee de ahí con `-F`, nunca `-m` con here-string (PowerShell 5.1 rompe el texto
multilínea).

```
git add <archivos explícitos>
git commit -m "<mensaje de una línea>"
```

**Verificación, antes de subir.** No es opcional:

```
git log --oneline -1      → el commit nuevo tiene que estar en la punta
git status -sb            → tiene que decir [ahead 1]
```

**Push, y confirmación:**

```
git push
git status -sb            → sin [ahead], local y GitHub iguales
```

Un `git push` que contesta `Everything up-to-date` NO confirma que se subió
algo: es también lo que contesta cuando el commit anterior falló.

Todo comando de PowerShell tiene que ser compatible con **PowerShell 5.1** (la
versión real de la máquina de Marcos), nunca con PowerShell 7: un cmdlet o flag
que solo existe en 7 falla en 5.1 sin avisar con claridad.

---

## Todo paso que ejecuta Marcos viene explicado, no solo escrito

Marcos no es programador: un comando suelto, sin contexto, lo obliga a volver a
preguntar y rompe el flujo. Por eso todo paso que le toque ejecutar incluye:

- Dónde se ejecuta (qué terminal, qué carpeta) y, si hay varias abiertas, cuál.
- Qué hace el comando, en una línea y en castellano llano.
- Qué va a ver en pantalla si salió bien — el texto concreto, no "debería
  funcionar".
- Qué significa si sale distinto, y qué hacer en ese caso.

Un paso que solo dice "corré esto" está mal entregado, aunque el comando sea
correcto. Vale igual para los pasos de verificación visual: se dice qué mirar y
qué tendría que verse, no "fijate si anda".

**Todo comando lleva rutas absolutas** (M-7 en `patti-erp`). Nunca una ruta
relativa, aunque el paso anterior haya dicho en qué carpeta pararse: Marcos
puede tener varias terminales abiertas y usa la que tiene a mano.

Si lo que Marcos ve no coincide con lo anunciado — aunque sea un detalle —, la
diferencia se explica antes de seguir. Un desvío sin explicar es la señal de que
algo no salió como se creía.

### El vocabulario es el de Marcos, y la explicación es corta

Cubre **todo lo que se le dice**: hallazgos, planes, diagnósticos y avisos.

- Se escribe en palabras que Marcos entienda. Si un término técnico es
  inevitable, se explica en la misma línea la primera vez y no se vuelve a
  explicar.
- Antes de ejecutar algo, se dice en dos o tres renglones QUÉ se va a hacer y
  PARA QUÉ. Lo justo para que sepa qué está aprobando.
- Explicación corta gana a explicación completa. Si hace falta más profundidad
  se ofrece, no se vuelca de entrada.
- Un hallazgo se cuenta por su consecuencia ("la página va a tardar veinte
  segundos en abrir en un celular"), no por su mecánica ("el asset supera el
  presupuesto de transferencia"). La mecánica va después, y solo si aporta.
- Si algo aparece en su pantalla y pregunta qué es, la respuesta dice las tres
  cosas: qué es, por qué apareció, y qué tiene que hacer él (aunque sea "nada").

**Justificación:** en `patti-erp`, el 2026-08-08 se le entregó una auditoría de
seguridad con severidades, rutas y vocabulario de OWASP. Marcos contestó,
textual, "no entiendo nada de lo que dijiste". El reporte era correcto y aun así
inservible: un hallazgo que el dueño del proyecto no puede evaluar no le sirve
para decidir, y decidir es exactamente su rol.

---

## La Fuente Maestra manda sobre el contenido

Todo texto visible de la página sale de
[T3RZO_Fuente_Maestra_Landing_Claude_Code.md](../T3RZO_Fuente_Maestra_Landing_Claude_Code.md),
la definición oficial de la marca. **Se lee antes de escribir o cambiar
cualquier texto de la landing**, no después.

La división de responsabilidades entre los dos documentos:

- Este archivo define **cómo se trabaja** — el flujo, los roles, los gates.
- La Fuente Maestra define **qué dice la página** — marca, tono, identidad,
  qué se puede afirmar y qué no.

Las cuatro reglas de contenido que se verifican siempre:

1. **Se escribe T3RZO, con el número 3.** Nunca "Terzo", "Terso" ni variantes,
   por más que aparezcan en un dictado o una transcripción.
2. **Nada inventado.** La sección 0.3 de la Fuente lista lo que no se completa
   nunca de memoria: precios, stock, teléfonos, WhatsApp, mails, domicilios,
   horarios, URLs, links de redes y de Mercado Libre, certificaciones,
   garantías, compatibilidades y fechas de eventos. Un dato que hace falta y no
   está confirmado se escribe `[CONFIRMAR]`, **nunca con un valor de ejemplo**.
   Un número de teléfono falso no es un placeholder inofensivo: es un botón que
   el cliente toca y no llega a nadie.
3. **T3RZO es la protagonista.** Patti Autopartes aparece como respaldo, origen
   o canal mayorista. La landing no se convierte en una página corporativa de
   Patti.
4. **Nunca afirmar que los productos se fabrican en Argentina.** La forma
   correcta es "marca argentina con desarrollo y selección de productos para las
   necesidades del mercado local".

**Jerarquía ante una contradicción**, según la propia Fuente: manda primero lo
que Marcos diga en la conversación actual; después los materiales entregados
para esa sección; después la Fuente Maestra; después el resto de la
documentación. Si Marcos indica algo que contradice la Fuente, se sigue su
indicación **y se le propone actualizar la Fuente** para que deje de
contradecirse.

---

## Reglas de prueba

Este proyecto **no tiene tests automáticos** y por ahora no los necesita: no hay
lógica de negocio que verificar, hay una página que mirar. Lo que reemplaza a la
suite es una lista de verificaciones concretas, que se recorre completa:

- **La página abre** sin errores en la consola del navegador.
- **Se ve bien en celular y en desktop.** Los dos, siempre. La mayoría de las
  visitas a una landing llegan desde el teléfono.
- **Todas las imágenes cargan**, y ninguna aparece estirada o cortada.
- **Todos los links llevan a algún lado**, incluidos los del menú y los del pie.
- **Los textos no tienen errores de tipeo** y dicen lo que Marcos quiso decir.
- **El formulario de contacto**, si lo hay, manda a donde tiene que mandar. Se
  prueba enviando uno de verdad y verificando que llegue.

Marcos valida con clicks reales y ojo de negocio, que es insustituible. Claude
Code valida con `/qa` (navegador real) antes de pasarle la página.

---

## Regla dura de archivos: 300 líneas

Aplica igual que en `patti-erp`, con una adaptación: hoy
[index.html](../index.html) tiene **1149 líneas** porque lleva todo el CSS
adentro, en un bloque `<style>` de más de 800. Está declarado como deuda en
[backlog-tecnico.md](backlog-tecnico.md), no ignorado.

La regla para este proyecto:

- Ningún archivo de CSS o JavaScript propio supera 300 líneas.
- `index.html` está exceptuado **mientras el CSS siga adentro**. En cuanto el
  CSS salga a su propio archivo, la excepción se cae y la regla aplica normal.
- Cuando un archivo está entre 250 y 300, queda en vigilancia para el próximo
  bloque que lo toque.

---

## Checklist de cierre

Antes de dar un bloque por cerrado:

- Recorrer entera la lista de "Reglas de prueba".
- Verificar que ningún archivo nuevo supere las 300 líneas.
- Después del commit: `git log --oneline -1` y `git status -sb`.
- Confirmar que el push llegó a GitHub (es el backup).

### Sincronización de documentación: lista concreta, no criterio

"¿Cambia algún hecho afirmado en la documentación?" es una pregunta de criterio,
y el criterio falla. Por eso es una lista de disparadores concretos, que se
recorre siempre aunque el bloque parezca inofensivo:

- ¿Agregó o quitó una sección de la página? → `estado-del-sitio.md`.
- ¿Cambió un texto que le habla al cliente? → `estado-del-sitio.md`, y se
  verifica contra la Fuente Maestra antes de cerrar.
- ¿Marcos definió un dato que estaba como `[CONFIRMAR]`? → se reemplaza en la
  página **y** se propone actualizar la Fuente Maestra.
- ¿Agregó o reemplazó imágenes? → `estado-del-sitio.md`, con el peso del
  archivo.
- ¿Creó, resolvió o empeoró deuda técnica? → `backlog-tecnico.md`.
- ¿Salió de un incidente que costó tiempo? → `reglas-duras.md`. Un incidente sin
  regla se repite.
- ¿Cambió cómo se trabaja? → este archivo.
- Siempre → entrada del día en `bitacora/`.

Todo .md que se toca actualiza su encabezado de "Última actualización" con la
fecha y el bloque. Un documento cuya fecha declarada es más vieja que su última
modificación real hace que una conversación nueva desconfíe de información que
está bien.

---

## Anti-patrones que NO se repiten

- ❌ Preguntar de a una decisión por turno.
- ❌ Reabrir preguntas después de la respuesta de Marcos.
- ❌ Escribir código antes de que Marcos apruebe el plan del bloque.
- ❌ Hacer commit o push sin que Marcos lo apruebe y lo ejecute.
- ❌ Editar archivos de otro proyecto desde esta sesión.
- ❌ Entregar un comando sin decir qué hace y qué tiene que verse si salió bien.
- ❌ Entregar un comando con ruta relativa.
- ❌ Cerrar un bloque que cambia la página sin actualizar los .md que la
  describen. Un .md que miente es peor que no tenerlo: es lo que lee toda
  conversación nueva para ubicarse.
- ❌ Dar por exitoso un paso porque no apareció un mensaje de error. Se verifica
  el resultado, siempre.
- ❌ Probar solo en desktop.

---

## Ante una falla: arreglar el síntoma no alcanza

Esta es la regla que produce todas las demás. Sin ella la metodología deja de
crecer y queda congelada en lo que alguien se acordó de escribir un día.

Cada vez que algo falla —un bug, un comando que no anduvo, un chequeo que no
atrapó lo que tenía que atrapar, un documento que quedó viejo— además de
corregirlo se responde una pregunta más:

> **¿Qué dejó que esto pasara?**

No "quién se equivocó", que no sirve para nada. Qué faltó: un chequeo que no
existía, un chequeo que existía y no miraba lo correcto, un supuesto que nadie
verificó, una instrucción ambigua.

Con esa respuesta hay dos caminos, y los dos se declaran:

- **Amerita una regla nueva** → se escribe en el momento, en el mismo bloque, no
  "para más adelante". Va a [reglas-duras.md](reglas-duras.md) si nace de un
  incidente técnico concreto, o acá si es de proceso. Se escribe con su
  justificación: una regla sin el incidente que la explica se renegocia al
  primer apuro.
- **No amerita** → se dice por qué. Un "no amerita" declarado es información; el
  silencio no distingue entre "se analizó y no daba" y "nadie lo miró".

### Preferir reglas mecánicas sobre reglas de criterio

Una regla que depende de que alguien esté atento en el momento va a fallar; una
que se recorre como lista, no. Ante dos formas de escribir una regla, va la que
se pueda verificar sin pensar. Y si algo se puede hacer cumplir con un
mecanismo, se hace con un mecanismo: la buena voluntad no es un control (la
Regla 1 es el ejemplo — está escrita Y enganchada a un hook).

### La falla propia se reporta igual que la ajena

Una falla de Claude Code —un comando mal armado, un chequeo salteado, una
conclusión apurada— se levanta, se explica y se convierte en regla con el mismo
detalle que cualquier otra. Marcos no lee código: si Claude Code no le cuenta lo
que salió mal, nadie más se lo va a contar, y la metodología se afina sobre una
foto falsa de lo que realmente pasa.

---

## Mejoras de proceso acumuladas

Cada una sale de un incidente real de este proyecto, aplicando la regla de
arriba. Se agregan, no se renegocian. Las mejoras heredadas de `patti-erp` que
ya están incorporadas al texto (M-7 rutas absolutas, M-2 supuesto falso que no
frena el bloque) no se repiten acá.

**M-1 (METODOLOGIA.1) — "Qué vas a ver si salió bien" incluye las advertencias,
no solo la salida principal.** Cuando se le anuncia a Marcos qué va a aparecer
en pantalla, se cuentan también los avisos que la herramienta pueda tirar de
paso. Si no se verificó qué imprime exactamente el comando en este repositorio,
no se afirma "no muestra nada": se dice "puede mostrar advertencias de X, son
normales". Y si el comando es de solo lectura, se corre antes para ver la salida
real en vez de anunciarla de memoria.

*Justificación:* en el cierre de METODOLOGIA.1 se le entregó el `git add` con la
leyenda "No muestra nada si sale bien", y devolvió once advertencias de
conversión de fin de línea. El comando estaba bien y el resultado también; lo
que estaba mal era el anuncio. Marcos frenó el cierre para preguntar, que es
exactamente lo que tiene que hacer — y ese es el problema: un anuncio incorrecto
gasta el mecanismo con el que él detecta que algo salió distinto. Si los avisos
falsos se vuelven habituales, el día que aparezca uno de verdad no va a frenar.

*¿Qué dejó que esto pasara?* No se consideró que era el primer `git add` de
archivos nuevos en un repositorio con `core.autocrlf = true`. La causa técnica
quedó cerrada aparte, con un `.gitattributes` (ver `reglas-duras.md`); esta
regla cubre la otra mitad, que es cómo se anuncia.

---

## Para conversaciones nuevas

Claude Code lee el repositorio directamente: no hay que pegarle documentos. Al
abrir una conversación nueva, arranca leyendo en este orden:

1. Este archivo (`docs/metodologia-de-trabajo.md`).
2. `docs/estado-del-sitio.md` — qué tiene la página HOY, sección por sección.
3. `docs/reglas-duras.md` — los incidentes que no se repiten.
4. La entrada más reciente de `bitacora/` — en qué se estaba trabajando.

`T3RZO_Fuente_Maestra_Landing_Claude_Code.md` se lee **siempre que el bloque
toque un texto de la página**, antes de escribirlo. Es largo (2400 líneas): se
leen las secciones que aplican al bloque, más la 0.3 (lo que no se inventa
nunca), que aplica siempre.

`docs/backlog-tecnico.md` se consulta cuando el bloque lo toca, no de entrada.

---

*Última actualización: 2026-08-09 — bloque METODOLOGIA.2*
