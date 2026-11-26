from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base

# status: uploaded | processing | processed | failed


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), nullable=False, default="uploaded")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    mime_type = Column(String(120))
    size_bytes = Column(Integer)
    error = Column(Text)


class DocumentPage(Base):
    """Tekst jednej strony PDF, arkusza XLSX albo całego DOCX. Zapisuje Epik 3, czyta Epik 4 i 5."""

    __tablename__ = "document_pages"
    __table_args__ = (UniqueConstraint("document_id", "page"),)

    id = Column(Integer, primary_key=True)
    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    page = Column(Integer, nullable=False)
    label = Column(String(120), nullable=False)
    text = Column(Text, nullable=False)
    is_ocr = Column(Boolean, nullable=False, server_default="false")
