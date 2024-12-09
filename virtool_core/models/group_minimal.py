from virtool_core.models.basemodel import BaseModel


class GroupMinimal(BaseModel):
    """A minimal representation of a group that can be nested in other models."""

    id: int | str
    """The unique ID of the group."""

    legacy_id: str | None
    """The legacy ID of the group."""

    name: str
    """The display name of the group."""
