from pydantic import BaseModel, validator

from virtool_core.models import normalize_hex_color


class LabelNested(BaseModel):
    color: str
    description: str
    id: int
    name: str


class Label(LabelNested):
    count: int

    _normalize_color = validator("color", allow_reuse=True)(normalize_hex_color)


LabelMinimal = Label
