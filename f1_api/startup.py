from fastapi import APIRouter, FastAPI
from f1_api.factories.router_factory import RouterFactory
from f1_api.settings import settings, Settings
from f1_api.middleware.db_session_middleware import db_session_middleware
from f1_api.middleware.cors_middleware import add_cors_middleware
from importlib.metadata import version, PackageNotFoundError
from f1_api.middleware.security_headers_middleware import security_headers_middleware
from f1_api.middleware.process_time_middleware import process_time_middleware
from f1_api.middleware.exception_handler_middleware import exception_handler_middleware

factory = RouterFactory()


def add_routers(app: FastAPI) -> list[APIRouter]:
    routers = factory.build_routers()
    for router in routers:
        app.include_router(router=router, prefix="/api/v" + get_major_version())

    return routers


def get_settings() -> Settings:
    return settings


def get_version() -> str:
    v = version("f1_api")
    if not v:
        raise PackageNotFoundError("f1_api package not found cant determine version")

    return v


def get_major_version() -> str:
    version = get_version()
    major_version = version.split(".")[0]
    return major_version


def add_middlewares(app: FastAPI) -> None:
    add_cors_middleware(app)
    app.middleware("http")(security_headers_middleware)
    app.middleware("http")(exception_handler_middleware)
    app.middleware("http")(process_time_middleware)
    app.middleware("http")(db_session_middleware)
