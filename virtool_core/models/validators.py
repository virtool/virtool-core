import re
from typing import Any

from pydantic import field_validator


def normalize_hex_color(color: str) -> str:
    """Validate a hex color and convert all alpha characters to uppercase.

    :param color: the hex color to validate

    """
    color = color.upper()

    if not re.search(r"^#(?:[\dA-F]{3}){1,2}$", color):
        raise ValueError("The format of the color code is invalid")

    return color


def prevent_none(*fields: str):
    @field_validator(*fields, mode="before")
    def func(value: Any) -> Any:
        if value is None:
            raise ValueError("Value may not be null")

        return value

    return func
