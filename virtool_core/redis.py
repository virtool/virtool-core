import asyncio
from structlog import get_logger
import sys
from contextlib import asynccontextmanager, suppress
from typing import Optional, AsyncGenerator
from redis import asyncio as aioredis
from redis import exceptions

logger = get_logger(__name__)


class Redis(aioredis.Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def subscribe(self, channel_name: str):
        channel = self.pubsub()
        await channel.subscribe(channel_name)
        return (channel,)

    async def lrange(self, name, start: int, end: int):
        names_list = await super().lrange(name, start, end)
        return [name for name in names_list]

    async def lpop(self, key):
        return (await super().lpop(key)).decode('utf-8')


class Channel(aioredis.client.PubSub):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConnectionClosedError(exceptions.TimeoutError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChannelClosedError(exceptions.TimeoutError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def create_redis_pool(redis_connection_string: str, **kwargs) -> Redis:
    return Redis.from_url(redis_connection_string, **kwargs)


async def check_redis_server_version(redis: Redis) -> Optional[str]:
    """
    Check the version of the server represented in the passed :class:`Redis` object.

    The version is logged and returned by the function.

    :param redis: the Redis connection
    :return: the version
    """
    info = await redis.info()
    version = info["redis_version"]
    logger.info(f"Found Redis {version}")


async def connect(redis_connection_string: str, timeout: int = 1) -> Redis:
    """
    Create a connection to Redis server specified in passed `redis_connection_string`.

    Will exit the application if the server cannot be reached.

    :param redis_connection_string: the Redis connection string
    :param timeout: DEPRECATED: Redis connection timeout
    :return: a Redis connection object

    """
    if not redis_connection_string.startswith("redis://"):
        logger.fatal("Invalid Redis connection string")
        sys.exit(1)

    logger.info("Connecting to Redis")

    try:
        redis = create_redis_pool(redis_connection_string)
        await check_redis_server_version(redis)

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


async def resubscribe(redis: Redis, redis_channel_name: str) -> Channel:
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
        redis_connection_string: str, timeout: int = 1
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
