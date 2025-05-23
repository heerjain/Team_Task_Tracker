Generic single-database configuration.
# Team Task Tracker API

A lightweight FastAPI service to track tasks across multiple projects.

## Features

- Full CRUD for **Projects** and **Tasks**
- PostgreSQL + SQLAlchemy ORM + Alembic migrations
- Pydantic v2 schemas for request/response validation
- Automated tests with `pytest`
- Continuous Integration with GitHub Actions
- Error handling & structured logging

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally (DB: `taskdb`, user: `postgres`, password: `Password@20`)
- [Optional] Docker & Docker Compose

### Installation

```bash
git clone <repo-url>
cd Team_task_tracker
python -m venv .venv
.venv\Scripts\activate         # Windows
# or: source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
