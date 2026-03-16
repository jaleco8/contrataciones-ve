from pydantic import BaseModel
from typing import Optional, List, Any


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_results: int
    total_pages: int
    sort: str
    order: str
    timezone: str = "UTC"
    interval_semantics: str = "[from,to)"
    request_id: Optional[str] = None


class PaginatedResponse(BaseModel):
    meta: PaginationMeta
    data: List[Any]
