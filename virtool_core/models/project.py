from pydantic import field_validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.user_base import UserNested
from virtool_core.models.validators import normalize_hex_color


class ProjectMinimal(BaseModel):
    """A provisional minimal project model.

    Do not use this model. Projects are not yet implemented in Virtool.
    """

    id: int
    """The project's unique ID."""

    name: str
    """The project name."""

    description: str
    """A longer description for the project."""

    color: str
    """The display color for the project."""

    user: UserNested
    """The user that created the project."""

    # Validators
    @field_validator("color")
    def validate_color(cls, value: str) -> str:
        return normalize_hex_color(value)


class Project(ProjectMinimal):
    """A provisional project model.

    Do not use this model. Projects are not yet implemented in Virtool.
    """

    samples: list[str] | None = None
    """The samples organized under the project."""

    users: list[UserNested] | None = None
    """The users that have access to the project."""
