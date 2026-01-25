import time
from typing import Awaitable, Callable
from fastapi import Request, Response
from f1_api.prodivers.logger import get_logger

logger = get_logger()


async def process_time_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to log the time taken to process each request.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    if process_time > 0.8:
        logger.warning(f"SLOW: {request.method} {request.url.path} took {process_time:.4f} seconds")

    logger.info(f"{request.method} {request.url.path} completed in {process_time:.4f} seconds")

    return response
