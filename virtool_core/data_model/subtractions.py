from abc import ABC
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NucleotideComposition:
    """
    The nucleotide composition for a sequence.

    https://en.wikipedia.org/wiki/Nucleic_acid_notation

    :param a: The proportion of adenine (A) bases in the sequence
    :param c: The proportion of cytosine (C) bases in the sequence
    :param g: The proportion of guanine (G) bases in the sequence
    :param t: The proportion of thymine (T) bases in the sequence
    :param n: The proportion of undetermined (N) bases in the sequence.
    """
    a: float = 0.0
    c: float = 0.0
    g: float = 0.0
    t: float = 0.0
    n: float = 0.0


@dataclass
class Subtraction(ABC):
    """
    A reference genome and mapping index.

    Subtractions can be used to eliminate reads from analyses.

    :param id: The unique database ID for the subtraction
    :param name: The name of the subtraction
    :param nickname: A user-defined nickname for the subtraction
    :param count: The number of distinct sequences in the dataset
    :param gc: The nucleotide composition
    :param path: The working directory for the subtraction
    """

    id: str
    name: str
    nickname: str
    count: int
    gc: NucleotideComposition
    path: Path

    @property
    def fasta_path(self) -> Path:
        """
        The path in the running workflow's work_path to the
        GZIP-compressed FASTA file for the subtraction.

        eg. ``<work_path>/subtractions/<id>/subtraction.fa.gz``

        :type Path:
        """
        return self.path / "subtraction.fa.gz"

    @property
    def bowtie2_index_path(self) -> str:
        """
        The bowtie2 prefix.

        This is passed to `bowtie2` to reference the files:

            - ``<work_path>/subtractions/<id>/subtraction.1.bt2``
            - ``<work_path>/subtractions/<id>/subtraction.2.bt2``
            - ``<work_path>/subtractions/<id>/subtraction.3.bt2``
            - ``<work_path>/subtractions/<id>/subtraction.4.bt2``
            - ``<work_path>/subtractions/<id>/subtraction.rev.1.bt2``
            - ``<work_path>/subtractions/<id>/subtraction.rev.2.bt2``

        :type str:
        """
        return self.path / "subtraction"
