"""Тест Струпа: слово-название цвета, напечатанное другим цветом."""

from random import sample, shuffle

from fastapi import APIRouter

from app.schemas import StroopCard, StroopOption

router = APIRouter(prefix="/api/stroop", tags=["stroop"])

STROOP_COLORS = {
    "red": {"label": "Красный", "hex": "#DC3545"},
    "green": {"label": "Зелёный", "hex": "#28A745"},
    "blue": {"label": "Синий", "hex": "#007BFF"},
    "yellow": {"label": "Жёлтый", "hex": "#E0A800"},
    "purple": {"label": "Фиолетовый", "hex": "#6F42C1"},
    "orange": {"label": "Оранжевый", "hex": "#FD7E14"},
}


@router.get("/generate", response_model=StroopCard)
async def generate_stroop():
    """Раунд Струпа: нужно назвать ЦВЕТ шрифта, а не слово."""
    word_key, color_key = sample(list(STROOP_COLORS), 2)  # разные ключи — слово и цвет не совпадают
    options = list(STROOP_COLORS)
    shuffle(options)
    return StroopCard(
        word=STROOP_COLORS[word_key]["label"],
        color_key=color_key,
        color_hex=STROOP_COLORS[color_key]["hex"],
        options=[
            StroopOption(key=key, label=STROOP_COLORS[key]["label"], hex=STROOP_COLORS[key]["hex"])
            for key in options
        ],
    )
