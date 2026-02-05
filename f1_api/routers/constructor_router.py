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
            summary="Get All Constructors",
            description=(
                "Retrieve a paginated list of all Formula 1 constructor teams."
                "Returns team information including official name, nationality, and historical data. "
                "Covers all teams from the championship's inception in 1950 to present."
            ),
            operation_id="getConstructors",
            response_model=PagedResponse[ConstructorResponse],
            responses={
                200: {
                    "description": "Successfully retrieved paginated constructor list",
                },
                422: {
                    "description": "Invalid query parameters",
                },
            },
        )

        self.router.add_api_route(
            "/{constructor_id}",
            self.get_constructor,
            methods=["GET"],
            summary="Get Constructor by ID",
            description=(
                "Retrieve detailed information about a specific Formula 1 constructor team. "
                "Returns complete team profile including full name, nationality, and reference ID. "
                "Use constructor reference ID (e.g., 'ferrari', 'mclaren', 'red_bull', 'mercedes')."
            ),
            operation_id="getConstructor",
            response_model=ConstructorResponse,
            responses={
                200: {
                    "description": "Successfully retrieved constructor information",
                },
                404: {
                    "description": "Constructor not found",
                },
                422: {
                    "description": "Invalid constructor ID format",
                },
            },
        )

        self.router.add_api_route(
            "/{constructor_id}/seasons",
            self.get_constructor_seasons,
            methods=["GET"],
            summary="Get Constructor Season History",
            description=(
                "Retrieve all seasons a constructor team competed in. Returns year-by-year "
                "participation including championship standings, total points, wins, podium finishes, "
                "pole positions, and fastest laps for each season. Essential for analyzing team "
                "performance evolution and historical success across different eras of Formula 1."
            ),
            operation_id="getConstructorSeasons",
            response_model=list[ConstructorSeasonResponse],
            responses={
                200: {
                    "description": "Successfully retrieved constructor season history",
                },
                404: {
                    "description": "Constructor not found or no season data available",
                },
                422: {
                    "description": "Invalid constructor ID format",
                },
            },
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
