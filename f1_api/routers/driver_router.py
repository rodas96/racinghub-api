from typing import Callable
from fastapi import APIRouter, Query
from f1_api.schemas.driver_schema import Driver, DriverOrderField
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
            response_model=PagedResponse[Driver],
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
    ) -> PagedResponse[Driver]:
        skip = (page - 1) * limit

        drivers, total = await self._driver_service.get_drivers(
            skip=skip, limit=limit, order_by=order_by, sort_by=sort_by
        )

        return PagedResponse[Driver].create(
            data=[Driver.model_validate(driver) for driver in drivers],
            page=page,
            limit=limit,
            total=total,
        )
