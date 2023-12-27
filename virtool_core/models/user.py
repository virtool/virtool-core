from datetime import datetime

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.group import Permissions, GroupMinimal
from virtool_core.models.roles import AdministratorRole
from virtool_core.models.searchresult import SearchResult


class UserB2C(BaseModel):
    display_name: str | None
    family_name: str | None
    given_name: str | None
    oid: str


class UserNested(BaseModel):
    id: str
    handle: str


class UserMinimal(UserNested):
    active: bool
    b2c: UserB2C | None
    b2c_display_name: str | None
    b2c_family_name: str | None
    b2c_given_name: str | None
    b2c_oid: str | None


class User(UserMinimal):
    administrator_role: AdministratorRole | None
    force_reset: bool
    groups: list[GroupMinimal]
    last_password_change: datetime
    permissions: Permissions
    primary_group: GroupMinimal | None


class UserSearchResult(SearchResult):
    items: list[User]
