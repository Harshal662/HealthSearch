# HealthSearch - semantic notes search (FastAPI)

## Overview

**HealthSearch** is a FastAPI-based microservice that ingests clinical notes and enables **semantic search** using vector embeddings.  
It demonstrates a clean architecture integrating **AI embeddings**, **token-based security**, and **vector similarity search**.

#### Key Features
- **Two storage backends**
  - **Memory** (default): Fast and simple for demos/tests.
  - **Postgres + pgvector**: Persistent, production-grade.
- **Embeddings**
  - Uses `sentence-transformers` model if installed.
  - Fallback to deterministic mock embeddings if not.
- **Token-based Authentication**
  - Secured endpoints with Bearer token validation.
- **Bonus Implementations**
  - Dockerized setup with `docker-compose`.
  - Integrated `pgvector` extension for vector storage.
  - Automated testing using `pytest`.

---
## Architecture

```
FastAPI
 ├── app/
 │   ├── main.py            → Entry point for API
 │   ├── auth.py            → Token-based authentication
 │   ├── embeddings.py      → Embedding generation logic
 │   ├── storage_memory.py  → In-memory storage backend
 │   ├── storage_pg.py      → PostgreSQL + pgvector backend
 │   ├── search.py          → Similarity computation logic
 │   ├── config.py          → Environment and configuration
 │   ├── models.py          → Pydantic schemas
 │   └── deps.py            → Dependency management
 ├── docker/
 │   └── init-db.sh         → Initializes pgvector extension
 ├── tests/                 → pytest test suite
 ├── Dockerfile
 ├── docker-compose.yml
 ├── requirements.txt
 ├── .env.example
 └── README.md
```
---
## Quick Start (Development Mode – Memory Backend)

#### 1. Setup Environment
```
cp .env.example .env
```
Edit `.env` if you wish to set a custom token or change configuration.

#### 2. Install Dependencies
```
pip install -r requirements.txt
```

#### 3. Run FastAPI Server
```
uvicorn app.main:app --reload
```

#### 4. Example API Usage
```
# Add a note
curl -X POST "http://localhost:8000/add_note" \
  -H "Authorization: Bearer change-to-a-secure-token" \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"P001","note":"Patient has fever and cough."}'

# Search for notes
curl "http://localhost:8000/search_notes?q=fever" \
  -H "Authorization: Bearer change-to-a-secure-token"
  ```
--- 

## Run with Postgres + pgvector (Dockerized Setup)

#### 1. Prerequisites

Ensure Docker and Docker Compose are installed.

#### 2.  Configure Environment
```
cp .env.example .env
```

**Then update:**
```
BACKEND=postgres
HEALTHSEARCH_TOKEN=your-secure-token
```

#### 3. Build and Launch
```
docker compose up --build
```

**This launches:**

- Postgres (with `pgvector` extension auto-created)
- FastAPI app (running on port `8000`)

#### 4. Example Test
```
curl -X POST "http://localhost:8000/add_note" \
  -H "Authorization: Bearer your-secure-token" \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"P001","note":"Patient has chest pain and cough."}'

curl "http://localhost:8000/search_notes?q=chest pain" \
  -H "Authorization: Bearer your-secure-token"
  ```

##### The API will return top-3 similar notes ranked by cosine similarity.

  **Note:**
      The script `docker/init-db.sh` ensures `CREATE EXTENSION IF NOT EXISTS vector;` on container startup.
  
---

## Running Tests
```
pytest -q
```

- Tests use the memory backend for speed and isolation.
- Includes authentication and search validation.



*If this gives error the use -*
```
python -m pytest -q
```

--- 

## API Endpoints


| Method | Endpoint        | Description               | Auth Required |
| ------ | --------------- | ------------------------- | ------------- |
| `POST` | `/add_note`     | Add a new clinical note   | ✅ Yes         |
| `GET`  | `/search_notes` | Search notes by semantics | ✅ Yes         |
| `GET`  | `/_health`      | Health check endpoint     | ❌ No          |

#### Request Body Example:
```
{
  "patient_id": "P001",
  "note": "Patient reports chest pain and shortness of breath."
}
```


#### Response Example:
```

{
  "query": "shortness of breath",
  "results": [
    {
      "patient_id": "P001",
      "note": "Patient reports chest pain and shortness of breath.",
      "similarity": 0.9784
    }
  ]
}
```
---
## Verify Inside DB

**Once it’s running:**
```
docker exec -it healthsearch-db psql -U postgres -d healthsearch
```

**Then in psql:**
```
\dx
```

**You should see:**
```
List of installed extensions
 Name   | Version | Schema | Description
--------+----------+--------+------------------------------------
 plpgsql | 1.0    | pg_catalog | PL/pgSQL procedural language
 vector  | 0.6.0  | public     | vector data type for embeddings
```

---

## Environment Variables
| Variable             | Description                          | Default                                                       |
| -------------------- | ------------------------------------ | ------------------------------------------------------------- |
| `HEALTHSEARCH_TOKEN` | API security token                   | `change-to-a-secure-token`                                 |
| `BACKEND`            | Backend mode (`memory` / `postgres`) | `memory`                                                      |
| `DATABASE_URL`       | Postgres connection URL              | `postgresql+asyncpg://postgres:postgres@db:5432/healthsearch` |
| `VECTOR_DIM`         | Embedding dimension                  | `384`                                                         |
| `EMBEDDING_MODEL`    | Sentence Transformer model name      | `all-MiniLM-L6-v2`                                            |

---

## Technologies Used
- **FastAPI -** High-performance Python web framework

- **SentenceTransformers -** For semantic embeddings

- **Postgres + pgvector -**  Persistent vector similarity search

- **Docker -** Containerization

- **Pytest -** Testing framework

--- 

## Commands Cheat Sheet

| Action                        | Command                                           |
| ----------------------------- | ------------------------------------------------- |
| Run app (local memory mode)   | `uvicorn app.main:app --reload`                   |
| Run app (dockerized Postgres) | `docker compose up --build`                       |
| Run tests                     | `pytest -q`  or `python -m pytest -q`                                     |
| Add note                      | `curl -X POST http://localhost:8000/add_note ...` |
| Search notes                  | `curl http://localhost:8000/search_notes?q=...`   |
| To creaate `HEALTHSEARCH_TOKEN` (one of the way)   | `python -c "import secrets; print(secrets.token_urlsafe(32))`                   |

---
**© 2025 Checkmed - HealthSearch Prototype by Harshal Abak**
*AI-powered semantic search for clinical notes.*