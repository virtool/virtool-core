from dataclasses import dataclass, field
from typing import List, Optional

from pathlib import Path
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
    :param path: The directory containing the sequencing data files

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
    path: Path = None

    @property
    def left(self):
        """
        The seqencing data for the sample.

        If the sample is paired, this is the first of two
        compressed fasta files for the sample. Otherwise it
        is the only fasta file.
        """
        return self.path / "reads_1.fq.gz"

    @property
    def right(self):
        """
        The second compressed fasta file containing the sequencing data.

        :return: The path to a compressed fasta file, or None if sample
                 is not paired.
        """
        if not self.paired:
            return None
        return self.path / "reads_2.fq.gz"

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
