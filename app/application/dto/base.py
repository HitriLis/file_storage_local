from typing import Generic, List, Optional, TypeVar, Annotated
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResult(BaseModel, Generic[T]):
    data: Annotated[List[T], Field(description="Список элементов на текущей странице")]
    page: int = Field(..., description="Текущая страница")
    total_pages: Optional[int] = Field(None, description="Общее количество страниц")
    next_page: Optional[int] = Field(None, description="Номер следующей страницы, если есть")
    prev_page: Optional[int] = Field(None, description="Номер предыдущей страницы, если есть")

    @classmethod
    def create(cls, data: List[T], total: int, page: int, page_size: int):
        total_pages = (total + page_size - 1) // page_size
        return cls(
            data=data,
            page=page,
            total_pages=total_pages,
            next_page=page + 1 if page < total_pages else None,
            prev_page=page - 1 if page > 1 else None
        )