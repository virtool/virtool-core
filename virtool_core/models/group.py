from virtool_core.models.basemodel import BaseModel
from virtool_core.models.group_minimal import GroupMinimal
from virtool_core.models.searchresult import SearchResult
from virtool_core.models.user_base import UserNested


class Permissions(BaseModel):
    """The permissions possessed by a user and group."""

    cancel_job: bool = False
    create_ref: bool = False
    create_sample: bool = False
    modify_hmm: bool = False
    modify_subtraction: bool = False
    remove_file: bool = False
    remove_job: bool = False
    upload_file: bool = False


class Group(GroupMinimal):
    permissions: Permissions
    users: list[UserNested]


class GroupSearchResult(SearchResult):
    items: list[GroupMinimal]
