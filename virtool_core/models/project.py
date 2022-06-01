from typing import List, Optional

from pydantic import BaseModel, validator

from virtool_core.models import normalize_hex_color
from virtool_core.models.user import UserMinimal


class ProjectMinimal(BaseModel):
    """
    A provisional minimal project model.

    Do not use this model. Projects are not yet implemented in Virtool.

    """

    #: The project's unique ID.
    id: int
    #: The project name.
    name: str
    #: A longer description for the project.
    description: str
    #: The display color for the project.
    color: str
    #: The user that created the project.
    user: UserMinimal

    # Validators
    _normalize_color = validator("color", allow_reuse=True)(normalize_hex_color)


class Project(ProjectMinimal):
    """
    A provisional project model.

    Do not use this model. Projects are not yet implemented in Virtool.

    """

    #: The samples organized under the project.
    samples: Optional[List[str]] = None
    #: The users that have access to the project.
    users: Optional[List[UserMinimal]] = None
