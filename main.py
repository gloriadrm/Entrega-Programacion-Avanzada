import os
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, List
from datetime import datetime, date, timedelta  
from sqlalchemy import func 
import logging
from logging.handlers import RotatingFileHandler

# ------ Módulos Locales ------
from database import Base, engine, SessionLocal
from models import  UserDB, DailyLogDB
from security import create_access_token, decode_access_token ,hash_password, verify_password, generate_user_id
from schemas import User, UserSignUp, UserLogin, UserUpdate, UserOut, DailyLogInput, DailyLogOutput, MetricType, LogTrendsOut, MetricsSummary



# ------ Logging ------
# Almacenaremos los logs en un archivo en lugar de verlos por la terminal
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
# Si no existe la carptea logs la creamos
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(name)s] - %(message)s")

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info(f"Sistema de Logging Inicializado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# -------------------

#  URL del endpoint que maneja la autenticación y genera el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# Creamos la base e datos
Base.metadata.create_all(bind=engine) 

# ------ Utilities ------
def get_current_user(token):
    """Verifica el token y devuelve el usuario actual."""
    try: 
        payload = decode_access_token(token)
    except Exception:
        logger.warning("Fallo de autenticación: Token inválido o expirado.")
        raise HTTPException(status_code=401, detail= "Token invalido o expirado")
    user_id = payload.get("sub")
    
    if not user_id:
        logger.warning("Fallo de autenticación: El token sin usuario asociado (sub).")
        raise HTTPException(status_code=401, detail="Token sin identidad")
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            logger.warning(f"Fallo de autenticación: ID de usuario {user_id} no encontrado en la base de datos.")
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    finally:
        db.close()

from textwrap import dedent
## ------ API setup ------ 
app = FastAPI(
    tittle= 'Healthy habits tracking 🧘‍♀️',
    description= dedent("""\
    # 🌿 API de Bienestar Personal

    **Esta API permite registrar y consultar hábitos diarios relacionados con el bienestar físico y emocional.**

    ---

    ### 🧘‍♀️ Hábitos que puedes registrar
    - 😴 Sueño    
    - 💧 Hidratación  
    - 🚶‍♂️ Pasos  
    - 🍽️ Alimentación  
    - 😊 Estado de ánimo  

    ---
    ### 📊 Consultas disponibles:     
    Puedes acceder a datos históricos y a métricas principales de los últimos X días para analizar tu progreso. 

    ---

    """), 
    version="1.0.0"
)


### Endpoint de inicio de sesión: POST
# ------ Creación de cuenta: Sign Up ------
@app.post(
    "/auth/signup",
    summary = "Registro de cuenta de usuario.",
    response_model = UserOut, 
    status_code = 201,
    tags = ['Authentication'],
    responses = {
        201 : {"description" : "Usuario creado exitosamente."},
        400 : {"description" : "Error en los datos de entrada."},
        500 : {"description" : "Error de servidor interno."}
    }
    )
def create_user(payload : UserSignUp):
    db = SessionLocal()
    try: 
        # Comprobamos si ya existe el usuario
        logger.info(f"Attempting to sign up user: {payload.email}") 
        user_db = db.query(UserDB).filter(UserDB.email == payload.email).first()
        if user_db:
            logger.warning(f"Signup rejected: User {payload.email} already exists.")
            raise HTTPException(status_code=400, detail="El usuario ya esta registrado.")
        
        # Creamos el usuario
        user_db = UserDB(
            id = generate_user_id(payload.email), 
            name=payload.name, 
            age=payload.age, 
            email=payload.email,
            password_hash=hash_password(payload.password)
            )
        
        db.add(user_db)
        db.commit()          # Confirmamos cambios
        db.refresh(user_db)  # Actualiza el objeto con el ID y demás campos generados
        logger.info(f"Usuario {payload.email} creado exitosamente con ID: {user_db.id}")       
        return user_db       # Pydantic devuelve el Modelo UserOut con los datos no sensibles
    except Exception as e:
        db.rollback()
        logger.error(f"Error durante el registro para {payload.email}: {e}")
        raise
    finally:
        db.close() 

# ----- Inicio de sesión: Login ------
@app.post(
    "/auth/login",
    summary="Inicio de sesión y obtención de token.",
    status_code=200,
    tags=["Authentication"],
    responses={
        200: {
            "description": "Autenticación exitosa. Token devuelto.",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1Ni…",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {"description": "Error en los datos de entrada."},
        500: {"description": "Error de servidor interno."}
    }
)

def login_user(payload: UserLogin ):
    db= SessionLocal()
    try:
        #Comprobamos que existe el ususario
        user_db = db.query(UserDB).filter(UserDB.email == payload.email).first()
        # Si no existe lanzamos error
        if not user_db:
            raise HTTPException(status_code=400, detail="Usuario no encontrado.")
        if not verify_password(payload.password, user_db.password_hash):
            raise HTTPException(status_code=400, detail="Contraseña incorrecta.")
        # Si existe creamos un token
        token = create_access_token({"sub": user_db.id})
        logger.info(f"Usuario {user_db.email} ha iniciado sesión correctamente.")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error durante el inicio de sesión para {payload.email}: {e}")
        raise
    finally:
        db.close()
    

### Endpoints de usuario: GET, PUT 
# ----- Consultar datos de usuario ------
@app.get(
    "/user/account",
    response_model=UserOut,
    summary="Devuelve información de la cuenta de usuario",
    tags=["User Profile"],
    responses = {
        200 : {"description" : "Datos de usuario devueltos exitosamente."},
        401 : {"description" : "Token inválido o expirado."}
    }
)
def get_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try: 
        user_db = get_current_user(token)
        # Las validaciones se realizan en  get_current_user()
        return user_db
    except Exception as e:
        logger.error(f"Error al recuperar la cuenta de usuario: {e}")
        raise
    finally:
        db.close() 
   
# ----- Modificar datos de usuario ------
@app.put(
    "/user/account",
    response_model=UserOut,
    summary="Actualizar datos de la cuenta de usuario.",
    tags=["User Profile"],
    responses={
        200 : {"description" : "Datos de usuario actualizados exitosamente."},
        401 : {"description" : "Token inválido o expirado."}
    }
)
def update_user(payload: UserUpdate, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try: 
        user_db_detached = get_current_user(token)
        user_db_persistent = db.merge(user_db_detached)
        # user_db_detached es una copia de los datos del usuario 
        # hacemos merge para sincronizar el estado del objeto con la bd 
        # con ello evitamos  el error Instance is not persistent within this Session
        
        # Actualizamos cada parámetro solo si se proporcionó 
        if payload.name is not None:
            user_db_persistent.name = payload.name 
        if payload.age is not None:
            user_db_persistent.age = payload.age

        db.commit()                         # Confirmamos cambios
        db.refresh(user_db_persistent)      # Actualizamos el objeto     
        logger.info(f"Perfil del ID de usuario {user_id} actualizado.")
        return user_db_persistent
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar la cuenta del ID de usuario {user_id}: {e}")
        raise
    finally:
        db.close() 

### Endpoint de logs: 
#  -- POST /logs ---  
@app.post(
    "/user/logs",
    response_model=DailyLogOutput,
    status_code= 201,
    summary="Create a new daily log entry.",
    tags=["Daily Logs"],
    responses={
        201 : {"description": "Log diario creado exitosamente."},
        401 : {"description" : "Token inválido o expirado."},
        400: {
            "description": "Ya existe un log para la fecha especificada.",
            "content": {
                "application/json": {
                    "example": {"detail": "Ya existe un log para la fecha 2023-10-25. Usa PUT/PATCH para actualizarlo."}
                }
            }
        }
    }
)
def insert_daily_log(log_data: DailyLogInput, token : str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try: 
        user_db = get_current_user(token)
        user_id = user_db.id

        log_date = log_data.log_date

        # Comprobamos si ya existe un log creado para esta fecha
        log_db =db.query(DailyLogDB).filter( 
            DailyLogDB.user_id == user_id, 
            DailyLogDB.log_date == log_date).first()
        if log_db: 
            logger.warning(f"Fallo en la creación del log: Ya existe un log para el usuario {user_id} en la fecha {log_date}.")
            raise HTTPException(status_code=400, detail=f"Ya existe un log para la fecha {log_date}. Usa PUT/PATCH para actualizarlo.")
        
        new_log = DailyLogDB(
            user_id = user_id,
            # Desempaquetamos los campos del Pydantic Model DalilyLogInput
            **log_data.model_dump(exclude_none=True)
        )

        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        logger.info(f"Nuevo log diario creado para el usuario {user_id} en la fecha {log_date}.")
        return new_log
    except Exception as e:
        db.rollback()
        logger.error(f"Error al insertar el log diario para el usuario {user_id}: {e}")
        raise
    finally:
        db.close()  
    
# PUT /logs/{user_email}/{date} (o POST idempotente)
@app.put(
    "/user/logs",
    response_model=DailyLogOutput,
    summary="Actualizar un log diario para una fecha ya introducida. Se admiten actualizaciones parciales.",
    tags=["Daily Logs"],
    responses={
        200: {"description": "Log diario actualizado exitosamente."},
        401 : {"description" : "Token inválido o expirado."},
        400: {
            "description": "No existe un log en la fecha especificada.",
            "content": {
                "application/json": {
                    "example": {"detail": "No existe un log que modificar para la fecha 2023-10-25."}
                }
            }
        }
    }
)
def update_daily_log(log_data:DailyLogInput, token : str = Depends(oauth2_scheme)): 
    db = SessionLocal()
    try: 
        user_db = get_current_user(token)
        user_id = user_db.id
        log_date = log_data.log_date

        # Comprobamos que exista el log que se desea modificar (para ese user y dia)
        log_db =db.query(DailyLogDB).filter( 
            DailyLogDB.user_id == user_id, 
            DailyLogDB.log_date == log_date).first()
        if not log_db: 
            logger.warning(f"Fallo en la actualización del log: Log no encontrado para el usuario {user_id} en la fecha {log_date}.")
            raise HTTPException(status_code=400, detail=f"No existe un log que modificar para la fecha {log_date}.")
        
        # model_dump(exclude_none=True) solo incluye los campos que se enviaron.
        # Esto permite una actualización parcial (PATCH-like) aunque use PUT
        update_data = log_data.model_dump(exclude_none=True)
        
        for key, value in update_data.items():
            # Excluimos la fecha --> 'log_date' de ser actualizada ya que es primery_key del registro
            if key not in ['log_date']:
                setattr(log_db, key, value)

        db.commit()
        db.refresh(log_db)
        logger.info(f"Log diario para el usuario {user_id} en la fecha {log_date} actualizado.")
        return log_db
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar el log diario para el usuario {user_id} en {log_date}: {e}")
        raise
    finally:
        db.close()


### Consultas: GET /trends.
@app.get(
    "/user/trends",
    response_model=MetricsSummary,
    summary="Calculo de métrica especificada para un período de tiempo especificado (máximo 30 días atrás).",
    tags=["Trends"],
    responses={
        200 : {"description": "Métricas devueltas exitosamente."},
        401 : {"description" : "Token inválido o expirado."},
        400: {
            "description": "No se encontraron datos para el período de tiempo especificado.",
            "content": {
                "application/json": {
                    "example": {"detail": "No se encontraron registros de hábitos para el período consultado."}
                }
            }
        }
    }
)
def get_log_trends(last_days: int ,metric_type: MetricType, token : str= Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user = get_current_user(token) 
        user_id = user.id
        
        func_map = {
            MetricType.AVERAGE: func.avg,
            MetricType.MINIMUM: func.min,
            MetricType.MAXIMUM: func.max
        }
        selected_func = func_map[metric_type]

        today = date.today()
        start_date = today - timedelta(days=last_days)

        metric_columns = [
            DailyLogDB.steps,
            DailyLogDB.exercise_minutes,
            DailyLogDB.sleep_hours,
            DailyLogDB.water_liters,
            DailyLogDB.diet_score,
            DailyLogDB.mood,
        ]
        # Ej: [func.avg(DailyLogDB.steps).label('steps'), func.avg(DailyLogDB.mood).label('mood'), ...]
        selected_metrics = [selected_func(col).label(col.name) for col in metric_columns]

        # 5. Ejecutar la consulta de agregación
        trends_query = db.query(*selected_metrics).filter(
            DailyLogDB.user_id == user_id,
            DailyLogDB.log_date >= start_date
        ).one_or_none()

        if not trends_query or all(value is None for value in trends_query):
            logger.info(f"No se encontraron registros para el usuario {user_id} en los últimos {last_days} días.")
            raise HTTPException(
                status_code=404,
                detail="No se encontraron registros de hábitos para el período consultado."
            )
        trends_data = trends_query._asdict()
        logger.info(f"Tendencias calculadas exitosamente para el usuario {user_id} ({metric_type.value} sobre {last_days} días).")
        return trends_data
    except Exception as e:
        logger.error(f"Error al recuperar tendencias de log para el usuario {user_id}: {e}")
        raise
    finally:
        db.close() 

