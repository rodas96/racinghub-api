from typing import Sequence
from sqlalchemy import RowMapping, func, select
from f1_api.models.models import (
    Circuit,
    Constructor,
    Driver,
    EngineManufacturer,
    GrandPrix,
    Race,
    TyreManufacturer,
    t_race_result,
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

    async def get_driver_by_id(self, driver_id: str) -> Driver | None:
        query = select(Driver).where(Driver.id == driver_id)
        result = await self._db.execute(query)

        return result.scalars().first()

    async def get_driver_races_results(self, skip: int, limit: int, driver_id: str) -> tuple[Sequence[RowMapping], int]:
        """Get all race results for a driver with full race context."""
        query = (
            select(
                # Race context
                Race.id.label("race_id"),
                Race.year.label("race_year"),
                Race.round.label("race_round"),
                Race.date.label("race_date"),
                Race.official_name.label("race_name"),
                GrandPrix.name.label("grand_prix_name"),
                Circuit.name.label("circuit_name"),
                Circuit.country.label("circuit_location"),
                # Result details
                t_race_result.c.position_number.label("position"),
                t_race_result.c.driver_number,
                Constructor.name.label("constructor_name"),
                # Performance
                t_race_result.c.laps,
                t_race_result.c.time,
                t_race_result.c.time_millis,
                t_race_result.c.gap,
                t_race_result.c.gap_millis,
                t_race_result.c.gap_laps,
                t_race_result.c.interval,
                t_race_result.c.interval_millis,
                # Penalties & retirement
                t_race_result.c.time_penalty,
                t_race_result.c.time_penalty_millis,
                t_race_result.c.reason_retired,
                # Points & achievements
                t_race_result.c.points,
                t_race_result.c.pole_position,
                t_race_result.c.fastest_lap,
                t_race_result.c.driver_of_the_day,
                t_race_result.c.grand_slam,
                # Grid & qualifying
                t_race_result.c.qualification_position_number.label("qualification_position"),
                t_race_result.c.grid_position_number.label("grid_position"),
                t_race_result.c.positions_gained,
                # Strategy
                t_race_result.c.pit_stops,
                TyreManufacturer.name.label("tyre_manufacturer"),
                EngineManufacturer.name.label("engine_manufacturer"),
            )
            .join(Race, Race.id == t_race_result.c.race_id)
            .join(GrandPrix, GrandPrix.id == Race.grand_prix_id)
            .join(Circuit, Circuit.id == Race.circuit_id)
            .join(Constructor, Constructor.id == t_race_result.c.constructor_id)
            .outerjoin(TyreManufacturer, TyreManufacturer.id == t_race_result.c.tyre_manufacturer_id)
            .outerjoin(EngineManufacturer, EngineManufacturer.id == t_race_result.c.engine_manufacturer_id)
            .where(t_race_result.c.driver_id == driver_id)
            .distinct(Race.id)
            .order_by(Race.id.desc())
            .offset(skip)
            .limit(limit)
        )
        count_query = select(func.count()).select_from(t_race_result).where(t_race_result.c.driver_id == driver_id)

        result = await self._db.execute(query)
        total = await self._db.scalar(count_query) or 0

        return result.mappings().all(), total
