from datetime import datetime
from typing import List, Optional

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.group import Permissions, GroupMinimal
from virtool_core.models.searchresult import SearchResult


class UserB2C(BaseModel):
    display_name: Optional[str]
    family_name: Optional[str]
    given_name: Optional[str]
    oid: str


class UserNested(BaseModel):
    id: str
    administrator: bool
    handle: str


class UserMinimal(UserNested):
    active: bool
    b2c: Optional[UserB2C]
    b2c_display_name: Optional[str]
    b2c_family_name: Optional[str]
    b2c_given_name: Optional[str]
    b2c_oid: Optional[str]


class User(UserMinimal):
    force_reset: bool
    groups: List[GroupMinimal]
    last_password_change: datetime
    permissions: Permissions
    primary_group: Optional[GroupMinimal]


class UserSearchResult(SearchResult):
    documents: List[UserMinimal]
