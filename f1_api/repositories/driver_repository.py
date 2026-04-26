from typing import Sequence
from sqlalchemy import func, or_, select
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
        tokens: list[str] | None = None,
    ) -> tuple[Sequence[Driver], int]:

        query = select(Driver)
        count_query = select(func.count()).select_from(Driver)

        if tokens:
            for token in tokens:
                token = token.lower()
                like = f"%{token}%"
                abbr_like = token + "%"

                condition = or_(
                    func.lower(Driver.first_name).like(like),
                    func.lower(Driver.last_name).like(like),
                    func.lower(Driver.full_name).like(like),
                    func.lower(Driver.name).like(like),
                    func.lower(Driver.abbreviation).like(abbr_like),
                )

                query = query.where(condition)
                count_query = count_query.where(condition)

        if order_by:
            order_column = getattr(Driver, order_by.value)
            order_column = order_column.desc() if sort_by == SortOrder.DESC else order_column.asc()
            query = query.order_by(order_column)

        query = query.offset(skip).limit(limit)

        result = await self._db.execute(query)
        drivers = result.scalars().all()

        total = await self._db.scalar(count_query) or 0

        return drivers, total

    async def get_driver(self, driver_id: str) -> Driver | None:
        query = select(Driver).where(Driver.id == driver_id)
        result = await self._db.execute(query)
        return result.scalars().first()
