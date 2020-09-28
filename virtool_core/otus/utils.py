from copy import deepcopy
from typing import Mapping, Any, Sequence, List, Generator


def extract_default_sequences(joined: Mapping[str, Mapping]) -> List[Mapping]:
    """Return a list of sequences from the default isolate of the passed joined otu document.

    :param joined: the joined otu document.
    :return: a list of sequences associated with the default isolate.

    """
    for isolate in joined["isolates"]:
        if isolate["default"]:
            return isolate["sequences"]


def extract_sequences(otu: Mapping[str, Mapping]) -> Generator[str, None, None]:
    """
    Extract sequences from an OTU document
    :param otu: The OTU document
    :return: a generator containing sequences from the isolates of the OTU
    """
    for isolate in otu["isolates"]:
        for sequence in isolate["sequences"]:
            yield sequence


def merge_otu(otu: Mapping[str, Any], sequences: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    """
    Merge the given sequences in the given otu document. The otu will gain a ``sequences`` field containing a
    list of its associated sequence documents.

    :param otu: a otu document.
    :type otu: dict

    :param sequences: the sequence documents to merge into the otu.
    :type sequences: list

    :return: the merged otu.
    :rtype: dict

    """
    merged = deepcopy(otu)

    for isolate in merged["isolates"]:
        isolate_id = isolate["id"]
        isolate["sequences"] = [s for s in sequences if s["isolate_id"] == isolate_id]

    return merged

