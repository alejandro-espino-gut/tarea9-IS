# Tarea 9: HTMX

En éste repositorio se encuentra el proyecto de django que contiene lo necesario para la tarea 9.

## Integrantes

* Elizalde Maza Jesus Eduardo
* Espino Gutiérrez Alejandro
* Flores Doniz Daniel
* Peredo Lopez Citlalli Abigail
* Santana de la Rosa Monica Guadalupe

## Ejecución
Para ejecutar el proyecto, abre una terminal y sigue estos pasos:
- Primero, activa tu entorno de Conda con el comando conda activate <nombre_de_tu_entorno>.

- Después, navega a la carpeta del proyecto usando cd Downloads/tarea9-IS-main/proyecto/proyecto.

- Una vez dentro, ejecuta el servidor de Django con python manage.py runserver.

- Finalmente, abre tu navegador y entra a: http://127.0.0.1:8000/

## Peguntas
### ¿Cuál es la filosofía de HTMX?
La filosofía de HTMX es que el navegador debería poder hacer mucho más de lo que HTML permite por defecto. Normalmente, en una página web tradicional, solo los enlaces y los formularios pueden comunicarse con el servidor. HTMX rompe esa limitación y permite que cualquier elemento HTML, como un botón, una tabla o una imagen, pueda enviar y recibir información del servidor sin necesidad de recargar la página.

Lo importante es que HTMX no reemplaza al servidor ni inventa una nueva forma de manejar datos: el servidor sigue respondiendo con HTML normal, no con JSON ni con estructuras complejas. Esto hace que el backend mantenga el control de la lógica y que el frontend sea mucho más sencillo. La idea central es escribir menos JavaScript y aprovechar la solidez de HTML para construir interfaces dinámicas de forma más natural y directa.

### Suponiendo que usas HTMX para el proyecto final ¿cuáles son las responsabilidades que tendrían Django, HTMX y la API de Google Maps?

Cada parte de la pila tiene un rol claro y bien separado:
- Django se encarga de toda la lógica del negocio: gestiona la base de datos, valida datos, controla permisos y genera las respuestas. En lugar de devolver JSON, devuelve fragmentos de HTML que HTMX puede insertar directamente en la página. Es el cerebro de la aplicación.
- HTMX actúa como el puente entre el usuario y Django. Cuando el usuario hace una acción, como hacer clic en un botón o escribir en un campo de búsqueda, HTMX envía la petición al servidor y coloca la respuesta HTML en el lugar correcto de la página, sin recargarla. Su trabajo es conectar, no procesar.
- Google Maps API se encarga exclusivamente de la parte visual del mapa: renderizarlo en pantalla, mostrar marcadores, calcular rutas y detectar interacciones del usuario sobre el mapa. Cuando ocurre algo relevante en el mapa, como seleccionar un punto, esa información puede enviarse a Django para obtener datos relacionados y mostrarlos en otra parte de la interfaz.

### ¿Qué nos permite hacer htmx.ajax?
Normalmente HTMX funciona de forma declarativa: pones atributos en el HTML y él solo sabe cuándo y cómo hacer las peticiones. Sin embargo, hay situaciones en las que el evento que dispara una acción viene de afuera de HTMX, por ejemplo, de Google Maps, de un calendario o de cualquier otra librería de JavaScript.

Para esos casos existe la función htmx.ajax(), que permite hacer una petición al servidor directamente desde código JavaScript, con todas las ventajas de HTMX: elige dónde insertar la respuesta, con qué estrategia reemplazar el contenido y qué método HTTP usar. Así, cuando el usuario hace clic en un marcador del mapa, ese evento de Google Maps puede disparar una petición a Django y mostrar información relacionada en un panel de la página, sin necesidad de recargar nada ni escribir lógica extra para manejar la respuesta.


