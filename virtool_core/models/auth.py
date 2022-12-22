from virtool_core.models.basemodel import BaseModel


class PermissionMinimal(BaseModel):
    id: int
    name: str
    description: str
    resource_type: str
    action: str
