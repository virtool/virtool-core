from datetime import datetime
from typing import List

from pydantic import BaseModel

from virtool_core.models.group import Permissions, GroupMinimal


class UserMinimal(BaseModel):
    id: str
    handle: str
    administrator: bool


class User(UserMinimal):
    force_reset: bool
    groups: List[GroupMinimal]
    last_password_change: datetime
    permissions: Permissions
    primary_group: GroupMinimal
