"""Epik 3: wgrywanie i przetwarzanie plików."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, get_editable_project, get_project
from app.models import Document, Project, User
from app.schemas.document import DocumentOut
from app.services.documents import storage

router = APIRouter(prefix="/api", tags=["documents"])


@router.get("/projects/{project_id}/documents", response_model=list[DocumentOut])
def list_documents(project: Project = Depends(get_project), db: Session = Depends(get_db)):
    query = select(Document).where(Document.project_id == project.id).order_by(Document.id.desc())
    return db.scalars(query).all()


@router.post(
    "/projects/{project_id}/documents",
    response_model=list[DocumentOut],
    status_code=status.HTTP_201_CREATED,
)
def upload_documents(
    files: list[UploadFile] = File(...),
    project: Project = Depends(get_editable_project),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # najpierw sprawdzamy wszystkie pliki, żeby błąd w jednym nie zostawił połowy wgranej
    checked = []
    try:
        for upload in files:
            name = storage.clean_name(upload.filename)
            ext = storage.extension(name)
            checked.append((name, ext, storage.read_limited(upload.file, name)))
    except storage.UnsupportedType as e:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, str(e)) from None
    except storage.TooLarge as e:
        raise HTTPException(413, str(e)) from None

    documents = [
        Document(
            filename=name,
            file_path=storage.save(data, ext),
            status="uploaded",
            project_id=project.id,
            uploaded_by_id=user.id,
            mime_type=storage.MIME_TYPES[ext],
            size_bytes=len(data),
        )
        for name, ext, data in checked
    ]
    db.add_all(documents)
    db.commit()
    for document in documents:
        db.refresh(document)
    return documents
