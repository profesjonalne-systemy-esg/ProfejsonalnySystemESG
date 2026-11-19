# Uruchomienie projektu (Docker Compose)

Docker Compose uruchamia trzy usługi: frontend (React + Vite), backend (FastAPI) i bazę danych (PostgreSQL + pgvector).

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
| http://localhost:5173 | Aplikacja frontendowa |
| http://localhost:5173/api/health/db | `{"status":"ok","pgvector":"…"}` – frontend → backend → baza |
| http://localhost:8000/api/health | `{"status":"ok"}` |
| http://localhost:8000/docs | Swagger UI |

Zmiany w plikach frontendu (`src/`) są widoczne od razu. Po zmianach w `backend/`, `requirements.txt` lub `package.json` uruchom ponownie z `--build`.
