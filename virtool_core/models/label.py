import re

from pydantic import BaseModel, validator


class Label(BaseModel):
    color: str
    count: int
    description: str
    id: int
    name: str

    @validator("color")
    def is_color_valid(cls, color: str) -> str:

        if not re.search(r'^#(?:[\da-fA-F]{3}){1,2}$', color):
            raise ValueError("The format of the color code is invalid")
        return color


LabelMinimal = Label
