from pathlib import Path
import sys
from f1_api.settings import settings
from loguru import logger


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._setup_logger()
            Logger._initialized = True

    def _setup_logger(self) -> None:
        logger.remove()

        logger.add(sys.stdout, level=settings.log_level, colorize=True)

        if settings.env == "prod":
            log_dir = Path(settings.log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)

            logger.add(
                log_dir / "app.json",
                rotation="10 MB",
                retention="3 days",
                serialize=True,
                level=settings.log_level,
            )

    def get_logger(self):
        return logger


__logger_provider = Logger()


def get_logger():
    return __logger_provider.get_logger()
