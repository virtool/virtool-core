from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Status:
    """
    A status update for a Virtool job.

    :param error: A string describing an error state, if an error occured
    :param progress: A float representing the current completion percentage
                     for the job. For example, a value of 0.4 would indicate
                     that the job is 40% complete
    :param stage: The current stage of the job
    :param state: The current state of the job
    :param timestamp: A timestamp for when this status update was created
    """
    error: str
    progress: float
    stage: str
    state: str
    timestamp: str


@dataclass
class Job:
    """
    A Virtool Job.

    :param id: Unique ID for the job
    :param args: A dictionary of arguments
    :param status: A list of :class:`Status` objects
    :param task: The name of the workflow which is used to
                 execute the job
    :param key: The authentication key to be used with Virtool's API
    """
    id: str
    args: dict
    status: List[Status] = field(default_factory=lambda: [])
    task: str = None
    key: str = None
