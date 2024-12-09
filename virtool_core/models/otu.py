from typing import Any, Optional, Union

from pydantic import Field, model_validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import Molecule
from virtool_core.models.history import HistoryNested
from virtool_core.models.reference import ReferenceNested
from virtool_core.models.searchresult import SearchResult


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
    """A sequence nested in an OTU.

    It does not include a nested reference field as this is included in the parent OTU.
    """

    accession: str
    definition: str
    host: str | None = ""
    id: str
    remote: OTURemote | None = None
    segment: str | None = None
    sequence: str
    target: str | None = None


class Sequence(OTUSequence):
    """A complete sequence resource as returned for sequence API requests."""

    otu_id: str
    reference: ReferenceNested


class OTUIsolate(BaseModel):
    default: bool
    id: str
    sequences: list[OTUSequence]
    source_name: str
    source_type: str


class OTUSegment(BaseModel):
    molecule: Molecule | None = None
    name: str

    @model_validator(mode="before")
    def make_molecule_nullable(cls, values: dict[str, Any]):
        """Convert unset molecule fields from empty strings to ``None``."""
        if values["molecule"] == "":
            values["molecule"] = None

        return values


class OTU(OTUMinimal):
    isolates: list[OTUIsolate]
    issues: Optional[Union[dict, bool]]
    last_indexed_version: Optional[int]
    most_recent_change: HistoryNested
    otu_schema: list[OTUSegment] = Field(alias="schema")
    remote: Optional[OTURemote]


class OTUSearchResult(SearchResult):
    documents: list[OTUMinimal]
    modified_count: int
