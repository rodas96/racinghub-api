from typing import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.season_schema import (
    SeasonDriverResponse,
    SeasonRaceResponse,
    SeasonResponse,
    SeasonConstructorResponse,
)
from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.season_service import SeasonService


class SeasonRouter:
    def __init__(self, season_service: SeasonService, factory: Callable[..., APIRouter]):
        self.router = factory(
            prefix="/seasons",
            tags=["Seasons"],
        )
        self._season_service = season_service

        self.router.add_api_route(
            "",
            self.get_seasons,
            methods=["GET"],
            summary="Get Seasons",
            operation_id="getSeasons",
            response_model=PagedResponse[SeasonResponse],
        )
        self.router.add_api_route(
            "/{year}",
            self.get_season,
            methods=["GET"],
            summary="Get Season by Year",
            operation_id="getSeasonByYear",
            response_model=SeasonResponse,
        )
        self.router.add_api_route(
            "/{year}/drivers",
            self.get_season_drivers,
            methods=["GET"],
            summary="Get Season Drivers",
            operation_id="getSeasonDrivers",
            response_model=list[SeasonDriverResponse],
        )
        self.router.add_api_route(
            "/{year}/constructors",
            self.get_season_constructors,
            methods=["GET"],
            summary="Get Season Constructors",
            operation_id="getSeasonConstructors",
            response_model=list[SeasonConstructorResponse],
        )
        self.router.add_api_route(
            "/{year}/races",
            self.get_season_races,
            methods=["GET"],
            summary="Get Season Races",
            operation_id="getSeasonRaces",
            response_model=list[SeasonRaceResponse],
        )

    async def get_seasons(
        self,
        page: int = Query(
            1,
            ge=1,
            description="Page number",
        ),
        limit: int = Query(
            1,
            ge=1,
            le=100,
            description="Number of items per page",
        ),
    ) -> PagedResponse[SeasonResponse]:
        skip = (page - 1) * limit
        seasons, total = await self._season_service.get_seasons(skip=skip, limit=limit)

        return PagedResponse[SeasonResponse].create(
            data=[SeasonResponse.model_validate(season) for season in seasons],
            total=total,
            page=page,
            limit=limit,
        )

    async def get_season(self, year: int) -> SeasonResponse:
        season = await self._season_service.get_season(year=year)
        return SeasonResponse.model_validate(season)

    async def get_season_drivers(self, year: int) -> list[SeasonDriverResponse]:
        seasons_drivers = await self._season_service.get_season_drivers(year=year)

        return [SeasonDriverResponse.model_validate(driver) for driver in seasons_drivers]

    async def get_season_constructors(self, year: int) -> list[SeasonConstructorResponse]:
        seasons_constructors = await self._season_service.get_season_constructors(year=year)

        return [SeasonConstructorResponse.model_validate(constructor) for constructor in seasons_constructors]

    async def get_season_races(self, year: int) -> list[SeasonRaceResponse]:
        seasons_races = await self._season_service.get_season_races(year=year)

        return [SeasonRaceResponse.model_validate(race) for race in seasons_races]
