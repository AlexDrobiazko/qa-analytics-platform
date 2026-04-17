from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    test_run_id: Mapped[int] = mapped_column(
        ForeignKey("test_runs.id"),
        nullable=False
    )

    test_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    duration_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )