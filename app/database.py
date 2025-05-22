# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Make sure this matches your setup (Password@20 → URL-encoded as %40)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Password%4020@localhost:5432/taskdb"

# 1) Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2) Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3) Base class for your ORM models
Base = declarative_base()

