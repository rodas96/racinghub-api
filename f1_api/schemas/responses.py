from datetime import date, datetime
from decimal import Decimal
from typing import Generic
from annotated_types import T
from pydantic import BaseModel, Field


class PagedResponse(BaseModel, Generic[T]):
    data: list[T]
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool = Field(description="Whether there's a next page")
    has_previous: bool = Field(description="Whether there's a previous page")

    @classmethod
    def create(cls, data: list[T], page: int, limit: int, total: int) -> "PagedResponse[T]":
        total_pages = (total + limit - 1) // limit
        return cls(
            data=data,
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


class RaceResultResponse(BaseModel):
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
    position_number: int | None = Field(None, description="Final classification position (null if DNF/DSQ)")
    position_text: str = Field(..., description="Position as shown (1, 2, 3, DNF, DSQ, etc.)")
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
    qualification_position_number: int | None = Field(None, description="Qualifying position")
    qualification_position_text: str | None = Field(None, description="Qualifying position text")
    grid_position_number: int | None = Field(None, description="Starting grid position")
    grid_position_text: str | None = Field(None, description="Grid position text")
    positions_gained: int | None = Field(None, description="Positions gained/lost from grid")

    # Strategy
    pit_stops: int | None = Field(None, description="Number of pit stops")
    tyre_manufacturer: str | None = Field(None, description="Tyre supplier")
    engine_manufacturer: str | None = Field(None, description="Engine supplier")

    # Additional Info
    shared_car: bool = Field(False, description="Car shared with another driver")

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    cache: str
