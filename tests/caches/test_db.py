import pytest
from aiohttp.test_utils import make_mocked_coro

import virtool_core.caches.db
import virtool_core.utils


@pytest.fixture
def trim_parameters():
    return {
        "end_quality": "20",
        "mode": "pe",
        "max_error_rate": "0.1",
        "max_indel_rate": "0.03",
        "max_length": None,
        "mean_quality": "25",
        "min_length": "20"
    }


def test_calculate_cache_hash(trim_parameters):
    hashed = virtool_core.caches.db.calculate_cache_hash(trim_parameters)
    assert hashed == "68b60be51a667882d3aaa02a93259dd526e9c990"


@pytest.mark.parametrize("exists", [True, False])
@pytest.mark.parametrize("missing", [True, False])
@pytest.mark.parametrize("returned_hash", ["abc123", "foobar"])
async def test_find(exists, missing, returned_hash, mocker, dbi):
    parameters = {
        "a": 1,
        "b": "hello",
        "c": "world"
    }

    if exists:
        await dbi.caches.insert_one({
            "_id": "bar",
            "program": "skewer-0.2.2",
            "hash": "abc123",
            "missing": missing,
            "sample": {
                "id": "foo"
            }
        })

    m_calculate_cache_hash = mocker.patch("virtool_core.caches.db.calculate_cache_hash", return_value=returned_hash)

    result = await virtool_core.caches.db.find(dbi, "foo", "skewer-0.2.2", parameters)

    m_calculate_cache_hash.assert_called_with(parameters)

    if missing or not exists or returned_hash == "foobar":
        assert result is None
        return

    assert result == {
        "id": "bar",
        "program": "skewer-0.2.2",
        "hash": "abc123",
        "missing": False,
        "sample": {
            "id": "foo"
        }
    }


@pytest.mark.parametrize("paired", [True, False], ids=["paired", "unpaired"])
async def test_create(paired, snapshot, dbi, static_time, test_random_alphanumeric, trim_parameters):
    """
    Test that the function works with default keyword arguments and when `paired` is either `True` or `False`.

    """
    cache = await virtool_core.caches.db.create(dbi, "foo", trim_parameters, paired)

    snapshot.assert_match(cache, "return")
    snapshot.assert_match(await dbi.caches.find_one(), "db")


async def test_create_legacy(snapshot, dbi, static_time, test_random_alphanumeric, trim_parameters):
    """
    Test that the function works when the `legacy` keyword argument is `True` instead of the default `False`.

    """
    cache = await virtool_core.caches.db.create(dbi, "foo", trim_parameters, False, legacy=True)

    snapshot.assert_match(cache, "return")
    snapshot.assert_match(await dbi.caches.find_one(), "db")


async def test_create_program(snapshot, dbi, static_time, test_random_alphanumeric, trim_parameters):
    """
    Test that the function works with a non-default trimming program keyword argument
    (trimmomatic-0.2.3 instead of skewer-0.2.2).

    """
    cache = await virtool_core.caches.db.create(dbi, "foo", trim_parameters, False, program="trimmomatic-0.2.3")

    snapshot.assert_match(cache, "return")
    snapshot.assert_match(await dbi.caches.find_one({"_id": test_random_alphanumeric.last_choice}), "db")


async def test_create_duplicate(snapshot, dbi, static_time, test_random_alphanumeric, trim_parameters):
    """
    Test that the function handles duplicate document ids smoothly. The function should retry with a new id.

    """
    await dbi.caches.insert_one({"_id": test_random_alphanumeric.next_choice[:8].lower()})

    cache = await virtool_core.caches.db.create(dbi, "foo", trim_parameters, False)

    snapshot.assert_match(cache, "return")
    snapshot.assert_match(await dbi.caches.find_one({"_id": test_random_alphanumeric.last_choice}), "db")


@pytest.mark.parametrize("exists", [True, False])
async def test_get(exists, dbi):
    """
    Test that the function returns a cache document when it exists and returns `None` when it does not.

    """
    if exists:
        await dbi.caches.insert_one({"_id": "foo"})

    result = await virtool_core.caches.db.get(dbi, "foo")

    if exists:
        assert result == {"id": "foo"}
        return

    assert result is None


@pytest.mark.parametrize("exception", [False, True])
async def test_remove(exception, dbi):
    run_in_thread = make_mocked_coro(raise_exception=FileNotFoundError) if exception else make_mocked_coro()

    await dbi.caches.insert_one({"_id": "baz"})

    await virtool_core.caches.db.remove(dbi, "/foo", "baz", run_in_thread)

    assert await dbi.caches.count_documents({}) == 0

    run_in_thread.assert_called_with(
        virtool_core.utils.rm,
        "/foo/caches/baz",
        True
    )
