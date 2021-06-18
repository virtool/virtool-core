from pathlib import Path
from typing import Any, Dict


def join_subtraction_path(settings: Dict[str, Any], subtraction_id: str) -> Path:
    return settings["data_path"] / "subtractions" / subtraction_id.replace(" ", "_").lower()


def join_subtraction_index_path(settings: Dict[str, Any], subtraction_id: str) -> Path:
    return join_subtraction_path(settings, subtraction_id) / "reference"
