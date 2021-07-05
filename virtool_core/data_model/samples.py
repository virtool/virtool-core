from dataclasses import dataclass, field
from typing import List, Optional

from virtool_workflow.analysis.library_types import LibraryType


@dataclass
class Sample:
    """
    Sequencing data which can be used to run analyses

    :param id: A unique ID for the sample
    :param name: The name of the sample
    :param host: The host of orgin
    :param isolate: The identifer for the related isolate
    :param locale: The locale
    :param library_type: The library type
    :param paired: A flag indicating that the sample contains paired data
    :param quality: The parsed output of `FastQC`
    :param nuvs: A flag indicating that the sample has
                 a completed NuVs analysis
    :param pathoscope: A flag indicating that the sample has
                 a completed pathoscope analysis
    :param files: A list of files associated with the sample

    """
    id: str
    name: str
    host: str
    isolate: str
    locale: str
    library_type: LibraryType
    paired: bool
    quality: dict
    nuvs: bool = False
    pathoscope: bool = False
    files: List[dict] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.reads_path = None
        self.read_paths = None

    @property
    def min_length(self) -> Optional[int]:
        """
        The minimum observed read length in the sample sequencing data.

        Returns ``None`` if the sample is still being created and no quality data is available.

        """
        return self.quality["length"][0] if self.quality else None

    @property
    def max_length(self) -> Optional[int]:
        """
        The maximum observed read length in the sample sequencing data.

        Returns ``None`` if the sample is still being created and no quality data is available.

        """
        return self.quality["length"][1] if self.quality else None
