import pytest

from app import seed
from app.models import Project, User


def test_health(anon):
    assert anon.get("/api/health").json() == {"status": "ok"}
    assert anon.get("/api/health/db").json()["pgvector"]


@pytest.mark.parametrize("path", ["/api/auth/me", "/api/projects", "/api/projects/1"])
def test_login_is_required(anon, demo, path):
    assert anon.get(path).status_code == 401


def test_demo_mode_only_when_enabled(anon, demo, monkeypatch):
    monkeypatch.setenv("AUTH_DEMO", "true")
    assert anon.get("/api/auth/me").json()["email"] == "specjalista@demo.pl"


def test_seed_can_run_twice(demo, db):
    seed.seed()
    assert db.query(Project).count() == 1
    assert db.query(User).count() == 3


def test_owner_sees_only_own_projects(client, demo, db, as_user):
    other = User(email="inny@demo.pl", full_name="Inny", password_hash="x")
    db.add(other)
    db.commit()
    assert [p["id"] for p in client.get("/api/projects").json()] == [demo.id]
    stranger = as_user("inny@demo.pl")
    assert stranger.get("/api/projects").json() == []
    assert stranger.get(f"/api/projects/{demo.id}").status_code == 404
    manager = as_user("kierownik@demo.pl")
    assert manager.get(f"/api/projects/{demo.id}").status_code == 200
