from datetime import datetime
from typing import Dict, Any

from virtool_core.models.basemodel import BaseModel


class Task(BaseModel):
    complete: bool
    context: Dict[str, Any]
    count: int
    created_at: datetime
    error: str = None
    file_size: int = None
    id: int
    progress: int
    step: str
    type: str


TaskMinimal = Task
