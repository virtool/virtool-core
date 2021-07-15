from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field, validator
from virtool_core.utils import timestamp


class Analysis(BaseModel):
    _id: str
    job: Union[str, dict]
    reference: Union[str, dict]
    sample: Union[str, dict]
    subtraction: Union[str, dict]
    user: Union[str, dict]
    cache: Union[str, dict]
    index: Union[str, dict]
    workflow: str
    quality: dict = None
    results: dict = None
    ready: bool = False
    created_at: datetime = Field(default_factory=timestamp)
    updated_at: datetime = Field(default_factory=timestamp)

    @validator(
        "job", 
        "sample", 
        "reference", 
        "subtraction",
        "user",
        "cache",
        "index",
        allow_reuse=True
    )
    def correct_dict_structure(cls, value):
        if isinstance(value, str):
            return {
                "id": value
            }

        assert "id" in value

        return value
