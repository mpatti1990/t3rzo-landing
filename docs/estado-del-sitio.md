# Estado del sitio

Qué tiene la página HOY, sección por sección. Es el documento que lee una
conversación nueva para ubicarse sin abrir el código.

Regla: acá se describe **lo que existe**, no lo que se planea. Lo que falta va a
[backlog-tecnico.md](backlog-tecnico.md).

**Aviso sobre los textos.** Todo el contenido visible se reescribió en el bloque
LANDING.1 tomándolo de
[la Fuente Maestra](../T3RZO_Fuente_Maestra_Landing_Claude_Code.md). Los textos
inventados que había antes ("50 años", "3ra generación", "Calidad OEM",
"Parque Avellaneda") se eliminaron. En LANDING.2 Marcos confirmó los dos datos
que faltaban —la feria y la política de garantía—, así que **ya no queda ningún
cartel amarillo `[CONFIRMAR]` a la vista en la página**.

---

## Resumen

| Dato | Valor |
|---|---|
| Tipo | Sitio estático de dos páginas |
| Archivos | `index.html` (1151 líneas, CSS y JS incluidos), `garantia.html` (201) + `assets/` |
| Build | No hay. Se abre el archivo y funciona. |
| Dependencias | Ninguna instalada. Tipografía Space Grotesk desde Google Fonts. |
| Peso que descarga el visitante | ~742 KB la landing, ~150 KB la de garantía |
| Repositorio | `mpatti1990/t3rzo-landing` |
| Publicado en | Todavía en ningún lado |

---

## Cómo se ve

Piel oscura de punta a punta sobre el azul marino de la marca, con **una sola
excepción declarada**: el encabezado y el pie son barras claras. Existen porque
el logo oficial es azul marino sobre transparente y sobre fondo oscuro no
contrasta; la alternativa era encerrarlo en un cuadrado blanco, que Marcos
rechazó. Las dos barras claras funcionan como marco del mundo oscuro.

- **Color:** azul `#20245C` estructural, verde `#00B541` como único acento de
  acción, rojo `#FF0000` **solo** dentro de la barra tricolor de marca.
- **Tipografía:** Space Grotesk.
- **Textura:** grano fijo muy sutil sobre toda la página, para que no se sienta
  plana.
- Las secciones aparecen con una entrada escalonada al entrar en pantalla.
  Respeta `prefers-reduced-motion`: si el sistema pide menos movimiento, todo se
  muestra quieto.

La dirección visual la dictaron las skills de diseño, no Claude Code (Regla 3).
El detalle de qué decidió cada una está en la bitácora del 2026-08-12.

---

## Secciones de la página, en orden

| # | Sección | Ancla | Qué muestra |
|---|---|---|---|
| — | Encabezado | — | Barra clara: logo, menú de 4 ítems y botón de WhatsApp |
| 1 | Hero | `#top` | Título de dos líneas, una frase, botón de WhatsApp y ancla a las líneas. A la derecha, foto real de producto sobre la caja |
| 2 | Cinta de productos | — | Doce piezas reales recortadas, en fila horizontal. Se mueve con la rueda del mouse, con el dedo y arrastrando |
| 3 | La marca | `#marca` | Qué es T3RZO, nacida en 2019, en dos columnas de texto |
| 4 | Pilares | — | Cuatro celdas: Calidad (con foto), Aplicación, Experiencia y Respaldo |
| 5 | Líneas | `#lineas` | Las seis familias de producto, en lista escalonada |
| 6 | La pieza correcta | `#pieza` | Placa técnica con los cinco datos que identifican una aplicación, y botón de consulta |
| 7 | Desarrollo | — | Los siete pasos, en riel horizontal |
| 8 | Historia y respaldo | `#respaldo` | Foto del stand a sangre con velo, texto y recuadro de Patti Autopartes. El pie de foto nombra **Automechanika Buenos Aires, ediciones 2024 y 2026** |
| 9 | Dónde conseguirla | `#comprar` | Dos caminos: casas de repuestos (WhatsApp de Patti) y consumidor final (Mercado Libre, con sello de **Tienda Oficial**) |
| 10 | Preguntas frecuentes | — | Seis preguntas en dos columnas, sin acordeón. La de garantía enlaza a la página de la política |
| 11 | Cierre | — | "Producto. Calidad. Desarrollo. Respaldo." y la caja |
| — | Pie | — | Barra clara: logo, cuatro links y año automático |

---

## La segunda página: `garantia.html`

La política de garantía completa, publicada como página propia dentro del mismo
sitio. Se llega desde dos lugares: el link "Leer la política completa" en la
pregunta de garantía, y "Garantía" en el pie.

- **El texto es una copia exacta** de `POLÍTICA DE GARANTÍA.doc`, el documento
  que aportó Marcos. Se verificó palabra por palabra: CUIT, domicilio, teléfono,
  la Ley 24.240, los cuatro plazos, la fecha de vigencia y las 12 exclusiones.
  Lo único que cambia es el formato del título.
- Diez secciones numeradas, misma piel que la landing (barras claras arriba y
  abajo, fondo azul, Space Grotesk), ancho de lectura de 75 caracteres por línea.
- Tiene estilos de impresión: en papel o PDF sale en fondo blanco y sin barras.
- Sus estilos viven aparte, en [assets/legal.css](../assets/legal.css) (81
  líneas), que **repite los colores y la tipografía** de `index.html` porque no
  hay hoja compartida todavía. Es deuda declarada, ver backlog #13.

**Pendiente que depende de Marcos:** el primer párrafo de la política dice que
"la versión vigente es la publicada en pattimap.com.ar". Como ahora está
publicada acá, esa frase quedó desactualizada. No se corrigió porque es texto
legal y lo cambia Marcos en el Word, no Claude Code en la página.

---

## Imágenes

Todas salen de `imagenes-para-la-pagina/`, que es la carpeta de Marcos
(Regla 4). Los originales pesan 97,5 MB en total; en la página pesan 720 KB.
**No se recortó ni se reencuadró ninguna**: los recortes con fondo transparente
vienen así del original.

| Archivo | Peso | Dónde se usa |
|---|---|---|
| `logo-t3rzo.png` | 108 KB | Encabezado y pie |
| `hero-producto-caja.webp` | 60 KB | Hero |
| `producto-caja-2.webp` | 68 KB | Celda "Calidad" |
| `p-01.webp` a `p-12.webp` | 12–44 KB c/u | Cinta de productos |
| `feria-1.webp` | 112 KB | Sección de respaldo |
| `caja.webp` | 55 KB | Cierre y página de garantía |

**Sobre `caja.webp`.** En LANDING.2 se re-exportó desde el original de Marcos
(`Diseño de cajas/Diseño caja T3RZO 1.png`, 6016×4016): pasó de 1100×1228 px y
33 KB a **1840×1228 px y 55 KB**. Mismo encuadre exacto, sin recortar nada; solo
más píxeles, porque en la página ahora se muestra al triple de tamaño y con el
archivo viejo se veía blanda en pantallas de alta resolución.

**Ojo con este archivo:** la caja ocupa apenas el **38,7% del ancho** de la
imagen y el resto es aire transparente, y además viene 39 px corrida a la
izquierda del centro. Por eso el CSS le pone un ancho mucho mayor de lo que
parece (hasta 920 px para que la caja se vea de 356), márgenes negativos que se
comen ese aire, y un `translateX` que centra la caja y no el archivo. Quien toque
ese bloque sin saberlo va a creer que los números están mal.

**En `assets/` pero sin usar:** `hero.jpg` (228 KB, la foto de feria vieja, la
reemplazó `feria-1.webp`) y `producto-1.jpg` (19,6 MB, backlog #3). Ninguna de
las dos se descarga, porque el HTML no las pide.

---

## Links salientes

| Destino | Estado |
|---|---|
| WhatsApp T3RZO (5 botones) | Real: +54 9 11 3767-7069 |
| WhatsApp Patti, casas de repuestos | Real: +54 9 11 6135-1111 |
| Mercado Libre (2 links) | Real, tienda de la marca |
| Instagram `@t3rzoautopartes` | Real |
| Facebook `facebook.com/t3rzo` | Real |
| Mail | **No aparece.** No existe todavía |
| TikTok | **No aparece.** No existe todavía |
| `garantia.html` (2 links: pregunta y pie) | Interno, la política completa |

Los botones de WhatsApp llevan un mensaje escrito de antemano, distinto según
desde dónde se toque.

---

## Comportamiento

- **La cinta de productos atrapa el scroll.** Con el cursor encima, la rueda
  mueve las piezas de costado en vez de bajar la página. Suelta al llegar a la
  punta o al sacar el cursor del bloque. Se arrastra con el mouse y se pasa con
  el dedo en el celular.
- El año del pie se completa solo con la fecha del navegador.
- Menú desplegable en celular, con el WhatsApp siempre visible como ícono.
- No hay formularios. Todo el contacto sale por links externos.
- No hay analítica, ni cookies, ni scripts de terceros más allá de la tipografía
  de Google Fonts.

---

*Última actualización: 2026-08-15 — bloque LANDING.2*
