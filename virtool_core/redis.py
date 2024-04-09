import asyncio

from redis.commands.core import ResponseT
from structlog import get_logger
import sys
from contextlib import asynccontextmanager, suppress
from typing import Optional, AsyncGenerator, Union, Awaitable
import redis.asyncio
import redis.exceptions

logger = get_logger(__name__)


class Redis(redis.asyncio.Redis):
    def __init__(self, redis_connection_string, **kwargs):
        self._client = redis.asyncio.from_url(redis_connection_string, **kwargs)

    async def client(self, *args, **kwargs):
        return self._client.client()

    async def get(self, *args, **kwargs):
        return await self._client.get(*args, **kwargs)

    async def set(self, key, value, ex=None, nx=False, **kwargs):
        return await self._client.set(key, value, ex=ex, nx=nx, **kwargs)

    async def delete(self, key):
        return await self._client.delete(key)

    async def ttl(self, session_identifier):
        return await self._client.ttl(session_identifier)

    async def subscribe(self, channel_name: str):
        channel = self._client.pubsub()
        await channel.subscribe(channel_name)
        return channel

    async def publish(self, channel_name: str, message: str):
        return await self._client.publish(channel_name, message)

    async def llen(self, name: str) -> Union[Awaitable[int], int]:
        return await self._client.llen(name)

    async def lrange(self, name, start: int, end: int):
        names_list = await self._client.lrange(name, start, end)
        return names_list

    async def lpop(self, key):
        return (await self._client.lpop(key)).decode('utf-8')

    async def lrem(self, key, count, element):
        return await self._client.lrem(key, count, element)

    async def rpush(self, key, *values):
        return await self._client.rpush(key, *values)

    async def flushdb(self, asynchronous: bool = False, **kwargs) -> ResponseT:
        return await self._client.flushdb(asynchronous)

    async def close(self):
        return await self._client.close()

    async def check_redis_server_version(self) -> Optional[str]:
        """
        Check the version of the server represented in the passed :class:`Redis` object.

        The version is logged and returned by the function.

        :param redis: the Redis connection
        :return: the version
        """
        info = await self._client.info()
        version = info["redis_version"]
        logger.info(f"Found Redis {version}")

        return version



class ConnectionClosedError(redis.exceptions.TimeoutError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChannelClosedError(redis.exceptions.TimeoutError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


async def connect(redis_connection_string: str) -> Redis:
    """
    Create a connection to Redis server specified in passed `redis_connection_string`.

    Will exit the application if the server cannot be reached.

    :param redis_connection_string: the Redis connection string
    :return: a Redis connection object

    """
    if not redis_connection_string.startswith("redis://"):
        logger.fatal("Invalid Redis connection string")
        sys.exit(1)

    logger.info("Connecting to Redis")

    try:
        redis = Redis(redis_connection_string)
        await redis.check_redis_server_version()

        return redis
    except ConnectionRefusedError:
        logger.fatal("Could not connect to Redis: Connection refused")
        sys.exit(1)


async def periodically_ping_redis(redis: Redis):
    """
    Ping the Redis server every two minutes.

    When using Azure Cache for Redis, connections inactive for more than 10 minutes
    are dropped. Regular pings prevent this from happening.

    :param redis: the Redis client
    """
    while True:
        await asyncio.sleep(120)
        await redis.ping()


async def resubscribe(redis: Redis, redis_channel_name: str):
    """
    Subscribe to the passed channel of the passed :class:`Redis` object.

    :param redis: the Redis connection
    :param redis_channel_name: name of the channel to reconnect to
    :return: Channel

    """
    while True:
        try:
            (channel,) = await redis.pubsub().subscribe(redis_channel_name)
            return channel
        except (ConnectionRefusedError, ConnectionResetError, ConnectionClosedError):
            await asyncio.sleep(5)


@asynccontextmanager
async def configure_redis(
        redis_connection_string: str
) -> AsyncGenerator[Redis, None]:
    """Prepare a redis connection."""
    redis = None
    ping_task = None

    try:
        redis = await connect(redis_connection_string)
        ping_task = asyncio.create_task(periodically_ping_redis(redis))
        yield redis
    finally:
        if ping_task is not None and redis is not None:
            logger.info("Disconnecting from Redis")
            ping_task.cancel()

            with suppress(asyncio.CancelledError):
                await ping_task

            await redis.close()
