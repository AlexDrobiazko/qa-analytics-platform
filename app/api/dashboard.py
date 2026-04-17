from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.test_run import TestRun
from app.models.test_result import TestResult

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    projects = db.query(func.count(Project.id)).scalar()
    test_runs = db.query(func.count(TestRun.id)).scalar()
    test_results = db.query(func.count(TestResult.id)).scalar()

    passed = db.query(func.count(TestResult.id)).filter(
        TestResult.status == "passed"
    ).scalar()

    failed = db.query(func.count(TestResult.id)).filter(
        TestResult.status == "failed"
    ).scalar()

    pass_rate = 0

    if test_results:
        pass_rate = round((passed / test_results) * 100, 2)

    return {
        "projects": projects,
        "test_runs": test_runs,
        "test_results": test_results,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate
    }