from typing import Sequence
from f1_api.repositories.base_repository import BaseRepository
from f1_api.models.models import (
    Circuit,
    Constructor,
    EngineManufacturer,
    GrandPrix,
    Race,
    TyreManufacturer,
    t_race_result,
    t_sprint_race_result,
    t_qualifying_result,
    t_starting_grid_position,
    t_sprint_starting_grid_position,
)
from sqlalchemy import RowMapping, select, func


class RaceRepository(BaseRepository):
    async def get_races(self, skip: int, limit: int) -> tuple[Sequence[Race], int]:
        query = select(Race).offset(skip).limit(limit).order_by(Race.date.desc())
        total_query = select(func.count()).select_from(Race)

        results = (await self._db.execute(query)).scalars().all()
        total = (await self._db.execute(total_query)).scalar_one() or 0

        return results, total

    async def get_race(self, race_id: int) -> Race | None:
        query = select(Race).where(Race.id == race_id)
        result = await self._db.execute(query)

        return result.scalars().first()

    async def get_race_results(self, race_id: int) -> Sequence[RowMapping]:
        query = (
            select(t_race_result)
            .where(t_race_result.c.race_id == race_id)
            .order_by(t_race_result.c.position_display_order)
        )

        return (await self._db.execute(query)).mappings().all()

    async def get_race_starting_grid(self, race_id: int) -> Sequence[RowMapping]:
        query = (
            select(t_starting_grid_position)
            .where(t_starting_grid_position.c.race_id == race_id)
            .order_by(t_starting_grid_position.c.position_number)
        )
        a = (await self._db.execute(query)).mappings().all()
        return a

        # return (await self._db.execute(query)).mappings().all()

    async def get_race_qualifying_results(self, race_id: int) -> Sequence[RowMapping]:
        query = (
            select(t_qualifying_result)
            .where(t_qualifying_result.c.race_id == race_id)
            .order_by(t_qualifying_result.c.position_display_order)
        )

        return (await self._db.execute(query)).mappings().all()

    async def get_race_sprint_results(self, race_id: int) -> Sequence[RowMapping]:
        query = (
            select(t_sprint_race_result)
            .where(t_sprint_race_result.c.race_id == race_id)
            .order_by(t_sprint_race_result.c.position_display_order)
        )

        return (await self._db.execute(query)).mappings().all()

    async def get_race_sprint_starting_grid(self, race_id: int) -> Sequence[RowMapping]:
        query = (
            select(t_sprint_starting_grid_position)
            .where(t_sprint_starting_grid_position.c.race_id == race_id)
            .order_by(t_sprint_starting_grid_position.c.position_number)
        )

        return (await self._db.execute(query)).mappings().all()

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
