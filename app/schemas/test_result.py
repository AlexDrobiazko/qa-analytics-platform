from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TestResultCreate(BaseModel):
    test_run_id: int
    test_name: str
    status: str
    duration_ms: int = 0
    error_message: str | None = None


class TestResultRead(BaseModel):
    id: int
    test_run_id: int
    test_name: str
    status: str
    duration_ms: int
    error_message: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)