from typing import Sequence
from sqlalchemy import RowMapping, func, select, text
from f1_api.models.models import (
    Season,
    SeasonDriver,
    SeasonDriverStanding,
)
from f1_api.repositories.base_repository import BaseRepository


class SeasonRepository(BaseRepository):
    _base_season_query = """
                WITH driver_champions AS (
                    SELECT 
                        sds.year, 
                        sds.driver_id, 
                        sds.points,
                        sd.total_race_wins,
                        sd.total_pole_positions
                    FROM season_driver_standing sds
                    JOIN season_driver sd 
                    ON sd.year = sds.year AND sd.driver_id = sds.driver_id
                    WHERE sds.position_number = 1
                ),
                constructor_champions AS (
                    SELECT 
                        scs.year, 
                        scs.constructor_id, 
                        scs.points,
                        sc.total_race_wins,
                        SUM(sd.total_pole_positions) AS total_pole_positions
                    FROM season_constructor_standing scs
                    JOIN season_constructor sc 
                    ON sc.year = scs.year AND sc.constructor_id = scs.constructor_id
                    LEFT JOIN season_driver_standing sds 
                    ON sds.year = scs.year
                    LEFT JOIN season_driver sd 
                    ON sd.year = sds.year AND sd.driver_id = sds.driver_id
                    WHERE scs.position_number = 1
                    GROUP BY scs.year, scs.constructor_id, scs.points, sc.total_race_wins
                )
                SELECT
                    s.year,
                    
                    -- Stats
                    COUNT(DISTINCT r.id) AS total_races,
                    COUNT(DISTINCT scs.constructor_id) AS total_constructors,
                    COUNT(DISTINCT CASE WHEN sds.points > 0 THEN sds.driver_id END) AS total_drivers,
                    
                    -- Driver champion
                    dc.driver_id AS champion_driver_id,
                    d.name AS champion_driver_name,
                    dc.points AS champion_points,
                    dc.total_race_wins AS champion_race_wins,
                    dc.total_pole_positions AS champion_pole_positions,
                    
                    -- Constructor champion
                    cc.constructor_id AS constructor_champion_id,
                    c.name AS constructor_champion_name,
                    cc.points AS constructor_champion_points,
                    cc.total_race_wins AS constructor_champion_race_wins,
                    cc.total_pole_positions AS constructor_champion_pole_positions,
                    
                    -- Constructors
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object(
                            'id', c_all.id,
                            'name', c_all.name,
                            'country_code', c_country.alpha2_code,
                            'engine_manufacturer', em.name,
                            'position', scs.position_number,
                            'points', scs.points,
                            'race_wins', sc.total_race_wins,
                            'pole_positions', sc.total_pole_positions

                        )) FILTER (WHERE c_all.id IS NOT NULL),
                        '[]'
                    ) AS constructors,

                    -- Drivers
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object(
                            'id', d_all.id,
                            'name', d_all.name,
                            'abbr', d_all.abbreviation,
                            'number', d_all.permanent_number,
                            'position', sds.position_number,
                            'points', sds.points,
                            'race_wins', sd.total_race_wins,
                            'pole_positions', sd.total_pole_positions
                        )) FILTER (WHERE d_all.id IS NOT NULL),
                        '[]'
                    ) AS drivers,

                    -- Engine manufacturers
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object(
                            'id', em_sum.id,
                            'name', em_sum.name,
                            'country_code', em_country.alpha2_code,
                            'total_points', sem.total_points,
                            'total_wins', sem.total_race_wins
                        )) FILTER (WHERE em_sum.id IS NOT NULL),
                        '[]'
                    ) AS engine_manufacturers,

                    -- Tyre manufacturers
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object(
                            'id', tm.id,
                            'name', tm.name,
                            'country_code', tm_country.alpha2_code,
                            'total_wins', stm.total_race_wins
                        )) FILTER (WHERE tm.id IS NOT NULL),
                        '[]'
                    ) AS tyre_manufacturers,

                    -- Races
                    COALESCE(
                        json_agg(DISTINCT jsonb_build_object(
                            'id', r.id,
                            'round', r.round,
                            'date', r.date,
                            'name', gp.full_name,
                            'circuit', circ.full_name,
                            'country_code', circ_country.alpha2_code,
                            'laps', r.laps,
                            'distance', r.distance
                        )) FILTER (WHERE r.id IS NOT NULL),
                        '[]'
                    ) AS races
                    
                FROM season s

                -- Races
                LEFT JOIN race r ON r.year = s.year
                LEFT JOIN circuit circ ON circ.id = r.circuit_id
                LEFT JOIN country circ_country ON circ_country.id = circ.country_id
                LEFT JOIN grand_prix gp ON gp.id = r.grand_prix_id

                -- Constructors
                LEFT JOIN season_constructor_standing scs ON scs.year = s.year
                LEFT JOIN constructor c_all ON c_all.id = scs.constructor_id
                LEFT JOIN country c_country ON c_country.id = c_all.country_id
                LEFT JOIN engine_manufacturer em ON em.id = scs.engine_manufacturer_id
                LEFT JOIN season_constructor sc ON sc.year = s.year AND sc.constructor_id = scs.constructor_id

                -- Drivers
                LEFT JOIN season_driver_standing sds ON sds.year = s.year
                LEFT JOIN driver d_all ON d_all.id = sds.driver_id
                LEFT JOIN season_driver sd ON sd.year = s.year AND sd.driver_id = sds.driver_id

                -- Engine manufacturers
                LEFT JOIN season_engine_manufacturer sem ON sem.year = s.year
                LEFT JOIN engine_manufacturer em_sum ON em_sum.id = sem.engine_manufacturer_id
                LEFT JOIN country em_country ON em_country.id = em_sum.country_id

                -- Tyre manufacturers
                LEFT JOIN season_tyre_manufacturer stm ON stm.year = s.year
                LEFT JOIN tyre_manufacturer tm ON tm.id = stm.tyre_manufacturer_id
                LEFT JOIN country tm_country ON tm_country.id = tm.country_id

                -- Champions
                LEFT JOIN driver_champions dc ON dc.year = s.year
                LEFT JOIN driver d ON d.id = dc.driver_id

                LEFT JOIN constructor_champions cc ON cc.year = s.year
                LEFT JOIN constructor c ON c.id = cc.constructor_id
                WHERE 1=1 {where_clause}
                GROUP BY s.year,
                        dc.driver_id, d.name, dc.points, dc.total_race_wins, dc.total_pole_positions,
                        cc.constructor_id, c.name, cc.points, cc.total_race_wins, cc.total_pole_positions
            """

    async def get_seasons(self, offset: int, limit: int) -> tuple[Sequence[RowMapping], int]:
        query = text(
            self._base_season_query.format(where_clause="") + " ORDER BY s.year DESC LIMIT :limit OFFSET :offset"
        )
        count_query = select(func.count()).select_from(Season)

        results = (await self._db.execute(query, {"limit": limit, "offset": offset})).mappings().all()
        total = await self._db.scalar(count_query) or 0

        return results, total

    async def get_season(self, year: int) -> RowMapping | None:
        query = text(self._base_season_query.format(where_clause="AND s.year = :year"))
        result = await self._db.execute(query, {"year": year})
        season = result.mappings().first()
        return season

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

        results = (await self._db.execute(query)).mappings().all()
        return results
