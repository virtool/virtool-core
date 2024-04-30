import asyncio
import datetime
import json
from typing import AsyncGenerator, TypeAlias

import arrow
import orjson
import redis.asyncio
from redis.exceptions import ConnectionError as RedisConnectionError
from structlog import get_logger

logger = get_logger("redis")

RedisElement: TypeAlias = float | int | str | dict


class RedisError(Exception):
    """A generic error raised when interacting with Redis."""


class RedisChannelClosedError(RedisError):
    """An error raised when a Redis channel is closed while it is being read."""


def _coerce_redis_request(value: RedisElement | None) -> bytes | int | float:
    if isinstance(value, (int, float)):
        return value

    if isinstance(value, dict):
        return orjson.dumps(value)

    return str(value).encode("utf-8")


def _coerce_redis_response(value: bytes | str | int | None) -> RedisElement | None:
    if value is None:
        return None

    decoded = value.decode("utf-8")

    try:
        return int(decoded)
    except ValueError:
        ...

    try:
        return json.loads(decoded)
    except json.JSONDecodeError:
        ...

    return decoded


class Redis:
    """A Redis client based on ``redis``.

    Example:
    -------
    .. code-block:: python

        async with Redis("redis://localhost:6379") as redis:
            await redis.set("virtool", "The best virus detection platform")

            value = await redis.get("virtool"))
            # The best virus detection platform

    Features:

    * After successful connection, the client automatically pings the server to keep the
      connection alive.
    * The connection is automatically closed when the context manager exits.
    * Dictionaries, strings, integers, and floats are automatically serialized and
      deserialized.

    :param connection_string: the connection string for the Redis server

    """

    def __init__(self, connection_string: str):
        if not connection_string.startswith("redis://"):
            raise RedisError("Invalid Redis connection string")

        self._client = redis.asyncio.from_url(connection_string)
        """The underlying Redis client object."""

        self._client_info: dict | None = None
        """The Redis server information, first fetched when the connection is opened."""

        self._ping_task: asyncio.Task | None = None
        """A task that pings the Redis server every two minutes to keep the connection
        alive.
        """

        self.last_pong: datetime.datetime | None = None
        """The time of the last successful ping.

        `None` if no pings have been acknowledged.
        """

    async def __aenter__(self):
        logger.info("Connecting to Redis")

        try:
            self._client_info = await self._client.info()
        except RedisConnectionError as e:
            if "Connect call failed" in str(e):
                raise RedisError("Could not connect")

            if "invalid username-password" in str(e):
                raise RedisError("Could not authenticate: invalid username or password")

            raise RedisError(f"Unhandled client error: {e}")

        self._ping_task = asyncio.create_task(self._ping())

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._ping_task:
            logger.info("Disconnecting from Redis")
            self._ping_task.cancel()
            await self._ping_task

        if self._client:
            await self._client.aclose()

    async def _ping(self):
        """Ping the Redis server every two minutes.

        When using Azure Cache for Redis, connections inactive for more than 10 minutes
        are dropped. Regular pings prevent this from happening.

        """
        try:
            while True:
                if await self._client.ping() is True:
                    self.last_pong = arrow.utcnow().naive

                await asyncio.sleep(120)

        except asyncio.CancelledError:
            ...

    @property
    def server_version(self) -> str:
        """The version of the connected Redis server."""
        try:
            return self._client_info["redis_version"]
        except TypeError:
            raise RedisError(
                "Could not get server version because server info is not available.",
            )

    async def get(self, key: str) -> RedisElement | None:
        """Get the value at ``key``.

        :param key: the key to get
        :return: the value at ``key``
        """
        return _coerce_redis_response(await self._client.get(key))

    async def set(self, key: str, value: RedisElement, expire: int = 0):
        """Set the value at ``key`` to value with an optional expiration time in
        seconds.

        :param key: the key to set
        :param value: the value to set
        :param expire: the expiration time in seconds

        """
        if expire == 0:
            await self._client.set(key, _coerce_redis_request(value))
        else:
            await self._client.setex(key, expire, _coerce_redis_request(value))

    async def delete(self, key: str):
        """Delete the value at ``key``."""
        await self._client.delete(key)

    async def ttl(self, key: str) -> int:
        """Get the time-to-live for a ``key`` in seconds."""
        return await self._client.ttl(key)

    async def subscribe(self, channel_name: str) -> AsyncGenerator[RedisElement, None]:
        """Subscribe to a channel with ``channel_name`` and yield messages.

        Example:
        -------
        .. code-block:: python

                async for message in redis.subscribe("channel:cancel"):
                    print(message)

        :param channel_name: the name of the channel to subscribe to
        :return: an async generator that yields messages

        """
        async with self._client.pubsub() as pubsub:
            await pubsub.subscribe(channel_name)

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)

                if message is None:
                    continue

                yield _coerce_redis_response(message["data"])

    async def publish(self, channel_name: str, message: RedisElement):
        """Publish a message to a channel.

        :param channel_name: the name of the channel to publish to
        :param message: the message to publish

        """
        await self._client.publish(channel_name, _coerce_redis_request(message))

    async def blpop(self, key: str) -> RedisElement:
        """Remove and return the first element of the list at ``key``, or block until
        one is available.

        """
        _, value = await self._client.blpop([key])
        return _coerce_redis_response(value)

    async def llen(self, key: str) -> int:
        """Get the length of the list at ``key``.

        :param key: the key of the list to get the length of
        :return: the length of the list
        """
        return await self._client.llen(key)

    async def lrange(self, key: str, start: int, end: int) -> list[RedisElement]:
        """Get a range of elements from the list at ``key``.

        :param key: the key of the list to get from
        :param start: the start index
        :param end: the end index
        :return: a list of elements

        """
        return [
            _coerce_redis_response(value)
            for value in await self._client.lrange(key, start, end)
        ]

    async def lpop(self, key: str):
        """Remove and return the first element of the list at ``key``."""
        return _coerce_redis_response(await self._client.lpop(key))

    async def lrem(self, key: str, count: int, element: str):
        """Remove the first ``count`` elements from the list at ``key``.

        The ``count`` argument influences the following behaviours:

        * count > 0: Remove head to tail.
        * count < 0: Remove tail to head.
        * count = 0: Remove everywhere.

        :param key: the key of the list to remove from
        :param count: the number of elements to remove
        :param element: the element to remove

        """
        return await self._client.lrem(key, count, element)

    async def rpush(self, key: str, *values):
        """Push ``values`` onto the tail of the list ``key``.

        :param key: the key of the list to push to
        :param values: the values to push
        """
        return await self._client.rpush(
            key,
            *[_coerce_redis_request(v) for v in values],
        )

    async def flushdb(self):
        """Delete all keys in the current database."""
        await self._client.flushdb(asynchronous=False)
