
from pydantic import ValidationError

from virtool_core.models.group import Group
import pytest


@pytest.fixture
def mock_group():
    return {
        "id": "magicians",
        "permissions": {
            "cancel_job": False,
            "create_ref": False,
            "create_sample": False,
            "modify_hmm": False,
            "modify_subtraction": False,
            "remove_file": False,
            "remove_job": False,
            "upload_file": False
        }
    }


def test_default_name(mock_group):
    """
    Tests if the `name` field is set to the `id` as default.
    """
    group = Group(**mock_group)

    assert group.name == group.id


def test_empty_name(mock_group):
    """
    Tests if an error is thrown when an empty `name` is provided.
    """
    with pytest.raises(ValidationError) as err:
        mock_group.update({"name": ""})
        Group(**mock_group)

        assert "ensure this value has at least 1 characters" in str(err)
