from dataclasses import dataclass
from typing import Dict

from virtool_workflow.data_model.references import Reference


@dataclass
class Index:
    """
    A Virtool index.

    An index is a build of a reference. OTUs of a reference
    change over time, requiring index builds to use the changes
    in subsequent analyses.

    :param id: A unique ID for the index build
    :param manifest: A mapping of OTU IDs to their current version number
    :param reference: The :class:`Reference` assocated with this index build.
    """
    id: str
    manifest: Dict[str, int]
    reference: Reference
