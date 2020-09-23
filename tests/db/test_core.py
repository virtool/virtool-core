import pymongo.results
import pytest
from aiohttp.test_utils import make_mocked_coro

from virtool_core import db


@pytest.mark.parametrize("document,result", [
    (None, None),
    ({"_id": "foo"}, {"id": "foo"}),
    ({"id": "foo"}, {"id": "foo"}),
])
def test_base_processor(document, result):
    assert db.utils.base_processor(document) == result


@pytest.fixture
def create_test_collection(mocker, test_motor):
    def func(name="samples", projection=None) -> db.Collection:
        processor = make_mocked_coro(return_value={"id": "foo", "mock": True})

        return db.Collection(
            name,
            test_motor[name],
            make_mocked_coro(),
            processor,
            projection,
        )

    return func


class TestCollection:

    @pytest.mark.parametrize("projection", [None, ["name"]], ids=["projection", "no projection"])
    def test_apply_projection(self, projection, create_test_collection):
        """
        Test that :meth:`Collection.apply_projection` returns a projected version of the passed document when
        :attr:`Collection.projection` is defined and returns the document untouched when no projection is defined.

        """
        collection = create_test_collection(projection=projection)

        document = {
            "_id": "foo",
            "name": "Foo",
            "tags": [
                "bar",
                "baz"
            ]
        }

        projected = collection.apply_projection(document)

        if projection:
            assert projected == {
                "_id": "foo",
                "name": "Foo"
            }
            return

        assert projected == document

    @pytest.mark.parametrize("param_silent", [True, False])
    async def test_delete_many(self, param_silent, test_motor, create_test_collection):
        collection = create_test_collection()

        await test_motor.samples.insert_many([
            {"_id": "foo", "tag": 1},
            {"_id": "bar", "tag": 2},
            {"_id": "baz", "tag": 1}
        ])

        delete_result = await collection.delete_many({"tag": 1}, silent=param_silent)

        assert isinstance(delete_result, pymongo.results.DeleteResult)
        assert delete_result.deleted_count == 2

        if not param_silent:
            collection._on_change[0].assert_called_with("samples", "delete", "baz", "foo")

        assert await test_motor.samples.find().to_list(None) == [
            {"_id": "bar", "tag": 2}
        ]

    async def test_delete_one(self, test_motor, create_test_collection):
        collection = create_test_collection()

        await test_motor.samples.insert_many([
            {"_id": "foo", "tag": 1},
            {"_id": "bar", "tag": 2},
            {"_id": "baz", "tag": 1}
        ])

        delete_result = await collection.delete_one({"tag": 1})

        assert isinstance(delete_result, pymongo.results.DeleteResult)
        assert delete_result.deleted_count == 1

        collection._on_change[0].assert_called_with("samples", "delete", "foo")

        assert await test_motor.samples.find().to_list(None) == [
            {"_id": "bar", "tag": 2},
            {"_id": "baz", "tag": 1}
        ]

        
async def test_connect(self, test_db_connection_string, test_db_name):
    testdb = await db.connect(test_db_connection_string, test_db_name, "test")

    on_change = make_mocked_coro()
    testdb.on_change(on_change)

    await testdb.insert_one({"_id":"test"})
    on_change.assert_called_with("test", "insert", "test")
    
async def test_connect_multiple_collections(self, test_db_connection_string, test_db_name):
    collections = await db.connect(test_db_connection_string, test_db_name, "collection1", "collection2", "collection3")
    assert len(collections.values()) == 3

    for name, collection in collections.items():
        coro = make_mocked_coro()
        collection.on_change(coro)
        await collection.insert_one({"_id": "test"})
        coro.assert_called_with(name, "insert", "test")

