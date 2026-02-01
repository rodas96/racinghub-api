from fastapi import APIRouter, Query
from typing import Callable

from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.race_service import RaceService
from f1_api.schemas.race_schema import RaceResponse


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
