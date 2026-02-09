from f1_api.conf.rate_limiter import RateLimiterSettings
from .logger import LoggerSettings
from .db import DatabaseSettings
from .cache import CacheSettings


class Settings(DatabaseSettings, CacheSettings, LoggerSettings, RateLimiterSettings):
    env: str = "dev"
