from typing import Optional

from pydantic import validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.otu import SequenceString

VALID_SEQUENCE = frozenset("cagntCAGNT")


class Genbank(BaseModel):
    accession: str
    definition: str
    host: str
    sequence: SequenceString

    @validator("sequence")
    def check_sequence(cls, sequence: Optional[SequenceString]) -> str:
        """
        Checks if the given sequence is valid.
        """
        if not set(sequence) <= VALID_SEQUENCE:
            raise ValueError("The format of the sequence is invalid")

        return sequence.upper()
