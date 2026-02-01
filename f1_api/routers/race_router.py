from fastapi import APIRouter, Query
from typing import Callable

from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.race_service import RaceService
from f1_api.schemas.race_schema import RaceQualifyingResponse, RaceResponse, RaceResultResponse


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
        )
        self.router.add_api_route(
            "{race_id}",
            self.get_race,
            methods=["GET"],
            summary="Get Race",
            operation_id="getRace",
            response_model=RaceResponse,
        )
        self.router.add_api_route(
            "{race_id}/results",
            self.get_race_results,
            methods=["GET"],
            summary="Get Race Results",
            operation_id="getRaceResults",
            response_model=list[RaceResultResponse],
        )
        self.router.add_api_route(
            "{race_id}/qualifying",
            self.get_race_qualifying_results,
            methods=["GET"],
            summary="Get Race Qualifying Results",
            operation_id="getRaceQualifyingResults",
            response_model=list[RaceQualifyingResponse],
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
        race = await self._race_service.get_race(race_id)

        return RaceResponse.model_validate(race)

    async def get_race_results(self, race_id: int) -> list[RaceResultResponse]:
        race_results = await self._race_service.get_race_results(race_id)

        return [RaceResultResponse.model_validate(result) for result in race_results]

    async def get_race_qualifying_results(self, race_id: int) -> list[RaceQualifyingResponse]:
        race_qualifying_results = await self._race_service.get_race_qualifying_results(race_id)

        return [RaceQualifyingResponse.model_validate(result) for result in race_qualifying_results]
