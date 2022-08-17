from datetime import datetime
from typing import List, Union, Optional

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import LibraryType
from virtool_core.models.label import LabelNested
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.subtraction import SubtractionNested
from virtool_core.models.upload import Upload
from virtool_core.models.user import UserMinimal


class SampleID(BaseModel):
    id: str


class SampleMinimal(SampleID):
    created_at: datetime
    host: str
    isolate: str
    labels: List[LabelNested]
    library_type: LibraryType
    name: str
    notes: str
    nuvs: bool
    pathoscope: bool
    ready: bool
    user: UserMinimal


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
