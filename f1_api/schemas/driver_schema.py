from enum import Enum
from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal


class DriverOrderField(str, Enum):
    NAME = "name"
    DATE_OF_BIRTH = "date_of_birth"
    TOTAL_CHAMPIONSHIP_WINS = "total_championship_wins"
    TOTAL_CHAMPIONSHIP_POINTS = "total_championship_points"
    TOTAL_RACE_WINS = "total_race_wins"
    TOTAL_PODIUMS = "total_podiums"
    TOTAL_POINTS = "total_points"
    TOTAL_POLE_POSITIONS = "total_pole_positions"
    TOTAL_FASTEST_LAPS = "total_fastest_laps"


class Driver(BaseModel):
    id: str
    name: str
    first_name: str
    last_name: str
    full_name: str
    abbreviation: str
    gender: str
    date_of_birth: date
    place_of_birth: str
    nationality_country_id: str
    country_of_birth_country_id: str
    second_nationality_country_id: Optional[str] = None
    permanent_number: Optional[str] = None
    date_of_death: Optional[date] = None

    total_championship_wins: int
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_points: Decimal
    total_championship_points: Decimal
    total_pole_positions: int
    total_fastest_laps: int
    total_driver_of_the_day: int
    total_grand_slams: int

    best_championship_position: Optional[int] = None
    best_starting_grid_position: Optional[int] = None
    best_race_result: Optional[int] = None

    class ConfigDict:
        from_attributes = True
