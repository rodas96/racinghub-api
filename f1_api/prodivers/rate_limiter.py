from dataclasses import dataclass
import hashlib
from fastapi import Request, HTTPException
from enum import Enum
from f1_api.settings import settings
from f1_api.prodivers.cache import get_cache


class RateLimitTier(Enum):
    FREE = "free"


@dataclass
class RateLimitInfo:
    tier: str
    limit: int
    remaining: int
    window: int


class RateLimiter:
    def __init__(self) -> None:
        self.tier_limits: dict[RateLimitTier, dict[str, int]] = {
            RateLimitTier.FREE: {
                "limit": settings.rate_limit_free_limit,
                "window": settings.rate_limit_free_window,
            },
        }

    async def check_rate_limit(self, request: Request) -> RateLimitInfo:
        tier = RateLimitTier.FREE
        config = self.tier_limits[tier]

        limit = config["limit"]
        window = config["window"]

        identifier = self._get_identifier(request)

        key = f"rate_limit:{tier.value}:{identifier}"

        cache = get_cache("persistent")

        current = await cache.increment(key)

        if current == 1:
            await cache.expire(key, window)

        if current > limit:
            ttl = await cache.ttl(key)

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "tier": tier.value,
                    "limit": limit,
                    "window": window,
                    "retry_after": ttl,
                },
                headers={"Retry-After": str(ttl)},
            )

        return RateLimitInfo(
            tier=tier.value,
            limit=limit,
            remaining=limit - current,
            window=window,
        )

    def _get_identifier(self, request: Request) -> str:
        if xff := request.headers.get("x-forwarded-for"):
            return xff
        elif request.client:
            return request.client.host
        else:
            return hashlib.sha256(str(request.scope).encode()).hexdigest()
