"""Точка входа FastAPI.

Запуск для разработки:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Интерактивная документация: http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import arithmetic, results, schulte, stroop


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Для MVP создаём таблицы при старте; в продакшене — миграции Alembic.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="SpeedRead API",
    description="Тренажёр скорочтения и внимания — MVP",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS: '*' допустим только в разработке; в продакшене указать конкретный домен.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schulte.router)
app.include_router(arithmetic.router)
app.include_router(stroop.router)
app.include_router(results.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
