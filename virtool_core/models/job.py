from datetime import datetime
from typing import List, Dict, Any, Optional

from virtool_core.models.user import UserMinimal, UserNested
from virtool_core.models.basemodel import BaseModel


class JobError(BaseModel):
    details: List[str]
    traceback: List[str]
    type: str


class JobStatus(BaseModel):
    error: Optional[JobError] = None
    progress: int
    stage: Optional[str] = None
    state: str
    step_description: Optional[str] = None
    step_name: Optional[str] = None
    timestamp: datetime


class JobNested(BaseModel):
    id: str


class JobMinimal(JobNested):
    archived: bool
    created_at: datetime
    progress: int
    stage: str
    state: str
    user: UserNested
    workflow: str


class Job(JobMinimal):
    acquired: bool = False
    args: Dict[str, Any]
    rights: Dict
    status: List[JobStatus]
