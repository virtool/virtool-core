from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

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
    job: JobMinimal | None
    labels: list[LabelNested]
    library_type: LibraryType
    notes: str
    nuvs: bool | str
    pathoscope: bool | str
    ready: bool
    user: UserNested
    workflows: SampleWorkflows


class Quality(BaseModel):
    bases: list[list[int | float]]
    composition: list[list[int | float]]
    count: int
    encoding: str
    gc: int | float
    length: list[int]
    sequences: list[int]


class Read(BaseModel):
    download_url: str
    id: int
    name: str
    name_on_disk: str
    sample: str
    size: int
    upload: Upload | None
    uploaded_at: datetime


class Sample(SampleMinimal):
    all_read: bool
    all_write: bool
    artifacts: list
    format: str
    group: int | str | None
    group_read: bool
    group_write: bool
    hold: bool
    is_legacy: bool
    locale: str
    paired: bool
    quality: Quality | None
    reads: list[Read]
    subtractions: list[SubtractionNested]


class SampleSearchResult(SearchResult):
    documents: list[SampleMinimal]
