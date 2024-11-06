from datetime import datetime
from typing import Annotated

from email_validator import EmailSyntaxError, validate_email
from pydantic import StringConstraints, field_validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import AnalysisWorkflow
from virtool_core.models.group import Permissions
from virtool_core.models.group_minimal import GroupMinimal
from virtool_core.models.user import User


def check_email(email: str | None) -> str | None:
    """Checks if the given email is valid.

    :param email: The email to check.
    :type email: str | None
    """
    if email is None:
        return None

    try:
        validate_email(email)
    except EmailSyntaxError:
        raise ValueError("The format of the email is invalid")

    return email


class AccountSettings(BaseModel):
    quick_analyze_workflow: AnalysisWorkflow
    show_ids: bool
    show_versions: bool
    skip_quick_analyze_dialog: bool


class Account(User):
    settings: AccountSettings
    email: Annotated[str, StringConstraints(strip_whitespace=True)]

    @field_validator("email")
    def check_email(cls, v: str | None) -> str | None:
        return check_email(v)


class APIKey(BaseModel):
    id: str
    created_at: datetime
    groups: list[GroupMinimal]
    name: str
    permissions: Permissions
