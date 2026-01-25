from typing import Sequence
from sqlalchemy import func, select
from f1_api.models.models import Driver, Season, SeasonDriver, t_race_result
from f1_api.repositories.base_repository import BaseRepository
from f1_api.schemas.driver_schema import DriverOrderField
from f1_api.schemas.requests import SortOrder


class DriverRepository(BaseRepository):
    async def get_drivers(
        self,
        skip: int,
        limit: int,
        order_by: DriverOrderField | None = None,
        sort_by: SortOrder | None = None,
    ) -> tuple[Sequence[Driver], int]:
        query = select(Driver).offset(skip).limit(limit)

        if order_by:
            order_column = getattr(Driver, order_by.value)
            if sort_by == SortOrder.DESC:
                order_column = order_column.desc()
            else:
                order_column = order_column.asc()

            query = query.order_by(order_column)

        result = await self.db.execute(query)
        drivers = result.scalars().all()

        count_query = select(func.count()).select_from(Driver)
        total = await self.db.scalar(count_query) or 0

        return drivers, total

    async def get_driver_by_id(self, driver_id: str) -> Driver | None:
        query = select(Driver).where(Driver.id == driver_id)
        result = await self.db.execute(query)

        return result.scalars().first()

    async def get_driver_results(self, driver_id: str) -> list[dict]:
        query = select(t_race_result).where(t_race_result.c.driver_id == driver_id)
        result = await self.db.execute(query)

        return [dict(row) for row in result.fetchall()]

    async def get_driver_seasons(self, driver_id: str) -> Sequence[Season]:
        query = select(Season).join(SeasonDriver).where(SeasonDriver.driver_id == driver_id).order_by(Season.year)

        result = await self.db.execute(query)
        seasons = result.scalars().all()

        return seasons
