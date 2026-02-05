from collections.abc import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.constructor_schema import ConstructorResponse, ConstructorSeasonResponse
from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.constructor_service import ConstructorService


class ConstructorRouter:
    def __init__(
        self,
        constructor_service: ConstructorService,
        factory: Callable[..., APIRouter],
    ):
        self._constructor_service = constructor_service
        self.router = factory(prefix="/constructors", tags=["Constructors"])
        self.router.add_api_route(
            "",
            self.get_constructors,
            methods=["GET"],
            response_model=PagedResponse[ConstructorResponse],
        )
        self.router.add_api_route(
            "/{constructor_id}",
            self.get_constructor,
            methods=["GET"],
            response_model=ConstructorResponse,
        )
        self.router.add_api_route(
            "/{constructor_id}/seasons",
            self.get_constructor_seasons,
            methods=["GET"],
            response_model=list[ConstructorSeasonResponse],
        )

    async def get_constructors(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(100, ge=1, le=100, description="Number of items per page"),
    ) -> PagedResponse[ConstructorResponse]:
        """Get all constructors with pagination."""
        skip = (page - 1) * limit
        constructors, total = await self._constructor_service.get_constructors(skip=skip, limit=limit)

        return PagedResponse[ConstructorResponse].create(
            data=[ConstructorResponse.model_validate(constructor) for constructor in constructors],
            total=total,
            page=page,
            limit=limit,
        )

    async def get_constructor(self, constructor_id: str) -> ConstructorResponse:
        """Get a single constructor by ID."""
        constructor = await self._constructor_service.get_constructor(constructor_id)

        return ConstructorResponse.model_validate(constructor)

    async def get_constructor_seasons(self, constructor_id: str) -> list[ConstructorSeasonResponse]:
        """Get all seasons a constructor competed in."""
        constructor_seasons = await self._constructor_service.get_constructor_seasons(constructor_id)

        return [ConstructorSeasonResponse.model_validate(season) for season in constructor_seasons]
