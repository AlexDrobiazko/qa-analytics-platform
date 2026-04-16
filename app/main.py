from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI(title="QA Analytics Platform")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()
        return {"database": "ok", "value": value}
    except Exception as exc:
        return {"database": "error", "details": str(exc)}