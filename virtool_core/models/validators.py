import re


def normalize_hex_color(color: str) -> str:
    """
    Validate a hex color and convert all alpha characters to uppercase.

    :param color: the hex color to validate

    """
    color = color.upper()

    if not re.search(r"^#(?:[\dA-F]{3}){1,2}$", color):
        raise ValueError("The format of the color code is invalid")

    return color
