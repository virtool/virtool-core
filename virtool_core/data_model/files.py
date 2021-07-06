from dataclasses import dataclass
from datetime import date
from typing import Literal

VirtoolFileFormat = Literal[
    "sam",
    "bam",
    "fasta",
    "fastq",
    "csv",
    "tsv",
    "json",
    "unknown",
]


@dataclass
class VirtoolFile:
    """
    Metadata for a file stored on the virtool server.

    :param id: A unique ID for the file
    :param name: The name of the file
    :param format: The format of the file
    :param name_on_disk: The name which the file is stored under
                         on the virtool server
    :param uploaded_at: A timestamp of when the file was uploaded to the server
    """
    id: int
    name: str
    size: int
    format: VirtoolFileFormat
    name_on_disk: str = None
    uploaded_at: date = None
