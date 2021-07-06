from dataclasses import dataclass
from typing import List

from virtool_workflow.data_model.files import VirtoolFile
from virtool_workflow.data_model.indexes import Index
from virtool_workflow.data_model.samples import Sample
from virtool_workflow.data_model.subtractions import Subtraction


@dataclass
class Analysis:
    """An analysis on a given sample.

    :param id: The unique ID of the analysis
    :param files: A list of files associated with the analysis
    :param index: The reference index being used for analysis
    :param subtractions: A list of subtractions being used for analysis

    """
    id: str
    files: List[VirtoolFile]
    sample: Sample = None
    index: Index = None
    subtractions: List[Subtraction] = None
