import gzip
import shutil
import subprocess
from typing import List, Union

Number = Union[int, float]


# TODO: average_list is only used by virtool.jobs.fastQC. Consider inlining this function there
def average_list(list1: List[Number], list2: List[Number]) -> List[Number]:
    """compute the average value at each index between two lists"""

    if len(list1) != len(list2):
        raise TypeError("Both arguments must be lists of the same length")

    return [(value + list2[i]) / 2 for i, value in enumerate(list1)]


# TODO: consider moving this function to virtool-core.db.mongo.py
def base_processor(document: Union[dict, None]) -> Union[dict, None]:
    """
    Converts a document `dict` returned from MongoDB into a `dict` that can be passed into a JSON response. Removes the
    '_id' key and reassigns it to `id`.

    :param document: the document to process
    :return: processed document

    """
    if document is None:
        return None

    document = dict(document)

    if "id" in document:
        document["id"] = document.pop("_id")

    return document


def should_use_pigz(processes: int) -> bool:
    """
    Decides whether pigz should be used for gzip decompression. If multiple processes are used and pigz is installed,
    the function evaluates true.

    :param processes: the number of processes to use for decompression
    :return: a boolean indicating if pigz should be used

    """
    return processes > 1 and shutil.which("pigz")


def compress_file(path: str, target: str, processes: int = 1) -> None:
    """
    Compress the file at `path` to a gzipped file at `target`.

    :param path: the path of the file to be compressed
    :param target: path where the compressed file should be saved
    :param processes: the number of processes available for compression
    """
    if should_use_pigz(processes):
        compress_file_with_pigz(path, target, processes)
    else:
        compress_file_with_gzip(path, target)


def compress_file_with_gzip(path: str, target: str) -> None:
    """
    compresses a file using gzip
    :param path: path to the file to be compressed
    :param target: path where the compressed file should be stored
    """
    with open(path, "rb") as f_in:
        with gzip.open(target, "wb", compresslevel=6) as f_out:
            shutil.copyfileobj(f_in, f_out)


def compress_file_with_pigz(path: str, target: str, processes: int):
    """
    use pigz to compress a file
    :param path: path to the file to be compressed
    :param target: path where the compressed file should be stored
    :param processes: number of processes allowable for pigz (-p argument)
    """
    command = [
        "pigz",
        "-p", str(processes),
        "-k",
        "--stdout",
        path
    ]

    with open(target, "wb") as f:
        subprocess.call(command, stdout=f)

