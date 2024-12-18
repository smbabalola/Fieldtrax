# app/core/pagination.py
from typing import Generic, Sequence, TypeVar
from uuid import UUID
from pydantic import BaseModel
from fastapi import Query

T = TypeVar("T")

class Params:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(20, ge=1, le=100, description="Items per page")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size
        self.limit = size

class Page(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    size: int

    @property
    def pages(self) -> int:
        return (self.total + self.size - 1) // self.size

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1