from datetime import datetime
from enum import Enum
from typing import List, Any

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
    error: JobError | None = None
    progress: int
    stage: str | None = None
    state: JobState
    step_description: str | None = None
    step_name: str | None = None
    timestamp: datetime


class JobNested(BaseModel):
    id: str


class JobMinimal(JobNested):
    archived: bool
    created_at: datetime
    progress: int
    stage: str | None
    state: JobState
    user: UserNested
    workflow: str


class Job(JobMinimal):
    acquired: bool = False
    args: dict[str, Any]
    rights: dict
    status: List[JobStatus]
    ping: JobPing | None


class JobAcquired(Job):
    key: str


class JobSearchResult(SearchResult):
    counts: dict
    documents: List[JobMinimal]
