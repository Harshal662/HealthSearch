import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, select
from pgvector.sqlalchemy import Vector
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
VECTOR_DIM = settings.VECTOR_DIM

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[str] = mapped_column(String, nullable=False)
    note_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list] = mapped_column(Vector(VECTOR_DIM))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_note_pg(patient_id: str, note_text: str, embedding):
    async with AsyncSessionLocal() as session:
        note = Note(patient_id=patient_id, note_text=note_text, embedding=list(map(float, embedding.tolist())))
        session.add(note)
        await session.commit()
        await session.refresh(note)
        return note.id

async def search_pg(query_embedding, top_k=3):
    # Using Postgres pgvector operator <=> (distance). We will select top-k by distance and compute similarity as 1 - distance (for cosine if using vector_cosine ops).
    async with AsyncSessionLocal() as session:
        q = """
        SELECT id, patient_id, note_text, 1 - (embedding <=> $1::vector) AS similarity
        FROM notes
        ORDER BY embedding <=> $1::vector
        LIMIT :k
        """
        from sqlalchemy import text
        vec_str = "[" + ",".join(map(str, map(float, query_embedding.tolist()))) + "]"
        stmt = text(q).bindparams(k=top_k)
        res = await session.execute(stmt, {"1": vec_str, "k": top_k})
        rows = res.fetchall()
        results = []
        for row in rows:
            # row[1]=patient_id, row[2]=note_text, row[3]=similarity
            results.append({
                "patient_id": row[1],
                "note": row[2],
                "similarity": float(row[3])
            })
        return results
