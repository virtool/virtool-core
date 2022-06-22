from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from virtool_core.models.group import Permissions, GroupMinimal
from virtool_core.models.searchresult import SearchResult


class UserMinimal(BaseModel):
    id: str
    handle: str
    administrator: bool


class User(UserMinimal):
    force_reset: bool
    groups: List[GroupMinimal]
    last_password_change: datetime
    permissions: Permissions
    primary_group: Optional[GroupMinimal]


class UserSearchResult(SearchResult):
    documents: List[UserMinimal]
