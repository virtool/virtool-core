from typing import Union

from pydantic import BaseModel, Field
from datetime import datetime
from virtool_core.utils import timestamp


class SubtractionFile(BaseModel):
    id: int
    name: str


class SubtractionMinimal(BaseModel):
    count: int
    created_at: datetime = Field(default_factory=timestamp)
    file: SubtractionFile
    has_file: bool
    id: str
    name: str
    nickname: str
    ready: bool = Field(default=False)
    user: Union[str, dict]


class Subtraction(SubtractionMinimal):
    deleted: bool = Field(default=False)







def test_subtraction():
    model = SubtractionMinimal(count=1, file={
        "id": 642,
        "name": "Apis_mellifera.Amel_HAv3.1.dna.toplevel.fa.gz"
    }, has_file=True, id="8dplz705", ready=True, name="Apis", nickname="common", user={
        "administrator": True,
        "handle": "mrott",
        "id": "ihvze2u9"
    })
    pass
