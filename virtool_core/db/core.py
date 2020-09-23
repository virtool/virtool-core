import motor.motor_asyncio
import pymongo.results
import pymongo.errors
import semver
import logging
from typing import Union, Callable, List, MutableMapping, Awaitable, Iterable
import virtool_core.utils
from . import utils

logger = logging.getLogger("mongo")


class Collection:

    """
    A wrapper for AsyncIOMotorCollection which dispatches updates via a provided
    callback function :func:`enqueue_change`
    """

    def __init__(
            self,
            name: str,
            collection: motor.motor_asyncio.AsyncIOMotorCollection,
            enqueue_change: Callable[[str, str, Iterable[str]], Awaitable[None]] = None,
            processor: Callable[[MutableMapping], Awaitable[MutableMapping]] = None,
            projection: Union[None, List, MutableMapping] = None,
    ):
        """

        :param name: name of the collection
        :param collection: the :class:`motor.motor_asyncio.AsyncIOMotorCollection to wrap
        :param enqueue_change: callback function for database changes, defaults to None
        :param processor: function applied to the mongodb document before it is returned.
        :param projection: the mongodb projection
        """
        self.name = name
        self._collection = collection
        self._on_change = []
        if enqueue_change:
            self._on_change.append(enqueue_change)
        self.processor = processor
        self.projection = projection

        # No dispatches are necessary for these collection methods
        # and they can be directly referenced instead of wrapped
        self.aggregate = self._collection.aggregate
        self.count_documents = self._collection.count_documents
        self.create_index = self._collection.create_index
        self.create_indexes = self._collection.create_indexes
        self.distinct = self._collection.distinct
        self.drop_index = self._collection.drop_index
        self.drop_indexes = self._collection.drop_indexes
        self.find_one = self._collection.find_one
        self.find = self._collection.find
        self.insert_many = self._collection.insert_many
        self.rename = self._collection.rename

    def apply_projection(self, document: dict) -> dict:
        """
        Apply the collection projection to the given document and return a new `dict`. If the collection `projection`
        attribute is not defined, the document will be returned unaltered.

        :param document: the document to apply the projection to
        :return: the projected document

        """
        if self.projection:
            return utils.apply_projection(document, self.projection)

        return document

    def on_change(self, on_change: Callable[[str, str, Iterable[str]], Awaitable[None]]):
        """
        Add a callback function for database updates
        :param on_change: The callback function to add, it's signature should be as follows.

        .. code-block:: python

            async def on_change(collection_name: str, operation: str, *id_list):
                ...

        :return: The :func:`on_change` function passed in, such that this function can be used as
            a decorator.
        """
        self._on_change.append(on_change)
        return on_change

    async def enqueue_change(self, operation: str, *id_list):
        """
        Dispatch updates. Applies the collection
        projection and processor.

        :param operation: the operation to label the dispatch with (insert, update, delete)
        :param *id_list: the id's of those records affected by the operation

        """
        for on_change in self._on_change:
            await on_change(
                self.name,
                operation,
                *id_list
            )

    async def apply_processor(self, document):
        if self.processor:
            return await self.processor(document)

        return utils.base_processor(document)

    async def delete_many(self, query: dict, silent: bool = False) -> pymongo.results.DeleteResult:
        """
        Delete many documents based on the passed `query`.

        :param query: a MongoDB query
        :param silent: don't dispatch websocket messages for this operation
        :return: the delete result

        """
        id_list = await self.distinct("_id", query)

        delete_result = await self._collection.delete_many(query)

        if not silent and len(id_list):
            await self.enqueue_change("delete", *id_list)

        return delete_result

    async def delete_one(self, query: dict):
        """
        Delete a single document based on the passed `query`.

        :param query: a MongoDB query
        :return: the delete result

        """
        document_id = await utils.get_one_field(self, "_id", query)
        delete_result = await self._collection.delete_one(query)

        if delete_result.deleted_count:
            await self.enqueue_change(
                "delete",
                document_id
            )

        return delete_result

    async def find_one_and_update(
            self,
            query: dict,
            update: dict,
            projection: Union[None, dict, list] = None,
            upsert: bool = False
    ):
        """
        Update a document and return the updated result.

        :param query: a MongoDB query used to select the documents to update
        :param update: a MongoDB update
        :param projection: a projection to apply to the returned document instead of the default
        :param upsert: insert a new document if the query doesn't match an existing document
        :return: the updated document

        """
        document = await self._collection.find_one_and_update(
            query,
            update,
            return_document=pymongo.ReturnDocument.AFTER,
            upsert=upsert
        )

        if document is None:
            return None

        await self.enqueue_change("update", document["_id"])

        if projection:
            return utils.apply_projection(document, projection)

        return document

    async def insert_one(self, document: dict, silent: bool = False) -> dict:
        """
        Insert a document into the database collection
        :param silent: If True, updates will not be dispatched
        :param document: the document to insert
        """

        if "_id" not in document:
            document["_id"] = virtool_core.utils.random_alphanumeric(8)

        try:
            await self._collection.insert_one(document)
            if not silent:
                await self.enqueue_change("insert", document["_id"])

            return document
        except pymongo.errors.DuplicateKeyError:
            # randomly assigned _id is a duplicate
            document.pop("_id")
            return await self._collection.insert_one(document)

    async def replace_one(self, query: dict, replacement: dict, upsert=False, silent=False):
        """
        replace a document in the database collection
        :param query: the MongoDB query document
        :param replacement: the new document
        :param upsert: if True, a new document will be created if none are found.
        :param silent: if True, updates will not be dispatched
        :return: the newly added document
        """
        document = await self._collection.find_one_and_replace(
            query,
            replacement,
            projection=self.projection,
            upsert=upsert
        )

        if not silent:
            await self.enqueue_change(
                "update",
                replacement["_id"]
            )

        return document

    async def update_many(self, query, update, silent=False):
        updated_ids = await self.distinct("_id", query)
        update_result = await self._collection.update_many(query, update)

        if not silent:
            await self.enqueue_change("update", *updated_ids)

        return update_result

    async def update_one(self, query, update, upsert=False, silent=False):
        document = await self.find_one(query, ["_id"])
        update_result = await self._collection.update_one(query, update, upsert=upsert)

        if document and not silent:
            await self.enqueue_change(
                "update",
                document["_id"]
            )

        return update_result


async def connect_by_client(db_name: str, client: motor.motor_asyncio.AsyncIOMotorClient, *collection_names: str):
    """
    Connect to one or more MongoDB collections using the given :class:`AsyncIOMotorClient`
    :param db_name: name of the database containing the collections
    :param client: the :class:`motor.motor_asyncio.AsyncIOMotorClient` connection to MongoDB
    :param collection_names: the names of any desired connections
    :raises EnvironmentError: If the MongoDB version does not meet the minimum requirement
    :return:
        A :class:`Collection` instance if only one `collection_name` is provided

        A dict containing all requested collections indexed by the
        collection name, if multiple `collection_names` are provided
    """

    db = client[db_name]

    mongo_version = "4.4.0"
    current_version = (await client.server_info())["version"]

    if semver.compare(current_version, mongo_version) == -1:
        raise EnvironmentError(f"Virtool requires MongoDB {mongo_version}. Found {current_version}.")

    if len(collection_names) == 0:
        raise ValueError("must provide at-least one collection name")
    elif len(collection_names) == 1:
        return Collection(collection_names[0], db.get_collection(collection_names[0]))
    else:
        return {name: Collection(name, db.get_collection(name)) for name in collection_names}


async def connect(
        connection_string: str,
        db_name: str,
        *collection_names: str,
        timeout: int = 6000,
) -> Union[MutableMapping[str, Collection], Collection]:
    """
    Connect to one or more MongoDB database collections

    :param connection_string: the MongoDB connection string
    :param db_name: the name of the MongoDB database
    :param collection_names: the names of all collections to connect to
    :param timeout: the timeout for connecting to MongoDB
    :raises pymongo.errors.ServerSelectionTimeoutError
    :return:
        A :class:`Collection` instance if only one `collection_name` is provided

        A dict containing all requested collections indexed by the
        collection name, if multiple `collection_names` are provided
    """
    mongo = motor.motor_asyncio.AsyncIOMotorClient(
        connection_string,
        serverSelectionTimeoutMS=timeout
    )

    return await connect_by_client(db_name, mongo, *collection_names)




