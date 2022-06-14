from typing import Dict

from pydantic import BaseModel


class Task(BaseModel):
    complete: bool
    context: Dict[str, any]
    count: int
    created_at: str
    error: str = None
    file_size: int = None
    id: int
    progress: int
    step: str
    type: str


TaskMinimal = Task
