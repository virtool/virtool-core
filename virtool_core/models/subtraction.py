from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from virtool_core.models.searchresult import SearchResult
from virtool_core.models.upload import UploadMinimal
from virtool_core.models.user import UserMinimal


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
    id: int
    name: str


class SubtractionLinkedSample(BaseModel):
    id: str
    name: str


class SubtractionNested(BaseModel):
    id: str
    name: str


class SubtractionMinimal(SubtractionNested):
    """
    Minimal Subtraction model used for WebSocked messages and resource listings.
    """

    count: Optional[int] = None
    created_at: datetime
    file: Union[UploadMinimal, SubtractionUpload]
    has_file: bool
    nickname: str = ""
    ready: bool
    user: UserMinimal


class Subtraction(SubtractionMinimal):
    """
    Complete Subtraction model.
    """

    deleted: bool
    files: List[SubtractionFile]
    gc: Optional[NucleotideComposition]
    linked_samples: List[SubtractionLinkedSample]


class SubtractionSearchResult(SearchResult):
    ready_count: int
    documents: List[SubtractionMinimal]
