from datetime import datetime
from typing import List, Dict

from virtool_core.models.user import UserMinimal
from virtool_core.models.basemodel import BaseModel


class JobError(BaseModel):
    details: List[str]
    traceback: List[str]
    type: str


class JobStatus(BaseModel):
    error: JobError = None
    progress: int
    stage: str = None
    state: str
    step_description: str = None
    step_name: str = None
    timestamp: datetime


class JobArgs(BaseModel):
    analysis_id: str
    index_id: str
    name: str = None
    sample_id: str
    username: str
    workflow: str


class JobNested(BaseModel):
    id: str


class JobMinimal(JobNested):
    archived: bool = False
    created_at: datetime
    progress: int
    rights: Dict
    stage: str
    state: str
    status: List[JobStatus]
    user: UserMinimal
    workflow: str


class Job(JobMinimal):
    acquired: bool = False
    args: JobArgs
