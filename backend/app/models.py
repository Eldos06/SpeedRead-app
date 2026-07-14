"""Таблицы базы данных."""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class ExerciseResult(Base):
    """Результат одного прохождения упражнения.

    Для MVP — без пользователей и авторизации; user_id появится вместе с JWT.
    """

    __tablename__ = "exercise_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_type: Mapped[str] = mapped_column(String(50), index=True)  # schulte / arithmetic / stroop / mental
    score: Mapped[float] = mapped_column(Float, default=0.0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    total_attempts: Mapped[int] = mapped_column(Integer, default=0)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0)
    extra_data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON-строка с деталями упражнения
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())



