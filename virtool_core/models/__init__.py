import re
from . import user
from . import group
from . import samples
from . import subtraction


group.Group.update_forward_refs(UserMinimal=user.UserMinimal)
samples.SampleMinimal.update_forward_refs(SubtractionNested=subtraction.SubtractionNested)
subtraction.Subtraction.update_forward_refs(SampleNested=samples.SampleNested)


def normalize_hex_color(color: str) -> str:
    """
    Validate a hex color and convert all alpha characters to uppercase.

    :param color: the hex color to validate

    """
    color = color.upper()

    if not re.search(r"^#(?:[\dA-F]{3}){1,2}$", color):
        raise ValueError("The format of the color code is invalid")

    return color
