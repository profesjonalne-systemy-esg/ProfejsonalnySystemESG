"""Testy działają na prawdziwym PostgreSQL, w osobnej bazie <nazwa>_test, po migracjach Alembic."""

import os
import tempfile
from pathlib import Path

import psycopg
import pytest
from sqlalchemy.engine import make_url

url = make_url(os.environ["DATABASE_URL"])
test_url = url.set(database=f"{url.database}_test")
admin_url = url.set(drivername="postgresql").render_as_string(hide_password=False)
with psycopg.connect(admin_url, autocommit=True) as conn:
    conn.execute(f'DROP DATABASE IF EXISTS "{test_url.database}" WITH (FORCE)')
    conn.execute(f'CREATE DATABASE "{test_url.database}"')
os.environ["DATABASE_URL"] = test_url.render_as_string(hide_password=False)
os.environ["AUTH_DEMO"] = "false"
os.environ["UPLOAD_DIR"] = tempfile.mkdtemp(prefix="esg_test_")

from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import seed  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.deps import get_current_user  # noqa: E402
from app.models import Project, User  # noqa: E402
from main import app  # noqa: E402

command.upgrade(Config(str(Path(__file__).resolve().parent.parent / "alembic.ini")), "head")


@pytest.fixture(autouse=True)
def clean_db():
    yield
    app.dependency_overrides.clear()
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def db():
    with SessionLocal() as session:
        yield session


@pytest.fixture
def anon():
    """Klient bez zalogowanego użytkownika."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def demo(db):
    """Dane przykładowe z app/seed.py. Zwraca projekt demo."""
    seed.seed()
    return db.query(Project).one()


@pytest.fixture
def as_user(db, anon):
    """as_user("kierownik@demo.pl") - klient działający jako wskazany użytkownik."""

    def _as(email: str):
        user = db.query(User).filter(User.email == email).one()
        app.dependency_overrides[get_current_user] = lambda: user
        return anon

    return _as


@pytest.fixture
def client(demo, as_user):
    """Klient zalogowany jako specjalista@demo.pl, właściciel projektu demo."""
    return as_user("specjalista@demo.pl")
