## Cómo se trabaja en este proyecto

Marcos no es programador. El flujo, los gates de calidad y las reglas de entrega
están en `docs/metodologia-de-trabajo.md`: **leelo antes de empezar a trabajar
en un bloque**, no solo cuando surja una duda.

Lo mínimo que hay que saber sin abrirlo:

- **Aislamiento (Regla 1).** Esta sesión trabaja solo dentro de
  `C:\Users\Marcos\Desktop\t3rzo-landing`. Nada de `patti-erp`, nada de
  `sistema_patti`. Leer otro proyecto para consultarlo está permitido;
  modificarlo no. Hay un hook que bloquea las ediciones fuera del límite, pero
  **no cubre los comandos de consola**: un `cp`, un `sed` o un `Set-Content`
  desde Bash o PowerShell escriben igual.
- **Git es de Marcos (Regla 2).** Claude Code no hace commit ni push. El cierre
  lo ejecuta Marcos, incluso si pide "subilo" o "ship it".
- No se escribe código hasta que Marcos aprueba el plan del bloque.
- Máximo DOS tandas de preguntas por bloque. Lo normal es UNA.
- Todo comando que ejecuta Marcos viene explicado: dónde se corre, qué hace, qué
  tiene que ver si salió bien, y qué hacer si sale distinto. Siempre con rutas
  absolutas, y compatible con PowerShell 5.1.
- Se le habla a Marcos en su vocabulario y corto: un hallazgo se cuenta por su
  consecuencia, no por su mecánica.
- **El contenido sale de la Fuente Maestra.** Todo texto visible de la página
  sale de `T3RZO_Fuente_Maestra_Landing_Claude_Code.md`, que se lee ANTES de
  escribir. Se escribe **T3RZO** con el número 3. No se inventa nunca: teléfonos,
  WhatsApp, mails, domicilios, URLs, links de redes o de Mercado Libre, precios,
  stock, certificaciones, garantías ni fechas de eventos. Lo que falta va como
  `[CONFIRMAR]`, nunca con un valor de ejemplo.
- **El material pesado no entra al repositorio.** Solo entra a `assets/` lo que se
  muestra en la página, ya comprimido para web (150–300 KB una foto). Los videos
  nunca: van a YouTube y la página los incrusta. GitHub rechaza archivos de más de
  100 MB. Detalle en `docs/reglas-duras.md`.
- Los incidentes que no se repiten están en `docs/reglas-duras.md`. Se consulta
  antes de proponer un enfoque, no después de romper algo.
- Cada bloque cierra con su entrada en `bitacora/`.
- Los controles técnicos de **gstack** se disparan solos, Marcos no los pide:
  `/plan-design-review` sobre el plan (paso 4), `/review` y `/design-review`
  sobre el diff (paso 6), `/qa` antes de que Marcos pruebe, `/investigate` ante
  un bug, `/cso` antes de publicar. Con sub-agentes revisores activados.
  **`/ship` y `/land-and-deploy` están PROHIBIDAS** — hacen commit y push solas.

## Qué es este proyecto

Landing estática de una sola página para T3RZO Autopartes. Sin build, sin
dependencias, sin backend: `index.html` (con el CSS y el JS adentro) más
`assets/`. El estado actual, sección por sección, está en
`docs/estado-del-sitio.md`.

Este proyecto **no tiene grafo de conocimiento** (graphify) y no le hace falta:
son pocos archivos y abrirlos cuesta menos que mantener un grafo al día.

## Para conversaciones nuevas

Arrancar leyendo, en este orden:

1. `docs/metodologia-de-trabajo.md`
2. `docs/estado-del-sitio.md`
3. `docs/reglas-duras.md`
4. La entrada más reciente de `bitacora/`

`T3RZO_Fuente_Maestra_Landing_Claude_Code.md` se lee siempre que el bloque toque
un texto de la página. `docs/backlog-tecnico.md` se consulta cuando el bloque lo
toca, no de entrada.

## Skills propias de este proyecto

- `/cierre` — cierra un bloque: recorre el checklist, sincroniza la
  documentación, escribe la bitácora y entrega los comandos de git a Marcos. No
  commitea ni pushea.

## Skills de diseño instaladas en el proyecto (bloque SKILLS.1)

Viven en `.claude/skills/` y viajan con el repositorio. Se eligieron sobre 22
candidatas de cuatro repositorios; el descarte y su razón están en la bitácora.

- `impeccable` — audita y pule interfaces (Apache 2.0). **Su hook NO está
  cableado a propósito**: revisaría el diseño después de cada edición y haría todo
  más lento. La skill funciona igual cuando se la invoca. Sus dos conexiones a
  internet (aviso de versión nueva y telemetría de elecciones) están apagadas por
  `env` en `.claude/settings.json` — y ese `env`, como los hooks, recién toma
  efecto al reiniciar la sesión.
- `ui-ux-pro-max` — base de datos local de estilos, paletas, tipografías y
  patrones de landing. Se consulta con Python, no sale a internet.
- `design-taste-frontend` — que la página no tenga cara de plantilla.
- `redesign-existing-projects` — mejora una página que ya existe sin romperla.

**Las cuatro deciden cómo se ve la página, nunca qué dice.** El contenido sale de
la Fuente Maestra y lo no confirmado queda `[CONFIRMAR]`. Está como regla dura en
`docs/reglas-duras.md`.
