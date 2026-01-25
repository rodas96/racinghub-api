from typing import Sequence
from f1_api.models.models import Driver
from f1_api.repositories.driver_repository import DriverRepository
from f1_api.constants.cache_keys import DRIVERS_PREFIX
from f1_api.schemas.driver_schema import DriverOrderField
from f1_api.schemas.requests import SortOrder
from f1_api.utils import get_cache_key
from f1_api.prodivers.cache import get_cached, set_cached
from fastapi import HTTPException


class DriverService:
    def __init__(self, driver_repository: DriverRepository):
        self._driver_repository = driver_repository

    async def get_drivers(
        self,
        skip: int,
        limit: int,
        order_by: DriverOrderField | None,
        sort_by: SortOrder | None,
    ) -> tuple[Sequence[Driver], int]:
        cache_key = get_cache_key(DRIVERS_PREFIX, skip=skip, limit=limit, order_by=order_by, sort_by=sort_by)

        res = await get_cached(cache_key)

        if res is not None:
            return res  # type: ignore

        drivers, total = await self._driver_repository.get_drivers(
            skip=skip,
            limit=limit,
            order_by=order_by,
            sort_by=sort_by,
        )

        await set_cached(cache_key, (drivers, total))

        return drivers, total

    async def get_driver(self, driver_id: str) -> Driver:
        return await self._get_existing_driver(driver_id)

    async def get_driver_results(self, driver_id: str) -> list[dict]:
        await self._get_existing_driver(driver_id)
        results = await self._driver_repository.get_driver_results(driver_id)

        return results

    async def _get_existing_driver(self, driver_id: str) -> Driver:
        driver = await self._driver_repository.get_driver_by_id(driver_id)

        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")

        return driver
