import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    HEALTHSEARCH_TOKEN = os.getenv("HEALTHSEARCH_TOKEN", "")
    BACKEND = os.getenv("BACKEND", "memory")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/healthsearch")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    VECTOR_DIM = int(os.getenv("VECTOR_DIM", 384))

settings = Settings()
