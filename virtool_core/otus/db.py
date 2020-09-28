from . import utils
from typing import Dict, Optional, Union


async def join(db, query: Union[Dict, str], document: Optional[Dict] = None):
    """
    Join the otu associated with the supplied ``otu_id`` with its sequences.

    If a otu entry is also passed,the database will not be queried for the otu based on its id.

    :param db: the application database client
    :type db: :class:`~motor.motor_asyncio.AsyncIOMotorClient`

    :param query: the id of the otu to join or a Mongo query.
    :type query: Union[dict,str]

    :param document: use this otu document as a basis for the join instead finding it using the otu id.
    :type document: dict

    :return: the joined otu document
    :rtype: Coroutine[dict]

    """
    # Get the otu entry if a ``document`` parameter was not passed.
    document = document or await db.otus.find_one(query)

    if document is None:
        return None

    cursor = db.sequences.find({"otu_id": document["_id"]})

    # Merge the sequence entries into the otu entry.
    return utils.merge_otu(document, [d async for d in cursor])
