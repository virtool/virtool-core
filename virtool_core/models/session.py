from datetime import datetime

from typing import List, Optional

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.enums import Permission
from virtool_core.models.group import Group
from virtool_core.models.user import UserNested


class SessionAuthentication(BaseModel):
    token: str
    groups: List[Group]
    permissions: Permission
    force_reset: bool
    user: UserNested


class SessionPasswordReset(BaseModel):
    code: str
    remember: bool
    user_id: str


class Session(BaseModel):
    authentication: Optional[SessionAuthentication]
    reset: Optional[SessionPasswordReset]
    created_at: datetime
    ip: str
