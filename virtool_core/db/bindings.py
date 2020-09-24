from .core import Processor
from dataclasses import dataclass
from typing import Optional, MutableMapping


@dataclass
class CollectionBinding:
    collection_name: str
    projection: Optional[MutableMapping] = None
    processor: Optional[Processor] = None
    silent: bool = False


# TODO: set projections for modules
BINDINGS = [
    CollectionBinding("analyses"),
    CollectionBinding("caches"),
    CollectionBinding("coverage"),
    CollectionBinding("files"),
    CollectionBinding("groups"),
    CollectionBinding("history"),
    CollectionBinding("hmm"),
    CollectionBinding("indexes"),
    CollectionBinding("jobs"),
    CollectionBinding("keys"),
    CollectionBinding("kinds"),
    CollectionBinding("processes"),
    CollectionBinding("references"),
    CollectionBinding("samples"),
    CollectionBinding("settings"),
    CollectionBinding("sequences"),
    CollectionBinding("sessions"),
    CollectionBinding("status"),
    CollectionBinding("subtraction"),
    CollectionBinding("users"),
]