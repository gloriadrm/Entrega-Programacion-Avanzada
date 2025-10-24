# 1. Pydantic (BaseModel, tipos, y validadores)
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr # <-- ¡AÑADIDO BaseModel y EmailStr!
from typing import Optional, List, Dict
# 2. Tipos de datos de Python (date, timedelta)
from datetime import date 
# 3. SQLAlchemy (Tipos de datos para el ORM si los necesitas en este archivo)
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
# 4. Importación de la Base de SQLAlchemy desde el módulo principal
from database import Base
from enum import Enum

# ------ Pydantic model ------
class User(BaseModel):
    """Información del usuario."""
    id : str = Field(None, description = "El id del usuario lo genera el servidor.")
    name: str = Field(..., max_length=100, description="El nombre de usuario es un campo obligatorio.")
    age: Optional[int] = Field(None, ge=0, description=" Tu edad debe ser mayor a 0" )
    email: EmailStr = Field(..., description="El correo es un campo obligatorio")
    password_hash: str = Field(..., description="Contraseña hasheada")

    # 	Con Pydantic v2 --> cls, value para @field_validator
    #	Con Pydantic v2 --> self (o cls, self) para @model_validator(mode="after")
    
class UserSignUp(BaseModel):
    """Modelo de entrada del endpoint /signup. Validamos que la contraseña sea correcta"""
    name: str = Field(...)
    age: Optional[int] = Field(None, ge=0, description=" Tu edad debe ser mayor a 0" )
    email: EmailStr = Field(...)
    password: str = Field(...,min_length=8, description="La contraseña debe tener al menos 8 caracteres alfanuméricos. ")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    age: Optional[int]
    email: EmailStr
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    """Modelo para actualizar datos del usuario"""
    # Ambos campos deben ser Optional para permitir actualizaciones parciales
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Mínimo 3 caracteres, máximo 100.")
    age: Optional[int] = Field(None, ge=0, description=" Tu edad debe ser mayor a 0" )


class DailyLogInput(BaseModel):
    """Registro de métricas diarias"""
    log_date: date = Field(...,description="Fecha del registro.")
    steps: Optional[int] = Field(None, ge=0, description="Solo pueden introducirse valores positivos.")
    exercise_minutes: Optional[int] = Field(None, ge=0, description="Solo pueden introducirse valores positivos.")
    sleep_hours: Optional[float] = Field(None, ge=0, le=24, description="Solo pueden introducirse valores entre 0 y 24.")
    water_liters: Optional[float] = Field(None, ge=0, le=10, description="Solo pueden introducirse valores positivos.")
    diet_score: Optional[int] = Field(None, ge=0, le=10, description="Solo pueden introducirse valores entre 0 y 10.")
    mood: Optional[int] = Field(None, ge=0, le=10, description="Solo pueden introducirse valores entre 0 y 10.")

    @field_validator("log_date")
    def validate_date(cls, value):
        if value > date.today():
            raise ValueError("La fecha introducida debe ser de hoy u otro día anterior.")
        return value
    
    @model_validator(mode="after")
    def validate_total_hours(self):
        ex_min = self.exercise_minutes if self.exercise_minutes is not None else 0
        sl_hrs = self.sleep_hours if self.sleep_hours is not None else 0
        __total_hours = (ex_min / 60) + sl_hrs
        if __total_hours > 24.01: # Pequeño margen por precisión de float
            raise ValueError("El numero de horas totales (sueño y deporte) no puede ser mayor de 24h.")
        return self 

class DailyLogOutput (DailyLogInput):
    user_id: str
    
    class Config:
        from_attributes = True


class MetricType(str, Enum):
    """Agregaciones diponibles para las métricas."""
    AVERAGE = "avg"
    MINIMUM = "min"
    MAXIMUM = "max"

# Modelo para la consulta que devuelve TODAS las métricas (AVG, MIN, MAX)
class LogTrendsOut(BaseModel):
    """Modelo para devolver las principales métricas de tendencia (promedios, mín y máx)."""

    avg_steps: Optional[float]
    min_steps: Optional[float]
    max_steps: Optional[float]

    avg_exercise_minutes: Optional[float]
    min_exercise_minutes: Optional[float]
    max_exercise_minutes: Optional[float]
    
    avg_sleep_hours: Optional[float]
    min_sleep_hours: Optional[float]
    max_sleep_hours: Optional[float]

    avg_water_liters: Optional[float]
    min_water_liters: Optional[float]
    max_water_liters: Optional[float]

    avg_diet_score: Optional[float]
    min_diet_score: Optional[float]
    max_diet_score: Optional[float]

    avg_mood: Optional[float]
    min_mood: Optional[float]
    max_mood: Optional[float]
    
# Alias para el endpoint dinámico (GET /user/trends)
MetricsSummary = Dict[str, Optional[float]]
