from typing import Optional

from email_validator import validate_email, EmailSyntaxError
from pydantic import constr, validator, Field

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import QuickAnalyzeWorkflow
from virtool_core.models.user import User


def check_email(email: Optional[str]) -> str:
    """
    Checks if the given email is valid.
    """
    try:
        validate_email(email)
    except EmailSyntaxError:
        raise ValueError("The format of the email is invalid")

    return email


class AccountSettings(BaseModel):
    quick_analyze_workflow: QuickAnalyzeWorkflow
    show_ids: bool
    show_versions: bool
    skip_quick_analyze_dialog: bool


class Account(User):
    settings: AccountSettings
    email: Optional[constr(strip_whitespace=True)] = Field(default="")

    _email_validation = validator("email", allow_reuse=True)(check_email)
