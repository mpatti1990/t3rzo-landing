# Backlog técnico

Lo que falta, lo que está a medias y la deuda que se aceptó a propósito. Se
consulta cuando un bloque toca el terreno de un ítem, no de entrada.

**BLOQUEANTE** marca lo que no puede quedar sin resolver antes de publicar la
página. Antes de cualquier paso que ponga el sitio en línea se busca esa palabra
en este archivo y se verifica cada aparición, una por una. Es un `grep`, no un
criterio: no depende de que alguien se acuerde.

---

## #1 — Los botones de WhatsApp no llevan a ningún lado — BLOQUEANTE

Cuatro botones (encabezado, hero, contacto y cierre) apuntan a
`https://wa.me/54911XXXXXXXXX`, que es el número de ejemplo que quedó de la
plantilla. Un cliente que toca el botón principal de la página no llega a nadie.

**Qué hace falta:** el número real de WhatsApp de T3RZO.

Además viola la Fuente Maestra (sección 0.3): los teléfonos y el WhatsApp están
en la lista de datos que nunca se completan con un valor de ejemplo. Mientras no
esté el número real, va `[CONFIRMAR]` — o se saca el botón. Un botón que no
llega a nadie es peor que no tener botón.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

---

## #2 — Links de MercadoLibre, Facebook y TikTok van a la home — BLOQUEANTE

Seis links apuntan a la página principal de cada plataforma en vez de al perfil
o la tienda de T3RZO. El visitante que quiere comprar termina en el buscador de
MercadoLibre, no en la tienda de la marca.

**Qué hace falta:** las direcciones reales de la tienda de MercadoLibre y de los
perfiles de Facebook y TikTok. Si alguno no existe todavía, se saca el botón: un
link que no lleva a la marca es peor que no tenerlo.

Mismo caso que el #1: la Fuente Maestra (sección 0.3) prohíbe expresamente
inventar URLs, enlaces de Mercado Libre y enlaces de redes sociales.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

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

## #4 — El recuadro principal del hero es un placeholder

La caja grande de la sección de arriba dice "Placeholder de video o imagen hero"
con texto de instrucciones adentro. Es lo primero que ve un visitante.

**Qué hace falta:** el video institucional o la foto premium que va ahí.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

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

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

---

## #7 — La página nunca se auditó contra la Fuente Maestra

`T3RZO_Fuente_Maestra_Landing_Claude_Code.md` se incorporó como fuente de verdad
del contenido el 2026-08-09, cuando la página ya estaba escrita. Nunca se
compararon una contra otra en forma completa.

En una lectura rápida de la sección 0.3 de la Fuente (la lista de datos que no
se inventan) ya aparecen textos de la página que hay que confirmar o corregir:

| Texto en la página | Por qué hay que revisarlo |
|---|---|
| "50 años de maestría" y "50+ años de experiencia" | La Fuente dice que T3RZO nació en **2019** y que Patti tiene "décadas" de experiencia, sin dar un número. Un número exacto necesita confirmación |
| "3ra generación" | Mismo caso: cifra exacta no confirmada en las secciones leídas |
| "Automechanika Buenos Aires 2024-2026" | La Fuente prohíbe inventar fechas de eventos |
| "Casa central en Parque Avellaneda" | Los domicilios están en la lista de datos que no se completan de memoria |
| "Calidad OEM" / "Calidad de equipo original" | OEM es un tema válido para la marca, pero la Fuente prohíbe afirmar OEM sin confirmar |
| "Sondas Lambda", "Inyectores", "Válvulas EGR" | Hay que confirmar que sean líneas reales de T3RZO y no un ejemplo de la plantilla |

**Qué hace falta:** un bloque propio de auditoría de contenido, leyendo la
Fuente completa (2400 líneas) contra la página completa. Los ítems de la tabla
son lo que saltó en una lectura parcial — no es la lista final.

**Detectado:** 2026-08-09, bloque METODOLOGIA.1.

---

*Última actualización: 2026-08-09 — bloque METODOLOGIA.1*
