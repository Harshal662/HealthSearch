import hashlib
import numpy as np
from app.config import settings

MODEL = None
try:
    from sentence_transformers import SentenceTransformer
    MODEL = SentenceTransformer(settings.EMBEDDING_MODEL)
except Exception:
    MODEL = None

def get_embedding(text: str):
    """
    Returns a numpy array vector of dimension settings.VECTOR_DIM.
    If sentence-transformers is available, uses it; otherwise deterministic mock.
    """
    if MODEL:
        vec = MODEL.encode(text)
        vec = np.array(vec, dtype=np.float32)
        # If model returns different dim, pad or trim
        if vec.shape[0] != settings.VECTOR_DIM:
            if vec.shape[0] > settings.VECTOR_DIM:
                vec = vec[:settings.VECTOR_DIM]
            else:
                pad = np.zeros(settings.VECTOR_DIM - vec.shape[0], dtype=np.float32)
                vec = np.concatenate([vec, pad])
        return vec
    h = hashlib.sha256(text.encode("utf-8")).digest()
    arr = np.frombuffer(h, dtype=np.uint8).astype(np.float32)
    # tile/resize to desired dimension and normalize
    vec = np.resize(arr, settings.VECTOR_DIM).astype(np.float32)
    norm = np.linalg.norm(vec) + 1e-9
    return vec / norm
