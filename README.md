## Task Manager Application
A simple full-stack task management application with authentication and CRUD functionality.
This Task Manager application allows users to create an account and securely log in to manage their tasks. Users can add, view, and access details of their tasks, as well as mark them as completed or delete them when no longer needed. Each user can access only their own tasks, ensuring privacy and proper task management.

  - Deployment link: `https://task-manager-mcgk.onrender.com/`
  - GitHub repository: `https://github.com/BarathThanigai/task-manager`

## Overview

A simple full-stack Task Manager application that includes:

- FastAPI REST API
- JWT authentication
- PostgreSQL database with SQLAlchemy
- Simple responsive frontend using HTML, CSS, and JavaScript
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

## Tech Stack
- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Frontend: HTML, CSS, JavaScript
- Authentication: JWT
- Testing: Pytest
- Containerization: Docker


## API Endpoints

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
DB_CONNECT_MAX_RETRIES=10
DB_CONNECT_RETRY_DELAY_SECONDS=2
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

The project is fully containerized using Docker and can be run using docker-compose.
Run the full stack with Docker Compose:

```bash
docker compose up --build
```

For local development, keep `DATABASE_URL` pointed at `localhost`.
For Docker Compose, the app service overrides `DATABASE_URL` internally to use the Docker hostname `db`.

## Deployment Notes

This project is ready to deploy on Render or Railway as a single web service.

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir backend`
- Ensure environment variables are set in the platform dashboard
- Keep `.env` out of version control
- Use a managed PostgreSQL instance and set `DATABASE_URL` from the provider connection string
