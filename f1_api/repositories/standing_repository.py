from typing import Sequence
from sqlalchemy import RowMapping, select
from f1_api.models.models import (
    Constructor,
    Country,
    Driver,
    EngineManufacturer,
    SeasonConstructor,
    SeasonConstructorStanding,
    SeasonDriver,
    SeasonDriverStanding,
)
from f1_api.repositories.base_repository import BaseRepository


class StandingRepository(BaseRepository):
    async def get_driver_standings(self, year: int) -> Sequence[RowMapping]:
        """Get final driver championship standings for a season."""
        query = (
            select(
                SeasonDriverStanding.position_number.label("position"),
                SeasonDriverStanding.position_text.label("position_text"),
                SeasonDriverStanding.driver_id.label("driver_id"),
                Driver.full_name.label("driver_name"),
                Driver.abbreviation.label("driver_abbr"),
                Driver.permanent_number.label("driver_number"),
                SeasonDriverStanding.points.label("points"),
                SeasonDriver.total_race_wins.label("race_wins"),
                SeasonDriver.total_pole_positions.label("pole_positions"),
                SeasonDriverStanding.championship_won.label("championship_won"),
            )
            .join(Driver, Driver.id == SeasonDriverStanding.driver_id)
            .join(
                SeasonDriver,
                (SeasonDriver.year == SeasonDriverStanding.year)
                & (SeasonDriver.driver_id == SeasonDriverStanding.driver_id),
            )
            .where(SeasonDriverStanding.year == year)
            .order_by(SeasonDriverStanding.position_display_order)
        )

        results = (await self._db.execute(query)).mappings().all()
        return results

    async def get_constructor_standings(self, year: int) -> Sequence[RowMapping]:
        """Get final constructor championship standings for a season."""
        query = (
            select(
                SeasonConstructorStanding.position_number.label("position"),
                SeasonConstructorStanding.position_text.label("position_text"),
                SeasonConstructorStanding.constructor_id.label("constructor_id"),
                Constructor.name.label("constructor_name"),
                Country.alpha2_code.label("country_code"),
                SeasonConstructorStanding.engine_manufacturer_id.label("engine_manufacturer_id"),
                EngineManufacturer.name.label("engine_manufacturer"),
                SeasonConstructorStanding.points.label("points"),
                SeasonConstructor.total_race_wins.label("race_wins"),
                SeasonConstructor.total_pole_positions.label("pole_positions"),
                SeasonConstructorStanding.championship_won.label("championship_won"),
            )
            .join(Constructor, Constructor.id == SeasonConstructorStanding.constructor_id)
            .join(Country, Country.id == Constructor.country_id)
            .join(
                EngineManufacturer,
                EngineManufacturer.id == SeasonConstructorStanding.engine_manufacturer_id,
            )
            .join(
                SeasonConstructor,
                (SeasonConstructor.year == SeasonConstructorStanding.year)
                & (SeasonConstructor.constructor_id == SeasonConstructorStanding.constructor_id),
            )
            .where(SeasonConstructorStanding.year == year)
            .order_by(SeasonConstructorStanding.position_display_order)
        )

        results = (await self._db.execute(query)).mappings().all()
        return results
