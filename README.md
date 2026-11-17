# Uruchomienie projektu (Docker Compose)

> **Stan:** w Docker Compose działają obecnie backend (FastAPI) i baza danych (PostgreSQL + pgvector).
> Kontener frontendu (React) zostanie dodany po ukończeniu US 1.4 – dopiero wtedy US 1.1 będzie kompletne.

## Wymagania

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) – uruchomiony (status „Engine running”)
- Git

## Uruchomienie

```bash
git clone https://github.com/profesjonalne-systemy-esg/ProfejsonalnySystemESG.git
cd ProfejsonalnySystemESG
cp .env.example .env
docker compose up --build
```

Pierwsze uruchomienie trwa kilka minut (pobieranie obrazów i zależności).

Zatrzymanie: `Ctrl+C`, a następnie `docker compose down`.

## Sprawdzenie, czy działa

| Adres | Oczekiwany wynik |
|---|---|
| http://localhost:8000/api/health | `{"status":"ok"}` |
| http://localhost:8000/api/health/db | `{"status":"ok","pgvector":"…"}` – backend połączył się z bazą |
| http://localhost:8000/docs | Swagger UI |
