from enum import Enum
from typing import Any

from fastapi import APIRouter

from f1_api.repositories.constructor_repository import ConstructorRepository
from f1_api.repositories.driver_repository import DriverRepository
from f1_api.repositories.race_repository import RaceRepository
from f1_api.repositories.season_repository import SeasonRepository
from f1_api.repositories.standing_repository import StandingRepository
from f1_api.routers.constructor_router import ConstructorRouter
from f1_api.routers.driver_router import DriverRouter
from f1_api.routers.health_router import HealthRouter
from f1_api.routers.race_router import RaceRouter
from f1_api.routers.season_router import SeasonRouter
from f1_api.routers.standing_router import StandingRouter
from f1_api.services.constructor_service import ConstructorService
from f1_api.services.driver_service import DriverService
from f1_api.services.race_service import RaceService
from f1_api.services.season_service import SeasonService
from f1_api.services.standing_service import StandingService


def _make_router(prefix: str, tags: list[str | Enum] | None, **kwargs: Any) -> APIRouter:
    """Build an APIRouter with normalized prefix."""
    if not prefix.startswith("/"):
        prefix = f"/{prefix}"
    return APIRouter(prefix=prefix, tags=tags, **kwargs)


def build_routers() -> list[APIRouter]:
    """Build and return a list of APIRouters for the application."""
    driver_repository = DriverRepository()
    season_repository = SeasonRepository()
    race_repository = RaceRepository()
    constructor_repository = ConstructorRepository()
    standing_repository = StandingRepository()

    driver_service = DriverService(
        driver_repository=driver_repository,
        season_repository=season_repository,
        race_repository=race_repository,
    )
    season_service = SeasonService(season_repository=season_repository)
    race_service = RaceService(race_repository=race_repository)
    constructor_service = ConstructorService(constructor_repository=constructor_repository)
    standing_service = StandingService(
        standing_repository=standing_repository,
        season_repository=season_repository,
    )

    driver_router = DriverRouter(driver_service=driver_service, factory=_make_router)
    season_router = SeasonRouter(season_service=season_service, factory=_make_router)
    race_router = RaceRouter(race_service=race_service, factory=_make_router)
    constructor_router = ConstructorRouter(constructor_service=constructor_service, factory=_make_router)
    standing_router = StandingRouter(standing_service=standing_service, factory=_make_router)
    health_router = HealthRouter(factory=_make_router)

    return [
        driver_router.router,
        season_router.router,
        race_router.router,
        constructor_router.router,
        standing_router.router,
        health_router.router,
    ]
