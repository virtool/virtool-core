import pytest
from pytest_mock import MockerFixture
from syrupy import SnapshotAssertion

from virtool_core.mongo import buffered_bulk_writer


@pytest.mark.parametrize("batch_size", (60, 100))
async def test_buffered_bulk_writer(
    batch_size: int, snapshot: SnapshotAssertion, mocker: MockerFixture
):
    collection = mocker.Mock()
    collection.bulk_write = mocker.AsyncMock()

    async with buffered_bulk_writer(collection, batch_size=batch_size) as writer:
        for number in range(372):
            await writer.add(number)

    assert collection.bulk_write.call_args_list == snapshot
