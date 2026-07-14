"""Сохранение и просмотр результатов упражнений."""

import json

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import ExerciseResult
from app.schemas import ResultCreate, ResultOut

router = APIRouter(prefix="/api/results", tags=["results"])


@router.post("", response_model=ResultOut, status_code=201)
async def save_result(data: ResultCreate, db: AsyncSession = Depends(get_db)):
    result = ExerciseResult(
        exercise_type=data.exercise_type,
        score=data.score,
        correct_answers=data.correct_answers,
        total_attempts=data.total_attempts,
        duration_seconds=data.duration_seconds,
        extra_data=json.dumps(data.extra_data, ensure_ascii=False) if data.extra_data else None,
    )
    db.add(result)
    await db.flush()
    await db.refresh(result)
    return _to_out(result)


@router.get("", response_model=list[ResultOut])
async def list_results(
    exercise_type: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = select(ExerciseResult).order_by(ExerciseResult.created_at.desc(), ExerciseResult.id.desc())
    if exercise_type:
        query = query.where(ExerciseResult.exercise_type == exercise_type)
    query = query.limit(min(max(limit, 1), 100))
    rows = (await db.execute(query)).scalars().all()
    return [_to_out(row) for row in rows]


def _to_out(row: ExerciseResult) -> ResultOut:
    return ResultOut(
        id=row.id,
        exercise_type=row.exercise_type,
        score=row.score,
        correct_answers=row.correct_answers,
        total_attempts=row.total_attempts,
        duration_seconds=row.duration_seconds,
        extra_data=json.loads(row.extra_data) if row.extra_data else None,
        created_at=row.created_at,
    )
