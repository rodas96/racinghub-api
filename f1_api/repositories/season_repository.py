from sqlalchemy import func, select, text
from f1_api.models.models import Season
from f1_api.repositories.base_repository import BaseRepository


class SeasonRepository(BaseRepository):
    async def get_seasons(self, offset: int, limit: int) -> tuple[list[dict], int]:
        query = text("""
                SELECT 
                    s.year,
                    
                    -- Stats
                    COUNT(DISTINCT r.id) as total_races,
                    COUNT(DISTINCT scs.constructor_id) as total_constructors,
                    COUNT(DISTINCT CASE WHEN sds.points > 0 THEN sds.driver_id END) as total_drivers,
                    
                    -- Driver champion
                    champ_d.id as champion_driver_id,
                    champ_d.name as champion_driver_name,
                    champ_sds.points as champion_points,
                    champ_sd.total_race_wins as champion_race_wins,
                    
                    -- Constructor champion
                    champ_c.id as constructor_champion_id,
                    champ_c.name as constructor_champion_name,
                    champ_scs.points as constructor_champion_points,
                    champ_sc.total_race_wins as constructor_champion_race_wins,
                    
                    -- Constructors
                    json_agg(DISTINCT jsonb_build_object(
                        'id', c.id,
                        'name', c.name,
                        'country_code', c_country.alpha2_code,
                        'engine_manufacturer', em.name,
                        'position', scs.position_number,
                        'points', scs.points,
                        'race_wins', sc.total_race_wins
                    )) FILTER (WHERE c.id IS NOT NULL) as constructors,
                    
                    -- Drivers
                    json_agg(DISTINCT jsonb_build_object(
                        'id', d.id,
                        'name', d.name,
                        'abbr', d.abbreviation,
                        'number', d.permanent_number,
                        'position', sds.position_number,
                        'points', sds.points,
                        'race_wins', sd.total_race_wins,
                        'pole_positions', sd.total_pole_positions
                    )) FILTER (WHERE d.id IS NOT NULL) as drivers,
                    
                    -- Engine manufacturers
                    json_agg(DISTINCT jsonb_build_object(
                        'id', em_sum.id,
                        'name', em_sum.name,
                        'country_code', em_country.alpha2_code,
                        'total_points', sem.total_points,
                        'total_wins', sem.total_race_wins
                    )) FILTER (WHERE em_sum.id IS NOT NULL) as engine_manufacturers,
                    
                    -- Tyre manufacturers
                    json_agg(DISTINCT jsonb_build_object(
                        'id', tm.id,
                        'name', tm.name,
                        'country_code', tm_country.alpha2_code,
                        'total_wins', stm.total_race_wins
                    )) FILTER (WHERE tm.id IS NOT NULL) as tyre_manufacturers,
                    
                    -- Races
                    json_agg(DISTINCT jsonb_build_object(
                        'id', r.id,
                        'round', r.round,
                        'date', r.date,
                        'name', gp.full_name,
                        'circuit', circ.full_name,
                        'country_code', circ_country.alpha2_code,
                        'laps', r.laps,
                        'distance', r.distance
                    )) FILTER (WHERE r.id IS NOT NULL) as races

                FROM season s
                
                -- Races
                LEFT JOIN race r ON r.year = s.year
                LEFT JOIN circuit circ ON circ.id = r.circuit_id
                LEFT JOIN country circ_country ON circ_country.id = circ.country_id
                LEFT JOIN grand_prix gp ON gp.id = r.grand_prix_id
                
                -- Constructor standings
                LEFT JOIN season_constructor_standing scs ON scs.year = s.year
                LEFT JOIN constructor c ON c.id = scs.constructor_id
                LEFT JOIN country c_country ON c_country.id = c.country_id
                LEFT JOIN engine_manufacturer em ON em.id = scs.engine_manufacturer_id
                LEFT JOIN season_constructor sc ON sc.year = s.year AND sc.constructor_id = scs.constructor_id
                
                -- Driver standings
                LEFT JOIN season_driver_standing sds ON sds.year = s.year
                LEFT JOIN driver d ON d.id = sds.driver_id
                LEFT JOIN season_driver sd ON sd.year = s.year AND sd.driver_id = sds.driver_id
                
                -- Engine manufacturer summary
                LEFT JOIN season_engine_manufacturer sem ON sem.year = s.year
                LEFT JOIN engine_manufacturer em_sum ON em_sum.id = sem.engine_manufacturer_id
                LEFT JOIN country em_country ON em_country.id = em_sum.country_id
                
                -- Tyre manufacturer
                LEFT JOIN season_tyre_manufacturer stm ON stm.year = s.year
                LEFT JOIN tyre_manufacturer tm ON tm.id = stm.tyre_manufacturer_id
                LEFT JOIN country tm_country ON tm_country.id = tm.country_id
                
                -- Champions (position 1)
                LEFT JOIN season_driver_standing champ_sds ON champ_sds.year = s.year AND champ_sds.position_number = 1
                LEFT JOIN driver champ_d ON champ_d.id = champ_sds.driver_id
                LEFT JOIN season_driver champ_sd ON champ_sd.year = s.year AND champ_sd.driver_id = champ_sds.driver_id
                LEFT JOIN season_constructor_standing champ_scs ON champ_scs.year = s.year AND champ_scs.position_number = 1
                LEFT JOIN constructor champ_c ON champ_c.id = champ_scs.constructor_id
                LEFT JOIN season_constructor champ_sc ON champ_sc.year = s.year AND champ_sc.constructor_id = champ_scs.constructor_id
                
                GROUP BY 
                    s.year,
                    champ_d.id, champ_d.name, champ_sds.points, champ_sd.total_race_wins,
                    champ_c.id, champ_c.name, champ_scs.points, champ_sc.total_race_wins
                
                ORDER BY s.year DESC
                LIMIT :limit OFFSET :offset
            """)

        count_query = select(func.count()).select_from(Season)

        results = (await self._db.execute(query, {"limit": limit, "offset": offset})).mappings().all()
        total = await self._db.scalar(count_query) or 0

        seasons = [
            {
                "year": row["year"],
                "total_races": row["total_races"],
                "total_constructors": row["total_constructors"],
                "total_drivers": row["total_drivers"],
                "champion": {
                    "driver_id": row["champion_driver_id"],
                    "driver_name": row["champion_driver_name"],
                    "points": row["champion_points"],
                    "race_wins": row["champion_race_wins"],
                }
                if row["champion_driver_id"]
                else None,
                "constructor_champion": {
                    "constructor_id": row["constructor_champion_id"],
                    "constructor_name": row["constructor_champion_name"],
                    "points": row["constructor_champion_points"],
                    "race_wins": row["constructor_champion_race_wins"],
                }
                if row["constructor_champion_id"]
                else None,
                "constructors": row["constructors"] or [],
                "drivers": row["drivers"] or [],
                "engine_manufacturers": row["engine_manufacturers"] or [],
                "tyre_manufacturers": row["tyre_manufacturers"] or [],
                "races": row["races"] or [],
            }
            for row in results
        ]

        return seasons, total
