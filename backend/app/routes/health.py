import os

import psycopg
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
async def health_check():
    return {"status": "ok"}


@router.get("/db")
def health_db():
    try:
        url = os.environ["DATABASE_URL"].replace("+psycopg", "")
        with psycopg.connect(url, connect_timeout=3) as conn:
            row = conn.execute(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            ).fetchone()
        return {"status": "ok", "pgvector": row[0] if row else None}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "error", "detail": str(e)})
