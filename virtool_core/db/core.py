import motor.motor_asyncio
import pymongo.results
import pymongo.errors
from functools import partial
from typing import Union, Callable, List, MutableMapping, Awaitable, Iterable
import virtool_core.utils
from . import utils


async def empty_processor(db, document):
    return document


async def no_op(*ids, **kwargs):
    return None


class Collection:
    """
    A wrapper for AsyncIOMotorCollection which dispatches updates via a provided
    callback function :func:`enqueue_change`
    """

    def __init__(
            self,
            name: str,
            collection: motor.motor_asyncio.AsyncIOMotorCollection,
            enqueue_change: Callable[[str, str, Iterable[str]], Awaitable[None]] = no_op,
            processor: Callable[["DB", MutableMapping], Awaitable[MutableMapping]] = empty_processor,
            projection: Union[None, List, MutableMapping] = None,
    ):
        """

        :param name: name of the collection
        :param collection: the :class:`motor.motor_asyncio.AsyncIOMotorCollection to wrap
        :param enqueue_change: function which is called when the database changes, defaults to a NOP
        :param processor: function applied to the mongodb document before it is returned.
        :param projection: the mongodb projection
        """
        self.name = name
        self._collection = collection
        self._enqueue_change = enqueue_change
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

    async def enqueue_change(self, operation: str, *id_list):
        """
        Dispatch updates if the collection is not `silent` and the `silent` parameter is `False`. Applies the collection
        projection and processor.

        :param operation: the operation to label the dispatch with (insert, update, delete)
        :param *id_list: the id's of those records affected by the operation

        """
        await self._enqueue_change(
            self.name,
            operation,
            *id_list
        )

    async def apply_processor(self, document):
        if self.processor:
            return await self.processor(self._collection.database, document)

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

    async def insert_one(self, document: dict) -> dict:
        """
        Insert a document into the database collection
        :param document: the document to insert
        """

        if "_id" not in document:
            document["_id"] = virtool_core.utils.random_alphanumeric(8)

        try:
            await self._collection.insert_one(document)
            await self.enqueue_change("insert", document["_id"])

            return document
        except pymongo.errors.DuplicateKeyError:
            # randomly assigned _id is a duplicate
            document.pop("_id")
            return await self._collection.insert_one(document)

    async def replace_one(self, query, replacement, upsert=False):
        document = await self._collection.find_one_and_replace(
            query,
            replacement,
            projection=self.projection,
            upsert=upsert
        )

        await self.enqueue_change(
            "update",
            replacement["_id"]
        )

        return document

    async def update_many(self, query, update):
        updated_ids = await self.distinct("_id", query)
        update_result = await self._collection.update_many(query, update)

        await self.enqueue_change("update", *updated_ids)

        return update_result

    async def update_one(self, query, update, upsert=False):
        document = await self.find_one(query, ["_id"])
        update_result = await self._collection.update_one(query, update, upsert=upsert)

        if document:
            await self.enqueue_change(
                "update",
                document["_id"]
            )

        return update_result


class DB:
    pass