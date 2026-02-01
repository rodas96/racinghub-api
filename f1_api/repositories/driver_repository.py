from typing import Sequence
from sqlalchemy import func, select
from f1_api.models.models import (
    Driver,
)
from f1_api.repositories.base_repository import BaseRepository
from f1_api.schemas.shared.enums import DriverOrderField
from f1_api.schemas.shared.requests import SortOrder


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

        result = await self._db.execute(query)
        drivers = result.scalars().all()

        count_query = select(func.count()).select_from(Driver)
        total = await self._db.scalar(count_query) or 0

        return drivers, total

    async def get_driver(self, driver_id: str) -> Driver | None:
        query = select(Driver).where(Driver.id == driver_id)
        result = await self._db.execute(query)

        return result.scalars().first()
