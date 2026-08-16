import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


def create_db_engine(db_url: str):
    if db_url.startswith("sqlite"):
        return create_async_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False}
        )
    return create_async_engine(
        db_url,
        echo=False,
        pool_pre_ping=True
    )


# Default engine setup
active_db_url = settings.DATABASE_URL
engine = create_db_engine(active_db_url)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection helper for FastAPI endpoints."""
    from app.db.init_db import async_session_factory as active_session_factory
    
    session_maker = active_session_factory or async_session_factory
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
