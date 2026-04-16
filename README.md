# Semantic Audio Search

> **Status: Active development (MVP in progress)**

Search inside long-form media using natural language. Submit a YouTube URL, process it asynchronously, then query the indexed content to get relevant transcript moments and timestamps.

---

## Current Architecture

```
Client -> FastAPI backend -> RabbitMQ -> transcription_worker -> embedding_queue -> embedding_worker
                      |
                      +-> PostgreSQL (content metadata, users, history)
```

### What is implemented now

- Backend API with content, search, auth, and history routes
- RabbitMQ integration for async processing
- `transcription_worker` with `yt-dlp + ffmpeg + Whisper`
- `embedding_worker` service scaffold (consumer loop exists; processing callback is still TODO)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, SQLAlchemy, Pydantic |
| Message Broker | RabbitMQ |
| Transcription | OpenAI Whisper, yt-dlp, ffmpeg |
| Database | PostgreSQL |
| Infra | Docker, Docker Compose |

---

## API Endpoints (Current)

### Content
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/content/preview` | Fetch metadata preview before processing |
| `POST` | `/api/v1/content/process` | Submit content for async processing |
| `GET` | `/api/v1/content/{id}` | Get content metadata |
| `GET` | `/api/v1/content/{id}/status` | Get processing status |

Possible statuses in code: `pending`, `extracting_media`, `transcribing`, `generating_vectors`, `ready`, `failed`.

### Search
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/search/` | Run semantic search for content |

### Auth
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register user |
| `POST` | `/api/v1/auth/login` | Login user |

### Users / History
| Method | Endpoint | Description |
|---|---|---|
| `PUT` | `/api/v1/users/profile` | Update user profile |
| `GET` | `/api/v1/users/history` | Get user search history |
| `DELETE` | `/api/v1/users/history/{id}` | Delete one history item |
| `DELETE` | `/api/v1/users/history` | Delete all user history |

---

## Environment Variables

At minimum, create root `.env` (copy from `.env.example`):

```env
DATABASE_URL=postgresql://user:password@localhost:5432/semantic_audio
RABBITMQ_USER=user
RABBITMQ_PASS=password
RABBITMQ_URL=amqp://user:password@rabbitmq:5672/
```

Worker-local `.env.example` files currently also include:

```env
INTERNAL_API_KEY=secured_api_key
```

`transcription_worker` additionally expects:

```env
BACKEND_URL=http://backend:8000
```

---

## Run With Docker Compose

```bash
docker compose up --build
```

Services currently defined in `docker-compose.yml`:

- `backend` on `http://localhost:8000`
- `transcription_worker`
- `rabbitmq` and management UI on `http://localhost:15672`

Note: `embedding_worker` exists in the repository but is not yet wired into `docker-compose.yml`.

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### Transcription Worker

```bash
cd transcription_worker
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Troubleshooting

### `ModuleNotFoundError` in `transcription_worker`

If you see import errors like `No module named 'extractors.base_extractor'`, verify:

- Imports reference `base_audio_extractor` (not `base_extractor`)
- You are running from `transcription_worker` directory with `python main.py`
- `transcription_worker/extractors/__init__.py` exists (it does in this repo)

---

## Project Structure

```
semantic-audio-search/
├── backend/
│   ├── api/routes/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   └── app.py
├── transcription_worker/
│   ├── extractors/
│   └── main.py
├── embedding_worker/
│   └── main.py
├── docker-compose.yml
└── .env.example
```