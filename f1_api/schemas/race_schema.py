from pydantic import BaseModel, ConfigDict
from datetime import date as _date
from decimal import Decimal
from typing import Optional


class SessionResponse(BaseModel):
    date: Optional[_date] = None
    time: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RaceResultResponse(BaseModel):
    position_number: Optional[int] = None
    position_text: str
    driver_number: str
    driver_id: str
    constructor_id: str
    constructor_name: Optional[str] = None
    laps: Optional[int] = None
    time: Optional[str] = None
    gap: Optional[str] = None
    interval: Optional[str] = None
    points: Optional[Decimal] = None
    pit_stops: Optional[int] = None
    grid_position: Optional[int] = None
    positions_gained: Optional[int] = None
    fastest_lap: Optional[bool] = None
    pole_position: Optional[bool] = None
    driver_of_the_day: Optional[bool] = None
    grand_slam: Optional[bool] = None
    reason_retired: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RaceQualifyingResponse(BaseModel):
    position_number: Optional[int] = None
    position_text: str
    driver_number: str
    driver_id: str
    constructor_id: str
    q1: Optional[str] = None
    q2: Optional[str] = None
    q3: Optional[str] = None
    time: Optional[str] = None
    gap: Optional[str] = None
    interval: Optional[str] = None
    laps: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class RaceSprintResponse(BaseModel):
    position_number: Optional[int] = None
    position_text: str
    driver_number: str
    driver_id: str
    constructor_id: str
    time: Optional[str] = None
    gap: Optional[str] = None
    interval: Optional[str] = None
    points: Optional[Decimal] = None
    reason_retired: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RacePracticeResponse(BaseModel):
    position_number: Optional[int] = None
    position_text: str
    driver_number: str
    driver_id: str
    constructor_id: str
    time: Optional[str] = None
    gap: Optional[str] = None
    interval: Optional[str] = None
    laps: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class RaceGridResponse(BaseModel):
    position_number: Optional[int] = None
    position_text: str
    driver_number: str
    driver_id: str
    constructor_id: str
    qualification_position_number: Optional[int] = None
    qualification_position_text: Optional[str] = None
    grid_penalty: Optional[str] = None
    grid_penalty_positions: Optional[int] = None
    time: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RaceFastestLapResponse(BaseModel):
    position_number: Optional[int] = None
    driver_number: str
    driver_id: str
    constructor_id: str
    lap: Optional[int] = None
    time: Optional[str] = None
    gap: Optional[str] = None
    interval: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RacePitStopResponse(BaseModel):
    driver_number: str
    driver_id: str
    constructor_id: str
    stop: Optional[int] = None
    lap: Optional[int] = None
    time: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RaceResponse(BaseModel):
    id: int
    year: int
    round: int
    date: _date
    official_name: str
    grand_prix_id: str
    circuit_id: str
    circuit_type: Optional[str] = None
    direction: Optional[str] = None
    course_length: Optional[Decimal] = None
    turns: Optional[int] = None
    laps: Optional[int] = None
    distance: Optional[Decimal] = None
    scheduled_laps: Optional[int] = None
    scheduled_distance: Optional[Decimal] = None
    time: Optional[str] = None
    qualifying_format: Optional[str] = None
    sprint_qualifying_format: Optional[str] = None
    drivers_championship_decider: bool = False
    constructors_championship_decider: bool = False

    pre_qualifying: Optional[SessionResponse] = None
    free_practice_1: Optional[SessionResponse] = None
    free_practice_2: Optional[SessionResponse] = None
    free_practice_3: Optional[SessionResponse] = None
    free_practice_4: Optional[SessionResponse] = None
    qualifying_1: Optional[SessionResponse] = None
    qualifying_2: Optional[SessionResponse] = None
    qualifying: Optional[SessionResponse] = None
    sprint_qualifying: Optional[SessionResponse] = None
    sprint_race: Optional[SessionResponse] = None
    warming_up: Optional[SessionResponse] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")
