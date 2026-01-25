from .db import DatabaseSettings
from .cache import CacheSettings


class Settings(DatabaseSettings, CacheSettings):
    project_name: str = "f1_api"
    debug: bool = False
