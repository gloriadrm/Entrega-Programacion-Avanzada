Healthy Habits Tracking API 🧘‍♀️

Descripción del Proyecto

Este proyecto es una API RESTful desarrollada con FastAPI que permite a los usuarios registrar, consultar y analizar sus hábitos diarios de bienestar y salud personal. Su objetivo principal es ofrecer una herramienta robusta y bien documentada para el seguimiento de métricas clave que influyen en el estado de ánimo y la salud física.

🎯 Caso de Uso y Funcionalidad

🧘‍♀️ Caso de Uso Principal

El caso de uso central es proporcionar una capa de datos (backend) para una aplicación móvil o web de bienestar, donde el usuario pueda llevar un registro diario de sus métricas de salud y visualizar su progreso a lo largo del tiempo.

Usuario Objetivo: Personas interesadas en el autoconocimiento y la mejora continua de su bienestar a través de datos cuantificables.

Funcionalidades Clave

Categoría

Endpoint

Descripción

Autenticación

/auth/signup

Creación de nuevas cuentas de usuario.

Autenticación

/auth/login

Inicio de sesión y obtención de un token de acceso (Bearer Token).

Perfil

/user/account (GET)

Consulta los datos del perfil del usuario autenticado.

Perfil

/user/account (PUT)

Permite modificar el nombre y la edad del usuario.

Logs Diarios

/user/logs (POST)

Registra un nuevo log diario para una fecha específica (201 Created).

Logs Diarios

/user/logs (PUT)

Actualiza un log existente para una fecha específica.

Métricas

/user/trends (GET)

Calcula y devuelve métricas agregadas (media, mínimo, máximo) de los hábitos para un período definido (last_days).

Hábitos Registrables

El API permite el seguimiento de los siguientes hábitos, fundamentales para el bienestar:

sleep_hours: Horas de sueño.

water_liters: Litros de agua consumidos (hidratación).

steps: Pasos dados.

exercise_minutes: Minutos de ejercicio.

diet_score: Puntuación de la calidad de la alimentación (ej. escala de 1 a 10).

mood: Estado de ánimo (ej. escala de 1 a 5).

🛠️ Detalles de Implementación Técnica (FastAPI)

Este proyecto sigue las mejores prácticas de una API moderna:

1. Documentación Explícita

Todos los endpoints están decorados para ofrecer una documentación precisa en el Swagger UI/ReDoc generado automáticamente por FastAPI:

Tags: Los endpoints están agrupados en categorías (Authentication, Daily Logs, etc.).

Responses: Se definen explícitamente los códigos de respuesta de éxito y de error (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found).

2. Sistema de Logging Persistente

La aplicación utiliza el módulo logging de Python para registrar el flujo de ejecución, advertencias y errores críticos:

Separación de Logs: Se ha configurado un manejador de archivos (FileHandler) que dirige todos los mensajes (nivel DEBUG o superior) al archivo logs/app.log.

Consola Limpia: Esta configuración asegura que la terminal de ejecución permanezca limpia, mientras se mantiene un registro detallado y persistente de la actividad del sistema en el archivo.

3. Seguridad

Autenticación: Se utiliza OAuth2PasswordBearer para asegurar los endpoints sensibles. El acceso requiere un token JWT (JSON Web Token) válido, generado tras el inicio de sesión.