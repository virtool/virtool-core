from typing import List

from pydantic import BaseModel, Field
from datetime import datetime
from virtool_core.utils import timestamp
from virtool_core.models import UserMinimal


class NucleotideComposition(BaseModel):
    a: float = Field(default=0.0)
    c: float = Field(default=0.0)
    g: float = Field(default=0.0)
    t: float = Field(default=0.0)
    n: float = Field(default=0.0)


class SubtractionFile(BaseModel):
    download_url: str
    id: int
    name: str
    size: int
    subtraction: str
    type: str


class SubtractionUpload(BaseModel):
    id: int
    name: str


class SubtractionLinkedSample(BaseModel):
    id: str
    name: str


class SubtractionMinimal(BaseModel):
    """
    Minimal Subtraction model used for WebSocked messages and resource listings.
    """
    count: int
    created_at: datetime = Field(default_factory=timestamp)
    file: SubtractionUpload
    has_file: bool = Field(default=False)
    id: str
    name: str
    nickname: str
    ready: bool = Field(default=False)
    user: UserMinimal


class Subtraction(SubtractionMinimal):
    """
    Complete Subtraction model.
    """
    deleted: bool = Field(default=False)
    linked_samples: List[SubtractionLinkedSample]
    files: List[SubtractionFile]
    gc: NucleotideComposition
