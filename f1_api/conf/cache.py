from pydantic_settings import BaseSettings


class CacheSettings(BaseSettings):
    cache_enabled: bool = True
    cache_redis_host: str | None = "localhost"
    cache_redis_port: int = 6379

    cache_default_ttl: int = 300  # 5 minutes for memory cache
    cache_persistent_ttl: int = 3600  # 1 hour for persistent cache
