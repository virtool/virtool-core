from copy import deepcopy
from typing import Mapping, Any, Sequence


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

