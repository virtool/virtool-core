from virtool_core.models.basemodel import BaseModel
from virtool_core.models.roles import AdministratorRole
from virtool_core.models.user_base import UserNested


class AdministratorMinimal(UserNested):
    role: AdministratorRole | None
    """The administrator role for a user.

    When `None`, the user is not an administrator.
    """


class Administrator(AdministratorMinimal):
    """An administrator user."""

    available_roles: list[dict]
    """A list of available administrator roles."""


class AdministratorSearch(BaseModel):
    """The result of a search for administrator users."""

    items: list[AdministratorMinimal]
    """A list of administrator users that match the search query."""

    available_roles: list[dict]
    """A list of available administrator roles."""
