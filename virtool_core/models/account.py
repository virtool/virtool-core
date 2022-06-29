from virtool_core.models.user import User
from pydantic import BaseModel


class AccountSettings(BaseModel):
    quick_analyze_workflow: str
    show_ids: bool
    show_versions: bool
    skip_quick_analyze_dialog: bool


class Account(User):
    settings: AccountSettings
