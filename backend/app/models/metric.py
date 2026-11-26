from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base

# pillar: E | S | G      status: pending | approved | rejected


class Metric(Base):
    """Wskaźnik wyciągnięty z dokumentu. Zapisuje Epik 4, weryfikuje Epik 5."""

    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    indicator = Column(String(40), nullable=False)
    pillar = Column(String(1), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(40), nullable=False)
    # ślad rewizyjny
    page = Column(Integer)
    quote = Column(Text)
    quote_verified = Column(Boolean, nullable=False, server_default="false")
    confidence = Column(Float)
    status = Column(String(20), nullable=False, server_default="pending")
    original_value = Column(Float)  # wartość sprzed ręcznej zmiany
    reviewed_by_id = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
