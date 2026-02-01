from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional


class RaceResponse(BaseModel):
    id: int
    year: int
    round: int
    date: date
    official_name: str
    grand_prix_id: str
    circuit_id: str
    laps: Optional[int] = None
    distance: Optional[Decimal] = None
    scheduled_laps: Optional[int] = None
    scheduled_distance: Optional[Decimal] = None
    time: Optional[str] = None
    course_length: Optional[Decimal] = None
    turns: Optional[int] = None
    qualifying_format: Optional[str] = None
    sprint_qualifying_format: Optional[str] = None
    circuit_type: Optional[str] = None
    direction: Optional[str] = None
    drivers_championship_decider: bool = False
    constructors_championship_decider: bool = False

    model_config = ConfigDict(from_attributes=True)
