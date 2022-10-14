from datetime import datetime
from typing import Optional, Dict

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.task import TaskNested


class NuvsBlast(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    last_checked_at: datetime
    error: Optional[str]
    rid: Optional[str]
    ready: bool = False
    result: Optional[Dict]
    task: Optional[TaskNested]
