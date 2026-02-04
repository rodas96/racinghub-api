from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import RowMapping
from f1_api.repositories.season_repository import SeasonRepository


class SeasonService:
    def __init__(self, season_repository: SeasonRepository):
        self._season_repository = season_repository

    async def get_seasons(self, skip: int, limit: int) -> tuple[Sequence[RowMapping], int]:
        rows, total = await self._season_repository.get_seasons(offset=skip, limit=limit)

        return rows, total

    async def get_season(self, year: int) -> RowMapping:
        return await self._get_existing_season(year=year)

    async def get_driver_seasons(self, driver_id: str) -> Sequence[RowMapping]:
        return await self._season_repository.get_driver_seasons(driver_id=driver_id)

    async def get_season_drivers(self, year: int) -> Sequence[RowMapping]:
        await self._get_existing_season(year=year)

        return await self._season_repository.get_season_drivers(year=year)

    async def get_season_constructors(self, year: int) -> Sequence[RowMapping]:
        await self._get_existing_season(year=year)

        return await self._season_repository.get_season_constructors(year=year)

    async def get_season_races(self, year: int) -> Sequence[RowMapping]:
        await self._get_existing_season(year=year)

        return await self._season_repository.get_season_races(year=year)

    async def _get_existing_season(self, year: int) -> RowMapping:
        season = await self._season_repository.get_season(year=year)

        if not season:
            raise HTTPException(status_code=404, detail="Season not found")

        return season
