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
        title="F1 API",
        description="An API for Formula 1 data",
        version=startup.get_version(),
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
    )

    @app.get(API_PREFIX, include_in_schema=False)
    async def api_root_redirect() -> RedirectResponse:
        return RedirectResponse(url=f"{API_PREFIX}/docs")

    @app.get("/", include_in_schema=False)
    async def root_redirect() -> RedirectResponse:
        return RedirectResponse(url=API_PREFIX)

    # Add routers under /api/v0
    routers = startup.add_routers(app)
    startup.add_middlewares(app)

except Exception as e:
    logger.exception(
        "app_initialization_failed",
        error_type=type(e).__name__,
    )
    raise
