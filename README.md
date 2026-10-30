# AI CSV Analyzer

> Turn your CSV into actionable insights — statistics, data-quality scoring, interactive
> visualizations, AI-powered analysis, and a chat with your own AI data analyst.

A production-ready, self-hosted full-stack web application. Upload a CSV, and the app
automatically inspects, cleans, and analyzes it with **Pandas/NumPy**, then layers optional
**OpenAI** insights and chat on top. The frontend is served directly by **FastAPI** — no
Node.js, no build step, no Live Server.

---

## Project Overview

```
Upload CSV
    ↓
Automatically inspect the dataset
    ↓
Clean / validate / detect data types
    ↓
Generate statistics & data-quality scores
    ↓
Generate visualizations (Chart.js)
    ↓
Generate AI-powered insights (OpenAI)
    ↓
Chat with the dataset (OpenAI)
    ↓
Download professional reports (PDF / CSV)
```

## Features

- **Smart CSV analysis** — automatic column type detection (numeric, categorical, date,
  boolean, text, constant) and semantic role detection (revenue, quantity, category, date, …).
- **Data-quality engine** — health score, missing values, duplicates, consistency,
  uniqueness, constant columns, sparse columns, and outlier detection.
- **Statistics** — count, mean, median, min, max, std, quartiles, sum, outliers for numeric
  columns; unique/top/frequency for categorical columns; date ranges.
- **Interactive visualizations** — bar, line, area, doughnut, histogram, and scatter charts
  built server-side from real data (never hard-coded), plus a custom chart builder.
- **Deterministic rule-based insights** — key findings, trends, risks and recommendations
  computed locally (works without AI).
- **AI-powered insights & chat** — grounded executive summaries, key findings, trends, data
  quality concerns, business insights, and recommended actions using your own **OpenAI API key**.
- **Reports** — downloadable **PDF** reports and **CSV** summaries of the analysis.
- **Demo dataset** — a clearly-labeled sample retail dataset for instant evaluation.
- **Privacy & security** — API key never stored on the server; uploads sanitized and stored
  under UUID names; no secrets in code, config, logs, or database.
- **Modern responsive UI** — SaaS-style dashboard, light/dark theme, mobile/tablet/desktop.

## Architecture

```
                    USER
                      │
                      ▼
                 index.html
                      │
          ┌───────────┴───────────┐
          │                       │
        CSS                  JavaScript
          │                       │
          └───────────┬───────────┘
                      ▼
                FASTAPI
                      │
       ┌──────────────┼──────────────┐
       │              │              │
       ▼              ▼              ▼
     Pandas         SQLite        OpenAI
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
                Dashboard
                Charts
                Insights
                AI Chat
                Reports
```

- **Backend** — FastAPI + SQLAlchemy + SQLite + Pandas/NumPy.
- **Frontend** — HTML5/CSS3/vanilla JS + Bootstrap 5 + Chart.js (served by FastAPI).
- **AI** — OpenAI Chat Completions via a compact, distilled *data context* (never the raw file).

## Tech Stack

| Layer      | Technology                                            |
|------------|-------------------------------------------------------|
| Backend    | Python 3.10+, FastAPI, Uvicorn, Pydantic v2           |
| Data       | Pandas, NumPy, CSV encoding/delimiter detection       |
| Database   | SQLite (auto-initialized) via SQLAlchemy 2.x          |
| AI         | OpenAI API (user-provided key, `gpt-4o-mini`) |
| Frontend   | HTML5, CSS3, vanilla JS, Bootstrap 5, Chart.js 4, Bootstrap Icons |
| Reports    | ReportLab (PDF), stdlib JSON/CSV                      |
| Testing    | pytest + FastAPI TestClient (tests use isolated storage and mocked AI) |

## Folder Structure

```
AI-CSV-ANALYZER/
│
├── index.html                 # SPA shell: landing + dashboard (served at /)
├── frontend/
│   ├── css/                   # style.css, dashboard.css, responsive.css
│   ├── js/                    # api, app, upload, dashboard, charts,
│   │                          #   insights, OpenAI, chat, reports
│   └── assets/vendor/         # Bootstrap 5, Chart.js, Bootstrap Icons (local)
├── backend/
│   ├── main.py                # FastAPI app, CORS, security headers, static mount
│   ├── config.py              # Environment-driven settings
│   ├── api/                   # health, datasets, analysis, chat, reports
│   ├── services/              # csv_analyzer, insights, ai_context, openai_service,
│   │                          #   report_service, demo_data
│   ├── database/              # database.py, models.py, repositories.py
│   ├── schemas/               # Pydantic request/response models
│   └── utils/                 # file_validation, security, logging
├── data/                      # SQLite database (auto-created: app.db)
├── tests/                     # test_health, test_upload, test_analysis,
│                              #   test_ai_service, test_chat
├── requirements.txt
├── .env.example
├── .gitignore
├── run.py
├── README.md
└── LICENSE
```

## Installation

Requires **Python 3.10+** (tested on 3.13). No Node.js or external database needed.

```bash
# 1. Clone / navigate into the project folder
cd AI-CSV-ANALYZER

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
# source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) copy the example config
copy .env.example .env        # Windows
# cp .env.example .env        # Linux / macOS
```

## Environment Variables

All settings are optional and read from environment variables / a `.env` file at the project
root. See [.env.example](./.env.example).

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | `production` disables `/docs` and `/redoc`, and requires `APP_ACCESS_TOKEN` |
| `HOST` / `PORT` | `127.0.0.1` / `8000` | Bind address (used by `run.py`) |
| `APP_ACCESS_TOKEN` | unset | Required in production; shared secret protecting data APIs |
| `DATABASE_URL` | `sqlite:///./data/app.db` | SQLAlchemy database URL |
| `DATA_DIR` | `./data` | SQLite storage directory |
| `UPLOAD_DIR` | `./uploads` | Uploaded CSV storage (UUID filenames) |
| `MAX_UPLOAD_SIZE_MB` | `25` | Maximum upload size |
| `MAX_ROWS` | `1000000` | Maximum rows loaded per file |
| `CORS_ORIGINS` | `http://localhost:8000,http://127.0.0.1:8000` | Allowed origins (comma-separated) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `OPENAI_API_KEY` | unset | Optional server-side OpenAI key; prefer the browser session connection dialog |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model for AI features |
| `OPENAI_API_URL` | OpenAI chat completions URL | OpenAI API endpoint |
| `OPENAI_FALLBACK_MODEL` | unset | Optional model tried if the primary model is unavailable |
| `OPENAI_TIMEOUT_SECONDS` | `60` | OpenAI request timeout |
| `OPENAI_MAX_RETRIES` | `2` | Retries on transient failures / rate limits |
| `OPENAI_MAX_CONTEXT_TOKENS` | `9000` | Context budget per AI request |
| `OPENAI_AI_INSIGHTS_TOKENS` | `1200` | Max output tokens for AI insights/chat |
| `CHAT_HISTORY_LIMIT` | `10` | Prior messages included in a chat request |
| `RATE_LIMIT_ENABLED` | `true` | Per-IP rate limiting for AI endpoints |
| `RATE_LIMIT_MAX_REQUESTS` | `30` | Requests per window |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Rate-limit window length |

> Enter your OpenAI API key through the app’s **Configure AI connection** dialog. It is kept
> in browser `sessionStorage` and sent per-request via `X-AI-API-Key`; do not commit keys.

For production, set `APP_ACCESS_TOKEN` to a unique random secret with at least 32 bytes of
randomness. Generate one with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
The browser prompts for the token on its first protected API request and retains it only in
tab-scoped `sessionStorage`. The token protects one shared workspace; this application does not
provide separate user accounts or per-user dataset ownership. Do not share the token with
untrusted users or use a single deployment as a multi-tenant service. Production API requests
are blocked if the token is missing.

## Running Locally

Preferred — a single command:

```bash
python run.py
```

Open <http://localhost:8000/> (or <http://127.0.0.1:8000>).

Alternative with hot reload:

```bash
uvicorn backend.main:app --reload
```

The app is **not** served via Live Server or `file://` — everything runs through FastAPI.

- Home page (frontend): <http://localhost:8000/>
- Interactive API docs: <http://localhost:8000/docs> (development only)
- Health check: <http://localhost:8000/api/health>

## OpenAI API Setup

AI features (AI insights, chat, connection test) require an OpenAI API key:

1. Create or sign in to an account at <https://platform.openai.com>.
2. Go to <https://platform.openai.com/api-keys> and create an API key.
3. Select the AI connection badge in the top bar, paste the key, click **Test connection**,
   then **Save for this session**. You can also open this dialog from the AI Insights or AI Chat prompt.

How the key is handled:

- Stored only in browser `sessionStorage` (cleared when the tab closes). Never in
  `localStorage`, the database, logs, or git.
- Sent with every AI request as an `X-AI-API-Key` header to the OpenAI API.
- The backend sends only a compact **data summary** (statistics, types, quality, top values)
  to the model — never the raw CSV contents.
- CSV-derived text is untrusted input. System instructions treat it as data, but prompt
  injection through uploaded content cannot be completely eliminated; review summaries before
  sharing sensitive datasets with an AI provider.

## API Documentation

All endpoints live under `/api` and return JSON. Errors use a consistent envelope:

```json
{ "success": false, "error": { "code": "MISSING_API_KEY", "message": "An OpenAI API key is required for AI requests." } }
```

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | App, version, environment, database status |

### Datasets

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/datasets/upload` | Upload a CSV (multipart `file`), analyze, return metadata |
| `POST` | `/api/datasets/demo` | Create and analyze a labeled demo dataset |
| `GET` | `/api/datasets` | List all datasets (newest first) |
| `GET` | `/api/datasets/{id}` | Dataset metadata |
| `GET` | `/api/datasets/{id}/preview?offset=&limit=` | Paginated row preview |
| `DELETE` | `/api/datasets/{id}` | Delete dataset and its stored file |

### Analysis

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/datasets/{id}/analysis` | Full stored analysis payload |
| `GET` | `/api/datasets/{id}/statistics` | Statistics grouped by column type |
| `GET` | `/api/datasets/{id}/insights` | Rule-based insights + summary |
| `POST` | `/api/datasets/{id}/chart-data` | Chart dataset from real values (`chart_type`, `x`, `y`/`value`, `aggregate`) |

### AI (requires `X-AI-API-Key` header)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ai/test` | Validate an OpenAI API key (returns model + latency) |
| `POST` | `/api/ai/insights` | Generate AI analysis (`dataset_id`), returns sections |
| `POST` | `/api/chat` | Ask a question about a dataset (`dataset_id`, `message`, `session_id?`) |
| `GET` | `/api/chat/suggestions?dataset_id=` | Dataset-aware starter questions |
| `GET` | `/api/chat/sessions?dataset_id=` | List chat sessions |
| `GET` | `/api/chat/{session_id}` | Full message history |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/reports?dataset_id=&report_format=pdf\|json\|csv` | Generate a downloadable report |

## Screenshots

*(Screenshots to be added — run the app locally, upload a CSV, and capture the landing page,
the dashboard overview with KPI cards, the visualizations section, and the AI chat.)*

## Deployment Guide

### Netlify Frontend Deployment

The frontend can be deployed to Netlify while FastAPI runs on a separate backend host.

1. **Point Netlify at the `frontend/` folder** (or set the publish directory to `frontend` if
   deploying the whole repo). No build command is required — it is plain static HTML/CSS/JS.
2. **Configure the backend URL.** Before deploying, inject the backend origin into
   `frontend/js/api.js` (or add a small snippet on the index page) using the supported
   configuration object:

   ```html
   <script>
     window.APP_CONFIG = { API_BASE_URL: "https://your-backend.example.com" };
   </script>
   ```

   `api.js` reads `window.APP_CONFIG.API_BASE_URL` (or `window.__APP_CONFIG__.API_BASE`) once,
   at load time, and prefixes every API call with it.
3. In development, where frontend and backend share an origin, leave `API_BASE_URL` unset —
   requests resolve to the same host automatically.

### FastAPI Backend Deployment

1. Deploy `backend/`, `index.html`, `requirements.txt`, and `run.py` to your host (Render,
   Railway, Fly.io, a VPS, etc.).
2. Set environment variables on the platform (see [Environment Variables](#environment-variables)),
   especially `APP_ENV=production`, a strong `APP_ACCESS_TOKEN`,
   `CORS_ORIGINS=https://your-app.netlify.app`, and a persistent
   `DATA_DIR` / `UPLOAD_DIR` if the platform does not persist the working directory.
3. Start with `python run.py` or `uvicorn backend.main:app --host 0.0.0.0 --port 8000`.
4. Put a reverse proxy (nginx / Caddy) in front for TLS and set `CORS_ORIGINS` to your public
   origin(s). Keep the shared access token private. SQLite + WAL is fine for single-node deployments; swap `DATABASE_URL` for
   PostgreSQL if you need multi-node concurrency.

## Running the Tests

```bash
python -m pytest tests -q
```

The suite spins up an isolated app with a temporary database and exercises the full
API — health, upload + validation errors, analysis, statistics, insights, chart data, reports,
and AI endpoints (with a mocked OpenAI client so no network or API key is required).


