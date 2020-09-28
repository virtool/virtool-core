import os
import aiofiles
import json
import arrow
from typing import Union, Mapping


def json_object_hook(o: Mapping) -> Mapping:
    """A JSON decoder hook for converting `created_at` fields from ISO format dates to `datetime` objects.

    :param o: the JSON parsing dict
    :return: the parsed dict
    """
    for key, value in o.items():
        if key == "created_at":
            o[key] = arrow.get(value).naive

    return o


def join_diff_path(data_path: str, otu_id: str, otu_version: Union[int, str]) -> str:
    """Derive the path to a diff file based on the application `data_path` setting and the OTU ID and version.

    :param data_path: the application data path settings
    :param otu_id: the OTU ID to join a diff path for
    :param otu_version: the OTU version to join a diff path for
    :return: the change path
    """
    return os.path.join(data_path, "history", f"{otu_id}_{otu_version}.json")


async def read_diff_file(data_path, otu_id, otu_version):
    """Read a history diff JSON file."""
    path = join_diff_path(data_path, otu_id, otu_version)

    async with aiofiles.open(path, "r") as f:
        return json.loads(await f.read(), object_hook=json_object_hook)
