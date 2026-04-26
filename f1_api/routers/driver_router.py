from typing import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.driver_schema import DriverResponse, DriverRaceResultResponse, DriverSeasonResponse
from f1_api.schemas.shared.enums import DriverOrderField
from f1_api.schemas.shared.requests import SortOrder
from f1_api.schemas.shared.responses import PagedResponse
from f1_api.services.driver_service import DriverService


class DriverRouter:
    def __init__(
        self,
        driver_service: DriverService,
        factory: Callable[..., APIRouter],
    ):
        self.router = factory(
            prefix="/drivers",
            tags=["Drivers"],
        )
        self._driver_service = driver_service

        self.router.add_api_route(
            "",
            self.get_drivers,
            methods=["GET"],
            summary="Get All Drivers",
            description=(
                "Retrieve a paginated list of all Formula 1 drivers."
                "Supports sorting by name, number, or code. Returns driver profiles including "
                "nationality, date of birth, and career information. Historical data from 1950 onwards."
            ),
            operation_id="getDrivers",
            response_model=PagedResponse[DriverResponse],
            responses={
                200: {
                    "description": "Successfully retrieved paginated driver list",
                },
                422: {
                    "description": "Invalid query parameters",
                },
            },
        )

        self.router.add_api_route(
            "/{driver_id}",
            self.get_driver,
            methods=["GET"],
            summary="Get Driver by ID",
            description=(
                "Retrieve detailed information about a specific Formula 1 driver. "
                "Returns complete driver profile including full name, nationality, birth date, "
                "permanent number, and biographical data. Use driver reference ID (e.g., 'hamilton', 'verstappen')."
            ),
            operation_id="getDriver",
            response_model=DriverResponse,
            responses={
                200: {
                    "description": "Successfully retrieved driver information",
                },
                404: {
                    "description": "Driver not found",
                },
                422: {
                    "description": "Invalid driver ID format",
                },
            },
        )

        self.router.add_api_route(
            "/{driver_id}/results",
            self.get_driver_races_results,
            methods=["GET"],
            summary="Get Driver Race Results",
            description=(
                "Retrieve complete race history for a specific driver. Returns paginated results "
                "including finishing position, points scored, grid position, status, fastest lap times, "
                "and race details. Covers all Grand Prix entries throughout the driver's career."
            ),
            operation_id="getDriverRacesResults",
            response_model=PagedResponse[DriverRaceResultResponse],
            responses={
                200: {
                    "description": "Successfully retrieved driver race results",
                },
                404: {
                    "description": "Driver not found",
                },
                422: {
                    "description": "Invalid parameters",
                },
            },
        )

        self.router.add_api_route(
            "/{driver_id}/seasons",
            self.get_driver_seasons,
            methods=["GET"],
            summary="Get Driver Season History",
            description=(
                "Retrieve all seasons a driver competed in. Returns year-by-year participation "
                "including constructor teams, championship standings, total points, wins, podiums, "
                "and pole positions for each season. Useful for career progression analysis."
            ),
            operation_id="getDriverSeasons",
            response_model=list[DriverSeasonResponse],
            responses={
                200: {
                    "description": "Successfully retrieved driver season history",
                },
                404: {
                    "description": "Driver not found or no season data available",
                },
                422: {
                    "description": "Invalid driver ID format",
                },
            },
        )

    async def get_drivers(
        self,
        page: int = Query(
            1,
            ge=1,
            description="Page number",
        ),
        limit: int = Query(
            100,
            ge=1,
            le=100,
            description="Number of items per page",
        ),
        order_by: DriverOrderField = Query(
            DriverOrderField.NAME,
            description="Field to order by if not specified, defaults to name",
        ),
        sort_by: SortOrder = Query(
            SortOrder.ASC,
            description="Order direction if not specified, defaults to ascending",
        ),
        q: str | None = Query(
            None,
            min_length=1,
            description="Search drivers by name (e.g. 'ham', 'lewis ham')",
        ),
    ) -> PagedResponse[DriverResponse]:
        skip = (page - 1) * limit

        drivers, total = await self._driver_service.get_drivers(
            skip=skip,
            limit=limit,
            order_by=order_by,
            sort_by=sort_by,
            q=q,
        )

        return PagedResponse[DriverResponse].create(
            data=[DriverResponse.model_validate(driver) for driver in drivers],
            page=page,
            limit=limit,
            total=total,
        )

    async def get_driver(self, driver_id: str) -> DriverResponse:
        driver = await self._driver_service.get_driver(driver_id=driver_id)

        return DriverResponse.model_validate(driver)

    async def get_driver_races_results(
        self,
        driver_id: str,
        page: int = Query(
            1,
            ge=1,
            description="Page number",
        ),
        limit: int = Query(
            100,
            ge=1,
            le=100,
            description="Number of items per page",
        ),
    ) -> PagedResponse[DriverRaceResultResponse]:
        skip = (page - 1) * limit
        driver_results, total = await self._driver_service.get_driver_races_results(
            skip=skip, limit=limit, driver_id=driver_id
        )

        return PagedResponse[DriverRaceResultResponse].create(
            data=[DriverRaceResultResponse.model_validate(result) for result in driver_results],
            page=page,
            limit=limit,
            total=total,
        )

    async def get_driver_seasons(
        self,
        driver_id: str,
    ) -> list[DriverSeasonResponse]:
        driver_seasons = await self._driver_service.get_driver_seasons(driver_id=driver_id)

        return [DriverSeasonResponse.model_validate(driver_season) for driver_season in driver_seasons]
