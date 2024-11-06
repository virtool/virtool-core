import asyncio
from pathlib import Path
from typing import AsyncIterable

COMPLEMENT_TABLE = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}

#: A standard translation table, including ambiguity.
TRANSLATION_TABLE = {
    "TTT": "F",
    "TTC": "F",
    "TTA": "L",
    "TTG": "L",
    "CTT": "L",
    "CTC": "L",
    "CTA": "L",
    "CTG": "L",
    "CTN": "L",
    "ATT": "I",
    "ATC": "I",
    "ATA": "I",
    "ATG": "M",
    "GTT": "V",
    "GTC": "V",
    "GTA": "V",
    "GTG": "V",
    "GTN": "V",
    "TCT": "S",
    "TCC": "S",
    "TCA": "S",
    "TCG": "S",
    "TCN": "S",
    "AGT": "S",
    "AGC": "S",
    "CCT": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CCN": "P",
    "ACT": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "ACN": "T",
    "GCT": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "GCN": "A",
    "TAT": "Y",
    "TAC": "Y",
    "TAA": "*",
    "TAG": "*",
    "TGA": "*",
    "CAT": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "AAT": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "GAT": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "TGT": "C",
    "TGC": "C",
    "TGG": "W",
    "CGT": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "CGN": "R",
    "AGA": "R",
    "AGG": "R",
    "GGT": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
    "GGN": "G",
}


def read_fasta(path: Path) -> list[tuple[str, str]]:
    """Parse the FASTA file at `path` and return its content as a
    `list` of tuples containing the header and sequence.

    :param path: the path to the FASTA file
    :return: the FASTA content

    """
    if str(path)[-3:] != ".fa":
        raise OSError("Invalid FASTA file")

    data = []

    with open(path) as f:
        header = None
        seq: list[str] = []

        for line in f:
            if line[0] == ">":
                if header:
                    data.append((header, "".join(seq)))

                header = line.rstrip().replace(">", "")
                seq = []
                continue

            if header:
                seq.append(line.rstrip())
                continue

            raise OSError(f"Illegal FASTA line: {line}")

        if header:
            data.append((header, "".join(seq)))

    return data


async def read_fastq_from_path(path: Path) -> AsyncIterable:
    """Read the FASTQ file at `path` and yields its content as tuples.

    Accepts both uncompressed and GZIP-compressed FASTQ
    files.

    :param path: the path to the FASTQ File
    :return: tuples containing the header, sequence, and quality

    """
    q: asyncio.Queue[tuple[str, str, str] | None] = asyncio.Queue()

    def func(path_: Path, q_: asyncio.Queue):
        had_plus = False
        header = None
        seq = None

        with open(path_) as f:
            for line in f:
                if line == "+\n":
                    had_plus = True
                    continue

                if not had_plus:
                    if line[0] == "@":
                        header = line.rstrip()
                        continue

                    seq = line.rstrip()
                    continue

                if had_plus:
                    q_.put_nowait((header, seq, line.rstrip()))

                    header = None
                    seq = None
                    had_plus = False

            q_.put_nowait(None)

    task = asyncio.create_task(asyncio.to_thread(func, path, q))

    while True:
        item = await q.get()

        if item is None:
            q.task_done()
            break

        yield item
        q.task_done()

    await task
    await q.join()


async def read_fastq_headers(path: Path) -> list[str]:
    """Return a list of FASTQ headers for the FASTQ file located at `path`.
    Only accepts uncompressed FASTQ files.

    :param path: the path to the FASTQ file
    :return: a list of FASTQ headers

    """

    def func(path_: Path) -> list[str]:
        had_plus = False
        headers = []

        with open(path_) as f:
            for line in f:
                if line == "+\n":
                    had_plus = True
                    continue

                if not had_plus and line[0] == "@":
                    headers.append(line.rstrip())
                    continue

                if had_plus:
                    had_plus = False

        return headers

    return await asyncio.to_thread(func, path)


def reverse_complement(sequence: str) -> str:
    """Calculate the reverse complement of the passed `sequence`.

    :param sequence: the sequence to transform
    :return: the reverse complement
    """
    complement = [COMPLEMENT_TABLE[s] for s in sequence.upper()]
    complement.reverse()

    return "".join(complement)


def translate(sequence: str) -> str:
    """Translate the passed nucleotide sequence to protein.
    Substitutes _X_ for invalid codons.

    :param sequence: the nucleotide sequence
    :return: a translated protein sequence

    """
    sequence = sequence.upper()

    protein = []

    for i in range(len(sequence) // 3):
        codon = sequence[i * 3 : (i + 1) * 3]

        # Translate to X if the codon matches no amino acid
        # (taking into account ambiguous codons where possible)
        protein.append(TRANSLATION_TABLE.get(codon, "X"))

    return "".join(protein)


def find_orfs(sequence: str) -> list[dict]:
    """Return all ORFs for the nucelotide sequence.
    No ORFs will be returned for sequences shorter than 300 bp
    Only ORFs 100 residues long or greater will be returned.

    :param sequence:
    :return: a list of ORFs and metadata
    """
    orfs = []

    sequence_length = len(sequence)

    # Only look for ORFs if the contig is at least 300 nucleotides long.
    if sequence_length > 300:
        # Looks at both forward (+) and reverse (-) strands.
        for strand, nuc in [(+1, sequence), (-1, reverse_complement(sequence))]:
            # Look in all three translation frames.
            for frame in range(3):
                translation = translate(nuc[frame:])
                translation_length = len(translation)

                aa_start = 0

                # Extract ORFs.
                while aa_start < translation_length:
                    aa_end = translation.find("*", aa_start)

                    if aa_end == -1:
                        aa_end = translation_length
                    if aa_end - aa_start >= 100:
                        if strand == 1:
                            start = frame + aa_start * 3
                            end = min(sequence_length, frame + aa_end * 3 + 3)
                        else:
                            start = sequence_length - frame - aa_end * 3 - 3
                            end = sequence_length - frame - aa_start * 3

                        orfs.append(
                            {
                                "pro": str(translation[aa_start:aa_end]),
                                "nuc": str(nuc[start:end]),
                                "frame": frame,
                                "strand": strand,
                                "pos": (start, end),
                            },
                        )

                    aa_start = aa_end + 1

    return orfs
