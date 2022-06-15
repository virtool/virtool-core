from pydantic import BaseModel


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


class Group(GroupMinimal):
    permissions: Permissions
