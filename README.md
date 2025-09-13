# GoIt PythonWeb HW-08

REST API project using **FastAPI** with **PostgreSQL**.  
Managed with **Poetry** and runnable via **Docker Compose**.

## 🚀 Features

- ✅ Async API with FastAPI
- ✅ PostgreSQL database
- ✅ Alembic migrations
- ✅ Async SQLAlchemy ORM
- ✅ User management (CRUD, search, upcoming birthdays)
- ✅ Custom error handling

---

## 📦 Requirements

- Python 3.11+
- Poetry
- Docker & Docker Compose

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory with the following content:

````env
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres

API_HOST=0.0.0.0
API_PORT=5000

```For development, you can also create a .env.dev with:
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres

API_HOST=127.0.0.1
API_PORT=8001
````

## Run with Docker

To build and start the app with Docker Compose:

docker compose up -d --build

## 💻 Run Locally with Poetry

- First, install dependencies:

1. poetry install
2. run postgres db
3. Setup .env.dev file
4. ➤ Start the development server (auto-reload):
   - poetry run dev

- OR Start the production server (no reload):

poetry run prod
