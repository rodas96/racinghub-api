from pathlib import Path
from fastapi import APIRouter, FastAPI
from f1_api.factories.router_factory import RouterFactory
from f1_api.settings import settings, Settings
from f1_api.middleware.db_session_middleware import db_session_middleware

from importlib.metadata import version, PackageNotFoundError

factory = RouterFactory()


def add_routers(app: FastAPI) -> list[APIRouter]:
    routers = factory.build_routers()
    for router in routers:
        app.include_router(router=router, prefix="/api/v" + get_major_version())

    return routers


def get_settings() -> Settings:
    return settings


def get_version() -> str:
    if not version:
        raise PackageNotFoundError("f1_api package not found cant determine version")
    return version("f1_api")


def get_major_version() -> str:
    version = get_version()
    major_version = version.split(".")[0]
    return major_version


def add_middlewares(app: FastAPI) -> None:
    app.middleware("http")(db_session_middleware)
