from typing import Awaitable, Callable
from fastapi import Request, Response
from f1_api.prodivers.db import db_context, get_session


async def db_session_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Set database session in context for each request."""
    async with get_session() as session:
        db_context.set(session)
        response = await call_next(request)

    return response
