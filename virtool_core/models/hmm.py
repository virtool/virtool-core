from typing import List, Dict, Any

from pydantic import validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.searchresult import SearchResult


class HMMMinimal(BaseModel):
    id: str
    cluster: int
    count: int
    families: Dict[str, int]
    names: List[str]

    @validator("names")
    def is_name_valid(cls, names: List[str]) -> List[str]:
        if len(names) > 3:
            raise ValueError("The length of name should be a maximum of 3")

        return names


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


class HMMSearchResult(SearchResult):
    documents: List[HMMMinimal]
    status: Dict[str, Any]
