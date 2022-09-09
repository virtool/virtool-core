import enum
from datetime import datetime
from typing import List, Any

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.task import Task
from virtool_core.models.user import UserNested


class ReferenceClonedFrom(BaseModel):
    id: str
    name: str


class ReferenceDataType(str, enum.Enum):
    barcode = "barcode"
    genome = "genome"


class ReferenceUser(UserNested):
    count: int
    build: bool
    created_at: datetime
    modify: bool
    modify_otu: bool
    remove: bool


class ReferenceRemotesFrom(BaseModel):
    errors: List[Any]
    slug: str


class ReferenceInstalled(BaseModel):
    body: str
    created_at: datetime
    filename: str
    html_url: str
    id: int
    name: str
    newer: bool
    published_at: datetime
    ready: bool
    size: int
    user: UserNested


class ReferenceRelease(BaseModel):
    body: str
    content_type: str
    download_url: str
    etag: str
    filename: str
    html_url: str
    id: int
    name: str
    newer: bool
    published_at: datetime
    retrieved_at: datetime
    size: int


class ReferenceBuild(BaseModel):
    created_at: datetime
    id: str
    version: int
    user: UserNested
    has_json: bool


class ReferenceNested(BaseModel):
    id: str


class AnalysisReference(ReferenceNested):
    name: str


class ReferenceMinimal(AnalysisReference):
    cloned_from: ReferenceClonedFrom = None
    created_at: datetime
    data_type: ReferenceDataType
    groups: List[ReferenceUser]
    installed: ReferenceInstalled = None
    internal_control: str
    latest_build: ReferenceBuild
    organism: str
    otu_count: int
    release: ReferenceRelease = None
    remotes_from: ReferenceRemotesFrom = None
    task: Task
    updating: bool = None
    unbuilt_change_count: int
    user: UserNested
    users: List[ReferenceUser]


class Reference(ReferenceMinimal):
    contributors: List[ReferenceUser]
    description: str
    restrict_source_types: bool
    source_types: List[str]


class ReferenceSearchResult(SearchResult):
    documents: List[ReferenceMinimal]
    official_installed: bool
