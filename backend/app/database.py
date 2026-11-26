import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# sciezka do pliku .env w glownym folderze backend
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# pobranie adresu bazy danych
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL nie zostal ustawiony w pliku .env")

# utworzenie polaczenia z postgresql
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# fabryka sesji
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# klasa bazowa dla modeli
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
