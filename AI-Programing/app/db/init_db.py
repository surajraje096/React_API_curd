import logging
from sqlalchemy import select
from app.db.base import Base, engine as current_engine, async_session_factory as current_session_factory, create_db_engine
from app.db.models import UserAccount
from app.config import settings

logger = logging.getLogger(__name__)

# Global active engine and session factory references
engine = current_engine
async_session_factory = current_session_factory


async def init_db():
    """Create database schema tables if they do not exist and seed initial demo data."""
    global engine, async_session_factory
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed ({e}). Switching engine fallback to SQLite ({settings.SQLITE_FALLBACK_URL}).")
        engine = create_db_engine(settings.SQLITE_FALLBACK_URL)
        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
        async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Seed initial user accounts if table is empty
    async with async_session_factory() as session:
        result = await session.execute(select(UserAccount))
        existing_users = result.scalars().all()
        
        if not existing_users:
            logger.info("Seeding demo user accounts...")
            demo_users = [
                UserAccount(
                    id="usr-101",
                    account_number="ACC-1001",
                    full_name="Alice Smith",
                    email="alice@example.com",
                    balance=2500.0,
                    is_active=True
                ),
                UserAccount(
                    id="usr-102",
                    account_number="ACC-1002",
                    full_name="Bob Jones",
                    email="bob@example.com",
                    balance=450.75,
                    is_active=True
                ),
                UserAccount(
                    id="usr-103",
                    account_number="ACC-1030",
                    full_name="Charlie Brown",
                    email="charlie@example.com",
                    balance=8900.0,
                    is_active=False
                )
            ]
            session.add_all(demo_users)
            await session.commit()
            logger.info("Demo user accounts successfully seeded.")
