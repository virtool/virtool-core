import asyncio
import logging
import sys
from contextlib import asynccontextmanager, suppress
from typing import Optional, AsyncGenerator

from aioredis import Redis, create_redis_pool, Channel, ConnectionClosedError

logger = logging.getLogger(__name__)


async def check_redis_server_version(redis: Redis) -> Optional[str]:
    """
    Check the version of the server represented in the passed :class:`Redis` object.

    The version is logged and returned by the function.

    :param redis: the Redis connection
    :return: the version
    """
    info = await redis.execute("INFO", encoding="utf-8")

    for line in info.split("\n"):
        if line.startswith("redis_version"):
            version = line.replace("redis_version:", "")
            logger.info(f"Found Redis {version}")

            return version

    return None


async def connect(redis_connection_string: str, timeout: int = 1) -> Redis:
    """
    Create a connection to Redis server specified in passed `redis_connection_string`.

    Will exit the application if the server cannot be reached.

    :param redis_connection_string: the Redis connection string
    :param timeout: max time to open a connection
    :return: a Redis connection object

    """
    if not redis_connection_string.startswith("redis://"):
        logger.fatal("Invalid Redis connection string")
        sys.exit(1)

    logger.info("Connecting to Redis")

    try:
        redis = await create_redis_pool(redis_connection_string, timeout=timeout)
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
            (channel,) = await redis.subscribe(redis_channel_name)
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
        redis = await connect(redis_connection_string, timeout)
        ping_task = asyncio.create_task(periodically_ping_redis(redis))
        yield redis
    finally:
        if ping_task is not None and redis is not None:
            logger.info("Disconnecting from Redis")
            ping_task.cancel()

            with suppress(asyncio.CancelledError):
                await ping_task

            redis.close()
            await redis.wait_closed()
