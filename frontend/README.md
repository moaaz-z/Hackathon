# CodeScope AI Frontend

React + Vite frontend for the AI Codebase Auditor.

## Run

```bash
npm install
cp .env.example .env
npm run dev
```

Backend defaults to `http://127.0.0.1:8000`.

The frontend sends:

```json
{ "github_url": "https://github.com/owner/repository" }
```

to `POST /repository/analyze`.

It accepts the AI report under `analysis`, `ai_analysis`, `report`, or `result`, so it can adapt to common backend response shapes.

No Gemini key is used in the frontend.
