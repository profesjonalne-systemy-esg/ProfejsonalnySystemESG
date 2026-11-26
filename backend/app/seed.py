"""Dane przykładowe do pracy lokalnej. Uruchamiane tylko przy SEED_DEMO=true, można powtarzać.

Dzięki nim każdy epik ma na czym pracować, zanim inne epiki dostarczą prawdziwe dane.
"""

import os

import bcrypt
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Document, DocumentPage, Metric, Project, Report, User

PASSWORD = "Demo1234"
USERS = [
    ("specjalista@demo.pl", "Anna Specjalista", "specialist"),
    ("kierownik@demo.pl", "Jan Kierownik", "manager"),
    ("admin@demo.pl", "Ewa Administrator", "admin"),
]
DOCS = {
    "faktura_energia.pdf": "FAKTURA VAT - rozliczenie roczne\nOkres: 01.01.2025 - 31.12.2025\n"
    "Razem zużycie energii czynnej: 412 350 kWh\nWartość netto: 252 481,91 zł",
    "statystyki_bhp.pdf": "Statystyki BHP 2025\nPrzepracowane godziny: 610 000\n"
    "Wypadki przy pracy ogółem: 3\nWypadki śmiertelne: 0",
    "lad_korporacyjny.pdf": "Ład korporacyjny 2025\nZarząd liczy 5 członków.\n"
    "Liczba potwierdzonych przypadków korupcji: 0",
}
METRICS = [
    ("faktura_energia.pdf", "GRI 302-1", "E", "Energia elektryczna", 412.35, "MWh", 2, 0.95),
    ("statystyki_bhp.pdf", "GRI 403-9", "S", "Przepracowane godziny", 610000, "h", 1, 0.93),
    ("statystyki_bhp.pdf", "GRI 403-9", "S", "Wypadki przy pracy", 3, "liczba", 2, 0.91),
    ("lad_korporacyjny.pdf", "GRI 2-9", "G", "Członkowie zarządu", 5, "osoby", 1, 0.9),
    ("lad_korporacyjny.pdf", "GRI 205-3", "G", "Przypadki korupcji", 0, "liczba", 2, 0.62),
]
DRAFT = (
    "<h1>Raport ESG 2025</h1><h2>Środowisko (E)</h2>"
    "<p>Zużycie energii elektrycznej wyniosło <strong>412,35 MWh</strong>.</p>"
    "<h2>Społeczeństwo (S)</h2><ul><li>Wypadki przy pracy: 3</li></ul>"
)


def seed() -> None:
    with SessionLocal() as db:
        if db.scalar(select(User.id).where(User.email == USERS[0][0])):
            return
        hashed = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()
        users = [User(email=e, full_name=n, role=r, password_hash=hashed) for e, n, r in USERS]
        db.add_all(users)
        db.flush()
        project = Project(
            name="Raport ESG 2025 (przykład)",
            company_name="Budomex S.A. (firma fikcyjna)",
            year=2025,
            owner_id=users[0].id,
        )
        db.add(project)
        db.flush()
        docs = {}
        for name, text in DOCS.items():
            doc = Document(
                filename=name,
                file_path=f"przyklad/{name}",
                status="processed",
                project_id=project.id,
                uploaded_by_id=users[0].id,
                mime_type="application/pdf",
                size_bytes=len(text.encode()),
            )
            db.add(doc)
            db.flush()
            db.add(DocumentPage(document_id=doc.id, page=1, label="Strona 1", text=text))
            docs[name] = doc
        for name, code, pillar, label, value, unit, line, confidence in METRICS:
            db.add(
                Metric(
                    project_id=project.id,
                    document_id=docs[name].id,
                    indicator=code,
                    pillar=pillar,
                    name=label,
                    value=value,
                    unit=unit,
                    page=1,
                    quote=DOCS[name].split("\n")[line],
                    quote_verified=True,
                    confidence=confidence,
                )
            )
        db.add(Report(project_id=project.id, content_html=DRAFT))
        db.commit()


if __name__ == "__main__":
    if os.getenv("SEED_DEMO", "false").lower() == "true":
        seed()
