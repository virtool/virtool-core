from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Union, TYPE_CHECKING, Optional


from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import LibraryType
from virtool_core.models.job import JobMinimal
from virtool_core.models.label import LabelNested
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.upload import Upload
from virtool_core.models.user import UserNested

if TYPE_CHECKING:
    from virtool_core.models.subtraction import SubtractionNested


class SampleID(BaseModel):
    id: str


class SampleNested(SampleID):
    name: str


class WorkflowState(Enum):
    COMPLETE = "complete"
    INCOMPATIBLE = "incompatible"
    NONE = "none"
    PENDING = "pending"


class SampleWorkflows(BaseModel):
    aodp: WorkflowState
    nuvs: WorkflowState
    pathoscope: WorkflowState


class SampleMinimal(SampleNested):
    created_at: datetime
    host: str
    isolate: str
    job: Optional[JobMinimal]
    labels: List[LabelNested]
    library_type: LibraryType
    notes: str
    nuvs: Union[bool, str]
    pathoscope: Union[bool, str]
    ready: bool
    user: UserNested
    workflows: SampleWorkflows


class Quality(BaseModel):
    bases: List[List[Union[int, float]]]
    composition: List[List[Union[int, float]]]
    count: int
    encoding: str
    gc: Union[int, float]
    length: List[int]
    sequences: List[int]


class Read(BaseModel):
    download_url: str
    id: int
    name: str
    name_on_disk: str
    sample: str
    size: int
    upload: Optional[Upload]
    uploaded_at: datetime


class Cache(BaseModel):
    created_at: datetime
    files: List
    id: str
    key: str
    legacy: bool
    missing: bool
    paired: bool
    quality: Quality
    ready: bool
    sample: SampleID


class Sample(SampleMinimal):
    all_read: bool
    all_write: bool
    artifacts: List
    caches: List[Cache]
    format: str
    group: str
    group_read: bool
    group_write: bool
    hold: bool
    is_legacy: bool
    locale: str
    paired: bool
    quality: Optional[Quality]
    reads: List[Read]
    subtractions: List[SubtractionNested]


class SampleSearchResult(SearchResult):
    documents: List[SampleMinimal]
