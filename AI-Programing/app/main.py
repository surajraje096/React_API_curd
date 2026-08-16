import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.base import get_db_session
from app.db.init_db import init_db
from app.api.router import api_router
from app.ui_html import UI_HTML_CONTENT

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup & shutdown events."""
    logger.info("Initializing database tables & demo seed data...")
    await init_db()
    logger.info("Database initialization complete.")
    yield
    logger.info("Shutting down AI Agent service.")


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-grade Python AI Agent with PostgreSQL persistence, "
        "function tools, Human-in-the-Loop approval for risky actions, "
        "and structured audit logs & evaluations."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API Router
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse, tags=["UI Dashboard"])
@app.get("/ui", response_class=HTMLResponse, tags=["UI Dashboard"])
async def render_ui_dashboard():
    """Serves the interactive web UI dashboard for the AI Agent & HITL Approval Center."""
    return HTMLResponse(content=UI_HTML_CONTENT)


@app.get("/health", tags=["System"], status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """Health check endpoint validating database connectivity."""
    try:
        await db.execute(select(1))
        db_status = "HEALTHY"
    except Exception as e:
        db_status = f"UNHEALTHY ({str(e)})"

    return {
        "status": "OK" if db_status == "HEALTHY" else "DEGRADED",
        "database": db_status,
        "active_model": settings.DEFAULT_MODEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
