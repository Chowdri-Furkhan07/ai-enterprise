# AI Enterprise Assistant

A multi-agent enterprise AI assistant that combines Retrieval-Augmented Generation (RAG), SQL querying, and role-based reporting. Built with **FastAPI**, **CrewAI**, **AutoGen**, and **LangChain**, powered by **AWS Bedrock** LLMs, with vector search across **Pinecone** and **FAISS**, and a **Streamlit** frontend.

## Features

- **Multi-agent orchestration** — a `Manager` routes each query to the right specialist agent:
  - `ResearchAgent` — in-depth topic research and analysis
  - `RetrievalAgent` — RAG over uploaded documents (Pinecone first, FAISS fallback)
  - `SQLAgent` — natural-language-to-SQL querying against MySQL
  - `ReportAgent` — formats output differently for `admin`, `analyst`, and `viewer` roles
  - `ValidationAgent` — sanity-checks generated responses before they're returned
- **Document ingestion pipeline** — upload PDF, CSV, or DOCX files; they're loaded, chunked, and indexed into both Pinecone and FAISS
- **Conversation memory** — the last 5 Q&A exchanges are persisted to `memory.json` and fed back in as context
- **Alternate agent frameworks included** — a parallel `CrewAI` crew (`crew/crew.py`) and an `AutoGen` group chat (`autogen/agents.py`, `autogen/chats.py`) implement the same researcher/retriever/reporter workflow
- **JWT-based auth** — role is embedded in the token and used to tailor report output
- **Streamlit UI** — simple frontend for file upload and chat, calling the FastAPI backend

## Architecture

```
frontend/app.py  ──(HTTP)──▶  app/main.py (FastAPI)
                                    │
                              agents/manager.py
                        ┌───────────┼────────────┐
                        ▼           ▼             ▼
                ResearchAgent  RetrievalAgent   SQLAgent
                   (core/llm)  (Pinecone/FAISS)  (MySQL)
                        │           │             │
                        └─────▶ ReportAgent ◀──────┘
                                    │
                            ValidationAgent
                                    │
                            core/memory.py (memory.json)
```

LLM calls go through `core/llm.py`, which invokes an AWS Bedrock model via `boto3`.

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Multi-agent frameworks | CrewAI, AutoGen (pyautogen), LangChain |
| LLM | AWS Bedrock (`boto3`) |
| Embeddings | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Vector stores | Pinecone, FAISS |
| Relational DB | MySQL |
| Document parsing | pypdf, python-docx, docx2txt, pandas |
| Auth | PyJWT, passlib |

## Project Structure

```
app/            FastAPI app, auth (JWT), config/env loading
agents/         Manager + specialist agents (research, retrieval, sql, report, validation)
core/           LLM client (Bedrock), embeddings, FAISS store, Pinecone store, memory
crew/           CrewAI-based alternate multi-agent implementation
autogen/        AutoGen-based alternate multi-agent implementation
tools/          File loader, text chunker, SQL tool, MCP-style tool router
database/       MySQL connection/query helper
frontend/       Streamlit UI
data/           Sample data / uploaded files
faiss_index/    Persisted local FAISS index
Screenshots/    App screenshots
enterprise.sql  Database bootstrap script
Dockerfile      Container build for the FastAPI backend
```

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/Chowdri-Furkhan07/ai-enterprise.git
cd ai-enterprise
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=meta.llama3-8b-instruct-v1:0

PINECONE_API_KEY=your_pinecone_api_key

MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=enterprise_ai

JWT_SECRET=your_jwt_secret
```

Make sure your AWS credentials (for Bedrock) are configured separately, e.g. via `aws configure` or standard AWS environment variables.

### 3. Set up the database

```bash
mysql -u root -p < enterprise.sql
```

### 4. Run the backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Run the frontend

```bash
streamlit run frontend/app.py
```

### Or run with Docker

```bash
docker build -t ai-enterprise .
docker run -p 8000:8000 --env-file .env ai-enterprise
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload` | Upload a file (PDF/CSV/DOCX); it's chunked and indexed into Pinecone + FAISS |
| `POST` | `/query` | Ask a question, with `q` (query) and `role` (`admin` / `analyst` / `viewer`) params |

## Screenshots

See the [`Screenshots/`](./Screenshots) folder for the upload flow, admin view, analyst view, and summary view.

## Notes

- `app/auth.py` currently uses a hardcoded `SECRET` placeholder for JWT signing — replace this with `JWT_SECRET` from your environment before deploying.
- This is a work-in-progress project; contributions and issues are welcome.

## License

No license specified yet.
