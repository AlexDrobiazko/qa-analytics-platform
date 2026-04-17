from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.project import Project
from app.models.test_run import TestRun
from app.schemas.test_run import TestRunCreate, TestRunRead

router = APIRouter(prefix="/test-runs", tags=["test-runs"])


@router.post("/", response_model=TestRunRead)
def create_test_run(payload: TestRunCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == payload.project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    test_run = TestRun(
        project_id=payload.project_id,
        run_name=payload.run_name,
        source_type=payload.source_type,
        status=payload.status,
        total_tests=payload.total_tests,
        passed_tests=payload.passed_tests,
        failed_tests=payload.failed_tests,
    )

    db.add(test_run)
    db.commit()
    db.refresh(test_run)
    return test_run


@router.get("/", response_model=list[TestRunRead])
def list_test_runs(db: Session = Depends(get_db)):
    return db.query(TestRun).order_by(TestRun.id.desc()).all()


@router.get("/{test_run_id}", response_model=TestRunRead)
def get_test_run(test_run_id: int, db: Session = Depends(get_db)):
    test_run = db.query(TestRun).filter(TestRun.id == test_run_id).first()

    if test_run is None:
        raise HTTPException(status_code=404, detail="Test run not found")

    return test_run


@router.get("/by-project/{project_id}", response_model=list[TestRunRead])
def list_test_runs_by_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return (
        db.query(TestRun)
        .filter(TestRun.project_id == project_id)
        .order_by(TestRun.id.desc())
        .all()
    )