from fastapi import Request, Response
from starlette.responses import JSONResponse
from typing import Awaitable, Callable
from f1_api.prodivers.logger import get_logger

logger = get_logger()


async def exception_handler_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """
    Middleware to catch unhandled exceptions and log structured info.
    """
    try:
        return await call_next(request)

    except Exception as e:
        client_ip = request.client.host if request.client else None
        request_id = request.headers.get("X-Request-ID")
        route_name = getattr(request.scope.get("endpoint"), "__name__", None)

        logger.exception(
            "unhandled_exception",
            method=request.method,
            path=request.url.path,
            route_name=route_name,
            error_type=type(e).__name__,
            client_ip=client_ip,
            request_id=request_id,
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."},
        )
