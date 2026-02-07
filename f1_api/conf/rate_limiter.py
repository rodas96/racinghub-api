from pydantic_settings import BaseSettings


class RateLimiterSettings(BaseSettings):
    rate_limit_free_limit: int = 100
    rate_limit_free_window: int = 60
