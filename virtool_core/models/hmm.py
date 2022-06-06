from typing import List, Dict

from pydantic import BaseModel, validator


class HMMMinimal(BaseModel):
    id: str
    cluster: int
    count: int
    families: Dict[str, int]
    name: List[str]

    @validator("name")
    def is_name_valid(cls, name: List[str]) -> List[str]:
        if len(name) > 3:
            raise ValueError("The length of name should be a maximum of 3")
        return name


class HMMSequenceEntry(BaseModel):
    accession: str
    gi: str
    name: str
    organism: str


class HMM(HMMMinimal):
    entries: List[HMMSequenceEntry]
    genera: Dict[str, int]
    hidden: bool
    length: int
    mean_entropy: float
    total_entropy: float
