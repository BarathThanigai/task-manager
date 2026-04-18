from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.core.config import get_settings
from app.db.session import Base, engine
import app.models  # noqa: F401


settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(tasks_router)

frontend_dir = Path(__file__).resolve().parents[2] / "frontend" / "static"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    return FileResponse(frontend_dir / "index.html")


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
