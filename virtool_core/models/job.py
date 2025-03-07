from datetime import datetime
from enum import Enum
from typing import Any

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user_base import UserNested


class JobError(BaseModel):
    details: list[str]
    traceback: list[str]
    type: str


class JobPing(BaseModel):
    """A model for the ping status a job."""

    pinged_at: datetime
    """The time the job was last pinged."""


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
    """A model for a job status record."""

    error: JobError | None = None
    progress: int
    stage: str | None = None
    state: JobState
    step_description: str | None = None
    step_name: str | None = None
    timestamp: datetime


class JobNested(BaseModel):
    """A model for a job that is nested within another model."""

    id: str


class JobMinimal(JobNested):
    archived: bool
    """Whether the job has been archived."""

    created_at: datetime
    """The time the job was created."""

    progress: int
    """The progress of the job as a percentage from 0 to 100."""

    stage: str | None
    """The current stage of the job."""

    state: JobState
    """The current state of the job."""

    user: UserNested
    """The user that created the job."""

    workflow: str
    """The workflow that the job is associated with."""


class Job(JobMinimal):
    acquired: bool = False
    """Whether the job has been acquired by a worker."""

    args: dict[str, Any]
    """The arguments used to run the job."""

    status: list[JobStatus]
    """The status record of a job."""

    ping: JobPing | None
    """The ping status of a job.

    This is ``None`` until the job is acquired by a worker.
    """


class JobAcquired(Job):
    """A model for a job that has been acquired by a worker.

    This model includes the ``key`` field, which is only returned from the API once. It
    is used to prove the identity of the worker that acquired the job in future request.

    """

    key: str
    """A unique key that is used to prove the identity of the worker that acquired the
    job."""


class JobSearchResult(SearchResult):
    counts: dict
    documents: list[JobMinimal]
