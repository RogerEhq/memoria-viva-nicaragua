📘 README — Memorias de mi pueblo
🏷️ Descripción del proyecto
Memorias de mi pueblo es una plataforma web diseñada para promover la cultura, los relatos, los negocios locales y el turismo en Nicaragua. El sitio está construido con HTML, CSS y Django (por las etiquetas {% url %}), y presenta una interfaz visual cálida y accesible, con elementos gráficos como imágenes de volcanes y fauna que refuerzan la identidad local.

🧱 Estructura del código
🔹 HTML
Contiene la estructura principal del sitio: <nav>, <main>, <footer>.

Usa plantillas de Django para renderizar contenido dinámico ({% block content %}, {% if user.is_authenticated %}, etc.).

Incluye enlaces condicionales para usuarios autenticados (crear relatos, recetas, sugerir negocios).

🔹 CSS
Utiliza variables CSS para mantener una paleta de colores coherente.

Aplica fuentes personalizadas desde Google Fonts (Playfair Display y Lato).

Estiliza el nav y el footer con imágenes de fondo (volcan.jpg y fauna.jpg) que se ajustan completamente al contenedor usando object-fit: cover.

Incluye estilos responsivos para pantallas pequeñas (@media max-width: 600px).

🌄 Imágenes destacadas
Volcán: imagen de fondo en el <nav>, representa fuerza natural y patrimonio.

Fauna: imagen de fondo en el <footer>, simboliza biodiversidad y conexión con la tierra.

Ambas imágenes están posicionadas absolutamente y se ajustan al contenedor sin dejar espacios vacíos.

🧭 Navegación
El menú de navegación incluye:

Inicio

Biblioteca

Calendario Cultural

Usuarios

Negocios

Juego

Acciones exclusivas para usuarios autenticados

📦 Requisitos
Este proyecto está pensado para integrarse con Django. Para que funcione correctamente:

Las rutas {% url %} deben estar definidas en urls.py.

Las imágenes deben estar ubicadas en /media/volcan.jpg y /media/fauna.jpg.

El sistema debe manejar autenticación de usuarios (user.is_authenticated).

🛠️ Personalización sugerida
Agregar rutas turísticas dinámicas desde la base de datos.

Incluir filtros por categoría (ej. solo negocios de turismo).

Mejorar accesibilidad con etiquetas ARIA y contraste de texto.

Añadir soporte multilingüe si se desea expandir a otras regiones.

📞 Contacto
Para dudas o colaboración, puedes contactar al equipo de desarrollo de memorias de mi pueblo
