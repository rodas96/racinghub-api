from fastapi import Request, Response
from typing import Callable, Awaitable
from f1_api.prodivers.rate_limiter import RateLimiter

limiter = RateLimiter()


async def rate_limiting_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    rate_info = await limiter.check_rate_limit(request)
    response = await call_next(request)

    response.headers["X-RateLimit-Limit"] = str(rate_info.limit)
    response.headers["X-RateLimit-Remaining"] = str(rate_info.remaining)
    response.headers["X-RateLimit-Reset"] = str(rate_info.window)

    return response
