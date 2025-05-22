from sqlalchemy import create_engine

try:
    engine = create_engine("postgresql://postgres:Password%4020@localhost:5432/taskdb")
    with engine.connect() as conn:
        print("Connection successful")
except Exception as e:
    print("Connection failed:", e)


sqlalchemy_url = "postgresql://postgres:Password%4020@localhost:5432/taskdb"
from sqlalchemy import create_engine


sqlalchemy_url = "postgresql://postgres:Password%4020@localhost:5432/taskdb"


engine = create_engine(sqlalchemy_url)


try:
    with engine.connect() as conn:
        print("Connection successful")
except Exception as e:
    print("Connection failed:", e)

