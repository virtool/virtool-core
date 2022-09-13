from datetime import datetime
from typing import List, Dict

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.job import JobMinimal
from virtool_core.models.reference import ReferenceMinimal
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user import UserNested


class IndexNested(BaseModel):
    id: str
    version: int


class IndexMinimal(IndexNested):
    change_count: int
    created_at: datetime
    has_files: bool
    job: JobMinimal
    modified_otu_count: int
    reference: ReferenceMinimal
    user: UserNested


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
    size: int
    type: str


class Index(IndexMinimal):
    contributors: List[IndexContributor]
    files: List[IndexFile]
    manifest: Dict[str, int]
    otus: List[IndexOTU]
    ready: bool


class IndexSearchResult(SearchResult):
    documents: List[IndexMinimal]
    modified_otu_count: int
    total_otu_count: int
