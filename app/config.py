# app/config/config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Detect environment: default to 'docker'
ENV = os.getenv("ENV", "docker")

if ENV == "local":
    user = os.getenv("LOCAL_DB_USER")
    password = os.getenv("LOCAL_DB_PASSWORD")
    host = os.getenv("LOCAL_DB_HOST", "127.0.0.1")
    port = os.getenv("LOCAL_DB_PORT", "5432")
    db = os.getenv("LOCAL_DB_NAME")
else:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "db")  # Docker service name
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
