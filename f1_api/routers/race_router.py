from fastapi import APIRouter, Query
from typing import Callable

from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.race_service import RaceService
from f1_api.schemas.race_schema import (
    RaceFastestLapResponse,
    RaceGridResponse,
    RacePitStopResponse,
    RaceQualifyingResponse,
    RaceResponse,
    RaceResultResponse,
)


class RaceRouter:
    def __init__(self, race_service: RaceService, factory: Callable[..., APIRouter]):
        self.router = factory(prefix="/races", tags=["Races"])
        self._race_service = race_service

        self.router.add_api_route(
            "",
            self.get_races,
            methods=["GET"],
            summary="Get Races",
            operation_id="getRaces",
            response_model=PagedResponse[RaceResponse],
            description=(
                "Retrieve a paginated list of all Formula 1 races, including race name, date, "
                "season, circuit, and round. Supports pagination with page and limit parameters."
            ),
        )
        self.router.add_api_route(
            "/{race_id}",
            self.get_race,
            methods=["GET"],
            summary="Get Race",
            operation_id="getRace",
            response_model=RaceResponse,
            description=(
                "Retrieve detailed information about a specific Formula 1 race by its unique ID. "
                "Includes date, circuit, country, season round, and race type."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/results",
            self.get_race_results,
            methods=["GET"],
            summary="Get Race Results",
            operation_id="getRaceResults",
            response_model=list[RaceResultResponse],
            description=(
                "Retrieve the official results of a specific Formula 1 race. "
                "Includes finishing positions, driver names, team results, points, and race status."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/starting-grid",
            self.get_race_starting_grid,
            methods=["GET"],
            summary="Get Race Starting Grid",
            operation_id="getRaceStartingGrid",
            response_model=list[RaceGridResponse],
            description=(
                "Retrieve the starting grid for a specific Formula 1 race. "
                "Includes driver positions, teams, and qualifying times."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/qualifying-results",
            self.get_race_qualifying_results,
            methods=["GET"],
            summary="Get Race Qualifying Results",
            operation_id="getRaceQualifyingResults",
            response_model=list[RaceQualifyingResponse],
            description=(
                "Retrieve qualifying session results for a specific Formula 1 race. "
                "Includes driver positions, lap times, and team performance."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/sprint-results",
            self.get_sprint_race_results,
            methods=["GET"],
            summary="Get Sprint Race Results",
            operation_id="getSprintRaceResults",
            response_model=list[RaceResultResponse],
            description=(
                "Retrieve the official results of a Formula 1 sprint race, including driver positions, "
                "teams, and points scored."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/sprint-starting-grid",
            self.get_race_sprint_starting_grid,
            methods=["GET"],
            summary="Get Sprint Race Starting Grid",
            operation_id="getSprintRaceStartingGrid",
            response_model=list[RaceGridResponse],
            description=(
                "Retrieve the starting grid for a Formula 1 sprint race. "
                "Includes driver positions, teams, and qualifying performance."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/fastest-lap",
            self.get_race_fastest_lap,
            methods=["GET"],
            summary="Get Race Fastest Lap",
            operation_id="getRaceFastestLap",
            response_model=list[RaceFastestLapResponse],
            description=(
                "Retrieve details of the fastest lap in a specific Formula 1 race. "
                "Includes driver, lap time, team, and lap number."
            ),
        )
        self.router.add_api_route(
            "/{race_id}/pit-stops",
            self.get_race_pit_stops,
            methods=["GET"],
            summary="Get Race Pit Stops",
            operation_id="getRacePitStops",
            response_model=list[RacePitStopResponse],
            description=(
                "Retrieve all pit stop information for a specific Formula 1 race. "
                "Includes driver, lap, duration, and team data."
            ),
        )

    async def get_races(
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
    ) -> PagedResponse[RaceResponse]:
        skip = (page - 1) * limit
        races, total = await self._race_service.get_races(skip=skip, limit=limit)

        return PagedResponse[RaceResponse].create(
            data=[RaceResponse.model_validate(race) for race in races],
            total=total,
            page=page,
            limit=limit,
        )

    async def get_race(self, race_id: int) -> RaceResponse:
        race = await self._race_service.get_race(race_id=race_id)

        return RaceResponse.model_validate(race)

    async def get_race_results(self, race_id: int) -> list[RaceResultResponse]:
        race_results = await self._race_service.get_race_results(race_id=race_id)

        return [RaceResultResponse.model_validate(result) for result in race_results]

    async def get_race_starting_grid(self, race_id: int) -> list[RaceGridResponse]:
        starting_grid = await self._race_service.get_race_starting_grid(race_id=race_id)

        return [RaceGridResponse.model_validate(grid) for grid in starting_grid]

    async def get_race_fastest_lap(self, race_id: int) -> list[RaceFastestLapResponse]:
        fastest_lap = await self._race_service.get_race_fastest_lap(race_id=race_id)

        return [RaceFastestLapResponse.model_validate(lap) for lap in fastest_lap]

    async def get_sprint_race_results(self, race_id: int) -> list[RaceResultResponse]:
        sprint_race_results = await self._race_service.get_sprint_race_results(race_id=race_id)

        return [RaceResultResponse.model_validate(result) for result in sprint_race_results]

    async def get_race_sprint_starting_grid(self, race_id: int) -> list[RaceGridResponse]:
        sprint_starting_grid = await self._race_service.get_race_sprint_starting_grid(race_id=race_id)

        return [RaceGridResponse.model_validate(grid) for grid in sprint_starting_grid]

    async def get_race_qualifying_results(self, race_id: int) -> list[RaceQualifyingResponse]:
        race_qualifying_results = await self._race_service.get_race_qualifying_results(race_id=race_id)

        return [RaceQualifyingResponse.model_validate(result) for result in race_qualifying_results]

    async def get_race_pit_stops(self, race_id: int) -> list[RacePitStopResponse]:
        race_pit_stops = await self._race_service.get_race_pit_stops(race_id=race_id)

        return [RacePitStopResponse.model_validate(pit_stop) for pit_stop in race_pit_stops]
