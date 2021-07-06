from dataclasses import dataclass, field
from typing import List

from virtool_workflow.data_model.references import Reference


@dataclass
class Isolate:
    """
    An isolate for an OTU.

    :param id: A unique ID for the isolate
    :param source_name: The identifying part of the the identifying
                        part of the isolate name (eg. Canada-1)
    :param source_type: The common first part of the isolate name (eg. Isolate)
    """
    id: str
    source_name: str
    source_type: str


@dataclass
class Segment:
    """
    An OTU segment.

    :param molecule: The genome nucleic acid class (eg. dsRNA)
    :param name: The display name for the segment
    :param required: A flag indicating that the segment is required
                     for an isolate to pass validation
    """
    molecule: str
    name: str
    required: bool


@dataclass
class OTU:
    """
    An Organizational Taxonomic Unit.

    Usually represents virus species, but can be used for other organisms.

    :param id: A unique ID for the OTU
    :param name: The display name of the OTU
    :param abbreviation: The abbreviated name of the OTU
    :param isolates: The list of isolates
    :param reference: The parent reference
    :param version: The current OTU version number
    :param schema: List of segments which should be contained in
                   isolates of the OTU
    :param verifed: A flag indicating that the OTU has been validated
    """
    id: str
    name: str
    abbreviation: str
    isolates: List[Isolate]
    reference: Reference
    version: int
    schema: List[Segment] = field(default_factory=lambda: [])
    verified: bool = False

    @property
    def lower_name(self) -> str:
        """The OTU name in lower case."""
        return self.name.lower()
