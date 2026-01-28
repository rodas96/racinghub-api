from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal


class DriverResponse(BaseModel):
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

    model_config = {"from_attributes": True}


class DriverRaceResultResponse(BaseModel):
    """Complete race result for a driver including race context."""

    # Race Information
    race_id: int
    race_year: int
    race_round: int
    race_date: date
    race_name: str = Field(..., description="Official race name")
    grand_prix_name: str = Field(..., description="Grand Prix name (e.g., 'Australian Grand Prix')")
    circuit_name: str = Field(..., description="Circuit name")
    circuit_location: str | bool = Field(..., description="City/Country")

    # Result Details
    position_display_order: int
    position: int | None = Field(None, description="Final classification position (null if DNF/DSQ)")

    driver_number: str
    constructor_name: str = Field(..., description="Team name")

    # Race Performance
    laps: int | None = Field(None, description="Laps completed")
    time: str | None = Field(None, description="Race time (winner) or gap")
    time_millis: int | None = Field(None, description="Race time in milliseconds")
    gap: str | None = Field(None, description="Gap to leader")
    gap_millis: int | None = Field(None, description="Gap in milliseconds")
    gap_laps: int | None = Field(None, description="Laps behind leader")
    interval: str | None = Field(None, description="Interval to car ahead")
    interval_millis: int | None = Field(None, description="Interval in milliseconds")

    # Penalties & Retirement
    time_penalty: str | None = Field(None, description="Time penalty applied")
    time_penalty_millis: int | None = Field(None, description="Penalty in milliseconds")
    reason_retired: str | None = Field(None, description="DNF reason if applicable")

    # Points & Achievements
    points: Decimal | None = Field(None, description="Championship points earned")
    pole_position: bool = Field(False, description="Started from pole")
    fastest_lap: bool | None = Field(False, description="Set fastest lap")
    driver_of_the_day: bool | None = Field(False, description="Won driver of the day")
    grand_slam: bool = Field(False, description="Pole + Win + Fastest Lap + Led every lap")

    # Grid & Qualifying
    qualification_position: int | None = Field(None, description="Qualifying position")
    grid_position: int | None = Field(None, description="Starting grid position")
    positions_gained: int | None = Field(None, description="Positions gained/lost from grid")

    # Strategy
    pit_stops: int | None = Field(None, description="Number of pit stops")
    tyre_manufacturer: str | None = Field(None, description="Tyre supplier")
    engine_manufacturer: str | None = Field(None, description="Engine supplier")

    model_config = {"from_attributes": True}
