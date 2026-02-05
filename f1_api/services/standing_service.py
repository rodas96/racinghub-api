from typing import Sequence
from fastapi import HTTPException
from sqlalchemy import RowMapping
from f1_api.repositories.standing_repository import StandingRepository
from f1_api.repositories.season_repository import SeasonRepository


class StandingService:
    def __init__(
        self,
        standing_repository: StandingRepository,
        season_repository: SeasonRepository,
    ):
        self._standing_repository = standing_repository
        self._season_repository = season_repository

    async def get_driver_standings(self, year: int) -> Sequence[RowMapping]:
        """Get final driver championship standings for a season."""
        await self._verify_season_exists(year)

        driver_standings = await self._standing_repository.get_driver_standings(year)

        return driver_standings

    async def get_constructor_standings(self, year: int) -> Sequence[RowMapping]:
        """Get final constructor championship standings for a season."""
        await self._verify_season_exists(year)

        constructor_standings = await self._standing_repository.get_constructor_standings(year)

        return constructor_standings

    async def _verify_season_exists(self, year: int) -> None:
        """Helper to check if season exists."""
        season = await self._season_repository.get_season(year)

        if not season:
            raise HTTPException(status_code=404, detail=f"Season {year} not found")
