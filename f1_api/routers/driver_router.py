from typing import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.driver_schema import DriverResponse, DriverRaceResultResponse, DriverSeasonStatsResponse
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
            tags=["drivers"],
        )
        self._driver_service = driver_service

        self.router.add_api_route(
            "",
            self.get_drivers,
            methods=["GET"],
            summary="Get Drivers",
            operation_id="getDrivers",
            response_model=PagedResponse[DriverResponse],
        )
        self.router.add_api_route(
            "/{driver_id}",
            self.get_driver_by_id,
            methods=["GET"],
            summary="Get Driver by ID",
            operation_id="getDriverById",
            response_model=DriverResponse,
        )
        self.router.add_api_route(
            "/{driver_id}/results",
            self.get_driver_races_results,
            methods=["GET"],
            summary="Get Driver Results",
            operation_id="getDriverRacesResults",
            response_model=PagedResponse[DriverRaceResultResponse],
        )
        self.router.add_api_route(
            "/{driver_id}/seasons",
            self.get_driver_seasons,
            methods=["GET"],
            summary="Get Driver Seasons",
            operation_id="getDriverSeasons",
            response_model=list[DriverSeasonStatsResponse],
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
    ) -> PagedResponse[DriverResponse]:
        skip = (page - 1) * limit

        drivers, total = await self._driver_service.get_drivers(
            skip=skip, limit=limit, order_by=order_by, sort_by=sort_by
        )

        return PagedResponse[DriverResponse].create(
            data=[DriverResponse.model_validate(driver) for driver in drivers],
            page=page,
            limit=limit,
            total=total,
        )

    async def get_driver_by_id(self, driver_id: str) -> DriverResponse:
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
    ) -> list[DriverSeasonStatsResponse]:
        driver_seasons = await self._driver_service.get_driver_seasons(driver_id=driver_id)

        return [DriverSeasonStatsResponse.model_validate(driver_season) for driver_season in driver_seasons]
