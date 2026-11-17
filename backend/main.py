import os

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="ESG Reporting Platform API",
    description="Backend dla systemu raportowania i ekstrakcji danych z plików budowlanych",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello ESG!"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/health/db")
def health_db():
    try:
        with psycopg.connect(os.environ["DATABASE_URL"].replace("+psycopg", ""), connect_timeout=3) as conn:
            row = conn.execute(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            ).fetchone()
        return {"status": "ok", "pgvector": row[0] if row else None}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "error", "detail": str(e)})
