from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from f1_api.prodivers.cache import configure_caches
from f1_api import startup
from f1_api.prodivers.logger import get_logger

logger = get_logger()


try:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Manage application lifespan events."""
        configure_caches()
        yield
        # Shutdown: cleanup would go here if needed

    app = FastAPI(
        lifespan=lifespan,
        title="F1 API",
        description="An API for Formula 1 data",
        version=startup.get_version(),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    routers = startup.add_routers(app)
    startup.add_middlewares(app)


except Exception as e:
    logger.exception(
        "app_initialization_failed",
        error_type=type(e).__name__,
    )
    raise
