from dataclasses import dataclass

from typing import Literal

DataType = Literal["barcode", "genome"]


@dataclass
class Reference:
    """
    A collection of OTUs.

    OTUs can be built and versioned into indexes.

    :param id: A unique ID for the reference
    :param data_type: The type of data the reference contains
    :param name: The display name
    :param description: A detailed description of the reference
    :param organism: The organism type represented by the reference
    """
    id: str
    data_type: DataType
    description: str
    name: str
    organism: str
