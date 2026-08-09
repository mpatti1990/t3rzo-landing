# Estado del sitio

Qué tiene la página HOY, sección por sección. Es el documento que lee una
conversación nueva para ubicarse sin abrir el código.

Regla: acá se describe **lo que existe**, no lo que se planea. Lo que falta va a
[backlog-tecnico.md](backlog-tecnico.md).

**Aviso sobre los textos.** El contenido de la página se escribió antes de que
[la Fuente Maestra](../T3RZO_Fuente_Maestra_Landing_Claude_Code.md) se
incorporara como fuente de verdad, y todavía no se auditó contra ella. Hay
textos con datos sin confirmar — están listados en el ítem #7 del backlog. Lo
que dice esta página hoy no es necesariamente lo que la marca aprueba decir.

---

## Resumen

| Dato | Valor |
|---|---|
| Tipo | Sitio estático de una sola página |
| Archivos | `index.html` (1149 líneas, CSS y JS incluidos) + `assets/` |
| Build | No hay. Se abre el archivo y funciona. |
| Dependencias | Ninguna instalada. Tipografías desde Google Fonts (pedido externo). |
| Repositorio | `mpatti1990/t3rzo-landing` |
| Publicado en | Todavía en ningún lado |

---

## Secciones de la página, en orden

| # | Sección | Ancla | Qué muestra |
|---|---|---|---|
| — | Encabezado | — | Logo, nombre, menú (Historia, Calidad, Productos, Contacto) y botón de WhatsApp |
| 1 | Hero | `#top` | Título principal, texto de propuesta, botones de WhatsApp y MercadoLibre, tres etiquetas, y un recuadro para video/imagen que **todavía es un placeholder** |
| 2 | Calidad | `#calidad` | Tres pilares: Calce Perfecto (FIT), Selección de proveedores (OEM), Ingeniería de nicho (NIC) |
| 3 | El legado | `#historia` | Línea de tiempo con la historia familiar del negocio |
| 4 | Especialidades | `#productos` | Tres tarjetas: Sondas Lambda, Inyectores, Válvulas EGR. Sin imágenes, solo texto |
| 5 | Hitos | `#hitos` | Automechanika Buenos Aires 2024-2026 y tres tarjetas de respaldo |
| 6 | Contacto | `#contacto` | Cinco canales: WhatsApp, Instagram, Facebook, TikTok y mail |
| 7 | Cierre | — | Panel final con los dos botones principales |
| — | Pie | — | Logo, "Casa central en Parque Avellaneda", año automático y cuatro links |

---

## Imágenes

| Archivo | Peso | Dónde se usa |
|---|---|---|
| `assets/logo-t3rzo.png` | 105 KB | Encabezado y pie |
| `assets/hero.jpg` | 226 KB | Fondo de la sección hero (vía CSS) |
| `assets/producto-1.jpg` | **19,1 MB** | **En ningún lado.** No está referenciada en el HTML |

---

## Links salientes

| Destino | Estado |
|---|---|
| Instagram `@t3rzoautopartes` | Real, apunta al perfil de la marca |
| Mail `ventas@t3rzoautopartes.com.ar` | Real |
| WhatsApp | **Placeholder** — 4 botones apuntan a `wa.me/54911XXXXXXXXX` |
| MercadoLibre | **Genérico** — 2 botones van a la home de MercadoLibre, no a la tienda |
| Facebook | **Genérico** — 2 links van a la home de Facebook |
| TikTok | **Genérico** — 2 links van a la home de TikTok |

---

## Comportamiento

- Las secciones aparecen con una animación al entrar en pantalla
  (`IntersectionObserver` sobre los elementos con clase `reveal`).
- El año del pie se completa solo con la fecha del navegador.
- No hay formularios. Todo el contacto sale por links externos.
- No hay analítica, ni cookies, ni scripts de terceros más allá de la
  tipografía de Google Fonts.

---

*Última actualización: 2026-08-09 — bloque METODOLOGIA.1*
