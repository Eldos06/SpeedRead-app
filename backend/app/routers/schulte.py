"""Таблицы Шульте: генерация цветной сетки.

Три стиля, как в референсе: classic (белые ячейки), red_black (красно-чёрная
таблица Горбова), multi (каждая ячейка — свой яркий цвет).
"""

from random import choice, shuffle

from fastapi import APIRouter

from app.schemas import SchulteCell, SchulteGrid

router = APIRouter(prefix="/api/schulte", tags=["schulte"])

ALLOWED_SIZES = (3, 4, 5, 6)
DEFAULT_SIZE = 5
STYLES = ("classic", "red_black", "multi")

DARK_TEXT = "#1F2933"
WHITE_TEXT = "#FFFFFF"

RED_BG = "#D7263D"
BLACK_BG = "#16161A"

# Палитра для multi-стиля: (фон, цвет цифры).
MULTI_PALETTE = [
    ("#22C55E", WHITE_TEXT),  # зелёный
    ("#F97316", WHITE_TEXT),  # оранжевый
    ("#3B82F6", WHITE_TEXT),  # синий
    ("#EF4444", WHITE_TEXT),  # красный
    ("#14B8A6", WHITE_TEXT),  # бирюзовый
    ("#A855F7", WHITE_TEXT),  # фиолетовый
    ("#EC4899", WHITE_TEXT),  # розовый
    ("#EAB308", DARK_TEXT),   # жёлтый
]


def _make_cells(size: int, style: str) -> list[SchulteCell]:
    numbers = list(range(1, size * size + 1))
    shuffle(numbers)

    if style == "red_black":
        # Половина ячеек чёрные, половина красные, распределены случайно.
        half = len(numbers) // 2
        colors = [BLACK_BG] * (len(numbers) - half) + [RED_BG] * half
        shuffle(colors)
        return [SchulteCell(number=n, bg=bg, text=WHITE_TEXT) for n, bg in zip(numbers, colors)]

    if style == "multi":
        return [
            SchulteCell(number=n, bg=bg, text=text)
            for n, (bg, text) in zip(numbers, (choice(MULTI_PALETTE) for _ in numbers))
        ]

    return [SchulteCell(number=n, bg="#FFFFFF", text=DARK_TEXT) for n in numbers]


@router.get("/generate", response_model=SchulteGrid)
async def generate_grid(size: int = DEFAULT_SIZE, style: str = "classic"):
    """Генерирует сетку Шульте выбранного размера и стиля."""
    if size not in ALLOWED_SIZES:
        size = DEFAULT_SIZE
    if style not in STYLES:
        style = "classic"
    return SchulteGrid(size=size, style=style, cells=_make_cells(size, style))
