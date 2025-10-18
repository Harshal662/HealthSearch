from typing import List, Dict
import numpy as np
from app.config import settings

_store: List[Dict] = []

def add_note(patient_id: str, note: str, embedding: np.ndarray):
    _store.append({"patient_id": patient_id, "note": note, "embedding": embedding.astype(np.float32)})

def all_notes():
    return _store

def clear_store():
    global _store
    _store = []
