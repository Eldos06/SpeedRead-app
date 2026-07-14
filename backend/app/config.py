"""Настройки приложения. Для MVP — SQLite, без внешних сервисов.

При переходе на PostgreSQL достаточно поменять DATABASE_URL, например:
postgresql+asyncpg://user:password@localhost/speedread
"""

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./speedread.db")
APP_ENV = os.environ.get("APP_ENV", "development")
