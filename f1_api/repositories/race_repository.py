from typing import Sequence
from f1_api.repositories.base_repository import BaseRepository
from f1_api.models.models import Race
from sqlalchemy import select, func


class RaceRepository(BaseRepository):
    async def get_races(self, skip: int, limit: int) -> tuple[Sequence[Race], int]:
        query = select(Race).offset(skip).limit(limit).order_by(Race.date.desc())
        total_query = select(func.count()).select_from(Race)

        results = (await self._db.execute(query)).scalars().all()
        total = (await self._db.execute(total_query)).scalar_one() or 0

        return results, total
