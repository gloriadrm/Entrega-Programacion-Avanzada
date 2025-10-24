from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

# ------ DB setup ------
DATABASE_URL = "sqlite:///./healthy_logs.db"  
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()