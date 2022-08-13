import pytest

from virtool_core.models.group import Group


@pytest.fixture
def mock_group():
    return {
        "_id": "magicians",
        "permissions": {
            "cancel_job": False,
            "create_ref": False,
            "create_sample": False,
            "modify_hmm": False,
            "modify_subtraction": False,
            "remove_file": False,
            "remove_job": False,
            "upload_file": False,
        },
        "users": [],
    }


@pytest.mark.parametrize("id", ["invalid", "valid"])
def test_id(id, mock_group):
    """
    Tests if _id is converted to id and _id is no longer in the model.
    If id is already provided, nothing should occur.
    """

    if id == "valid":
        mock_group["id"] = mock_group.pop("_id")

    group = Group(**mock_group)

    assert group.id == "magicians"

    with pytest.raises(AttributeError):
        group._id
