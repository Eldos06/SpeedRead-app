"""Pydantic-схемы запросов и ответов API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SchulteCell(BaseModel):
    number: int
    bg: str    # HEX цвет фона ячейки
    text: str  # HEX цвет цифры


class SchulteGrid(BaseModel):
    size: int
    style: str  # classic / red_black / multi
    cells: list[SchulteCell]  # плоский список из size*size ячеек, слева направо построчно


class MathProblem(BaseModel):
    equation: str
    result: float
    difficulty: str


class StroopOption(BaseModel):
    key: str
    label: str
    hex: str


class StroopCard(BaseModel):
    word: str        # слово-название цвета
    color_key: str   # ключ реального цвета шрифта — правильный ответ
    color_hex: str   # HEX реального цвета шрифта
    options: list[StroopOption]


class ResultCreate(BaseModel):
    exercise_type: str = Field(pattern="^(schulte|arithmetic|stroop|mental)$")
    score: float = 0.0
    correct_answers: int = 0
    total_attempts: int = 0
    duration_seconds: float = 0.0
    extra_data: dict[str, Any] | None = None


class ResultOut(BaseModel):
    id: int
    exercise_type: str
    score: float
    correct_answers: int
    total_attempts: int
    duration_seconds: float
    extra_data: dict[str, Any] | None = None
    created_at: datetime
