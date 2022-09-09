from datetime import datetime
from typing import List, Optional, Any, Dict

from pydantic import root_validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.index import IndexNested
from virtool_core.models.job import JobNested
from virtool_core.models.reference import AnalysisReference
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.subtraction import SubtractionNested
from virtool_core.models.user import UserNested


class AnalysisSample(BaseModel):
    id: str


class AnalysisMinimal(BaseModel):
    created_at: datetime
    id: str
    index: IndexNested
    job: JobNested
    ready: bool
    reference: AnalysisReference
    sample: AnalysisSample
    subtractions: List[SubtractionNested]
    updated_at: datetime
    user: UserNested
    workflow: str

    @root_validator(pre=True)
    def check_updated_at(cls, values):
        if "updated_at" not in values:
            values["updated_at"] = values["created_at"]
        return values


class AnalysisFile(BaseModel):
    analysis: str
    description: Optional[str] = None
    format: str
    id: int
    name: str
    name_on_disk: str
    size: Optional[int]
    uploaded_at: Optional[datetime]


class Analysis(AnalysisMinimal):
    files: List[AnalysisFile]
    results: Optional[Dict[str, Any]]


class AnalysisSearchResult(SearchResult):
    documents: List[AnalysisMinimal]
