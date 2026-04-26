from typing import Any, Sequence

from sqlalchemy import RowMapping
from f1_api.models.models import Driver
from f1_api.repositories.driver_repository import DriverRepository
from f1_api.constants.cache_keys import DRIVERS_SEASONS_PREFIX
from f1_api.repositories.race_repository import RaceRepository
from f1_api.repositories.season_repository import SeasonRepository
from f1_api.schemas.shared.enums import DriverOrderField
from f1_api.schemas.shared.requests import SortOrder
from f1_api.utils import get_cache_key, parse_search_query
from f1_api.providers.cache import get_cached, set_cached
from fastapi import HTTPException


class DriverService:
    def __init__(
        self,
        driver_repository: DriverRepository,
        season_repository: SeasonRepository,
        race_repository: RaceRepository,
    ):
        self._driver_repository = driver_repository
        self._season_repository = season_repository
        self._race_repository = race_repository

    async def get_drivers(
        self,
        skip: int,
        limit: int,
        order_by: DriverOrderField | None,
        sort_by: SortOrder | None,
        q: str | None = None,
    ) -> tuple[Sequence[Driver], int]:

        drivers, total = await self._driver_repository.get_drivers(
            skip=skip,
            limit=limit,
            order_by=order_by,
            sort_by=sort_by,
            tokens=parse_search_query(q) if q else None,
        )

        return drivers, total

    async def get_driver(self, driver_id: str) -> Driver:
        return await self._get_existing_driver(driver_id)

    async def get_driver_races_results(self, skip: int, limit: int, driver_id: str) -> tuple[Sequence[RowMapping], int]:
        await self._get_existing_driver(driver_id)

        results, total = await self._race_repository.get_driver_races_results(
            skip=skip, limit=limit, driver_id=driver_id
        )

        return results, total

    async def get_driver_seasons(self, driver_id: str) -> list[dict[str, Any]]:
        cache_key = get_cache_key(DRIVERS_SEASONS_PREFIX, driver_id=driver_id)
        cached = await get_cached(cache_key)

        if cached is not None:
            return cached  # type: ignore

        await self._get_existing_driver(driver_id)

        seasons = await self._season_repository.get_driver_seasons(driver_id=driver_id)
        constructors = await self._season_repository.get_driver_season_constructors(driver_id=driver_id)

        constructor_by_year = {r["year"]: r["constructor_name"] for r in constructors}

        res = [dict(season, constructor_name=constructor_by_year.get(season["year"])) for season in seasons]

        await set_cached(cache_key, res)

        return res

    async def _get_existing_driver(self, driver_id: str) -> Driver:
        driver = await self._driver_repository.get_driver(driver_id)

        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")

        return driver
