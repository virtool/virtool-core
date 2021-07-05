from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class HMM:
    """
    A Virtool HMM (Hidden Markov Model).

    :param id: A unique ID for the HMM
    :param cluster: The cluster number for the HMM
    :param entries: Dictionary descriptions of the sequences in the cluster
    :param families: A dictionary mapping each family to the number of
                     sequences belonging to it
    :param genera: A dictionary mapping each genera to the number of
                   sequences belonging to it
    :param hidden: A flag indicating that the HMM dataset has been removed,
                   but is being perisisted due to an active analysis
    :param length: The length of the HMM profile
    :param mean_entrophy: The mean entrophy for the HMM
    :param total_entrophy: The total entrophy for the HMM
    :param names: The three most common names for the HMM
                  as observed in the cluster members
    """
    id: str
    cluster: int
    count: int
    entries: List[dict]
    families: Dict[str, int]
    genera: Dict[str, int]
    hidden: bool
    length: int
    mean_entropy: float
    total_entropy: float
    names: Tuple[str, str, str]
