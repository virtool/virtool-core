from dataclasses import dataclass
from typing import Optional, MutableMapping, Coroutine, Callable, Tuple, Any

import virtool_core.caches.db

Processor = Callable[["DB", MutableMapping], Coroutine[None, None, MutableMapping]]
DatabaseUpdateListener = Callable[[str, str, Tuple[str, ...]], Coroutine[Any, Any, None]]


@dataclass
class CollectionBinding:
    collection_name: str
    projection: Optional[MutableMapping] = None
    processor: Optional[Callable[["DB", MutableMapping], Coroutine[None, None, MutableMapping]]] = None
    silent: bool = False


# TODO: set projections for modules
BINDINGS = [
    CollectionBinding("analyses"),
    CollectionBinding("caches", projection=virtool_core.caches.db.PROJECTION),
    CollectionBinding("coverage"),
    CollectionBinding("files"),
    CollectionBinding("groups"),
    CollectionBinding("history"),
    CollectionBinding("hmm"),
    CollectionBinding("indexes"),
    CollectionBinding("jobs"),
    CollectionBinding("keys"),
    CollectionBinding("kinds"),
    CollectionBinding("otus"),
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

