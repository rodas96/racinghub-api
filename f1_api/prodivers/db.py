from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from f1_api.settings import settings

db_url = settings.database_url
if not db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(db_url, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

db_context: ContextVar[AsyncSession | None] = ContextVar("db_session", default=None)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for a DB session."""
    async with async_session() as session:
        yield session


def get_db_from_context() -> AsyncSession:
    """
    Get database session from context.

    Raises:
        RuntimeError: If called outside of request context.
    """
    session = db_context.get()
    if session is None:
        raise RuntimeError("No database session in context. Did you forget middleware?")

    return session


async def test_data(session: AsyncSession) -> None:
    """Populate the database with initial test data."""
    import os

    if os.environ.get("IS_DEV", "") == "":
        raise ValueError("This function should not be called in production. Set IS_DEV to enable.")
