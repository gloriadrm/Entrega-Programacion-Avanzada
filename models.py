from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Importamos Base (definida en database.py) para que los modelos hereden de ella

class UserDB(Base): 
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    age = Column(Integer, nullable =True)
    email = Column(String, unique = True, index= True)
    password_hash = Column(String, nullable=False)
    # back_populates, on delete cascade
    logs = relationship("DailyLogDB", back_populates="user", cascade="all, delete-orphan" )
    # mejora --> timestamps: created_at, updated_at.

class DailyLogDB(Base):
    __tablename__='logs'
    # Clave primaria compuesta
    user_id = Column(String,ForeignKey("users.id"), primary_key=True )
    log_date=Column(Date, primary_key=True ,index=True)
    # Métricas 
    steps = Column(Integer, nullable = True)
    exercise_minutes = Column(Integer, nullable = True)
    sleep_hours = Column(Float, nullable = True)
    water_liters = Column(Float, nullable = True)
    diet_score = Column(Integer, nullable = True)
    mood = Column(Integer, nullable = True)
    # back_populates
    user = relationship("UserDB", back_populates="logs")
