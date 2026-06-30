"""
Reusable pagination helper for list endpoints.
"""
import math
from dataclasses import dataclass
from sqlalchemy.orm import Query


@dataclass
class PaginationParams:
    page: int = 1
    page_size: int = 10

    def __post_init__(self):
        self.page = max(1, self.page)
        self.page_size = min(max(1, self.page_size), 100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def paginate(query: Query, params: PaginationParams) -> dict:
    """
    Apply pagination to a SQLAlchemy query.
    Returns a dict with items, total, page, page_size, total_pages.
    """
    total = query.count()
    items = query.offset(params.offset).limit(params.page_size).all()
    total_pages = math.ceil(total / params.page_size) if total > 0 else 0
    return {
        "items": items,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "total_pages": total_pages,
    }
