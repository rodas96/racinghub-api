from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional


class DriverStandingResponse(BaseModel):
    """Driver championship standing."""

    position: Optional[int] = None
    position_text: str
    driver_id: str
    driver_name: str
    driver_abbr: str
    driver_number: Optional[str] = None
    points: Decimal
    race_wins: int
    pole_positions: int
    championship_won: bool

    model_config = ConfigDict(from_attributes=True)


class ConstructorStandingResponse(BaseModel):
    """Constructor championship standing."""

    position: Optional[int] = None
    position_text: str
    constructor_id: str
    constructor_name: str
    country_code: str
    engine_manufacturer_id: str
    engine_manufacturer: str
    points: Decimal
    race_wins: int
    pole_positions: int
    championship_won: bool

    model_config = ConfigDict(from_attributes=True)
