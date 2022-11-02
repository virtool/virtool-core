from datetime import datetime
from typing import Dict, Any, Optional

from virtool_core.models.basemodel import BaseModel


class TaskNested(BaseModel):
    id: int


class TaskDetailedNested(TaskNested):
    complete: bool
    created_at: datetime
    error: str = None
    progress: int
    step: Optional[str]
    type: str


class Task(TaskDetailedNested):
    context: Dict[str, Any]
    count: int
    file_size: int = None


TaskMinimal = Task
