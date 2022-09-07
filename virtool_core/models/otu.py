from datetime import datetime
from typing import List, Union, Optional

from pydantic import root_validator, Field

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import Molecule
from virtool_core.models.history import HistoryMinimal
from virtool_core.models.reference import ReferenceMinimal
from virtool_core.models.user import UserMinimal


class OTUMinimal(BaseModel):
    abbreviation: str
    id: str
    name: str
    reference: ReferenceMinimal
    verified: bool
    version: int


class OTURemote(BaseModel):
    id: str


class OTUSequence(BaseModel):
    accession: str
    definition: str
    host: str
    id: str
    reference: ReferenceMinimal
    remote: OTURemote
    segment: str
    sequence: str


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
    created_at: datetime
    imported: bool
    isolates: List[OTUIsolate]
    issues: Optional[Union[dict, bool]] = None
    last_indexed_version: Optional[int] = None
    most_recent_change: Optional[HistoryMinimal] = None
    remote_id: OTURemote
    otu_schema: List[OTUSegment] = Field(alias="schema")
    user: UserMinimal
