from pydantic import BaseModel, validator

from virtool_core.models import normalize_hex_color


class Label(BaseModel):
    color: str
    count: int
    description: str
    id: int
    name: str

    # Validators
    _normalize_color = validator("color", allow_reuse=True)(normalize_hex_color)


LabelMinimal = Label
