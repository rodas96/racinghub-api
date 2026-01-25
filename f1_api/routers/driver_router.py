from typing import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.driver_schema import DriverSchema, DriverOrderField
from f1_api.schemas.requests import SortOrder
from f1_api.schemas.responses import PagedResponse
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
            response_model=PagedResponse[DriverSchema],
        )
        self.router.add_api_route(
            "/{driver_id}",
            self.get_driver_by_id,
            methods=["GET"],
            summary="Get Driver by ID",
            operation_id="getDriverById",
            response_model=DriverSchema,
        )
        self.router.add_api_route(
            "/{driver_id}/results",
            self.get_driver_results,
            methods=["GET"],
            summary="Get Driver Results",
            operation_id="getDriverResults",
            response_model=list[dict],
        )
        self.router.add_api_route(
            "/{driver_id}/seasons",
            self.get_driver_seasons,
            methods=["GET"],
            summary="Get Driver Seasons",
            operation_id="getDriverSeasons",
            response_model=list[int],
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
    ) -> PagedResponse[DriverSchema]:
        skip = (page - 1) * limit

        drivers, total = await self._driver_service.get_drivers(
            skip=skip, limit=limit, order_by=order_by, sort_by=sort_by
        )

        return PagedResponse[DriverSchema].create(
            data=[DriverSchema.model_validate(driver) for driver in drivers],
            page=page,
            limit=limit,
            total=total,
        )

    async def get_driver_by_id(self, driver_id: str) -> DriverSchema:
        driver = await self._driver_service.get_driver(driver_id=driver_id)

        return DriverSchema.model_validate(driver)

    async def get_driver_results(self, driver_id: str) -> list[dict]:
        return await self._driver_service.get_driver_results(driver_id=driver_id)

    async def get_driver_seasons(self, driver_id: str) -> list[int]:
        driver_seasons = await self._driver_service.get_driver_seasons(driver_id=driver_id)

        return [season.year for season in driver_seasons]
