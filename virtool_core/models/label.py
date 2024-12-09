"""Models for label resources."""

from pydantic import field_validator

from virtool_core.models.basemodel import BaseModel
from virtool_core.models.validators import normalize_hex_color


class LabelNested(BaseModel):
    """A label for categorizing samples in Virtool."""

    color: str
    description: str
    id: int
    name: str


class Label(LabelNested):
    """A label for categorizing samples in Virtool.

    This is the full representation of a label and includes the number of samples that
    have been assigned the label.
    """

    count: int

    @field_validator("color")
    def check_color(cls, color: str) -> str:
        return normalize_hex_color(color)


LabelMinimal = Label
"""A minimal representation of a label.

At this time, it is the same as the full representation.
"""
