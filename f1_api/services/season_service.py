from typing import Sequence

from sqlalchemy import RowMapping
from f1_api.constants.cache_keys import SEASONS_PREFIX
from f1_api.prodivers.cache import get_cached, set_cached
from f1_api.repositories.season_repository import SeasonRepository
from f1_api.utils import get_cache_key


class SeasonService:
    def __init__(self, season_repository: SeasonRepository):
        self._season_repository = season_repository

    async def get_seasons(self, skip: int, limit: int) -> tuple[Sequence[RowMapping], int]:
        cache_key = get_cache_key(SEASONS_PREFIX, skip=skip, limit=limit)

        res = await get_cached(cache_key)
        if res is not None:
            return res  # type: ignore

        res = await self._season_repository.get_seasons(offset=skip, limit=limit)
        await set_cached(cache_key, res)

        return res

    async def get_driver_seasons(self, driver_id: str) -> Sequence[RowMapping]:
        return await self._season_repository.get_driver_seasons(driver_id=driver_id)
