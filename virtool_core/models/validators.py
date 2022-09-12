import re
from typing import Any


def normalize_hex_color(color: str) -> str:
    """
    Validate a hex color and convert all alpha characters to uppercase.

    :param color: the hex color to validate

    """
    color = color.upper()

    if not re.search(r"^#(?:[\dA-F]{3}){1,2}$", color):
        raise ValueError("The format of the color code is invalid")

    return color


def prevent_none(value: Any) -> Any:
    """
    Validate an optional value to check if it is being set to null when
    it is not nullable.

    :param value: the optional value to validate

    """
    if value is None:
        raise ValueError("Value may not be null")

    return value
