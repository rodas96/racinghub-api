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
    try:
        print("VERSION:", version("f1_api"))
        return version("f1_api")
    except PackageNotFoundError:
        possible_paths = [
            Path(__file__).resolve().parent.parent / "pyproject.toml",
            Path("/app/pyproject.toml"),
        ]

        for pyproject in possible_paths:
            if pyproject.exists():
                with open(pyproject, "r") as f:
                    for line in f:
                        if line.startswith("version"):
                            return line.split("=")[1].strip().strip('"')

        raise RuntimeError("Version not found in pyproject.toml or package metadata")


def get_major_version() -> str:
    version = get_version()
    major_version = version.split(".")[0]
    return major_version


def add_middlewares(app: FastAPI) -> None:
    app.middleware("http")(db_session_middleware)
