# Estado del sitio

Qué tiene la página HOY, sección por sección. Es el documento que lee una
conversación nueva para ubicarse sin abrir el código.

Regla: acá se describe **lo que existe**, no lo que se planea. Lo que falta va a
[backlog-tecnico.md](backlog-tecnico.md).

**Aviso sobre los textos.** Todo el contenido visible se reescribió en el bloque
LANDING.1 tomándolo de
[la Fuente Maestra](../T3RZO_Fuente_Maestra_Landing_Claude_Code.md). Los textos
inventados que había antes ("50 años", "3ra generación", "Calidad OEM",
"Automechanika 2024-2026", "Parque Avellaneda") se eliminaron. Quedan dos datos
sin confirmar, marcados a la vista con un cartel amarillo `[CONFIRMAR]`.

---

## Resumen

| Dato | Valor |
|---|---|
| Tipo | Sitio estático de una sola página |
| Archivos | `index.html` (1103 líneas, CSS y JS incluidos) + `assets/` |
| Build | No hay. Se abre el archivo y funciona. |
| Dependencias | Ninguna instalada. Tipografía Space Grotesk desde Google Fonts. |
| Peso que descarga el visitante | ~720 KB |
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
| 8 | Historia y respaldo | `#respaldo` | Foto del stand a sangre con velo, texto y recuadro de Patti Autopartes |
| 9 | Dónde conseguirla | `#comprar` | Dos caminos: casas de repuestos (WhatsApp de Patti) y consumidor final (Mercado Libre) |
| 10 | Preguntas frecuentes | — | Seis preguntas en dos columnas, sin acordeón |
| 11 | Cierre | — | "Producto. Calidad. Desarrollo. Respaldo." y la caja |
| — | Pie | — | Barra clara: logo, tres links y año automático |

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
| `caja.webp` | 36 KB | Cierre |

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

*Última actualización: 2026-08-12 — bloque LANDING.1*
