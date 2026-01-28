from fastapi import APIRouter
from typing import Callable
from datetime import datetime, timezone
from f1_api.prodivers.cache import health_check_cache
from f1_api.prodivers.db import health_check_db
from f1_api.schemas.shared.responses import HealthResponse


class HealthRouter:
    def __init__(
        self,
        factory: Callable[..., APIRouter],
    ):
        self.router = factory(
            prefix="/health",
            tags=["health"],
        )

        self.router.add_api_route(
            "",
            self.get_health,
            methods=["GET"],
            summary="Get Health Status",
            operation_id="getHealthStatus",
            response_model=HealthResponse,
        )

    async def get_health(self) -> HealthResponse:
        db_healthy = await health_check_db()
        cache_healthy = await health_check_cache()

        overall_status = "healthy" if db_healthy == "healthy" and cache_healthy == "healthy" else "unhealthy"

        return HealthResponse(
            status=overall_status,
            timestamp=datetime.now(timezone.utc),
            database=db_healthy,
            cache=cache_healthy,
        )
