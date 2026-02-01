from fastapi import HTTPException
from f1_api.repositories.race_repository import RaceRepository
from f1_api.models.models import Race, RaceData
from f1_api.schemas.race_schema import RaceResponse, RaceResultResponse


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

    async def get_race_results(self, race_id: int) -> list[RaceResultResponse]:
        await self._get_existing_race(race_id=race_id)
        results = await self._race_repository.get_race_results(race_id=race_id)

        return [self._map_race_result(result) for result in results]

    def _map_race_result(self, row: RaceData) -> RaceResultResponse:
        return RaceResultResponse(
            position_number=row.position_number,
            position_text=row.position_text,
            driver_number=row.driver_number,
            driver_id=row.driver_id,
            constructor_id=row.constructor_id,
            laps=row.race_laps,
            time=row.race_time,
            gap=row.race_gap,
            interval=row.race_interval,
            points=row.race_points,
            pit_stops=row.race_pit_stops,
            grid_position=row.race_grid_position_number,
            positions_gained=row.race_positions_gained,
            fastest_lap=row.race_fastest_lap,
            pole_position=row.race_pole_position,
            driver_of_the_day=row.race_driver_of_the_day,
            grand_slam=row.race_grand_slam,
            reason_retired=row.race_reason_retired,
        )

    def _map_race(self, row: Race) -> RaceResponse:
        data = {c.key: getattr(row, c.key) for c in row.__table__.columns}
        for session in _SESSION_FIELDS:
            date_val = data.pop(f"{session}_date", None)
            time_val = data.pop(f"{session}_time", None)
            if date_val or time_val:
                data[session] = {"date": date_val, "time": time_val}

        return RaceResponse.model_validate(data)
