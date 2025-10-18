import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage_memory import clear_store
from app.config import settings

@pytest.fixture(autouse=True)
def clear():
    clear_store()
    yield
