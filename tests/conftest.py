import pytest
from virtool_core.redis import Redis


@pytest.fixture()
async def _redis_with_connection_string(request):
    _redis_connection_string = request.config.getoption("--redis-connection-string")

    async with Redis(_redis_connection_string) as _redis:
        yield _redis, _redis_connection_string
        await _redis.flushdb()


@pytest.fixture()
async def redis(_redis_with_connection_string: tuple[Redis, str]):
    """A Redis client instance."""
    return _redis_with_connection_string[0]


@pytest.fixture()
async def redis_connection_string(_redis_with_connection_string: tuple[Redis, str]):
    """The connection string for a Redis test instance."""
    return _redis_with_connection_string[1]


def pytest_addoption(parser):
    parser.addoption(
        "--redis-connection-string",
        action="store",
        default="redis://:virtool@localhost:9003",
    )
