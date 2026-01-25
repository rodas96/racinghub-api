from fastapi import Request, Response
from starlette.responses import JSONResponse
from typing import Awaitable, Callable
from f1_api.prodivers.logger import get_logger

logger = get_logger()


async def exception_handler_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Middleware to handle exceptions and return JSON responses.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception(f"Exception: {request.method} {request.url.path} - {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."},
        )
