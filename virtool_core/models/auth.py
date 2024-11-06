from virtool_core.models.basemodel import BaseModel


class PermissionMinimal(BaseModel):
    id: str
    action: str
    description: str
    name: str
    resource_type: str
