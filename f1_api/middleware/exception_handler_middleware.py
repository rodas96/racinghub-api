from fastapi import Request, Response
from starlette.responses import JSONResponse
from typing import Awaitable, Callable


async def exception_handler_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Middleware to handle exceptions and return JSON responses.
    """
    try:
        response = await call_next(request)
        return response
    except Exception:
        print("An unhandled exception occurred.")
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."},
        )
