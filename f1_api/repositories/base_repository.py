from sqlalchemy.ext.asyncio import AsyncSession
from f1_api.providers.db import get_db_from_context


class BaseRepository:
    """Base repository with database session property."""

    @property
    def _db(self) -> AsyncSession:
        """Get current request's database session from context."""
        return get_db_from_context()
