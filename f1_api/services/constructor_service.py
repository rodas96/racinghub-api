from typing import Sequence
from fastapi import HTTPException
from sqlalchemy import RowMapping
from f1_api.models.models import Constructor
from f1_api.repositories.constructor_repository import ConstructorRepository


class ConstructorService:
    def __init__(self, constructor_repository: ConstructorRepository):
        self._constructor_repository = constructor_repository

    async def get_constructors(self, skip: int, limit: int) -> tuple[Sequence[Constructor], int]:
        rows, total = await self._constructor_repository.get_constructors(offset=skip, limit=limit)

        return rows, total

    async def get_constructor(self, constructor_id: str) -> Constructor:
        return await self._get_existing_constructor(constructor_id=constructor_id)

    async def get_constructor_seasons(self, constructor_id: str) -> Sequence[RowMapping]:
        await self._get_existing_constructor(constructor_id=constructor_id)

        return await self._constructor_repository.get_constructor_seasons(constructor_id=constructor_id)

    async def _get_existing_constructor(self, constructor_id: str) -> Constructor:
        constructor = await self._constructor_repository.get_constructor(constructor_id=constructor_id)

        if not constructor:
            raise HTTPException(status_code=404, detail="Constructor not found")

        return constructor
