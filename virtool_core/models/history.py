from datetime import datetime
from typing import Any, List

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import HistoryMethod
from virtool_core.models.reference import ReferenceNested
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user import UserMinimal


class HistoryIndex(BaseModel):
    id: str
    version: int


class HistoryOTU(BaseModel):
    id: str
    name: str
    version: str


class HistoryMinimal(BaseModel):
    created_at: datetime
    description: str
    id: str
    index: HistoryIndex
    method_name: HistoryMethod
    otu: HistoryOTU
    reference: ReferenceNested
    user: UserMinimal


class History(HistoryMinimal):
    diff: Any


class HistorySearchResult(SearchResult):
    documents: List[HistoryMinimal]
