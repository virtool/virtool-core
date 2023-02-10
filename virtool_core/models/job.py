from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user import UserNested


class JobError(BaseModel):
    details: List[str]
    traceback: List[str]
    type: str


class JobPing(BaseModel):
    pinged_at: datetime


class JobState(Enum):
    CANCELLED = "cancelled"
    COMPLETE = "complete"
    ERROR = "error"
    PREPARING = "preparing"
    RUNNING = "running"
    TIMEOUT = "timeout"
    TERMINATED = "terminated"
    WAITING = "waiting"


class JobStatus(BaseModel):
    error: Optional[JobError] = None
    progress: int
    stage: Optional[str] = None
    state: JobState
    step_description: Optional[str] = None
    step_name: Optional[str] = None
    timestamp: datetime


class JobNested(BaseModel):
    id: str


class JobMinimal(JobNested):
    archived: bool
    created_at: datetime
    progress: int
    stage: Optional[str]
    state: JobState
    user: UserNested
    workflow: str


class Job(JobMinimal):
    acquired: bool = False
    args: Dict[str, Any]
    rights: Dict
    status: List[JobStatus]
    ping: Optional[JobPing]


class JobAcquired(Job):
    key: str


class JobSearchResult(SearchResult):
    counts: Dict
    documents: List[JobMinimal]
