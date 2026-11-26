import os
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# dodanie folderu backend do sciezki importowania
sys.path.append(str(Path(__file__).resolve().parent.parent))

# wczytanie zmiennych z pliku .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# import bazy i modeli
from app.database import Base
from app import models

# adres bazy danych
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL nie zostal ustawiony")

# konfiguracja alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# metadane modeli
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
