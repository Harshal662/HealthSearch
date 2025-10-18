import numpy as np
from app.storage_memory import all_notes

def cosine_sim(a: np.ndarray, b: np.ndarray):
    denom = (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b) / denom)

def search_memory(query_vec, top_k=3):
    items = all_notes()
    results = []
    for item in items:
        sim = cosine_sim(query_vec, item["embedding"])
        results.append({"patient_id": item["patient_id"], "note": item["note"], "similarity": sim})
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
