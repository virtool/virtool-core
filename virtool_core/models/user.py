from datetime import datetime

from virtool_core.models.group import Permissions
from virtool_core.models.group_minimal import GroupMinimal
from virtool_core.models.roles import AdministratorRole
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user_base import UserB2C, UserNested


class UserMinimal(UserNested):
    active: bool
    b2c: UserB2C | None = None
    b2c_display_name: str | None = None
    b2c_family_name: str | None = None
    b2c_given_name: str | None = None
    b2c_oid: str | None = None


class User(UserMinimal):
    administrator_role: AdministratorRole | None
    force_reset: bool
    groups: list[GroupMinimal]
    last_password_change: datetime
    permissions: Permissions
    primary_group: GroupMinimal | None


class UserSearchResult(SearchResult):
    items: list[User]
