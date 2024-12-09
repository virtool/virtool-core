from virtool_core.models.basemodel import BaseModel


class UserNested(BaseModel):
    """A minimal representation of a user that can be nested in other models."""

    id: str
    """The unique ID of the user."""

    handle: str
    """The user's handle."""


class UserB2C(BaseModel):
    display_name: str | None
    family_name: str | None
    given_name: str | None
    oid: str
