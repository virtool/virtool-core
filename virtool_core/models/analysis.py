from datetime import datetime
from typing import List, Optional, Any, Dict

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.index import IndexNested
from virtool_core.models.job import JobNested
from virtool_core.models.reference import AnalysisReference
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.subtraction import SubtractionNested
from virtool_core.models.user import UserMinimal


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
    user: UserMinimal
    workflow: str


class AnalysisFile(BaseModel):
    analysis: str
    description: Optional[str] = None
    format: str
    id: int
    name: str
    name_on_disk: str
    size: int
    uploaded_at: datetime


class Analysis(AnalysisMinimal):
    files: List[AnalysisFile]
    results: Optional[Dict[str, Any]]


class AnalysisSearchResult(SearchResult):
    documents: List[AnalysisMinimal]
