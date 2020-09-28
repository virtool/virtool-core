import os
from typing import Mapping


def join_subtraction_path(settings: Mapping, subtraction_id: str) -> str:
    return os.path.join(
        settings["data_path"],
        "subtractions",
        subtraction_id.replace(" ", "_").lower()
    )


def join_subtraction_index_path(settings: Mapping, subtraction_id: str) -> str:
    return os.path.join(
        join_subtraction_path(settings, subtraction_id),
        "reference"
    )
