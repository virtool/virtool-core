from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING, Union

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.job import JobMinimal
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user import UserNested

if TYPE_CHECKING:
    from virtool_core.models.samples import SampleNested


class NucleotideComposition(BaseModel):
    a: float
    c: float
    g: float
    t: float
    n: float


class SubtractionFile(BaseModel):
    download_url: str
    id: int
    name: str
    size: int
    subtraction: str
    type: str


class SubtractionUpload(BaseModel):
    id: Union[int, str]
    name: str


class SubtractionNested(BaseModel):
    id: str
    name: str


class SubtractionMinimal(SubtractionNested):
    """
    Minimal Subtraction model used for websocket messages and resource listings.
    """

    count: Optional[int]
    created_at: datetime
    file: SubtractionUpload
    job: Optional[JobMinimal]
    nickname: str
    ready: bool
    user: Optional[UserNested]


class Subtraction(SubtractionMinimal):
    """
    Complete Subtraction model.
    """

    files: List[SubtractionFile]
    gc: Optional[NucleotideComposition]
    linked_samples: List[SampleNested]


class SubtractionSearchResult(SearchResult):
    ready_count: int
    documents: List[SubtractionMinimal]
