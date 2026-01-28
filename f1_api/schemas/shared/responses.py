from datetime import datetime
from typing import Generic
from annotated_types import T
from pydantic import BaseModel, Field


class PagedResponse(BaseModel, Generic[T]):
    data: list[T]
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool = Field(description="Whether there's a next page")
    has_previous: bool = Field(description="Whether there's a previous page")

    @classmethod
    def create(cls, data: list[T], page: int, limit: int, total: int) -> "PagedResponse[T]":
        total_pages = (total + limit - 1) // limit
        return cls(
            data=data,
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    cache: str
