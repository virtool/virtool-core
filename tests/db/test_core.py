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

    async def test_delete_many(self, test_motor, create_test_collection):
        collection = create_test_collection()

        await test_motor.samples.insert_many([
            {"_id": "foo", "tag": 1},
            {"_id": "bar", "tag": 2},
            {"_id": "baz", "tag": 1}
        ])

        delete_result = await collection.delete_many({"tag": 1})

        assert isinstance(delete_result, pymongo.results.DeleteResult)
        assert delete_result.deleted_count == 2

        collection._enqueue_change.assert_called_with("samples", "delete", *("baz", "foo"))

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

        collection._enqueue_change.assert_called_with("samples", "delete", "foo")

        assert await test_motor.samples.find().to_list(None) == [
            {"_id": "bar", "tag": 2},
            {"_id": "baz", "tag": 1}
        ]




