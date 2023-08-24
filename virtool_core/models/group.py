from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from pydantic import validator, constr

from virtool_core.models.basemodel import BaseModel

if TYPE_CHECKING:
    from virtool_core.models.user import UserNested


class Permissions(BaseModel):
    """
    The permissions possessed by a user and group.
    """

    cancel_job: bool = False
    create_ref: bool = False
    create_sample: bool = False
    modify_hmm: bool = False
    modify_subtraction: bool = False
    remove_file: bool = False
    remove_job: bool = False
    upload_file: bool = False


class GroupMinimal(BaseModel):
    id: int
    legacy_id: str
    name: str


class Group(GroupMinimal):
    permissions: Permissions
    users: List[UserNested]
