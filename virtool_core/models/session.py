from datetime import datetime
from typing import Optional

from virtool_core.models.basemodel import BaseModel


class SessionAuthentication(BaseModel):
    token: str
    user_id: str


class SessionPasswordReset(BaseModel):
    code: str
    remember: bool
    user_id: str


class Session(BaseModel):
    authentication: Optional[SessionAuthentication]
    reset: Optional[SessionPasswordReset]
    created_at: datetime
    ip: str
