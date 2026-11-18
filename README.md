# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```

You can also install [eslint-plugin-react-x](https://npmx.dev/package/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://npmx.dev/package/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```
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
