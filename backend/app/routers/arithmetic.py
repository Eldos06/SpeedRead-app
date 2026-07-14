"""Арифметика: генерация уравнений (логика перенесена из Flask-версии)."""

import operator
from random import choice, randint

from fastapi import APIRouter

from app.schemas import MathProblem

router = APIRouter(prefix="/api/arithmetic", tags=["arithmetic"])

OPERATOR_MAP = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
DIFFICULTY_RANGES = {"easy": (1, 20), "medium": (1, 50), "hard": (1, 99)}


def generate_math_problem(difficulty: str = "easy") -> dict:
    """Формирует уравнение с результатом. Для деления результат всегда целый."""
    lo, hi = DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES["easy"])
    operator_symbol = choice(list(OPERATOR_MAP))

    number_left = randint(lo, hi)
    number_right = randint(lo, hi)
    if operator_symbol == "/":
        number_left = number_right * randint(1, 10)

    result = OPERATOR_MAP[operator_symbol](number_left, number_right)
    return {
        "equation": f"{number_left} {operator_symbol} {number_right}",
        "result": float(result),
        "difficulty": difficulty if difficulty in DIFFICULTY_RANGES else "easy",
    }


@router.get("/problem", response_model=MathProblem)
async def get_problem(difficulty: str = "easy"):
    return generate_math_problem(difficulty)
