from datetime import datetime

from typing import List

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import Permission
from virtool_core.models.group import Group
from virtool_core.models.user import UserNested


class Session(BaseModel):
    created_at: datetime
    ip: str
    token: str
    groups: List[Group]
    permissions: Permission
    force_reset: bool
    user: UserNested
