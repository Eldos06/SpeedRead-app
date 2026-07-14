# SpeedRead MVP — FastAPI + Flutter

Кроссплатформенный тренажёр скорочтения и внимания. Backend на Python (FastAPI + SQLite),
мобильное приложение на Flutter/Dart. Реализация по плану из StackPlan (MVP-этап: без
авторизации, PostgreSQL и Docker — их легко добавить следующим шагом).

## Структура

```
SpeedRead-app/
├── backend/            # Python FastAPI
│   ├── app/
│   │   ├── main.py     # точка входа, CORS, /api/health
│   │   ├── config.py   # DATABASE_URL (по умолчанию SQLite)
│   │   ├── database.py # async SQLAlchemy
│   │   ├── models.py   # таблица exercise_results
│   │   ├── schemas.py  # Pydantic-схемы
│   │   └── routers/
│   │       ├── schulte.py     # GET /api/schulte/generate?size=&style=
│   │       ├── arithmetic.py  # GET /api/arithmetic/problem?difficulty=
│   │       ├── stroop.py      # GET /api/stroop/generate
│   │       └── results.py     # POST/GET /api/results
│   └── requirements.txt
└── flutter_app/        # Flutter (iOS + Android + Web из одного кода)
    ├── pubspec.yaml
    └── lib/
        ├── main.dart
        ├── config.dart          # адрес API (--dart-define=API_BASE_URL=...)
        ├── models/
        ├── services/api_service.dart
        └── screens/             # home, schulte, arithmetic, stroop, mental, history
```

## Запуск backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger-документация: http://localhost:8000/docs

## Запуск Flutter-приложения

Нужен установленный Flutter SDK (https://docs.flutter.dev/get-started/install).
Папки платформ (android/, ios/, web/) генерируются одной командой:

```bash
cd flutter_app
flutter create . --project-name speedread_app
flutter pub get
flutter run
```

Адрес API подбирается автоматически (Android-эмулятор → `10.0.2.2:8000`,
остальные → `localhost:8000`). Для реального телефона укажи IP компьютера:

```bash
flutter run --dart-define=API_BASE_URL=http://192.168.1.10:8000
```

## Что умеет MVP

| Модуль | Экран Flutter | API |
|---|---|---|
| Таблица Шульте — 3 стиля: классика, красно-чёрная (Горбова), мульти-колор; размеры 3×3…6×6, таймер, счёт ошибок | `schulte_screen.dart` | `GET /api/schulte/generate` |
| Арифметика — 10 раундов, 3 уровня сложности | `arithmetic_screen.dart` | `GET /api/arithmetic/problem` |
| Тест Струпа — 10 раундов, замер реакции | `stroop_screen.dart` | `GET /api/stroop/generate` |
| Устный счёт — секундомер | `mental_count_screen.dart` | — |
| История результатов | `history_screen.dart` | `GET/POST /api/results` |

Цвета таблицы Шульте генерирует backend (HEX для фона и цифры каждой ячейки),
поэтому веб-версия и мобильное приложение всегда выглядят одинаково.

## Следующие шаги (по StackPlan)

1. JWT-авторизация (`/api/auth/register`, `/api/auth/login`) + `users` в БД.
2. PostgreSQL вместо SQLite (поменять `DATABASE_URL`) + миграции Alembic.
3. 60-дневная программа: таблица `training_sessions`, экран прогресса с графиком.
4. Redis (кэш, rate limiting), Docker Compose + Nginx, деплой на VPS.
