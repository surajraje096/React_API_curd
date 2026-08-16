# 🤖 Python AI Agent Platform

A production-ready Python AI Agent application built with **FastAPI**, **PostgreSQL** (via SQLAlchemy 2.0 async), **Function Tools**, **Human-in-the-Loop (HITL)** approval workflows for risky actions, **Structured Audit Logging**, and **Automated Quality Evaluations**.

---

## 🌟 Features

- **Single Core AI Agent**: Intelligent orchestrator for natural language tool selection, execution, and state handling.
- **4 Function Tools**:
  - `search_user_account` *(Safe Tool)*: Read-only lookup for user account details and balances.
  - `get_system_health` *(Safe Tool)*: Diagnostic health metrics and database connection status.
  - `transfer_funds` *(Risky Tool - HITL Required)*: Money transfer between accounts.
  - `reset_user_status` *(Risky Tool - HITL Required)*: Account status reset and suspension.
- **Human-in-the-Loop (HITL) Security**:
  - Automatically intercepts risky actions prior to execution.
  - Pauses execution and persists a `PENDING_APPROVAL` record in PostgreSQL.
  - Exposes approval APIs (`GET /api/v1/approvals`, `POST /api/v1/approvals/{id}/respond`) to inspect and approve or reject actions before database mutation occurs.
- **PostgreSQL Persistence**:
  - Stores `UserAccount`, `Conversation`, `Message`, `PendingApproval`, `AuditLog`, and `EvaluationRun` models.
  - Automatic fallback to local SQLite if PostgreSQL is offline for standalone development.
- **Logs & Evaluations System**:
  - **Structured Audit Logging**: Tracks tool calls, human decisions, execution latency, and input/output payloads in `audit_logs`.
  - **Evaluation Engine**: Measures tool selection accuracy, groundedness/faithfulness, and HITL safety compliance.

---

## 🏗️ Project Architecture

```
AI-Programing/
├── app/
│   ├── main.py                 # FastAPI application & entry point
│   ├── config.py               # Pydantic Settings
│   ├── db/
│   │   ├── base.py             # Async SQLAlchemy Engine & Session
│   │   ├── models.py           # Database Schema (ORM Models)
│   │   └── init_db.py          # DB Initialization & Seed Data
│   ├── agent/
│   │   ├── agent.py            # Core Agent orchestrator & tool router
│   │   ├── state.py            # Pydantic state models & API schemas
│   │   └── tools/              # Function tools
│   │       ├── database_tools.py # Safe read-only tools
│   │       └── risky_tools.py    # Sensitive tools requiring approval
│   ├── hitl/
│   │   └── approval_manager.py # Human approval pipeline
│   ├── logging_eval/
│   │   ├── logger.py           # Audit logger
│   │   └── evaluator.py        # Quality & safety evaluator
│   └── api/
│       ├── chat.py             # Agent chat endpoint
│       ├── approvals.py        # HITL approval endpoints
│       ├── logs.py             # Audit trail endpoints
│       └── evaluations.py     # Evaluation metrics endpoints
├── tests/
│   └── test_agent.py           # Pytest test suite
├── docker-compose.yml          # Postgres + FastAPI setup
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

If you have an OpenAI API key, add it to `.env`:
```env
OPENAI_API_KEY="sk-..."
```
*(Note: If no API key is provided, the platform automatically activates its built-in fallback intent router for local testing without external API dependencies.)*

### 2. Run with Docker Compose (Recommended for PostgreSQL)

```bash
docker-compose up --build
```

Access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 3. Run Locally (Python 3.11+)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/chat` | Send prompt to AI Agent. Safe tools execute automatically; risky tools pause and return `PENDING_APPROVAL`. |
| `GET` | `/api/v1/approvals` | List all risky tool execution requests awaiting human authorization. |
| `GET` | `/api/v1/approvals/{id}` | Retrieve full details of a specific approval request. |
| `POST` | `/api/v1/approvals/{id}/respond` | Approve (`action: "APPROVED"`) or reject (`action: "REJECTED"`) a risky tool. |
| `GET` | `/api/v1/logs` | Fetch audit logs and execution traces. |
| `GET` | `/api/v1/evaluations` | Get summary of accuracy, safety, and faithfulness evaluation metrics. |
| `POST` | `/api/v1/evaluations/run` | Run automated evaluation benchmark suite. |

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest tests/ -v
```

---

## 💡 Example Usage Workflow

1. **Query Safe Data (Direct Execution)**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Search account details for user Alice"}'
   ```

2. **Trigger Risky Action (Pauses for Human Approval)**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Transfer $300 from ACC-1001 to ACC-1002"}'
   ```
   *Response*: Returns `status: "PENDING_APPROVAL"` with `approval_id`.

3. **Approve Action via HITL Endpoint**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/api/v1/approvals/<APPROVAL_ID>/respond" \
     -H "Content-Type: application/json" \
     -d '{"action": "APPROVED", "responded_by": "supervisor@company.com"}'
   ```
   *Response*: Money transfer executes and database record is updated securely.
