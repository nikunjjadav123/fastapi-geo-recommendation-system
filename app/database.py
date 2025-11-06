# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app import config

Base = declarative_base()

# Create SQLAlchemy engine
engine = create_engine(config.DATABASE_URL, echo=True)
print("Database URL:", config.DATABASE_URL)
# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database (create tables)
def init_db():
    import app.models  # Ensure models are imported before metadata.create_all
    Base.metadata.create_all(bind=engine)

# Optional: test connection
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ Database connected successfully!")
    except Exception as e:
        print("❌ Failed to connect to database:", e)
