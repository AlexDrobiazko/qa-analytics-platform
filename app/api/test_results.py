from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.test_result import TestResult
from app.models.test_run import TestRun
from app.schemas.test_result import TestResultCreate, TestResultRead

router = APIRouter(prefix="/test-results", tags=["test-results"])


@router.post("/", response_model=TestResultRead)
def create_test_result(payload: TestResultCreate, db: Session = Depends(get_db)):
    test_run = db.query(TestRun).filter(TestRun.id == payload.test_run_id).first()

    if test_run is None:
        raise HTTPException(status_code=404, detail="Test run not found")

    result = TestResult(
        test_run_id=payload.test_run_id,
        test_name=payload.test_name,
        status=payload.status,
        duration_ms=payload.duration_ms,
        error_message=payload.error_message,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result


@router.get("/", response_model=list[TestResultRead])
def list_results(db: Session = Depends(get_db)):
    return db.query(TestResult).order_by(TestResult.id.desc()).all()


@router.get("/by-run/{test_run_id}", response_model=list[TestResultRead])
def list_results_by_run(test_run_id: int, db: Session = Depends(get_db)):
    return (
        db.query(TestResult)
        .filter(TestResult.test_run_id == test_run_id)
        .order_by(TestResult.id.desc())
        .all()
    )