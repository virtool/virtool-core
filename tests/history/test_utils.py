import os
import sys
import virtool_core.history.utils

TEST_DIFF_PATH = os.path.join(sys.path[0], "tests", "test_files", "diff.json")

def test_json_object_hook(static_time):
    """
    Test that the hook function correctly decodes created_at ISO format fields to naive `datetime` objects.

    """
    o = {
        "foo": "bar",
        "created_at": static_time.iso
    }

    result = virtool_core.history.utils.json_object_hook(o)

    assert result == {
        "foo": "bar",
        "created_at": static_time.datetime
    }


async def test_read_diff_file(mocker, snapshot):
    """
    Test that a diff is parsed to a `dict` correctly. ISO format dates must be converted to `datetime` objects.

    """
    m = mocker.patch("virtool_core.history.utils.join_diff_path", return_value=TEST_DIFF_PATH)

    diff = await virtool_core.history.utils.read_diff_file("foo", "bar", "baz")

    m.assert_called_with("foo", "bar", "baz")
    snapshot.assert_match(diff)
