# Favorite Links

* **Autor**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Fecha de creación**: 04/11/2024
* **Licencia**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introducción

El complemento **FavoriteLinks** es una herramienta para gestionar tus enlaces favoritos de forma organizada y eficiente. Te permite guardar, editar y eliminar enlaces en una lista categorizada, ofreciendo una interfaz intuitiva con funciones como añadir nuevos enlaces, renombrar títulos, eliminar entradas no deseadas y gestionar categorías. Además, el complemento permite importar marcadores directamente desde archivos HTML exportados por los navegadores.

Al abrir el complemento, obtienes acceso rápido a tus enlaces y puedes abrirlos directamente en el navegador predeterminado. Ahora también dispone de soporte para abrir enlaces en un navegador secundario, en caso de que necesites más flexibilidad.

## Instalación

Sigue los pasos a continuación para instalar el complemento **FavoriteLinks** en NVDA:

1. En NVDA, abre el menú **Herramientas** y selecciona **Tienda de complementos**.
2. En la pestaña **Complementos disponibles**, navega hasta el campo de **Búsqueda**.
3. Busca "favoriteLinks". En los resultados, pulsa **Intro** o **Aplicar**, y luego elige **Instalar**.
4. Reinicia NVDA para aplicar los cambios.

## Configuración

Tienes control total sobre dónde se guardan tus enlaces y qué navegador los abre.

1. Accede al menú de NVDA: `NVDA+N` > *Preferencias* > *Opciones*.
2. En la lista de categorías, selecciona **Favorite Links**.

Puedes elegir una ubicación personalizada para guardar el archivo de enlaces utilizando el botón **"Seleccionar o añadir un directorio"** (`Alt+S`).

Para definir un navegador secundario, que puede ser instalado o portátil:

1. Navega con el `Tabulador` hasta el campo **Ruta del navegador**.
2. Utiliza el botón **"Seleccionar ruta del navegador"** (`Alt+N`) para añadir el ejecutable del navegador deseado.

## Uso

### Acceder al complemento

* Pulsa `Alt+Windows+K`.
* O accede a través de `NVDA+N` > *Herramientas* > *Favorite Links*.

### Interfaz Principal

La interfaz principal consta de dos campos principales, por los que se puede navegar con la tecla `Tab`:

1. **Categoría**: Un cuadro combinado con las categorías existentes.
2. **Lista de enlaces**: Una lista que muestra los enlaces asociados a la categoría seleccionada.

Utiliza el **menú contextual** (tecla aplicaciones) en cualquiera de estos campos para acceder a opciones adicionales.

### Acciones Disponibles

#### En el Cuadro Combinado de Categorías

* **Añadir categoría**: Crea una nueva categoría.
* **Editar categoría**: Renombra la categoría seleccionada.
* **Eliminar categoría**: Borra la categoría y todos sus enlaces.
* **Exportar enlaces**: Guarda todos los enlaces y categorías en un archivo `.json`.
* **Importar enlaces**: Carga enlaces y categorías desde un archivo `.json`.

#### En la Lista de Enlaces

* **Abrir enlace**: Abre el enlace en el navegador que hayas configurado.
    > **Nota**: Es necesario configurar previamente el navegador secundario en los ajustes.
* **Añadir enlace**: Permite insertar una nueva URL. El título se obtendrá automáticamente, pero puedes introducirlo manualmente si la obtención falla.
* **Editar enlace**: Modifica el título y la URL de un enlace existente.
* **Eliminar enlace**: Borra el enlace seleccionado.
* **Exportar enlaces** / **Importar enlaces**: Igual que las opciones de categoría.
* **Importar marcadores HTML**: Importa enlaces desde un archivo `.html` exportado por navegadores.
* **Ordenar enlaces**: Organiza los enlaces de la categoría actual en orden alfabético.

### Importar Marcadores HTML

FavoriteLinks también permite importar marcadores directamente desde archivos HTML, como los exportados por navegadores (Chrome, Firefox, Edge, entre otros).

Esta función es útil para migrar tus marcadores existentes al complemento de forma rápida y organizada.

#### Cómo importar marcadores desde un archivo HTML

1. Abre el complemento **Favorite Links**.
2. Accede al menú contextual en el **Cuadro combinado de categorías** o utiliza la opción disponible en el menú principal.
3. Selecciona **Importar marcadores HTML**.
4. Elige el archivo `.html` exportado desde tu navegador.
5. Espera a que se procesen los enlaces.

Durante la importación:

* El progreso se muestra en una barra de progreso.
* Puedes **cancelar la operación en cualquier momento**.
* NVDA sigue respondiendo durante todo el proceso.

#### Organización de los enlaces importados

* Los enlaces importados se añaden automáticamente al archivo JSON configurado en las preferencias del complemento.
* Por defecto, los marcadores se insertan en la categoría **“Imported Bookmarks”**.
* Los enlaces duplicados (con la misma URL) no se añaden de nuevo.

Al finalizar la importación, se muestra un mensaje de confirmación y la interfaz del complemento se actualiza automáticamente.

### Atajos de teclado

| Función | Atajo |
| :--- | :--- |
| Abrir enlace | `Alt+B` o `Intro` (en la lista de enlaces) |
| Añadir enlace | `Alt+A` |
| Añadir categoría | `Alt+D` |
| Editar enlace | `Alt+E` o `F2` |
| Eliminar enlace | `Alt+L` o `Supr` |
| Guardar URL de la página actual | `Shift+Control+D` |
| Mostrar URL de la página actual | `Windows+Control+P` (Pulsar dos veces copia la URL al portapapeles) |
| Salir | `Alt+S`, `Esc` o `Alt+F4` |

## Diálogo "Añadir nuevo enlace"

1. **Categoría**: Selecciona la categoría deseada.
2. **URL**: Pega o escribe la dirección del enlace.
    > Si ya has copiado una URL, se pegará automáticamente.
3. **Aceptar (`Alt+O`)**: Añade el enlace.
    > El título se obtendrá automáticamente. Si falla, podrás introducirlo manualmente.
4. **Cancelar (`Alt+C`)**: Cierra el diálogo. `Esc` o `Alt+F4` también funcionan.

## Diálogo "Editar enlace"

1. **Categoría**: Al cambiar la categoría aquí, el enlace se moverá a la nueva categoría.
2. **Título**: Edita el título del enlace.
3. **URL**: Cambia la dirección del enlace.
4. **Aceptar (`Alt+O`)**: Guarda los cambios.
5. **Cancelar (`Alt+C`)**: Cierra sin guardar. `Esc` o `Alt+F4` también funcionan.

## Agradecimientos

Un agradecimiento especial a **Rue Fontes** y **Ângelo Abrantes** por las pruebas realizadas y por las valiosas sugerencias que contribuyeron significativamente a mejorar este proyecto.

También agradezco a **Abel Passos** por su contribución con la funcionalidad de importar marcadores desde archivos HTML.

El complemento FavoriteLinks fue desarrollado con la asistencia de **ChatGPT** y **Google Gemini**, utilizados para la creación de funciones, optimización y refactorización del código, y la mejora de la documentación.

## 🌍 Traductores

* 🇸🇦 **Árabe** — Ahmed Bakr
* 🇧🇷 **Portugués (Brasil)** — Edilberto Fonseca
* 🇵🇹 **Portugués (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Ruso (Rusia)** — Valentin Kupriyanov
* 🇹🇷 **Turco (Turquía)** — Umut KORKMAZ
* 🇺🇦 **Ucraniano (Ucrania)** — Heorhii Halas
* 🇪🇸 **Español** — [Tu Nombre/User]
