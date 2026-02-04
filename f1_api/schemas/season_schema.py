from pydantic import BaseModel, ConfigDict, model_validator
from datetime import date as _date
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import RowMapping


class DriverChampionResponse(BaseModel):
    driver_id: str
    driver_name: str
    points: float
    race_wins: int
    pole_positions: int

    model_config = ConfigDict(from_attributes=True)


class ConstructorChampionResponse(BaseModel):
    constructor_id: str
    constructor_name: str
    points: float
    race_wins: int
    pole_positions: int

    model_config = ConfigDict(from_attributes=True)


class SeasonResponse(BaseModel):
    year: int
    total_races: int
    total_drivers: int
    total_constructors: int
    champion: DriverChampionResponse
    constructor_champion: ConstructorChampionResponse

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def build_nested(cls: type, data: RowMapping) -> dict[str, Any]:
        return {
            "year": data.year,
            "total_races": data.total_races,
            "total_drivers": data.total_drivers,
            "total_constructors": data.total_constructors,
            "champion": DriverChampionResponse(
                driver_id=data.champion_driver_id,
                driver_name=data.champion_driver_name,
                points=float(data.champion_driver_points),
                race_wins=data.champion_driver_race_wins,
                pole_positions=data.champion_driver_pole_positions,
            ),
            "constructor_champion": ConstructorChampionResponse(
                constructor_id=data.champion_constructor_id,
                constructor_name=data.champion_constructor_name,
                points=float(data.champion_constructor_points),
                race_wins=data.champion_constructor_race_wins,
                pole_positions=data.champion_constructor_pole_positions,
            ),
        }


class SeasonDriverResponse(BaseModel):
    """Driver standings for a specific season."""

    id: str
    name: str
    abbr: str
    number: Optional[str] = None
    position: Optional[int] = None
    points: Optional[Decimal] = None
    race_wins: Optional[int] = None
    pole_positions: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonConstructorResponse(BaseModel):
    """Constructor standings for a specific season."""

    id: str
    name: str
    country_code: str
    engine_manufacturer_id: str
    engine_manufacturer: str
    position: Optional[int] = None
    points: Optional[Decimal] = None
    race_wins: Optional[int] = None
    pole_positions: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonRaceResponse(BaseModel):
    """Race in a season calendar."""

    id: int
    round: int
    date: _date
    name: str
    circuit: str
    country_code: str
    laps: Optional[int] = None
    distance: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)
