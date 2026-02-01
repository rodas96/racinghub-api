from typing import Sequence
from f1_api.models.models import Race
from f1_api.repositories.race_repository import RaceRepository


class RaceService:
    def __init__(self, race_repository: RaceRepository):
        self._race_repository = race_repository

    async def get_races(self, skip: int, limit: int) -> tuple[Sequence[Race], int]:
        return await self._race_repository.get_races(skip=skip, limit=limit)
