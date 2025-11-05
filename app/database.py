from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

Base = declarative_base()

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print("Failed to connect to database:", e)

def init_db():
    Base.metadata.create_all(bind=engine)


