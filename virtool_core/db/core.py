from typing import Optional
from typing import Union, List, MutableMapping

import motor.motor_asyncio
import pymongo.errors
import pymongo.results

import virtool_core.utils
import virtool_core.utils
from . import utils
from .bindings import BINDINGS, DatabaseUpdateListener, Processor


class Collection:
    """
    A wrapper for AsyncIOMotorCollection which dispatches updates via a provided
    callback function :func:`enqueue_change`
    """

    def __init__(
            self,
            name: str,
            collection: motor.motor_asyncio.AsyncIOMotorCollection,
            enqueue_change: DatabaseUpdateListener = None,
            processor: Processor = None,
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
        Dispatch an update about this collection


        :param operation: the operation to label the dispatch with (insert, update, delete)
        :param *id_list: the id's of those records affected by the operation

        """
        if self._enqueue_change:
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
        :param silent: if True, don't dispatch updates for this operation
        :return: the delete result

        """
        id_list = await self.distinct("_id", query)

        delete_result = await self._collection.delete_many(query)

        if not silent and len(id_list):
            await self.enqueue_change("delete", *id_list)

        return delete_result

    async def delete_one(self, query: dict, silent: bool = False):
        """
        Delete a single document based on the passed `query`.

        :param query: a MongoDB query
        :param silent: if True, don't dispatch updates for this operation
        :return: the delete result

        """
        document_id = await utils.get_one_field(self, "_id", query)
        delete_result = await self._collection.delete_one(query)

        if delete_result.deleted_count and not silent:
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
            upsert: bool = False,
            silent: bool = False,
    ):
        """
        Update a document and return the updated result.

        :param query: a MongoDB query used to select the documents to update
        :param update: a MongoDB update
        :param projection: a projection to apply to the returned document instead of the default
        :param upsert: insert a new document if the query doesn't match an existing document
        :param silent: if True, don't dispatch updates for this operation
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

        if not silent:
            await self.enqueue_change("update", document["_id"])
        await self.enqueue_change("update", document["_id"])

        if projection:
            return utils.apply_projection(document, projection)

        return document

    async def insert_one(self, document: dict, silent: bool = False) -> dict:
        """
        Insert a document into the database collection
        
        :param document: the document to insert
        :param silent: if True, don't dispatch updates for this operation
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

    async def replace_one(self, query: dict, replacement: dict, upsert: bool = False, silent: bool = False):
        """
        Replace a document in the database collection
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

    async def update_many(self, query: dict, update: dict, silent: bool = False):
        """
        Apply an update to multiple documents in the collection
        :param query: The MongoDB query document
        :param update: The MongoDB update document or replacement document
        :param silent: if True, updates will not be dispatched
        :return: The result of the update
        """

        updated_ids = await self.distinct("_id", query)
        update_result = await self._collection.update_many(query, update)

        if not silent:
            await self.enqueue_change("update", *updated_ids)

        return update_result

    async def update_one(self, query: dict, update: dict, upsert: bool = False, silent: bool = False):
        """
        :param query: The MongoDB query document
        :param update: The MongoDB update document or replacement document
        :param upsert: If True, the update document will be inserted if there is no document matching the query
        :param silent: if True, updates will not be dispatched
        :return: The result of the update
        """

        document = await self.find_one(query, ["_id"])
        update_result = await self._collection.update_one(query, update, upsert=upsert)

        if document and not silent:
            await self.enqueue_change(
                "update",
                document["_id"]
            )

        return update_result


class DB:
    """
    Main interface to the Virtool database
    """
    def __init__(
            self,
            motor_client: motor.motor_asyncio.AsyncIOMotorClient,
            enqueue_change: Optional[DatabaseUpdateListener],
    ):
        """
        :param motor_client: The :class:`motor.motor_asyncio.AsyncIOMotorClient` instance
        :param enqueue_change: A callback function for receiving database update events
        """

        self.motor_client = motor_client
        self.enqueue_change = enqueue_change
        for binding in BINDINGS:
            collection = Collection(
                binding.collection_name,
                motor_client[binding.collection_name],
                None if binding.silent else enqueue_change,
                binding.processor,
                binding.projection,
            )
            setattr(self, binding.collection_name, collection)
