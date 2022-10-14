from datetime import datetime
from typing import Optional, Dict

from virtool_core.models.task import TaskNested


class NuvsBlast:
    id: int
    created_at: datetime
    updated_at: datetime
    last_checked_at: datetime
    error: Optional[str]
    rid: Optional[int]
    ready: bool = False
    result: Optional[Dict]
    task: Optional[TaskNested]
