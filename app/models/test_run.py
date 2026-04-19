from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TestRun(Base):
    __tablename__ = "test_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    run_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    source_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    external_run_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    total_tests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    passed_tests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    failed_tests: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )