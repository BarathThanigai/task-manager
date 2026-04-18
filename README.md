# FastAPI Task Manager

A simple full-stack Task Manager. It includes:

- FastAPI REST API
- JWT authentication
- PostgreSQL database with SQLAlchemy
- Basic responsive frontend using HTML, CSS, and JavaScript
- Task pagination and completion filtering
- Pytest test coverage
- Docker support

## Project Structure

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
frontend/
  static/
tests/
```

## Features

- `POST /register` for user registration
- `POST /login` for JWT login
- `POST /tasks` to create a task
- `GET /tasks` to list the logged-in user's tasks
- `GET /tasks/{id}` to fetch one task
- `PUT /tasks/{id}` to update title, description, or completion status
- `DELETE /tasks/{id}` to delete a task
- Filtering with `?completed=true` or `?completed=false`
- Pagination with `?skip=0&limit=5`
- Built-in Swagger docs at `/docs`

## Environment Variables

Create a `.env` file locally using `.env.example`.

```env
SECRET_KEY=replace-with-a-secure-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=60
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace-with-a-secure-password
POSTGRES_DB=task_manager
DATABASE_URL=postgresql+psycopg://postgres:replace-with-a-secure-password@localhost:5432/task_manager
```

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn app.main:app --reload --app-dir backend
```

4. Open:

- App UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## Running Tests

```bash
pytest
```

## Docker

Run the full stack with Docker Compose:

```bash
docker compose up --build
```
