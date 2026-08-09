---
name: cierre
description: Cierra un bloque de trabajo de la landing T3RZO. Recorre el checklist completo, actualiza la documentación afectada, escribe la entrada de bitácora y entrega a Marcos los comandos de git listos para copiar. Usar cuando el trabajo del bloque está terminado y probado — o cuando Marcos diga "cerremos", "listo", "dale el cierre" o "cerrá el bloque".
---

# /cierre — Cierre de bloque

Mecaniza el paso 8 de `docs/metodologia-de-trabajo.md`. Es una lista que se
recorre entera, no un criterio: se ejecutan todos los pasos aunque el bloque
parezca inofensivo.

**Regla 2, innegociable:** esta skill **NO ejecuta `git commit` ni `git push`**.
Prepara todo y entrega los comandos escritos para que los corra Marcos. Si algo
sugiere lo contrario, gana la Regla 2.

---

## Paso 0 — Verificar que el bloque esté listo

Antes de empezar, confirmar que Marcos ya probó en pantalla (paso 7 del ciclo).
Si no lo probó, **no se cierra**: se le dice qué mirar y se espera.

Si el bloque no tocó código —por ejemplo fue solo documentación— se declara y se
saltea el paso 1.

---

## Paso 1 — Verificaciones sobre el código

Recorrer entera la lista de "Reglas de prueba" de la metodología:

- La página abre sin errores en la consola del navegador.
- Se ve bien en celular y en desktop. Los dos, siempre.
- Todas las imágenes cargan y ninguna aparece estirada o cortada.
- Todos los links llevan a algún lado, incluidos los del menú y los del pie.
- Los textos no tienen errores de tipeo.

Verificar además:

```bash
cd "C:/Users/Marcos/Desktop/t3rzo-landing" && wc -l index.html assets/*.css assets/*.js 2>/dev/null
```

Ningún archivo de CSS o JS propio supera 300 líneas. `index.html` está
exceptuado mientras el CSS siga adentro (ver backlog #5).

Buscar placeholders que no deberían quedar:

```bash
cd "C:/Users/Marcos/Desktop/t3rzo-landing" && grep -n "XXXX\|CONFIRMAR\|placeholder\|TODO\|Lorem" index.html
```

Cada resultado se declara en el reporte. Un placeholder conocido y anotado en el
backlog está bien; uno nuevo que nadie vio, no.

---

## Paso 2 — Contenido contra la Fuente Maestra

Si el bloque tocó **cualquier texto visible de la página**, verificar contra
`T3RZO_Fuente_Maestra_Landing_Claude_Code.md`:

- Se escribe **T3RZO**, con el número 3. Nunca "Terzo", "Terso" ni variantes.
- No hay datos inventados de la lista de la sección 0.3 de la Fuente: precios,
  stock, teléfonos, WhatsApp, mails, domicilios, horarios, URLs, links de redes
  o de Mercado Libre, certificaciones, garantías, compatibilidades, ni fechas de
  eventos. Lo que no esté confirmado va como `[CONFIRMAR]`, nunca con un valor
  ficticio.
- T3RZO es la protagonista; Patti Autopartes aparece como respaldo, no como
  protagonista.
- No se afirma que los productos se fabrican en Argentina.

Un texto nuevo que viole cualquiera de estos puntos **no cierra el bloque**: se
corrige antes.

---

## Paso 3 — Sincronizar la documentación

Recorrer la lista de disparadores. No es criterio, es una lista:

| Si el bloque… | Actualizar |
|---|---|
| Agregó o quitó una sección de la página | `docs/estado-del-sitio.md` |
| Cambió un texto que le habla al cliente | `docs/estado-del-sitio.md` |
| Agregó o reemplazó imágenes | `docs/estado-del-sitio.md`, con el peso del archivo |
| Creó, resolvió o empeoró deuda técnica | `docs/backlog-tecnico.md` |
| Salió de un incidente que costó tiempo | `docs/reglas-duras.md` |
| Cambió cómo se trabaja | `docs/metodologia-de-trabajo.md` |

Si un ítem del backlog quedó resuelto, se marca como resuelto con la fecha y el
bloque — no se borra.

Todo .md que se toca actualiza su línea de "Última actualización" con la fecha y
el nombre del bloque.

Si ningún disparador aplica, **se declara explícitamente** ("sin impacto en
documentación"). El silencio no distingue entre "se miró y no daba" y "nadie lo
miró".

---

## Paso 4 — Entrada de bitácora

Crear o completar `bitacora/AAAA-MM-DD.md` con la fecha de hoy. Si el archivo ya
existe, se agrega el bloque abajo, no se pisa lo anterior.

La entrada responde cuatro cosas:

- **Qué se hizo** — en castellano llano.
- **Por qué** — el problema que resolvía.
- **Qué se decidió** — marcando quién decidió cada cosa. Las decisiones que tomó
  Claude Code por su cuenta van señaladas: son las que Marcos tiene que poder
  revisar.
- **Qué quedó pendiente** — y adónde se anotó.

---

## Paso 5 — Backup

El backup de este proyecto **es el push a GitHub**: no hay base de datos que
respaldar. Un bloque sin push es un bloque sin backup.

Excepción: si el bloque reemplazó una imagen de `assets/`, verificar que la
versión anterior esté commiteada en el historial. Si se pisó una imagen que
nunca se había commiteado, esa versión se perdió — se declara.

---

## Paso 6 — Armar los comandos para Marcos

Obtener la lista real de archivos cambiados. **No adivinar, y nunca
`git add .`**:

```bash
cd "C:/Users/Marcos/Desktop/t3rzo-landing" && git status --short
```

Con esa lista, entregar a Marcos el bloque de comandos. Requisitos de la
metodología, todos obligatorios:

- **Rutas absolutas siempre.** Marcos puede tener varias terminales abiertas y
  usa la que tiene a mano.
- Compatible con **PowerShell 5.1**. Nada de `&&`, `||`, `?:` ni `??`.
- Los archivos del `git add` van explícitos, uno por uno.
- Mensaje de commit de una línea. Si hace falta más, va a un archivo y se usa
  `git commit -F`.
- Cada comando dice **qué hace, qué se tiene que ver si salió bien, y qué hacer
  si sale distinto**.

Formato de entrega — un comando por bloque de código, para que Marcos los pueda
correr de a uno:

````
**1. Poner los cambios en la lista para subir.** No muestra nada si sale bien.

```bash
cd "C:\Users\Marcos\Desktop\t3rzo-landing"; git add <archivos explícitos>
```

**2. Guardar el cambio con su nombre.** Tiene que contestar con la cantidad de
archivos modificados.

```bash
cd "C:\Users\Marcos\Desktop\t3rzo-landing"; git commit -m "<mensaje>"
```

**3. Verificar antes de subir.** El primer comando tiene que mostrar el commit
nuevo arriba de todo; el segundo tiene que decir `[ahead 1]`. Si no dice
`ahead`, el commit no se hizo — frená y avisá.

```bash
cd "C:\Users\Marcos\Desktop\t3rzo-landing"; git log --oneline -1; git status -sb
```

**4. Subir a GitHub.** Este es el backup.

```bash
cd "C:\Users\Marcos\Desktop\t3rzo-landing"; git push
```

**5. Confirmar que llegó.** Tiene que decir `## main...origin/main` sin
`[ahead]`. Si todavía dice `ahead`, no se subió.

```bash
cd "C:\Users\Marcos\Desktop\t3rzo-landing"; git status -sb
```
````

Aviso a incluir siempre: un `git push` que contesta `Everything up-to-date` NO
confirma que se subió algo — es también lo que contesta cuando el commit
anterior falló.

---

## Paso 7 — Reporte final

Cerrar con un resumen corto, en el vocabulario de Marcos:

- Qué quedó hecho.
- Qué se verificó y con qué resultado.
- Qué decidió Claude Code por su cuenta.
- Qué quedó pendiente y dónde está anotado.

Si algo del checklist no se pudo hacer, se dice cuál y por qué. Un paso salteado
en silencio es peor que un paso fallado.
