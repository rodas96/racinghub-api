from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import RowMapping
from f1_api.repositories.season_repository import SeasonRepository


class SeasonService:
    def __init__(self, season_repository: SeasonRepository):
        self._season_repository = season_repository

    async def get_seasons(self, skip: int, limit: int) -> tuple[list[dict], int]:
        rows, total = await self._season_repository.get_seasons(offset=skip, limit=limit)

        return [self._map_season_row(dict(row)) for row in rows], total

    async def get_season(self, year: int) -> dict:
        row = await self._get_existing_season(year=year)

        return self._map_season_row(dict(row))

    async def get_driver_seasons(self, driver_id: str) -> Sequence[RowMapping]:
        return await self._season_repository.get_driver_seasons(driver_id=driver_id)

    async def _get_existing_season(self, year: int) -> RowMapping:
        season = await self._season_repository.get_season(year=year)

        if not season:
            raise HTTPException(status_code=404, detail="Season not found")

        return season

    def _map_season_row(self, row: dict) -> dict:
        if row.get("champion_driver_id"):
            row["champion"] = {
                "driver_id": row["champion_driver_id"],
                "driver_name": row["champion_driver_name"],
                "points": row["champion_points"],
                "race_wins": row["champion_race_wins"],
                "pole_positions": row["champion_pole_positions"],
            }

        if row.get("constructor_champion_id"):
            row["constructor_champion"] = {
                "constructor_id": row["constructor_champion_id"],
                "constructor_name": row["constructor_champion_name"],
                "points": row["constructor_champion_points"],
                "race_wins": row["constructor_champion_race_wins"],
                "pole_positions": row["constructor_champion_pole_positions"],
            }

        return row
