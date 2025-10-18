from pydantic import BaseModel, Field
from typing import List

class AddNoteRequest(BaseModel):
    patient_id: str = Field(..., example="P001")
    note: str = Field(..., example="Patient reports chest pain and shortness of breath.")

class SearchResult(BaseModel):
    patient_id: str
    note: str
    similarity: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
