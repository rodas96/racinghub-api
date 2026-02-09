import time
from typing import Awaitable, Callable
from fastapi import Request, Response
from f1_api.providers.logger import get_logger

logger = get_logger()


async def process_time_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response_ms = round(process_time * 1000, 2)

    response.headers["X-Process-Time"] = str(process_time)
    client_ip = request.client.host if request.client else None
    request_id = request.headers.get("X-Request-ID")
    route_name = getattr(request.scope.get("endpoint"), "__name__", None)
    status_code = getattr(response, "status_code", None)

    try:
        request_size = len(await request.body())
    except Exception:
        request_size = None
    response_size = len(response.body) if hasattr(response, "body") else None

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        route_name=route_name,
        status_code=status_code,
        process_time_ms=response_ms,
        client_ip=client_ip,
        request_id=request_id,
        request_size=request_size,
        response_size=response_size,
    )

    return response
