from virtool_core.models.user import UserNested
from virtool_core.models.roles import AdministratorRole


class Administrator(UserNested):
    role: AdministratorRole
