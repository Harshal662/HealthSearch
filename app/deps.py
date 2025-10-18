from app.config import settings
from app import storage_memory, storage_pg

def choose_backend():
    if settings.BACKEND == "postgres":
        return "postgres"
    return "memory"
