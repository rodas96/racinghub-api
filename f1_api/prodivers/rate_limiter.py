from dataclasses import dataclass
import hashlib
import time
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
        data = await cache.get(key)

        current_time = int(time.time())

        if data is None:
            current = 1
            reset_time = current_time + window
            await cache.set(key, {"count": current, "reset": reset_time}, ttl=window)
        else:
            reset_time = data["reset"]
            if current_time >= reset_time:
                current = 1
                reset_time = current_time + window
                await cache.set(key, {"count": current, "reset": reset_time}, ttl=window)
            else:
                current = data["count"] + 1
                await cache.set(key, {"count": current, "reset": reset_time}, ttl=window)

        if current > limit:
            retry_after = max(1, reset_time - current_time)

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "tier": tier.value,
                    "limit": limit,
                    "window": window,
                    "retry_after": retry_after,
                },
                headers={"Retry-After": str(retry_after)},
            )

        return RateLimitInfo(
            tier=tier.value,
            limit=limit,
            remaining=limit - current,
            window=window,
        )

    def _get_identifier(self, request: Request) -> str:
        if xff := request.headers.get("x-forwarded-for"):
            return xff.split(",")[0].strip()
        elif request.client:
            return request.client.host
        else:
            return hashlib.sha256(str(request.scope).encode()).hexdigest()
