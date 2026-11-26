from pathlib import Path

import pytest

from app.models import Document
from app.services.documents import storage


def url(project):
    return f"/api/projects/{project.id}/documents"


def files(*names, data=b"tresc"):
    return [("files", (name, data)) for name in names]


def test_upload_many_files(client, demo, db):
    r = client.post(url(demo), files=files("a.pdf", "b.XLSX", "c.docx"))
    assert r.status_code == 201
    assert [d["filename"] for d in r.json()] == ["a.pdf", "b.XLSX", "c.docx"]
    saved = db.query(Document).filter(Document.filename == "b.XLSX").one()
    assert Path(saved.file_path).read_bytes() == b"tresc"
    assert saved.uploaded_by_id == demo.owner_id
    assert [d["filename"] for d in client.get(url(demo)).json()][:3] == [
        "c.docx",
        "b.XLSX",
        "a.pdf",
    ]


def test_same_name_does_not_overwrite(client, demo, db):
    client.post(url(demo), files=files("x.pdf", data=b"pierwszy"))
    client.post(url(demo), files=files("x.pdf", data=b"drugi"))
    paths = [d.file_path for d in db.query(Document).filter(Document.filename == "x.pdf")]
    assert {Path(p).read_bytes() for p in paths} == {b"pierwszy", b"drugi"}


@pytest.mark.parametrize("name", ["../../etc/x.pdf", "..\\..\\x.pdf"])
def test_path_in_filename_is_removed(client, demo, name):
    r = client.post(url(demo), files=files(name))
    assert r.json()[0]["filename"] == "x.pdf"


def test_one_bad_file_rejects_all(client, demo):
    before = len(client.get(url(demo)).json())
    assert client.post(url(demo), files=files("dobry.pdf", "zly.exe")).status_code == 415
    assert len(client.get(url(demo)).json()) == before


def test_too_large_file(client, demo, monkeypatch):
    monkeypatch.setattr(storage, "MAX_BYTES", 10)
    assert client.post(url(demo), files=files("a.pdf", data=b"x" * 11)).status_code == 413


def test_locked_and_foreign_projects(client, demo, db, as_user):
    assert as_user("kierownik@demo.pl").post(url(demo), files=files("a.pdf")).status_code == 403
    demo.status = "in_review"
    db.commit()
    assert as_user("specjalista@demo.pl").post(url(demo), files=files("a.pdf")).status_code == 409
