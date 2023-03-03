from typing import List

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.user import UserNested
from virtool_core.models.roles import AdministratorRole


class AdministratorMinimal(UserNested):
    role: AdministratorRole


class Administrator(AdministratorMinimal):
    available_roles: List[dict]


class AdministratorSearch(BaseModel):
    documents: List[AdministratorMinimal]
    available_roles: List[dict]
