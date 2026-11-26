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

## Praca równoległa

Każdy epik ma swoje pliki i nie zmienia cudzych. Wspólne pliki (`main.py`, `App.tsx`, `AppShell.tsx`, `models/`, `requirements.txt`, `package.json`, `docker-compose.yml`) zmieniamy tylko po uzgodnieniu w zespole.

| Epik | Osoba | Backend (`backend/`) | Frontend (`src/`) |
|---|---|---|---|
| 2 Użytkownicy i panel | Damian | `app/deps.py`, `routes/auth.py`, `routes/projects.py`, `services/auth`, `services/projects` | `features/auth`, `features/projects`, `api/client.ts` |
| 3 Pliki | Piotr K | `routes/documents.py`, `services/documents` | `features/documents` |
| 4 Silnik AI | Piotr B | `routes/ai.py`, `services/ai` | `features/knowledge` |
| 5 Weryfikacja | Mateusz | `routes/metrics.py`, `services/metrics` | `features/metrics` |
| 6 Edytor i akceptacja | Michał | `routes/reports.py`, `services/reports` | `features/editor` |
| 7 Eksport i testy | cały zespół | `routes/exports.py`, `services/exports` | uzgodnić |

Schematy i testy: osobne pliki na epik w `app/schemas` i `tests`.

Domyślnie aplikacja działa bez logowania (`AUTH_DEMO=true`) na danych przykładowych (`SEED_DEMO=true`). Dzięki temu nikt nie czeka na cudzy epik.

Po zmianie `package.json` uruchom `docker compose up --build -V` (bez `-V` kontener nie zobaczy nowych paczek).

Testy backendu (przy działającym `docker compose up --build`):

```bash
docker compose run --rm backend sh -c "pip install -q -r requirements-dev.txt && python -m pytest -q"
```
