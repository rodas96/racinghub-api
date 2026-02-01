from enum import Enum
from fastapi import APIRouter
from f1_api.repositories.season_repository import SeasonRepository
from f1_api.repositories.driver_repository import DriverRepository
from f1_api.routers.race_router import RaceRouter
from f1_api.repositories.race_repository import RaceRepository
from f1_api.routers.season_router import SeasonRouter
from f1_api.services.driver_service import DriverService
from f1_api.routers.driver_router import DriverRouter
from f1_api.routers.health_router import HealthRouter
from typing import Any

from f1_api.services.race_service import RaceService
from f1_api.services.season_service import SeasonService


class RouterFactory:
    """Factory to build FastAPI routers with proper type hints."""

    def build(self, prefix: str, tags: list[str | Enum] | None, **kwargs: Any) -> APIRouter:
        """Build an APIRouter, forwarding all arguments to FastAPI's APIRouter."""
        if not prefix.startswith("/"):
            prefix = f"/{prefix}"

        return APIRouter(prefix=prefix, tags=tags, **kwargs)

    def build_routers(self) -> list[APIRouter]:
        """Build and return a list of APIRouters for the application."""

        driver_repository = DriverRepository()
        season_repository = SeasonRepository()
        race_repository = RaceRepository()

        driver_service = DriverService(driver_repository=driver_repository, season_repository=season_repository)
        season_service = SeasonService(season_repository=season_repository)
        race_service = RaceService(race_repository=race_repository)

        season_router = SeasonRouter(season_service=season_service, factory=self.build)
        driver_router = DriverRouter(driver_service=driver_service, factory=self.build)
        race_router = RaceRouter(race_service=race_service, factory=self.build)
        health_router = HealthRouter(factory=self.build)

        return [
            driver_router.router,
            season_router.router,
            race_router.router,
            health_router.router,
        ]
