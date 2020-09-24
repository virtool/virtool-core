import os
import gzip
import tarfile
import shutil
import subprocess
import aiofiles
import arrow
import datetime
from typing import Union, Iterable
from random import choice
from string import ascii_letters, ascii_lowercase, digits


def ensure_data_dir(data_path):
    """
    Ensure the application data structure is correct. Fix it if it is broken.
    :param data_path: the path to create the data folder structure in

    """
    subdirectories = [
        "caches",
        "files",
        "references",
        "subtractions",
        "samples",
        "history",
        "hmm",
        "logs/jobs"
    ]

    for subdir in subdirectories:
        os.makedirs(os.path.join(data_path, subdir), exist_ok=True)


def random_alphanumeric(length: int = 6, mixed_case: bool = False, excluded: Union[None, Iterable[str]] = None) -> str:
    """
    Generates a random string composed of letters and numbers.
    :param length: the length of the string.
    :param mixed_case: included alpha characters will be mixed case instead of lowercase
    :param excluded: strings that may not be returned.
    :return: a random alphanumeric string.
    """
    excluded = set(excluded or list())

    characters = digits + (ascii_letters if mixed_case else ascii_lowercase)

    candidate = "".join([choice(characters) for _ in range(length)])

    if candidate not in excluded:
        return candidate

    return random_alphanumeric(length=length, excluded=excluded)


def should_use_pigz(processes: int) -> bool:
    """
    Decides whether pigz should be used for gzip decompression. If multiple processes are used and pigz is installed,
    the function evaluates true.

    :param processes: the number of processes to use for decompression
    :return: a boolean indicating if pigz should be used

    """
    return bool(processes > 1 and shutil.which("pigz"))


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


def decompress_file(path: str, target: str, processes: int = 1) -> None:
    """
    Decompress the gzip-compressed file at `path` to a `target` file.

    pigz will be used when multiple processes are allowed, otherwise gzip is used

    :param path: path to the compressed file to be decompressed
    :param target: path for the newly decompressed file to be stored
    :param processes: number of allowable processes for decompression

    """
    if should_use_pigz(processes):
        decompress_file_with_pigz(path, target, processes)
    else:
        decompress_file_with_gzip(path, target)


def decompress_file_with_gzip(path, target):
    """
    decompress a file using gzip

    :param path: path to the compressed file to be decompressed
    :param target: path for the newly decompressed file to be stored
    """
    with gzip.open(path, "rb") as f_in:
        with open(target, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def decompress_file_with_pigz(path: str, target: str, processes: int):
    """
    decompress a file using pigz

    :param path: path to the compressed file to be decompressed
    :param target: path for the newly decompressed file to be stored
    :param processes: the number of allowable processes for pigz (-p argument)
    """
    command = [
        "pigz",
        "-p", str(processes),
        "-d",
        "-k",
        "--stdout",
        path
    ]

    with open(target, "w") as f:
        subprocess.call(command, stdout=f)


def decompress_tgz(path: str, target: str):
    """
    Decompress the tar.gz file at ``path`` to the directory ``target``.

    :param path: the path to the tar.gz file.
    :param target: the path to directory into which to decompress the tar.gz file.

    """
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(target)
        
        
def file_stats(path: str) -> dict:
    """
    Return the size and last modification date for the file at `path`.
    Wraps :func:`os.stat`
    :param path: the file path
    :return: the file size and modification datetime
    """
    stats = os.stat(path)

    return {
        "size": stats.st_size,
        "modify": arrow.get(stats.st_mtime).datetime
    }


async def file_length(path: str) -> int:
    """
    Asynchronously determine length of a file

    :param path: path to file of which to compute the length
    :return: the length of the file in bytes
    """
    length = 0

    async with aiofiles.open(path) as f:
        async for _ in f:
            length += 1

    return length


def rm(path: str, recursive: bool = False) -> bool:
    """
    Remove files. Wraps :func:`os.remove` and func:`shutil.rmtree`.
    :param path: the path to remove
    :param recursive: the operation should recursively descend into dirs
    :return: a `bool` indicating if the operation was successful.
    """
    try:
        os.remove(path)
        return True
    except IsADirectoryError:
        if recursive:
            shutil.rmtree(path)
            return True
        raise


def is_gzipped(path: str) -> bool:
    """
    :param path: path of the file to check
    :return: True if the file is gzipped, else False
    """
    try:
        with gzip.open(path, "rb") as f:
            f.peek(1)
    except OSError as err:
        if "Not a gzipped file" in str(err):
            return False

    return True


def timestamp() -> datetime.datetime:
    """
    Returns a datetime object representing the current UTC time. The last 3 digits of the microsecond frame are set
    to zero.
    :return: a UTC timestamp
    """
    # Get tz-aware datetime object.
    dt = arrow.utcnow().naive

    # Set the last three ms digits to 0.
    dt = dt.replace(microsecond=int(str(dt.microsecond)[0:3] + "000"))

    return dt

