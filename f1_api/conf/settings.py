from .logger import LoggerSettings
from .db import DatabaseSettings
from .cache import CacheSettings


class Settings(DatabaseSettings, CacheSettings, LoggerSettings):
    project_name: str = "f1_api"
    debug: bool = False
    env: str = "dev"
