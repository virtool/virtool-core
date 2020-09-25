import asyncio
import hashlib
import json
import os
import pymongo.errors

from typing import Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor
import virtool_core.utils
import virtool_core.db.utils
import virtool_core.db

PROJECTION = [
    "_id",
    "created_at",
    "files",
    "hash",
    "program",
    "ready",
    "sample"
]


def calculate_cache_hash(parameters: Dict[str, str]) -> str:
    """
    Calculate a hash from the parameters `dict` for a cache. The parameters are arguments passed to a trimming program.
    Caches can be reused when the hash of the trim parameters for a a new analysis matches an existing cache.

    :param parameters: the trimming parameters
    :return: the cache hash

    """
    string = json.dumps(parameters, sort_keys=True)
    return hashlib.sha1(string.encode()).hexdigest()


async def find(db, sample_id: str, program: str, parameters: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Find a cache matching the passed `sample_id`, `program` name and version, and set of trimming `parameters`.

    If no matching cache exists, `None` will be returned.

    :param db: the application database interface
    :param sample_id: the id of the parent sample
    :param program: the program and version used to create the cache
    :param parameters: the parameters used for the trim
    :return: a cache document

    """
    document = await db.caches.find_one({
        "hash": calculate_cache_hash(parameters),
        "missing": False,
        "program": program,
        "sample.id": sample_id
    })

    return virtool_core.db.utils.base_processor(document)


async def get(db, cache_id: str) -> Dict:
    """
    Get the complete representation for the cache with the given `cache_id`.

    :param db: the application database client
    :param cache_id: the id of the cache to get
    :return: the cache document

    """
    document = await db.caches.find_one(cache_id)
    return virtool_core.db.utils.base_processor(document)


async def create(db, sample_id: str, parameters: Dict[str, str], paired: bool, legacy: bool = False, program: str = "skewer-0.2.2"):
    """
    Create and insert a new cache database document. Return the generated unique cache id.

    :param db: the application database client
    :param sample_id: the id of the sample the cache is derived from
    :param parameters: the trim parameters
    :param paired: boolean indicating if the sample contains paired data
    :param legacy: boolean indicating if the cache is derived from a trimmed legacy sample
    :param program: the trimming program used
    :return: the new cache id

    """
    try:
        cache_id = virtool_core.utils.random_alphanumeric(length=8)

        document = {
            "_id": cache_id,
            "created_at": virtool_core.utils.timestamp(),
            "files": list(),
            "hash": calculate_cache_hash(parameters),
            "legacy": legacy,
            "missing": False,
            "paired": paired,
            "parameters": parameters,
            "program": program,
            "ready": False,
            "sample": {
                "id": sample_id
            }
        }

        await db.caches.insert_one(document)

        return virtool_core.db.utils.base_processor(document)

    except pymongo.errors.DuplicateKeyError:
        # Keep trying to add the cache with new ids if the generated id is not unique.
        return await create(db, sample_id, parameters, paired, legacy=legacy, program=program)


async def remove(
        db,
        data_path: str,
        cache_id: str,
        executor: ThreadPoolExecutor,
        event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
):
    """
    Remove the cache database document and files with the given `cache_id`.

    :param db: The Virtool caches database
    :param data_path: The Virtool data path
    :param cache_id: The id of the cache to remove
    :param executor: A :class:`concurrent.futures.ThreadPoolExecutor`
    :param event_loop: The asyncio event loop. Defaults to `asyncio.get_event_loop()`
    """

    await db.caches.delete_one({
        "_id": cache_id
    })

    path = os.path.join(data_path, "caches", cache_id)

    try:
        await event_loop.run_in_executor(executor, virtool_core.utils.rm, path, True)
    except FileNotFoundError:
        pass
