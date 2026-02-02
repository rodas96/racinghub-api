from typing import Sequence
from fastapi import HTTPException
from sqlalchemy import RowMapping
from f1_api.repositories.race_repository import RaceRepository
from f1_api.models.models import Race
from f1_api.schemas.race_schema import RaceResponse


_SESSION_FIELDS = [
    "pre_qualifying",
    "free_practice_1",
    "free_practice_2",
    "free_practice_3",
    "free_practice_4",
    "qualifying_1",
    "qualifying_2",
    "qualifying",
    "sprint_qualifying",
    "sprint_race",
    "warming_up",
]


class RaceService:
    def __init__(self, race_repository: RaceRepository):
        self._race_repository = race_repository

    async def get_races(self, skip: int, limit: int) -> tuple[list[RaceResponse], int]:
        races, total = await self._race_repository.get_races(skip=skip, limit=limit)

        return [self._map_race(race) for race in races], total

    async def get_race(self, race_id: int) -> RaceResponse:
        race = await self._get_existing_race(race_id=race_id)

        return self._map_race(race)

    async def _get_existing_race(self, race_id: int) -> Race:
        race = await self._race_repository.get_race(race_id=race_id)

        if not race:
            raise HTTPException(status_code=404, detail="Race not found")

        return race

    async def get_race_results(self, race_id: int) -> Sequence[RowMapping]:
        await self._get_existing_race(race_id=race_id)

        return await self._race_repository.get_race_results(race_id=race_id)

    async def get_race_starting_grid(self, race_id: int) -> Sequence[RowMapping]:
        await self._get_existing_race(race_id=race_id)

        return await self._race_repository.get_race_starting_grid(race_id=race_id)

    async def get_race_qualifying_results(self, race_id: int) -> Sequence[RowMapping]:
        await self._get_existing_race(race_id=race_id)

        return await self._race_repository.get_race_qualifying_results(race_id=race_id)

    async def get_sprint_race_results(self, race_id: int) -> Sequence[RowMapping]:
        await self._get_existing_race(race_id=race_id)

        return await self._race_repository.get_race_sprint_results(race_id=race_id)

    async def get_race_sprint_starting_grid(self, race_id: int) -> Sequence[RowMapping]:
        await self._get_existing_race(race_id=race_id)

        return await self._race_repository.get_race_sprint_starting_grid(race_id=race_id)

    def _map_race(self, row: Race) -> RaceResponse:
        data = {c.key: getattr(row, c.key) for c in row.__table__.columns}
        for session in _SESSION_FIELDS:
            date_val = data.pop(f"{session}_date", None)
            time_val = data.pop(f"{session}_time", None)
            if date_val or time_val:
                data[session] = {"date": date_val, "time": time_val}

        return RaceResponse.model_validate(data)
