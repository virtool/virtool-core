import pytest
from pydantic import ValidationError

from virtool_core.models.account import Account


@pytest.fixture()
def mock_account():
    return {
        "administrator": False,
        "administrator_role": None,
        "active": True,
        "email": "dev@virtool.ca",
        "groups": [],
        "handle": "bob",
        "force_reset": False,
        "id": "test",
        "last_password_change": "2015-10-06T20:00:00Z",
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
        "primary_group": None,
        "settings": {
            "quick_analyze_workflow": "pathoscope_bowtie",
            "show_ids": True,
            "show_versions": True,
            "skip_quick_analyze_dialog": True,
        },
    }


class TestEmail:
    def test_ok(self, mock_account: dict):
        Account(**mock_account)

    def test_invalid_email(self, mock_account: dict):
        """Test that an invalid email fails validation."""
        with pytest.raises(ValidationError) as err:
            mock_account.update({"email": "devvirtool.ca"})
            Account(**mock_account)

        print(err)

        assert "The format of the email is invalid" in str(err)
