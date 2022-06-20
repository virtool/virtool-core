from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel

from virtool_core.models.job import JobMinimal
from virtool_core.models.reference import ReferenceMinimal
from virtool_core.models.user import UserMinimal


class IndexMinimal(BaseModel):
    change_count: int
    created_at: datetime
    has_files: bool
    id: str
    job: JobMinimal
    modified_otu_count: int
    reference: ReferenceMinimal
    user: UserMinimal
    version: int


class IndexContributor(UserMinimal):
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
