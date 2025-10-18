from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List
from app.models import AddNoteRequest, SearchResponse
from app.auth import get_token
from app.embeddings import get_embedding
from app.config import settings
from app.search import search_memory
from app.storage_memory import add_note as add_note_memory, clear_store
from app.deps import choose_backend

# If using postgres
from app.storage_pg import init_db, add_note_pg, search_pg
import asyncio

app = FastAPI(title="HealthSearch", version="1.0")

BACKEND = choose_backend()

@app.on_event("startup")
async def startup_event():
    if BACKEND == "postgres":
        # call init_db
        try:
            await init_db()
        except Exception as e:
            # fail loudly for misconfiguration
            raise RuntimeError(f"Failed to init DB: {e}")

@app.post("/add_note", dependencies=[Depends(get_token)])
async def add_note_endpoint(payload: AddNoteRequest):
    emb = get_embedding(payload.note)
    if BACKEND == "memory":
        add_note_memory(payload.patient_id, payload.note, emb)
        return {"status": "ok"}
    else:
        # Postgres
        try:
            nid = await add_note_pg(payload.patient_id, payload.note, emb)
            return {"status": "ok", "id": nid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

@app.get("/search_notes", dependencies=[Depends(get_token)])
async def search_notes(q: str = Query(..., min_length=1), top_k: int = Query(3, ge=1, le=50)):
    q_emb = get_embedding(q)
    if BACKEND == "memory":
        results = search_memory(q_emb, top_k=top_k)
        return {"query": q, "results": results}
    else:
        try:
            results = await search_pg(q_emb, top_k=top_k)
            return {"query": q, "results": results}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

@app.get("/_health")
async def health():
    return {"status": "ok", "backend": BACKEND}
