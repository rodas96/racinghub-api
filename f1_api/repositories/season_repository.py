from typing import Any, Optional, Sequence
from sqlalchemy import RowMapping, Select, distinct, func, select
from sqlalchemy.orm import aliased
from f1_api.models.models import (
    Circuit,
    Constructor,
    Country,
    Driver,
    EngineManufacturer,
    GrandPrix,
    Race,
    Season,
    SeasonConstructor,
    SeasonConstructorStanding,
    SeasonDriver,
    SeasonDriverStanding,
    SeasonEntrantDriver,
)
from f1_api.repositories.base_repository import BaseRepository


class SeasonRepository(BaseRepository):
    def _base_season_query(self) -> Select[Any]:

        race_counts = (
            select(
                Race.year.label("year"),
                func.count(Race.id).label("total_races"),
            )
            .group_by(Race.year)
            .subquery()
        )

        driver_counts = (
            select(
                SeasonDriver.year.label("year"),
                func.count(distinct(SeasonDriver.driver_id)).label("total_drivers"),
            )
            .group_by(SeasonDriver.year)
            .subquery()
        )

        constructor_counts = (
            select(
                SeasonConstructor.year.label("year"),
                func.count(distinct(SeasonConstructor.constructor_id)).label("total_constructors"),
            )
            .group_by(SeasonConstructor.year)
            .subquery()
        )

        driver_champ_stats = (
            select(
                SeasonDriver.year,
                SeasonDriver.driver_id,
                SeasonDriver.total_race_wins,
                SeasonDriver.total_pole_positions,
            ).join(
                SeasonDriverStanding,
                (SeasonDriverStanding.year == SeasonDriver.year)
                & (SeasonDriverStanding.driver_id == SeasonDriver.driver_id)
                & (SeasonDriverStanding.position_number == 1),
            )
        ).subquery()

        constructor_champ_stats = (
            select(
                SeasonConstructor.year,
                SeasonConstructor.constructor_id,
                SeasonConstructor.total_race_wins,
                SeasonConstructor.total_pole_positions,
            ).join(
                SeasonConstructorStanding,
                (SeasonConstructorStanding.year == SeasonConstructor.year)
                & (SeasonConstructorStanding.constructor_id == SeasonConstructor.constructor_id)
                & (SeasonConstructorStanding.position_number == 1),
            )
        ).subquery()

        DriverChamp = aliased(SeasonDriverStanding)
        ConstructorChamp = aliased(SeasonConstructorStanding)

        query = (
            select(
                Season.year.label("year"),
                race_counts.c.total_races,
                driver_counts.c.total_drivers,
                constructor_counts.c.total_constructors,
                Driver.id.label("champion_driver_id"),
                Driver.full_name.label("champion_driver_name"),
                DriverChamp.points.label("champion_driver_points"),
                driver_champ_stats.c.total_race_wins.label("champion_driver_race_wins"),
                driver_champ_stats.c.total_pole_positions.label("champion_driver_pole_positions"),
                Constructor.id.label("champion_constructor_id"),
                Constructor.name.label("champion_constructor_name"),
                ConstructorChamp.points.label("champion_constructor_points"),
                constructor_champ_stats.c.total_race_wins.label("champion_constructor_race_wins"),
                constructor_champ_stats.c.total_pole_positions.label("champion_constructor_pole_positions"),
            )
            .join(race_counts, race_counts.c.year == Season.year)
            .join(driver_counts, driver_counts.c.year == Season.year)
            .join(constructor_counts, constructor_counts.c.year == Season.year)
            .join(
                DriverChamp,
                (DriverChamp.year == Season.year) & (DriverChamp.position_number == 1),
            )
            .join(Driver, Driver.id == DriverChamp.driver_id)
            .join(driver_champ_stats, driver_champ_stats.c.year == Season.year)
            .join(
                ConstructorChamp,
                (ConstructorChamp.year == Season.year) & (ConstructorChamp.position_number == 1),
            )
            .join(Constructor, Constructor.id == ConstructorChamp.constructor_id)
            .join(constructor_champ_stats, constructor_champ_stats.c.year == Season.year)
        )

        return query

    async def get_seasons(self, offset: int, limit: int) -> tuple[Sequence[RowMapping], int]:
        """Get a paginated list of seasons."""
        query = self._base_season_query().order_by(Season.year.desc()).limit(limit).offset(offset)
        count_query = select(func.count()).select_from(Season)

        return (await self._db.execute(query)).mappings().all(), await self._db.scalar(count_query) or 0

    async def get_season(self, year: int) -> Optional[RowMapping]:
        """Get a specific season by year."""
        query = self._base_season_query().where(Season.year == year)
        return (await self._db.execute(query)).mappings().first()

    async def get_season_drivers(self, year: int) -> Sequence[RowMapping]:
        """Get all drivers who competed in a specific season with their stats."""
        query = (
            select(
                SeasonDriverStanding.driver_id.label("id"),
                Driver.full_name.label("name"),
                Driver.abbreviation.label("abbr"),
                Driver.permanent_number.label("number"),
                SeasonDriverStanding.position_number.label("position"),
                SeasonDriverStanding.points.label("points"),
                SeasonDriver.total_race_wins.label("race_wins"),
                SeasonDriver.total_pole_positions.label("pole_positions"),
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

        return (await self._db.execute(query)).mappings().all()

    async def get_season_constructors(self, year: int) -> Sequence[RowMapping]:
        """Get all constructors who competed in a specific season with their stats."""
        query = (
            select(
                SeasonConstructorStanding.constructor_id.label("id"),
                Constructor.name.label("name"),
                Country.alpha2_code.label("country_code"),
                SeasonConstructorStanding.engine_manufacturer_id.label("engine_manufacturer_id"),
                EngineManufacturer.name.label("engine_manufacturer"),
                SeasonConstructorStanding.position_number.label("position"),
                SeasonConstructorStanding.points.label("points"),
                SeasonConstructor.total_race_wins.label("race_wins"),
                SeasonConstructor.total_pole_positions.label("pole_positions"),
            )
            .join(Constructor, Constructor.id == SeasonConstructorStanding.constructor_id)
            .join(Country, Country.id == Constructor.country_id)
            .join(EngineManufacturer, EngineManufacturer.id == SeasonConstructorStanding.engine_manufacturer_id)
            .join(
                SeasonConstructor,
                (SeasonConstructor.year == SeasonConstructorStanding.year)
                & (SeasonConstructor.constructor_id == SeasonConstructorStanding.constructor_id),
            )
            .where(SeasonConstructorStanding.year == year)
            .order_by(SeasonConstructorStanding.position_display_order)
        )

        return (await self._db.execute(query)).mappings().all()

    async def get_season_races(self, year: int) -> Sequence[RowMapping]:
        """Get all races in a specific season."""
        query = (
            select(
                Race.id.label("id"),
                Race.round.label("round"),
                Race.date.label("date"),
                GrandPrix.name.label("name"),
                Circuit.name.label("circuit"),
                Country.alpha2_code.label("country_code"),
                Race.laps.label("laps"),
                Race.distance.label("distance"),
            )
            .join(GrandPrix, GrandPrix.id == Race.grand_prix_id)
            .join(Circuit, Circuit.id == Race.circuit_id)
            .join(Country, Country.id == Circuit.country_id)
            .where(Race.year == year)
            .order_by(Race.round)
        )

        return (await self._db.execute(query)).mappings().all()

    async def get_driver_seasons(self, driver_id: str) -> Sequence[RowMapping]:
        query = (
            select(
                SeasonDriverStanding.year.label("year"),
                SeasonDriverStanding.position_number.label("position"),
                SeasonDriverStanding.points.label("points"),
                SeasonDriver.total_race_wins.label("race_wins"),
                SeasonDriver.total_pole_positions.label("pole_positions"),
            )
            .join(
                SeasonDriver,
                (SeasonDriver.year == SeasonDriverStanding.year)
                & (SeasonDriver.driver_id == SeasonDriverStanding.driver_id),
            )
            .where(SeasonDriverStanding.driver_id == driver_id)
            .group_by(
                SeasonDriverStanding.year,
                SeasonDriverStanding.position_number,
                SeasonDriverStanding.points,
                SeasonDriver.total_race_wins,
                SeasonDriver.total_pole_positions,
            )
            .order_by(SeasonDriverStanding.year.desc())
        )

        return (await self._db.execute(query)).mappings().all()

    async def get_driver_season_constructors(self, driver_id: str) -> Sequence[RowMapping]:
        query = (
            select(
                SeasonEntrantDriver.year.label("year"),
                Constructor.name.label("constructors_name"),
            )
            .join(Constructor, Constructor.id == SeasonEntrantDriver.constructor_id)
            .where(SeasonEntrantDriver.driver_id == driver_id)
            .distinct()
            .order_by(SeasonEntrantDriver.year.desc())
        )
        return (await self._db.execute(query)).mappings().all()
