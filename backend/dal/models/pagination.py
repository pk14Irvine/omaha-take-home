from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationMeta(BaseModel):
    count: int
    page: int
    per_page: int

class PaginationWrapper(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta
