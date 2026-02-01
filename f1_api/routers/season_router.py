from typing import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.season_schema import SeasonResponse
from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.season_service import SeasonService


class SeasonRouter:
    def __init__(self, season_service: SeasonService, factory: Callable[..., APIRouter]):
        self.router = factory(
            prefix="/seasons",
            tags=["seasons"],
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

    async def get_seasons(
        self,
        page: int = Query(
            1,
            ge=1,
            description="Page number",
        ),
        limit: int = Query(
            20,
            ge=1,
            le=20,
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
