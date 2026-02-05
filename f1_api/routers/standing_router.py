from typing import Callable
from fastapi import APIRouter
from f1_api.services.standing_service import StandingService
from f1_api.schemas.standing_schema import ConstructorStandingResponse, DriverStandingResponse


class StandingRouter:
    def __init__(
        self,
        standing_service: StandingService,
        factory: Callable[..., APIRouter],
    ):
        self._standing_service = standing_service
        self.router = factory(prefix="/standings", tags=["Standings"])
        self.router.add_api_route(
            "/{year}/drivers",
            self.get_driver_standings,
            methods=["GET"],
            response_model=list[DriverStandingResponse],
        )
        self.router.add_api_route(
            "/{year}/constructors",
            self.get_constructor_standings,
            methods=["GET"],
            response_model=list[ConstructorStandingResponse],
        )

    async def get_driver_standings(self, year: int) -> list[DriverStandingResponse]:
        """Get final driver championship standings for a season."""
        driver_standings = await self._standing_service.get_driver_standings(year)

        return [DriverStandingResponse.model_validate(standing) for standing in driver_standings]

    async def get_constructor_standings(self, year: int) -> list[ConstructorStandingResponse]:
        """Get final constructor championship standings for a season."""
        constructor_standings = await self._standing_service.get_constructor_standings(year)

        return [ConstructorStandingResponse.model_validate(standing) for standing in constructor_standings]
