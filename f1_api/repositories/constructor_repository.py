from typing import Optional, Sequence
from sqlalchemy import RowMapping, func, select
from f1_api.models.models import (
    Constructor,
    SeasonConstructor,
    SeasonConstructorStanding,
)
from f1_api.repositories.base_repository import BaseRepository


class ConstructorRepository(BaseRepository):
    async def get_constructors(self, offset: int, limit: int) -> tuple[Sequence[Constructor], int]:
        """Get all constructors with pagination."""
        query = select(Constructor).order_by(Constructor.total_championship_wins.desc()).offset(offset).limit(limit)
        count_query = select(func.count()).select_from(Constructor)

        results = (await self._db.execute(query)).scalars().all()
        total = await self._db.scalar(count_query) or 0

        return results, total

    async def get_constructor(self, constructor_id: str) -> Optional[Constructor]:
        """Get a single constructor by ID."""
        query = select(Constructor).where(Constructor.id == constructor_id)
        result = await self._db.execute(query)

        return result.scalars().first()

    async def get_constructor_seasons(self, constructor_id: str) -> Sequence[RowMapping]:
        """Get all seasons a constructor competed in with their stats."""
        query = (
            select(
                SeasonConstructorStanding.year.label("year"),
                SeasonConstructorStanding.position_number.label("position"),
                SeasonConstructorStanding.points.label("points"),
                SeasonConstructor.total_race_wins.label("race_wins"),
                SeasonConstructor.total_pole_positions.label("pole_positions"),
            )
            .join(
                SeasonConstructor,
                (SeasonConstructor.year == SeasonConstructorStanding.year)
                & (SeasonConstructor.constructor_id == SeasonConstructorStanding.constructor_id),
            )
            .where(SeasonConstructorStanding.constructor_id == constructor_id)
            .order_by(SeasonConstructorStanding.year.desc())
        )

        results = (await self._db.execute(query)).mappings().all()
        return results
