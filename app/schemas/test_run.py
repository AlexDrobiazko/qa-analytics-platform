from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TestRunCreate(BaseModel):
    project_id: int
    run_name: str
    source_type: str
    status: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0


class TestRunRead(BaseModel):
    id: int
    project_id: int
    run_name: str
    source_type: str
    status: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)