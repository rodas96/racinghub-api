from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional


class ConstructorResponse(BaseModel):
    """Full constructor profile with career statistics."""

    id: str
    name: str
    full_name: str
    country_id: str

    total_championship_wins: int
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_1_and_2_finishes: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_points: Decimal
    total_championship_points: Decimal
    total_pole_positions: int
    total_fastest_laps: int
    total_sprint_race_starts: int
    total_sprint_race_wins: int

    best_championship_position: Optional[int] = None
    best_starting_grid_position: Optional[int] = None
    best_race_result: Optional[int] = None
    best_sprint_race_result: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ConstructorSeasonResponse(BaseModel):
    """Constructor's performance in a specific season."""

    year: int
    position: Optional[int] = None
    points: Optional[Decimal] = None
    race_wins: Optional[int] = None
    pole_positions: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
