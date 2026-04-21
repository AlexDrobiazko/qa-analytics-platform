from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.test_result import TestResult
from app.models.test_run import TestRun

router = APIRouter(tags=["ui"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard/ui")
def dashboard_ui(request: Request, db: Session = Depends(get_db)):
    projects = db.query(func.count(Project.id)).scalar()
    test_runs = db.query(func.count(TestRun.id)).scalar()
    test_results = db.query(func.count(TestResult.id)).scalar()

    passed = (
        db.query(func.count(TestResult.id))
        .filter(TestResult.status == "passed")
        .scalar()
    )

    failed = (
        db.query(func.count(TestResult.id))
        .filter(TestResult.status == "failed")
        .scalar()
    )

    pass_rate = 0
    if test_results:
        pass_rate = round((passed / test_results) * 100, 2)

    top_failures = (
        db.query(
            TestResult.test_name,
            func.count(TestResult.id).label("failures")
        )
        .filter(TestResult.status == "failed")
        .group_by(TestResult.test_name)
        .order_by(func.count(TestResult.id).desc())
        .all()
    )

    flaky_tests = (
        db.query(
            TestResult.test_name,
            func.count(func.distinct(TestResult.status)).label("unique_statuses"),
            func.count(TestResult.id).label("total_runs"),
        )
        .group_by(TestResult.test_name)
        .having(func.count(func.distinct(TestResult.status)) > 1)
        .order_by(func.count(TestResult.id).desc())
        .all()
    )
    recent_runs = (
        db.query(TestRun)
        .order_by(TestRun.id.desc())
        .limit(10)
        .all()
    )
    
    total_for_chart = passed + failed
    passed_percent = 0
    failed_percent = 0

    if total_for_chart:
        passed_percent = round((passed / total_for_chart) * 100, 2)
        failed_percent = round((failed / total_for_chart) * 100, 2)
    
    return templates.TemplateResponse(
    request,
    "dashboard.html",
    {
        "summary": {
            "projects": projects,
            "test_runs": test_runs,
            "test_results": test_results,
            "passed": passed,
            "failed": failed,
            "pass_rate": pass_rate,
        },
        "top_failures": top_failures,
        "flaky_tests": flaky_tests,
        "recent_runs": recent_runs,
        "chart": {
            "passed_percent": passed_percent,
            "failed_percent": failed_percent,
            "passed": passed,
            "failed": failed,
        },
    },
)