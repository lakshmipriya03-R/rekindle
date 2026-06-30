# Rekindle

> AI Life Journal for Dementia and Alzheimer's Patients

Rekindle is a compassionate journaling application powered by AI, designed to help patients living with dementia preserve memories, track emotions, and have meaningful conversations with an AI companion that remembers their story.

## Features

- **Journal** — Write, search, and revisit memories with full-text search and pagination
- **Emotion Detection** — Automatic emotion analysis on every journal entry and chat message
- **AI Companion** — Memory-aware chat that uses journal history to provide contextual, compassionate responses
- **Timeline** — Chronological view of memories with emotion overlays
- **Emotion Dashboard** — Charts and statistics for emotional trends
- **Dashboard** — Overview of activity, mood trends, and recent entries

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env         # Fill in SECRET_KEY and OPENAI_API_KEY
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### Docker (full stack)

```bash
cp backend/.env.example .env
# Edit .env with your keys
docker-compose up --build
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, SQLAlchemy, Alembic |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Authentication | JWT + bcrypt |
| AI Companion | OpenAI GPT-4o-mini (or HuggingFace local) |
| Emotion Detection | HuggingFace Transformers (distilroberta) |
| Frontend | React, Vite, Tailwind CSS |
| Deployment | Docker, GitHub Actions |

## Architecture

```
Request → Router → Service → Model/AI → Pydantic Schema → Response
```

Clean architecture: routers never contain business logic. Services are independently testable.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | JWT signing key (min 32 chars) |
| `DATABASE_URL` | SQLite or PostgreSQL URL |
| `AI_PROVIDER` | `openai` or `huggingface` |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_MODEL` | Model name (default: gpt-4o-mini) |
| `EMOTION_MODEL` | HuggingFace emotion model |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins |

## Deployment

**Railway / Render** — set env vars in dashboard, deploy from GitHub, run `alembic upgrade head` as release command.

**Vercel** — deploy `frontend/` with `VITE_API_URL` pointing to your backend URL.
