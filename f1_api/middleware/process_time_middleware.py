import time
from typing import Awaitable, Callable
from fastapi import Request, Response


async def process_time_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to log the time taken to process each request.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(end_time)

    return response
