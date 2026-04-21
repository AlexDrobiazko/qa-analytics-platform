from fastapi import FastAPI
from sqlalchemy import text
from app.api.test_runs import router as test_runs_router
from app.api.projects import router as projects_router
from app.api.test_results import router as test_results_router
from app.api.dashboard import router as dashboard_router
from app.db.session import engine
from app.api.ui import router as ui_router
from app.api.demo_ui import router as demo_ui_router

app = FastAPI(title="QA Analytics Platform")

app.include_router(projects_router)
app.include_router(test_runs_router)
app.include_router(test_results_router)
app.include_router(dashboard_router)
app.include_router(ui_router)
app.include_router(demo_ui_router)

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