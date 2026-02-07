from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from f1_api.prodivers.cache import configure_caches
from f1_api import startup
from f1_api.prodivers.logger import get_logger

logger = get_logger()

API_PREFIX = f"/api/v{startup.get_major_version()}"

try:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Manage application lifespan events."""
        configure_caches()
        yield
        # Cleanup on shutdown (if needed)

    app = FastAPI(
        lifespan=lifespan,
        title="RacingHub API - Formula 1 Historical Data & Statistics",
        description=(
            "Open-source REST API providing comprehensive Formula 1 historical data and statistics. "
            "Access driver profiles, constructor information, race results, qualifying sessions, "
            "sprint races, pit stop data, fastest laps, championship standings, and season calendars. "
            "Powered by the F1DB open-source project. Perfect for motorsport analytics, "
            "data visualization, fantasy racing apps, and historical research. "
            "Data spans from 1950 to present.  "
            "Note: This is an independent project and is not affiliated with or endorsed by Formula 1®. "
            "Official endpoint: racinghub.net/api/v1"
        ),
        version=startup.get_version(),
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
        openapi_url=f"{API_PREFIX}/openapi.json",
        openapi_tags=[
            {"name": "Drivers", "description": "Driver data, career statistics, race results, and season history"},
            {
                "name": "Constructors",
                "description": "Team information, constructor history, and championship participation",
            },
            {
                "name": "Races",
                "description": "Race results, qualifying, sprint races, starting grids, pit stops, and fastest laps",
            },
            {
                "name": "Seasons",
                "description": "Season calendars, participating drivers, constructors, and race schedules",
            },
            {"name": "Standings", "description": "Final championship standings for drivers and constructors by season"},
            {"name": "Health", "description": "API health check and status monitoring"},
        ],
        contact={
            "name": "RacingHub",
            "url": "https://github.com/rodas96/f1-api",
        },
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
        },
    )

    @app.get(API_PREFIX, include_in_schema=False)
    async def api_root_redirect() -> RedirectResponse:
        return RedirectResponse(url=f"{API_PREFIX}/docs")

    @app.get("/", include_in_schema=False)
    async def root_redirect() -> RedirectResponse:
        return RedirectResponse(url=API_PREFIX)

    routers = startup.add_routers(app)
    startup.add_middlewares(app)

except Exception as e:
    logger.exception(
        "app_initialization_failed",
        error_type=type(e).__name__,
    )
    raise
