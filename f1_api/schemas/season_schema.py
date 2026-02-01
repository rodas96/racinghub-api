from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal
from typing import Optional


class SeasonChampionResponse(BaseModel):
    driver_id: str
    driver_name: str
    points: Decimal
    race_wins: int
    pole_positions: Optional[int] = None


class SeasonConstructorChampionResponse(BaseModel):
    constructor_id: str
    constructor_name: str
    points: Decimal
    race_wins: int
    pole_positions: Optional[int] = None


class SeasonConstructorResponse(BaseModel):
    id: str
    name: str
    country_code: str
    engine_manufacturer: str
    position: Optional[int] = None
    points: Optional[Decimal] = None
    race_wins: Optional[int] = None
    pole_positions: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonDriverResponse(BaseModel):
    id: str
    name: str
    abbr: str
    number: Optional[str] = None
    position: Optional[int] = None
    points: Optional[Decimal] = None
    race_wins: Optional[int] = None
    pole_positions: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonEngineManufacturerResponse(BaseModel):
    id: str
    name: str
    country_code: str
    total_points: Optional[Decimal] = None
    total_wins: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonTyreManufacturerResponse(BaseModel):
    id: str
    name: str
    country_code: str
    total_wins: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonRaceResponse(BaseModel):
    id: int
    round: int
    date: date
    name: str
    circuit: str
    country_code: str
    laps: Optional[int] = None
    distance: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class SeasonResponse(BaseModel):
    year: int
    total_races: int
    total_constructors: int
    total_drivers: int

    champion: Optional[SeasonChampionResponse] = None
    constructor_champion: Optional[SeasonConstructorChampionResponse] = None

    constructors: list[SeasonConstructorResponse]
    drivers: list[SeasonDriverResponse]
    engine_manufacturers: list[SeasonEngineManufacturerResponse]
    tyre_manufacturers: list[SeasonTyreManufacturerResponse]
    races: list[SeasonRaceResponse]

    model_config = ConfigDict(from_attributes=True)
