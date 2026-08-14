# Acá van las imágenes que Marcos quiere en la página

Esta carpeta es de Marcos. Es el **único** lugar de donde Claude Code saca
imágenes para la landing.

## Cómo se usa

Marcos copia acá las fotos que quiere que aparezcan en la página. Como le salga:
del celular, del Escritorio, de donde sea. No importa el peso ni el formato.

Si querés que una foto vaya en una sección determinada, poné el nombre del
archivo empezando con la sección. Por ejemplo:

```
hero - caja azul.jpg
lineas - sensores.png
respaldo - stand feria.jpg
```

Si no ponés nada, Claude Code pregunta antes de ubicarla. **No la ubica por su
cuenta.**

## Qué hace Claude Code con esto

- Usa **solamente** lo que está en esta carpeta. No sale a buscar imágenes a
  ninguna otra parte de la computadora, ni a internet.
- **No recorta, no cambia el encuadre y no borra fondos.** Si una foto necesita
  el fondo transparente, Marcos la trae ya recortada.
- Lo único que le hace es bajarle el peso para que la página abra rápido: la
  misma imagen, archivo más chico. El original queda intacto acá.
- La versión liviana la deja en `assets/`, que es la carpeta que usa la página.

## Por qué esta carpeta no se sube a GitHub

Está en el `.gitignore`. Los originales pueden pesar 30 MB cada uno y GitHub
rechaza archivos de más de 100 MB. Lo que sí se sube es la versión liviana que
queda en `assets/`.

**Consecuencia:** los archivos de esta carpeta viven solo en la máquina de
Marcos. No son un backup.
