from typing import Union


def apply_projection(document: dict, projection: Union[list, dict]):
    """
    Apply a Mongo-style projection to a document and return it.

    :param document: the document to project
    :type document: dict

    :param projection: the projection to apply
    :type projection: Union[dict,list]

    :return: the projected document
    :rtype: dict

    """
    if isinstance(projection, list):
        if "_id" not in projection:
            projection.append("_id")

        return {key: document[key] for key in document if key in projection}

    if not isinstance(projection, dict):
        raise TypeError(f"Invalid type for projection: {type(projection)}")

    if projection == {"_id": False}:
        return {key: document[key] for key in document if key != "_id"}

    if all(value is False for value in projection.values()):
        return {key: document[key] for key in document if key not in projection}

    if "_id" not in projection:
        projection["_id"] = True

    return {key: document[key] for key in document if projection.get(key, False)}


def base_processor(document: Union[dict, None]) -> Union[dict, None]:
    """
    Converts a document `dict` returned from MongoDB into a `dict` that can be passed into a JSON response. Removes the
    '_id' key and reassigns it to `id`.

    :param document: the document to process
    :return: processed document

    """
    if document is None:
        return None

    document = dict(document)

    try:
        document["id"] = document.pop("_id")
    except KeyError:
        pass

    return document


async def get_one_field(collection, field, query):
    projected = await collection.find_one(query, [field])

    if projected is None:
        return None

    return projected.get(field)