import datetime
import os
import shutil
import sys
from pathlib import Path

import arrow
import pytest

import virtool_core.utils

sys.path.append(str(Path(__file__).parent.parent))


def test_decompress_tgz(tmpdir):
    path = Path(tmpdir)

    src_path = Path(__file__).parent / "test_files/virtool.tar.gz"

    shutil.copy(src_path, path)

    virtool_core.utils.decompress_tgz(path / "virtool.tar.gz", path / "de")

    assert set(os.listdir(path)) == {"virtool.tar.gz", "de"}

    assert os.listdir(os.path.join(path, "de")) == ["virtool"]

    assert set(os.listdir(os.path.join(path, "de", "virtool"))) == {
        "run",
        "client",
        "VERSION",
        "install.sh",
    }


@pytest.mark.parametrize(
    "recursive,expected", [(True, {"foo.txt"}), (False, {"foo.txt", "baz"})]
)
def test_rm(recursive, expected, tmpdir):
    """Test that a file can be removed and that a folder can be removed when `recursive` is set to `True`."""
    tmpdir.join("foo.txt").write("hello world")
    tmpdir.join("bar.txt").write("hello world")
    tmpdir.mkdir("baz")

    assert set(os.listdir(str(tmpdir))) == {"foo.txt", "bar.txt", "baz"}

    virtool_core.utils.rm(tmpdir / "bar.txt")

    if recursive:
        virtool_core.utils.rm(tmpdir / "baz", recursive=recursive)
    else:
        with pytest.raises(IsADirectoryError):
            virtool_core.utils.rm(tmpdir / "baz", recursive=recursive)

    assert set(os.listdir(str(tmpdir))) == expected


@pytest.mark.parametrize("processes", [1, 4])
@pytest.mark.parametrize("which", [None, "/usr/local/bin/pigz"])
def test_should_use_pigz(processes, which, mocker):
    mocker.patch("shutil.which", return_value=which)

    result = virtool_core.utils.should_use_pigz(processes)

    if processes == 4 and which is not None:
        assert result is True
    else:
        assert result is False


def test_timestamp(mocker):
    """
    Test that the timestamp util returns a datetime object with the last 3 digits of the microsecond frame set to
    zero.

    """
    m = mocker.Mock(return_value=arrow.Arrow(2017, 10, 6, 20, 0, 0, 612304))

    mocker.patch("arrow.utcnow", new=m)

    timestamp = virtool_core.utils.timestamp()

    assert isinstance(timestamp, datetime.datetime)

    assert timestamp == arrow.arrow.Arrow(2017, 10, 6, 20, 0, 0, 612000).naive
