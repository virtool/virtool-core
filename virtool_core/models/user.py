from datetime import datetime
from typing import List

from pydantic import BaseModel

from virtool_core.models.group import Group, Permissions


class UserMinimal(BaseModel):
    id: str
    handle: str
    administrator: bool
    force_reset: bool
    groups: List[Group]
    last_password_change: datetime
    primary_group: str


class User(UserMinimal):
    permissions: Permissions
