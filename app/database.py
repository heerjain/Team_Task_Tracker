
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Password%%4020@localhost:5432/taskdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app import models
def create_tables():
    Base.metadata.create_all(bind=engine)


