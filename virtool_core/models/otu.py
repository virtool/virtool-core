from typing import List, Union, Optional

from pydantic import root_validator, Field, BaseModel as PydanticBaseModel

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import Molecule
from virtool_core.models.history import HistoryNested
from virtool_core.models.reference import ReferenceNested
from virtool_core.models.searchresult import SearchResult


class SequenceString(str):
    ALLOWED_CHARS = set('ATCGRYKM\n ')

    def __new__(cls, value):
        if not set(value).issubset(cls.ALLOWED_CHARS):
            raise ValueError("Invalid characters in the string. Only A, T, C, G, R, Y, K, and M are allowed.")

        return super().__new__(cls, value)

    def __add__(self, other):
        new_value = super().__add__(other)

        return SequenceString(new_value)


class OTUMinimal(BaseModel):
    abbreviation: str
    id: str
    name: str
    reference: ReferenceNested
    verified: bool
    version: int


class OTURemote(BaseModel):
    id: str


class OTUSequence(BaseModel):
    """
    A sequence nested in an OTU.

    It does not include a nested reference field as this is included in the parent OTU.
    """

    accession: str
    definition: str
    host: str
    id: str
    remote: Optional[OTURemote]
    segment: Optional[str]
    sequence: SequenceString
    target: Optional[str]


class Sequence(OTUSequence):
    """
    A complete sequence resource as returned for sequence API requests.
    """

    otu_id: str
    reference: ReferenceNested


class OTUIsolate(BaseModel):
    default: bool
    id: str
    sequences: List[OTUSequence]
    source_name: str
    source_type: str


class OTUSegment(BaseModel):
    molecule: Optional[Molecule]
    name: str
    required: bool

    @root_validator(pre=True)
    def make_molecule_nullable(cls, values):
        """
        Convert unset molecule fields from empty strings to ``None``.

        """
        if values["molecule"] == "":
            values["molecule"] = None

        return values


class OTU(OTUMinimal):
    isolates: List[OTUIsolate]
    issues: Optional[Union[dict, bool]]
    last_indexed_version: Optional[int]
    most_recent_change: HistoryNested
    otu_schema: List[OTUSegment] = Field(alias="schema")
    remote: Optional[OTURemote]


class OTUSearchResult(SearchResult):
    documents: List[OTUMinimal]
    modified_count: int
