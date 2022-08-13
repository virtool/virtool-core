from pydantic import validator

from virtool_core.models import normalize_hex_color
from virtool_core.models.basemodel import BaseModel


class LabelNested(BaseModel):
    color: str
    description: str
    id: int
    name: str


class Label(LabelNested):
    count: int

    _normalize_color = validator("color", allow_reuse=True)(normalize_hex_color)


LabelMinimal = Label
