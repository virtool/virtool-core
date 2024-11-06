from datetime import datetime

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.job import JobMinimal
from virtool_core.models.reference import ReferenceNested
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user_base import UserNested


class IndexNested(BaseModel):
    id: str
    version: int


class IndexMinimal(IndexNested):
    change_count: int
    created_at: datetime
    has_files: bool
    job: JobMinimal | None
    modified_otu_count: int
    reference: ReferenceNested
    user: UserNested
    ready: bool


class IndexContributor(UserNested):
    count: int


class IndexOTU(BaseModel):
    change_count: int
    id: str
    name: str


class IndexFile(BaseModel):
    download_url: str
    id: int
    index: str
    name: str
    size: int | None
    type: str


class Index(IndexMinimal):
    contributors: list[IndexContributor]
    files: list[IndexFile]
    manifest: dict[str, int]
    otus: list[IndexOTU]


class IndexSearchResult(SearchResult):
    documents: list[IndexMinimal]
    modified_otu_count: int
    total_otu_count: int
    change_count: int
