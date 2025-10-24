# 🌿 Healthy Habits Tracking API 🧘‍♀️

## 📝 Descripción del Proyecto

Este proyecto es una **API RESTful** desarrollada con **FastAPI** que permite a los usuarios registrar, consultar y analizar sus **hábitos diarios de bienestar y salud personal**.

Su objetivo principal es ofrecer una herramienta robusta y bien documentada para el seguimiento de métricas clave que influyen en el **estado de ánimo** y la **salud física**.

---

## 🎯 Caso de Uso y Funcionalidad

### 🧘‍♀️ Caso de Uso Principal
El caso de uso central es proporcionar una capa de datos (**backend**) para una aplicación móvil o web de bienestar, donde el usuario pueda llevar un registro diario de sus métricas de salud y visualizar su progreso a lo largo del tiempo.

**Usuario objetivo:** personas interesadas en el autoconocimiento y la mejora continua de su bienestar a través de datos cuantificables.

---

## ⚙️ Funcionalidades Clave

| Categoría | Endpoint | Descripción |
|------------|-----------|-------------|
| **Autenticación** | `/auth/signup` | Creación de nuevas cuentas de usuario. |
| **Autenticación** | `/auth/login` | Inicio de sesión y obtención de un token de acceso (**Bearer Token**). |
| **Perfil** | `/user/account (GET)` | Consulta los datos del perfil del usuario autenticado. |
| **Perfil** | `/user/account (PUT)` | Permite modificar el nombre y la edad del usuario. |
| **Perfil** | `/user/account (DELETE)` | Permite eliminar la cuenta del nombre y todos sus datos asociados. |
| **Logs Diarios** | `/user/logs (POST)` | Registra un nuevo log diario para una fecha específica (**201 Created**). |
| **Logs Diarios** | `/user/logs (PUT)` | Actualiza un log existente para una fecha específica. |
| **Métricas** | `/user/trends (GET)` | Calcula y devuelve métricas agregadas (media, mínimo, máximo) de los hábitos para un período definido (`last_days`). |

---

## 💪 Hábitos Registrables

La API permite el seguimiento de los siguientes hábitos, fundamentales para el bienestar:

- 💤 **sleep_hours** → Horas de sueño  
- 💧 **water_liters** → Litros de agua consumidos  
- 🚶‍♀️ **steps** → Pasos dados  
- 🏋️ **exercise_minutes** → Minutos de ejercicio  
- 🍽️ **diet_score** → Puntuación de la calidad de la alimentación *(escala de 1 a 10)*  
- 😊 **mood** → Estado de ánimo *(escala de 1 a 5)*  

---

## 🛠️ Detalles de Implementación Técnica (FastAPI)

### 1️⃣ Documentación Explícita
Todos los endpoints están decorados para ofrecer una documentación precisa en el **Swagger UI** y **ReDoc** generados automáticamente por FastAPI.

- **Tags:** los endpoints están agrupados por categorías (`Authentication`, `Daily Logs`, etc.)  
- **Responses:** se definen los códigos de respuesta de éxito y error (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`)

---

### 2️⃣ Sistema de Logging Persistente

La aplicación utiliza el módulo **logging** de Python para registrar el flujo de ejecución, advertencias y errores críticos.

- 🗂️ **Separación de logs:** se ha configurado un *FileHandler* que dirige todos los mensajes (nivel `DEBUG` o superior) al archivo `logs/app.log`  
- 🧼 **Consola limpia:** mantiene la terminal libre de ruido mientras conserva un registro detallado y persistente de la actividad del sistema  

---

### 3️⃣ 🔒 Seguridad

- **Autenticación:** se utiliza `OAuth2PasswordBearer` para proteger endpoints sensibles  
- **Autorización:** el acceso requiere un token JWT (**JSON Web Token**) válido, generado tras el inicio de sesión  

---

### SWAGGER
- **Descripción**
<img width="1159" height="460" alt="image" src="https://github.com/user-attachments/assets/af5e8ec9-d201-4f0c-9f10-bcbd4240c4aa" />
- **Endpoints**
<img width="983" height="444" alt="image" src="https://github.com/user-attachments/assets/28e38bc2-9a8d-441f-af2d-58a8b6303c92" />
- **Ejemplos de respuesta:**
 <img width="975" height="767" alt="image" src="https://github.com/user-attachments/assets/897d0424-ffb8-4165-876a-32ce390d49f6" />

  



---
