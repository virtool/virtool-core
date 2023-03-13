import ast
import datetime
import gzip
import inspect
import os
import shutil
import subprocess
import tarfile
import warnings
from pathlib import Path
from tarfile import TarFile
from textwrap import dedent

import aiofiles
import arrow

from enum_tools.documentation import (
    EnumType,
    EnumMeta,
    _docstring_from_expr,
    _docstring_from_eol_comment,
    _docstring_from_sphinx_comment,
    MultipleDocstringsWarning,
)


def should_use_pigz(processes: int) -> bool:
    """
    Decides whether pigz should be used for gzip decompression.

    :param processes: the number of processes to use for decompression
    :return: True if pigz is available and multiple processes
             should be used, and False otherwise

    """
    return bool(processes > 1 and shutil.which("pigz"))


def compress_file(path: Path, target: Path, processes: int = 1) -> None:
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


def compress_file_with_gzip(path: Path, target: Path) -> None:
    """
    compresses a file using gzip
    :param path: path to the file to be compressed
    :param target: path where the compressed file should be stored
    """
    with open(path, "rb") as f_in:
        with gzip.open(target, "wb", compresslevel=6) as f_out:
            shutil.copyfileobj(f_in, f_out)


def compress_file_with_pigz(path: Path, target: Path, processes: int):
    """
    use pigz to compress a file
    :param path: path to the file to be compressed
    :param target: path where the compressed file should be stored
    :param processes: number of processes allowable for pigz (-p argument)
    """
    command = ["pigz", "-p", str(processes), "-k", "--stdout", path]

    with open(target, "wb") as f:
        subprocess.call(command, stdout=f)


def decompress_file(path: Path, target: Path, processes: int = 1) -> None:
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


def decompress_file_with_gzip(path: Path, target: Path):
    """
    decompress a file using gzip

    :param path: path to the compressed file to be decompressed
    :param target: path for the newly decompressed file to be stored
    """
    with gzip.open(path, "rb") as f_in:
        with open(target, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def decompress_file_with_pigz(path: Path, target: Path, processes: int):
    """
    decompress a file using pigz

    :param path: path to the compressed file to be decompressed
    :param target: path for the newly decompressed file to be stored
    :param processes: the number of allowable processes for pigz (-p argument)
    """
    command = ["pigz", "-p", str(processes), "-d", "-k", "--stdout", path]

    with open(target, "w") as f:
        subprocess.call(command, stdout=f)


def is_within_directory(directory: Path, target: Path) -> bool:
    """
    Check whether a file is within a directory.

    :param directory: the path to the directory
    :param target: the path to the file

    """
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    prefix = os.path.commonprefix([abs_directory, abs_target])

    return prefix == abs_directory


def safely_extract_tgz(tar: TarFile, path: Path):
    """
    Safely extract a tar.gz file, ensuring that all member files are within the tarball.

    This prevents directory traversal attacks described in CVE-2007-4559.

    :param tar: the tarfile
    :param path: the path to extract to
    """
    for member in tar.getmembers():
        if not is_within_directory(path, path / member.name):
            raise Exception("Attempted Path Traversal in Tar File")

    tar.extractall(path)


def decompress_tgz(path: Path, target: Path):
    """
    Decompress the tar.gz file at ``path`` to the directory ``target``.

    :param path: the path to the tar.gz file.
    :param target: the path to directory into which to decompress the tar.gz file.

    """
    with tarfile.open(path, "r:gz") as tar:
        safely_extract_tgz(tar, target)


def file_stats(path: Path) -> dict:
    """
    Return the size and last modification date for the file at `path`.
    Wraps :func:`os.stat`
    :param path: the file path
    :return: the file size and modification datetime
    """
    stats = os.stat(path)

    return {"size": stats.st_size, "modify": arrow.get(stats.st_mtime).datetime}


async def file_length(path: Path) -> int:
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


def rm(path: Path, recursive: bool = False) -> bool:
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


def is_gzipped(path: Path) -> bool:
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
    Returns a datetime object representing the current UTC time.
    The last 3 digits of the microsecond frame are set to zero.

    :return: a UTC timestamp
    """
    # Get tz-aware datetime object.
    dt = arrow.utcnow().naive

    # Set the last three ms digits to 0.
    dt = dt.replace(microsecond=int(str(dt.microsecond)[0:3] + "000"))

    return dt


def document_enum(an_enum: EnumType) -> EnumType:
    """
    Document all members of an enum by parsing a docstring from the Python source.

    The docstring can be added in several ways:

    #. A comment at the end the line, starting with ``doc:``:

       .. code-block:: python

           Running = 1  # doc: The system is running.

    #. A comment on the previous line, starting with ``#:``.

       .. code-block:: python

           #: The system is running.
           Running = 1

    #. A string on the line *after* the attribute.
    This can be used for multiline docstrings.

       .. code-block:: python

           Running = 1
           \"\"\"
           The system is running.

           Hello World
           \"\"\"

    If more than one docstring format is found for an enum member
    a :exc:`MultipleDocstringsWarning` is emitted.

    :param an_enum: An :class:`~enum.Enum` subclass
    :type an_enum: :class:`enum.Enum`

    :returns: The same object passed as ``an_enum``.
    This allows this function to be used as a decorator.
    :rtype: :class:`enum.Enum`
    """

    if not isinstance(an_enum, EnumMeta):
        raise TypeError(f"'an_enum' must be an 'Enum', not {type(an_enum)}!")

    func_source = dedent(inspect.getsource(an_enum))
    func_source_tree = ast.parse(func_source)

    module_body = func_source_tree.body[0]
    class_body = module_body.body

    for idx, node in enumerate(class_body):
        targets = []

        if isinstance(node, ast.Assign):
            for t in node.targets:
                targets.append(t.id)

        elif isinstance(node, ast.AnnAssign):
            targets.append(node.target.id)
        else:
            continue

        if idx + 1 == len(class_body):
            next_node = None
        else:
            next_node = class_body[idx + 1]

        docstring_candidates = []

        if isinstance(next_node, ast.Expr):
            # might be docstring
            docstring_candidates.append(_docstring_from_expr(next_node))

        # maybe no luck with """ docstring? look for EOL comment.
        docstring_candidates.append(_docstring_from_eol_comment(func_source, node))

        # check non-whitespace lines above for Sphinx-style comment.
        docstring_candidates.append(_docstring_from_sphinx_comment(func_source, node))

        docstring_candidates_nn = list(filter(None, docstring_candidates))
        if len(docstring_candidates_nn) > 1:
            # Multiple docstrings found, warn
            warnings.warn(
                MultipleDocstringsWarning(
                    getattr(an_enum, targets[0]), docstring_candidates_nn
                )
            )

        if docstring_candidates_nn:
            docstring = docstring_candidates_nn[0]

            for target in targets:
                getattr(an_enum, target).__doc__ = docstring

    return an_enum
