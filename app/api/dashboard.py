from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/top-failures")
def get_top_failures(db: Session = Depends(get_db)):
    rows = (
        db.query(
            TestResult.test_name,
            func.count(TestResult.id).label("failures")
        )
        .filter(TestResult.status == "failed")
        .group_by(TestResult.test_name)
        .order_by(func.count(TestResult.id).desc())
        .all()
    )

    return [
        {
            "test_name": row.test_name,
            "failures": row.failures,
        }
        for row in rows
    ]


@router.get("/flaky-tests")
def get_flaky_tests(db: Session = Depends(get_db)):
    rows = (
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

    return [
        {
            "test_name": row.test_name,
            "total_runs": row.total_runs,
            "is_flaky": True,
        }
        for row in rows
    ]


@router.get("/by-project/{project_id}")
def get_project_dashboard(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    run_ids_subquery = (
        db.query(TestRun.id)
        .filter(TestRun.project_id == project_id)
        .subquery()
    )

    test_runs = db.query(func.count(TestRun.id)).filter(
        TestRun.project_id == project_id
    ).scalar()

    test_results = db.query(func.count(TestResult.id)).filter(
        TestResult.test_run_id.in_(run_ids_subquery)
    ).scalar()

    passed = db.query(func.count(TestResult.id)).filter(
        TestResult.test_run_id.in_(run_ids_subquery),
        TestResult.status == "passed"
    ).scalar()

    failed = db.query(func.count(TestResult.id)).filter(
        TestResult.test_run_id.in_(run_ids_subquery),
        TestResult.status == "failed"
    ).scalar()

    pass_rate = 0

    if test_results:
        pass_rate = round((passed / test_results) * 100, 2)

    return {
        "project_id": project.id,
        "project_name": project.name,
        "test_runs": test_runs,
        "test_results": test_results,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
    }


