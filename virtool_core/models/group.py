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
    id: str
    name: Optional[constr(min_length=1)]

    @validator("name", always=True)
    def check_name(cls, name, values):
        """
        Sets `name` to the provided `id` if it is `None`.
        """
        return name or values["id"]


class Group(GroupMinimal):
    permissions: Permissions
    users: List[UserNested]
