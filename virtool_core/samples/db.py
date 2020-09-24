import asyncio
from .utils import calculate_workflow_tags

LIST_PROJECTION = [
    "_id",
    "created_at",
    "host",
    "isolate",
    "library_type",
    "pathoscope",
    "name",
    "nuvs",
    "ready",
    "user"
]

PROJECTION = [
    "_id",
    "created_at",
    "library_type",
    "name",
    "pathoscope",
    "nuvs",
    "group",
    "group_read",
    "group_write",
    "all_read",
    "all_write",
    "ready",
    "user",
]

RIGHTS_PROJECTION = {
    "_id": False,
    "group": True,
    "group_read": True,
    "group_write": True,
    "all_read": True,
    "all_write": True,
    "user": True
}


async def recalculate_workflow_tags(db, sample_id: str) -> dict:
    """
    Recalculate and apply workflow tags (eg. "ip", True) for a given sample.

    :param db: the application database client
    :param sample_id: the id of the sample to recalculate tags for
    :return: the updated sample document

    """
    analyses = await asyncio.shield(db.analyses.find({"sample.id": sample_id}, ["ready", "workflow"]).to_list(None))

    return await db.samples.find_one_and_update({"_id": sample_id}, {
        "$set": calculate_workflow_tags(analyses)
    }, projection=LIST_PROJECTION)
