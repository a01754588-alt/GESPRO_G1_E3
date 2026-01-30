Equipo de trabajo

Rodrigo Gutierrez García

Liliana Ortega

Victoria Rodriguez 

Carlos Lopez 

Vicente Ramos

📋 Gestor de Tareas Kanban - Equipo de Desarrollo

Un sistema completo de gestión de tareas estilo Kanban desarrollado por un equipo de estudiantes comprometidos con la innovación y la excelencia en el desarrollo de software.

👥 Equipo de Desarrollo
Integrantes del Proyecto:
Nombre	Rol Principal	Contribuciones
Rodrigo Gutiérrez García	Backend Architect	API REST, lógica del servidor, validaciones
Liliana Odette Ortega Quezada	UX/UI Designer	Diseño de interfaz, experiencia de usuario, responsive design
Victoria Rodríguez Domínguez	Frontend Developer	Implementación JavaScript, funcionalidades interactivas
Carlos Julián López Chávez	Full Stack Developer	Integración frontend-backend, manejo de datos
Vicente Jesús Ramos Chávez	DevOps & QA	Configuración servidor, testing, documentación
Filosofía del Equipo
Unidos por la pasión por la tecnología y el trabajo colaborativo, nuestro equipo combinó habilidades complementarias para crear una solución robusta y elegante para la gestión de tareas. Creemos en el código limpio, la documentación completa y la experiencia de usuario intuitiva.

✨ Características Principales
📋 Gestión de Tareas
✅ Crear tareas con título, puntos de complejidad y tiempo estimado

✅ Asignar responsables a cada tarea

✅ Tres estados: TODO, IN PROGRESS, DONE

✅ Ordenar tareas por tiempo o puntos (ascendente/descendente)

✅ Cálculo automático del tiempo total estimado

🎨 Interfaz Kanban
🎯 Tres columnas visuales (TODO, IN PROGRESS, DONE)

🎨 Diseño responsive que funciona en móviles y desktop

📊 Contadores en tiempo real por columna

🔄 Arrastre virtual mediante botones de movimiento

⏱️ Gestión de Tiempo
⏰ Estimación de tiempo en minutos (5-480 min)

📈 Ordenamiento automático por tiempo estimado

🕒 Cálculo de tiempo total por proyecto

📊 Visualización en horas/minutos

🔧 Funciones Avanzadas
✏️ Edición completa de tareas (modal integrado)

🗑️ Eliminación con confirmación

🔔 Sistema de notificaciones visuales

🔄 Actualización automática cada 60 segundos

📱 Compatible con múltiples dispositivos

🚀 Instalación Rápida
Prerrequisitos
Python 3.8 o superior

pip (gestor de paquetes de Python)

Paso 1: Clonar o descargar
bash
git clone https://github.com/tu-usuario/gestor-tareas-kanban.git
cd gestor-tareas-kanban
Paso 2: Instalar dependencias
bash
pip install flask
Paso 3: Estructura del proyecto
text
gestor-tareas-kanban/
│
├── Frontend/
│   └── index.html          # Interfaz web completa
│
├── data/
│   └── task_data.py        # Gestión de datos y persistencia
│
├── models/
│   └── task.py             # Modelo de datos de tareas
│
├── app.py                  # Servidor Flask principal
├── tasks.json              # Base de datos JSON (se crea automáticamente)
├── README.md               # Este archivo
└── LICENSE                 # Licencia del proyecto
Paso 4: Ejecutar la aplicación
bash
python app.py
La aplicación estará disponible en: 🌐 http://localhost:5000

📖 Uso de la Aplicación
1. Crear una Nueva Tarea
Rellena el formulario en la parte superior

Especifica:

Título: Nombre descriptivo de la tarea

Puntos: Complejidad (1-10)

Tiempo: Estimación en minutos (5-480)

Asignado a: Responsable (opcional)

Estado: TODO, IN PROGRESS o DONE

Haz clic en "➕ Crear Tarea"

2. Mover Tareas entre Columnas
Cada tarea muestra botones para moverla a otros estados

Ejemplo: Una tarea en TODO tendrá botones para moverla a IN PROGRESS o DONE

3. Editar Tareas
Haz clic en el botón "✏️ Editar" de cualquier tarea

Se abrirá un modal con todos los campos editables

Modifica los datos necesarios

Haz clic en "Guardar Cambios"

4. Ordenar Tareas
Cada columna tiene un selector de ordenamiento

Opciones disponibles:

Mayor tiempo primero

Menor tiempo primero

Mayor puntos primero

Menor puntos primero

5. Eliminar Tareas
Haz clic en el botón "🗑️" de la tarea

Confirma la eliminación en el diálogo

La tarea será removida permanentemente

🛠️ API RESTful
La aplicación expone una API completa para integraciones:

Endpoints Disponibles
Método	Endpoint	Descripción
GET	/tasks	Obtener todas las tareas
GET	/tasks/<id>	Obtener una tarea específica
POST	/tasks	Crear una nueva tarea
PUT	/tasks/<id>	Actualizar una tarea existente
DELETE	/tasks/<id>	Eliminar una tarea
GET	/stats	Obtener estadísticas del proyecto
GET	/tasks/search?q=<query>	Buscar tareas
Ejemplo de Creación (POST /tasks)
json
{
  "titulo": "Desarrollar nueva funcionalidad",
  "puntos": 5,
  "estimacion_minutos": 120,
  "asignado_a": "Juan Pérez",
  "estado": "TODO"
}
📊 Estructura de Datos
Modelo de Tarea
python
{
  "id": 1,
  "titulo": "Revisar documentación",
  "estado": "TODO",
  "puntos": 3,
  "estimacion_minutos": 60,
  "asignado_a": "Ana García"
}
Persistencia
Los datos se guardan automáticamente en tasks.json

Formato JSON legible y editable

Carga automática al iniciar la aplicación

🏗️ Arquitectura Técnica
Backend (Desarrollado por Rodrigo y Carlos)
Framework: Flask 2.0+

Patrón: REST API

Persistencia: JSON File-based

Validaciones: Completa en servidor

Manejo de errores: Códigos HTTP estándar

Frontend (Desarrollado por Liliana y Victoria)
Tecnologías: HTML5, CSS3, JavaScript ES6+

Patrón: Component-based (sin frameworks)

Estilos: CSS Grid & Flexbox

Animaciones: CSS Transitions & Keyframes

Responsive: Mobile-first approach

DevOps (Coordinado por Vicente)
Configuración: CORS manual, headers de seguridad

Logging: Sistema de tracking de peticiones

Performance: Caché optimizado, actualización inteligente

Documentación: README completo y detallado

🎨 Decisiones de Diseño
UI/UX (Liderado por Liliana)
Paleta de colores: Rojo (TODO), Naranja (PROGRESS), Verde (DONE)

Tipografía: Arial sans-serif para máxima legibilidad

Espaciado: Sistema consistente de márgenes y paddings

Iconografía: Emojis y símbolos universales

Feedback: Notificaciones visuales inmediatas

Experiencia de Usuario
Formularios: Validación en tiempo real

Navegación: Flujo intuitivo entre acciones

Accesibilidad: Contraste adecuado, tamaños de texto legibles

Performance: Carga rápida, sin dependencias externas

Consistencia: Mismos patrones en toda la aplicación

🔧 Proceso de Desarrollo
Fase 1: Planificación
Definición de requisitos

Diseño de arquitectura

Asignación de roles

Creación de roadmap

Fase 2: Desarrollo Backend
Implementación de API REST

Sistema de persistencia

Validaciones y seguridad

Pruebas de endpoints

Fase 3: Desarrollo Frontend
Diseño de interfaces

Implementación de componentes

Integración con API

Pruebas de usabilidad

Fase 4: Integración y Testing
Conexión frontend-backend

Pruebas de funcionalidad completa

Optimización de performance

Documentación técnica

Fase 5: Despliegue y Documentación
Configuración final

Creación de README

Preparación para entrega

Revisión final de equipo

🐛 Solución de Problemas
Problema: "Servidor no responde"
bash
# Verifica que Flask esté instalado
pip list | grep Flask

# Verifica que el puerto 5000 esté libre
netstat -an | grep 5000

# Reinicia el servidor
python app.py
Problema: "No se guardan los cambios"
Verifica que el archivo tasks.json tenga permisos de escritura

Revisa la consola del servidor para errores

Problema: "Error de CORS"
Asegúrate de acceder desde http://localhost:5000

El servidor incluye headers CORS manuales

📱 Compatibilidad
✅ Chrome 60+

✅ Firefox 55+

✅ Safari 12+

✅ Edge 79+

✅ Mobile Safari

✅ Chrome para Android

🔮 Futuras Mejoras (Roadmap)
Fase 1 (Próxima versión)
Arrastrar y soltar entre columnas

Etiquetas y categorías para tareas

Fechas límite y recordatorios

Fase 2
Gráficos de progreso y métricas

Exportación a PDF/Excel

Autenticación de usuarios

Fase 3
Múltiples proyectos/equipos

Comentarios en tareas

Integración con calendarios

🤝 Contribuir
Haz fork del proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.



📞 Soporte
📧 Email: equipo.kanban@ejemplo.com

🐛 Issues: GitHub Issues

💬 Discord: Servidor del Equipo

⭐ ¡Dale una estrella al proyecto si te ha sido útil! ⭐

<div align="center">
🏆 Logros del Equipo
Hito	Estado	Impacto
API REST completa	✅ Logrado	Backend robusto y escalable
UI/UX profesional	✅ Logrado	Experiencia de usuario excepcional
Responsive design	✅ Logrado	Accesible en todos los dispositivos
Documentación completa	✅ Logrado	Fácil mantenimiento y extensión
Trabajo colaborativo	✅ Logrado	Sinergia de habilidades diversas
</div>
🎯 Visión del Equipo: Crear herramientas que simplifiquen la gestión del trabajo, combinando tecnología moderna con principios de usabilidad sólidos.

🚀 ¡Comienza a organizar tus tareas con nuestra solución hoy mismo!

