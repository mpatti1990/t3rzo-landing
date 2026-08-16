# Backlog técnico

Lo que falta, lo que está a medias y la deuda que se aceptó a propósito. Se
consulta cuando un bloque toca el terreno de un ítem, no de entrada.

**BLOQUEANTE** marca lo que no puede quedar sin resolver antes de publicar la
página. Antes de cualquier paso que ponga el sitio en línea se busca esa palabra
en este archivo y se verifica cada aparición, una por una. Es un `grep`, no un
criterio: no depende de que alguien se acuerde.

---

## #1 — Los botones de WhatsApp no llevan a ningún lado — RESUELTO

Cuatro botones (encabezado, hero, contacto y cierre) apuntan a
`https://wa.me/54911XXXXXXXXX`, que es el número de ejemplo que quedó de la
plantilla. Un cliente que toca el botón principal de la página no llega a nadie.

**Qué hace falta:** el número real de WhatsApp de T3RZO.

Además viola la Fuente Maestra (sección 0.3): los teléfonos y el WhatsApp están
en la lista de datos que nunca se completan con un valor de ejemplo. Mientras no
esté el número real, va `[CONFIRMAR]` — o se saca el botón. Un botón que no
llega a nadie es peor que no tener botón.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.
**Resuelto:** 2026-08-12, bloque LANDING.1. Marcos aportó el número real
(+54 9 11 3767-7069) y el de Patti para casas de repuestos
(+54 9 11 6135-1111). Los cinco botones apuntan ahí, con mensaje escrito de
antemano segun desde donde se toque.

---

## #2 — Links de MercadoLibre, Facebook y TikTok van a la home — RESUELTO

Seis links apuntan a la página principal de cada plataforma en vez de al perfil
o la tienda de T3RZO. El visitante que quiere comprar termina en el buscador de
MercadoLibre, no en la tienda de la marca.

**Qué hace falta:** las direcciones reales de la tienda de MercadoLibre y de los
perfiles de Facebook y TikTok. Si alguno no existe todavía, se saca el botón: un
link que no lleva a la marca es peor que no tenerlo.

Mismo caso que el #1: la Fuente Maestra (sección 0.3) prohíbe expresamente
inventar URLs, enlaces de Mercado Libre y enlaces de redes sociales.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.
**Resuelto:** 2026-08-12, bloque LANDING.1. Mercado Libre, Instagram y Facebook
apuntan a los destinos reales. Mail y TikTok **no existen todavía**: en vez de
dejarlos apagados, directamente no aparecen en la página.

---

## #3 — `assets/producto-1.jpg` pesa 19 MB y no se usa

El archivo está en el repositorio y en el historial de git, pero el HTML no lo
referencia en ningún lado. Hoy no afecta a quien visita la página (no se
descarga porque nadie la pide), pero sí hace pesado el repositorio, y si alguien
la usa tal cual está, la página pasaría a tardar cerca de un minuto en abrir
desde un celular.

**Qué hace falta:** decidir si la imagen se usa o se saca. Si se usa, primero se
achica — una foto de producto para web debería pesar entre 150 y 300 KB, no 19
MB. Borrarla del repositorio no la borra del historial de git; eso es un paso
aparte y solo vale la pena si el peso del repo llega a molestar.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

---

## #4 — El recuadro principal del hero es un placeholder — RESUELTO

La caja grande de la sección de arriba dice "Placeholder de video o imagen hero"
con texto de instrucciones adentro. Es lo primero que ve un visitante.

**Qué hace falta:** el video institucional o la foto premium que va ahí.

**El material existe** (relevado el 2026-08-09, bloque SKILLS.1): en
`C:\Users\Marcos\Desktop\imagenes para la pagina de t3rzo` hay tres videos
candidatos (`DDA 5.mp4`, `DDA 6.mp4`, `DDA 7.mp4`) y fotos de cámara profesional
(`_MAP*.JPG`). Los videos **no** se copian al repositorio: van a YouTube y la
página los incrusta (ver `reglas-duras.md`). Falta que Marcos elija.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.
**Resuelto:** 2026-08-12, bloque LANDING.1. En el hero va una foto real de
producto sobre la caja de la marca, recortada. Ya no hay ningún placeholder
visible fuera de los dos `[CONFIRMAR]` declarados.

---

## #5 — `index.html` tiene 1149 líneas con todo el CSS adentro

Más de 800 líneas del archivo son el bloque `<style>`. Funciona perfecto y para
una página sola no es un problema de rendimiento; es un problema de trabajo:
cada cambio de estilo obliga a navegar un archivo largo, y el navegador no puede
cachear los estilos por separado.

**Deuda aceptada a propósito**, no un error. Se resuelve sacando el CSS a
`assets/styles.css` y el JavaScript a `assets/main.js`. Mientras el CSS siga
adentro, `index.html` está exceptuado de la regla de 300 líneas (ver
[metodologia-de-trabajo.md](metodologia-de-trabajo.md)).

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

---

## #6 — La página no está publicada en ningún lado

Vive solo en la máquina de Marcos y en GitHub. No hay dominio ni hosting
configurado.

**Qué hace falta:** decidir dónde se publica. Para un sitio estático como este,
GitHub Pages es gratis y sale de este mismo repositorio.

**Dos dominios de la marca, medidos el 2026-08-15 contra el resolutor del sistema
y contra el público de Google:**

| Dominio | Estado |
|---|---|
| `pattimap.com.ar` | Registrado, pero **sin sitio**: devuelve el registro de zona y ninguna dirección |
| `t3rzo.com.ar` | **No resuelve** |

**Atado a este ítem, para que no se pierda:** cuando el sitio esté publicado y
tenga dirección definitiva, hay que **volver a la política de garantía y poner esa
dirección**. Hoy el documento dice "la versión vigente es la que Patti Autopartes
publica en su sitio oficial", sin nombrar ninguna, justamente porque todavía no
hay ninguna que responda. Es el paso que cierra el circuito del punto 10 de la
política, que obliga a que exista un lugar donde consultar la versión vigente.

**También atado a este ítem (2026-08-16, AUDITORIA.1): la imagen que se ve cuando
alguien comparte la página.** El `og:image` de `index.html` apunta a
`assets/hero-producto-caja.webp` con dirección relativa. WhatsApp, Facebook e
Instagram necesitan la dirección completa (`https://dominio/assets/...`) para
poder bajarla: tal como está hoy, el link compartido saldría **sin foto**. No se
puede arreglar hasta que haya dominio, porque la dirección completa todavía no
existe. Cuando se publique el sitio, se corrige junto con la dirección de la
política de garantía.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1. **Ampliado:** 2026-08-15, LANDING.2,
y 2026-08-16, AUDITORIA.1.

---

## #7 — La página nunca se auditó contra la Fuente Maestra — RESUELTO

`T3RZO_Fuente_Maestra_Landing_Claude_Code.md` se incorporó como fuente de verdad
del contenido el 2026-08-09, cuando la página ya estaba escrita. Nunca se
compararon una contra otra en forma completa.

**RESUELTO el 2026-08-16, bloque AUDITORIA.1.** Se leyeron los 2425 renglones de
la Fuente contra la página entera y el marco de `garantia.html`. Resultado:

- **La página no inventa nada sobre la marca.** Título, descripción, hero, marca,
  pilares, líneas, la placa de la pieza correcta, los pasos del desarrollo, el
  respaldo, los dos caminos de compra, las seis preguntas y el cierre salen de la
  Fuente, casi siempre textuales. Las cuatro reglas de contenido pasan: T3RZO con
  el 3, ningún dato de contacto inventado, T3RZO protagonista y Patti como
  respaldo, y en ningún lado se afirma fabricación en Argentina.
- **Sí inventaba los nombres de las piezas.** Las catorce fotos de producto tenían
  nombres deducidos de mirar la foto. Marcos los confirmó uno por uno: **trece
  estaban bien y uno estaba mal** — lo que la página llamaba *válvula EGR* es una
  bomba de agua eléctrica. Corregido. La lista completa quedó en la Fuente,
  sección 13, para que no haya que volver a preguntarla.
- **Una frase sin confirmar quedaba blindada dentro de la Fuente** (el superlativo
  de Automechanika). Marcos la confirmó y de ahí sale la **M-10** de la
  metodología.
- **Dos correcciones menores:** la pregunta de dónde comprar decía "presencia
  oficial" donde el resto de la página dice **Tienda Oficial**, y `garantia.html`
  declaraba español neutro en vez de español de Argentina.

**Lo que la tabla de abajo pedía revisar ya no aplica.** Cuatro de sus seis
renglones ("50 años", "3ra generación", "Parque Avellaneda", "Calidad OEM") son
textos que LANDING.1 borró de la página el 2026-08-12; la tabla quedó describiendo
una versión que ya no existía. Se conserva como historia de qué se sospechaba:

| Texto en la página | Por qué hay que revisarlo |
|---|---|
| "50 años de maestría" y "50+ años de experiencia" | La Fuente dice que T3RZO nació en **2019** y que Patti tiene "décadas" de experiencia, sin dar un número. Un número exacto necesita confirmación |
| "3ra generación" | Mismo caso: cifra exacta no confirmada en las secciones leídas |
| ~~"Automechanika Buenos Aires 2024-2026"~~ | **RESUELTO 2026-08-15 (LANDING.2).** Marcos confirmó las ediciones 2024 y 2026 de Buenos Aires, las dos ya realizadas. Publicado en el pie de la foto del stand |
| "Casa central en Parque Avellaneda" | Los domicilios están en la lista de datos que no se completan de memoria |
| "Calidad OEM" / "Calidad de equipo original" | OEM es un tema válido para la marca, pero la Fuente prohíbe afirmar OEM sin confirmar |
| "Sondas Lambda", "Inyectores", "Válvulas EGR" | Hay que confirmar que sean líneas reales de T3RZO y no un ejemplo de la plantilla |

**Avance parcial 2026-08-15 (LANDING.2):** se resolvieron los dos `[CONFIRMAR]`
que quedaban visibles en la página (la feria y la política de garantía) y se
confirmó la Tienda Oficial de Mercado Libre.

**Lección que deja este ítem.** Un ítem de backlog que enumera hallazgos envejece
igual que el código: cuatro de sus seis renglones estaban resueltos hacía cuatro
días y el ítem seguía pidiéndolos. Un bloque que arranca de un backlog viejo
empieza verificando que el problema todavía exista.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1. **Resuelto:** 2026-08-16,
bloque AUDITORIA.1.

---

## #8 — Hay material real de T3RZO sin seleccionar ni preparar

Marcos tiene el material que la página necesita, pero todavía no entró: fotos de
Automechanika 2024 y 2026, de mercadería, de las cajas, y videos de entrevistas
en TV, streaming y podcasts. Relevado el 2026-08-09 (bloque SKILLS.1).

Lo que se midió en `Desktop\imagenes para la pagina de t3rzo` (828 MB, 75
archivos):

| Grupo | Estado |
|---|---|
| 6 videos `.mp4` (536 MB, dos de 222 y 141 MB) | van a YouTube, no al repositorio |
| `FotoMercaderia-*.png` (hasta 31 MB) | fotos en PNG: formato equivocado, hay que pasarlas a JPG/WebP y achicarlas ~100 veces |
| `_MAP*.JPG` (5–11 MB, cámara profesional) | candidatas al hero y a secciones |
| `Diseño caja T3RZO *.png` | candidatas a la sección de producto |
| `META_*_1080x1920.jpg` | creativos verticales de publicidad para Instagram; no son material de landing |
| Fotos numeradas (`3184400.png` y similares, 0,1–0,5 MB) | ya livianas, hay que ver qué son |

Las carpetas originales (`Automechanika 2026` con 20 GB, `Videos mercaderia` con
22 GB, `Videos Automechanika` con 14 GB) **no se tocan**: son el archivo de
material, no parte del sitio.

**Qué hace falta:** que Marcos elija qué se muestra y en qué sección. Después la
conversión la hace Claude Code con Pillow (Python), que está instalado. `ffmpeg`
y `ImageMagick` **no** están en la máquina, así que el video no se puede procesar
localmente — otro motivo para que vaya a YouTube.

**Ojo con los derechos:** un clip de un programa de TV o de un podcast es del
canal o del programa, no de T3RZO. Enlazar al original es seguro; alojar una copia
propia, no necesariamente.

**Detectado:** 2026-08-09, bloque SKILLS.1.

---

---

## #9 — El video 360 de la caja — DESCARTADO

Marcos generó el video (`imagenes-para-la-pagina/Video de caja 360/`, 25,7 MB,
1920×1080, 11,8 s, vuelta completa que cierra sin salto) y en LANDING.2 se probó
en el cierre. **Se descartó y la página volvió a la foto quieta.**

Por qué no sirvió, en orden de importancia:

1. **El fondo del video es gris claro y la página es azul oscuro.** Se intentó
   disolverlo con un fundido y no alcanza: un degradado de claro a oscuro da un
   halo, nunca un recorte. Marcos quería la caja "como si fuera una foto
   transparente" y por ahí no se llega. Ver la regla nueva en `reglas-duras.md`.
2. **Tiene la marca de agua de IA** (la estrellita de Gemini) abajo a la derecha,
   en todos los cuadros. Recortarla está prohibido por la Regla 4.
3. **El texto chico de la caja está mal escrito**: dice "Dizzribu/dor ezzlusivo"
   donde la caja real dice "Distribuidor exclusivo". Se lee si se muestra grande.

**CERRADO el 2026-08-15 por decisión de Marcos: "el video olvidate, no va".** No
se va a regenerar y el cierre de la página se queda con la foto de la caja, que
en LANDING.2 pasó a verse casi tres veces más grande. **Este ítem no espera nada
de nadie.**

Si algún día se retoma, lo que quedó averiguado y no hay que volver a investigar:

- El video comprime a **1,12 MB** en 1280×720 sin audio, con `imageio-ffmpeg`, que
  ya está instalado en la máquina.
- El material tendría que venir con **fondo negro liso**, sin degradado de estudio
  ni piso visible. Con fondo claro no hay forma de integrarlo a una página oscura.
- El reproductor arranca por el atributo `autoplay` del HTML, nunca por
  JavaScript, que varios navegadores rechazan.

**Detectado:** 2026-08-12, bloque LANDING.1. **Cerrado:** 2026-08-15, LANDING.2.

---

## #10 — El podcast Detrás del Algoritmo no está en la página

Marcos aportó tres fragmentos de la entrevista que Mariano Sirena le hizo a su
hermano sobre Patti y T3RZO (452 MB en `imagenes-para-la-pagina/`). Es prueba
social fuerte y todavía no aparece.

**Qué hace falta:** los links de YouTube. Marcos mencionó seis fragmentos y hay
tres archivos: pueden faltar tres.

**Ojo con los derechos:** el video es del podcast, no de T3RZO. Enlazar al
original es seguro; alojar una copia propia, no necesariamente.

**Detectado:** 2026-08-12, bloque LANDING.1.

---

## #11 — Una de las fotos de packaging tiene el recorte incompleto

`imagenes-para-la-pagina/Diseño de cajas/FotoMercaderia+caja.png` conserva un
rectángulo gris de fondo: el recorte no llegó a los bordes. Medido: 48% de
transparencia y las cuatro esquinas opacas, contra 66% y esquinas limpias en las
otras dos.

Se usó una de las buenas en su lugar. Si se quiere usar esa foto, hay que
rehacerle el recorte.

**Detectado:** 2026-08-12, bloque LANDING.1.

---

## #12 — El candado de la Regla 1 lanza una consola por cada edición

El hook que impide editar fuera del proyecto se dispara en cada Edit y Write, y
cada disparo lanza un proceso de Python desde la consola. En Windows eso abre una
ventana que a veces roba el foco. Un bloque que toca `index.html` veinte veces
son veinte ventanas.

**Deuda aceptada a propósito:** el candado protege un ERP con datos reales. Bajar
la frecuencia sin debilitarlo es un bloque de trabajo aparte, y hay que probarlo
en vivo antes de confiar en él.

**Detectado:** 2026-08-12, bloque LANDING.1, a partir de una queja de Marcos.

---

---

## #13 — `assets/legal.css` repite los colores y la tipografía de `index.html`

La página de garantía tiene su propia hoja de estilos y ahí se volvieron a
declarar los mismos tokens que viven dentro del `<style>` de `index.html`: los
colores de marca, las superficies, la tipografía. Si mañana cambia un color hay
que tocarlo en dos lados, y si alguien se olvida de uno las dos páginas dejan de
parecerse.

**Qué hace falta:** resolver antes el ítem #5 (sacar el CSS de `index.html` a
`assets/styles.css`). Con eso hecho, `legal.css` importa los tokens de ahí en vez
de redeclararlos. Está anotado como comentario en la cabecera del propio archivo,
para que quien lo abra lo sepa sin leer este backlog.

**Deuda aceptada a propósito:** la alternativa era hacer el refactor completo del
CSS dentro de un bloque cuyo alcance era publicar un documento legal.

**Detectado:** 2026-08-15, bloque LANDING.2.

---

## #14 — La clase `.pendiente` quedó sin usar

El cartel amarillo que marcaba los datos sin confirmar ya no se usa en ninguna
parte de la página: los dos `[CONFIRMAR]` que quedaban se resolvieron en
LANDING.2. La regla CSS sigue en `index.html`.

**No se borró a propósito:** es la convención del proyecto para marcar un dato no
confirmado, y van a aparecer más. Si dentro de unos bloques sigue sin usarse, se
saca.

**Detectado:** 2026-08-15, bloque LANDING.2.

---

## #15 — Falta la sección "Calidad y detalle" que pide la Fuente

La Fuente Maestra (sección 28.8) pide un bloque titulado **"Los detalles también
hablan de calidad"**, con fotos macro reales: un conector, una junta, un encastre,
un mecanizado, una terminación. Es la forma que la propia Fuente elige para
demostrar calidad sin decir "somos los mejores" — señales concretas en vez de
adjetivos (sección 11).

La página no lo tiene. Hoy la calidad se cuenta con palabras en el pilar "Calidad"
y con la foto de producto sobre la caja, que no es un macro.

**Qué hace falta:** que Marcos elija fotos de detalle. En
`imagenes-para-la-pagina/Productos/` hay fotos de cámara profesional (`_MAP*.png`)
que podrían servir, pero **la elección es suya** (Regla 4).

**Por qué no se hizo en el bloque donde se detectó:** agregar una sección cambia
cómo se ve la página, y eso dispara la Regla 3 — se abren las skills de diseño y
se propone antes de escribir. Decisión de Marcos en la apertura de AUDITORIA.1:
lo que aparezca a nivel sección se anota y se decide aparte.

**Detectado:** 2026-08-16, bloque AUDITORIA.1.

---

*Última actualización: 2026-08-16 — bloque AUDITORIA.1*
