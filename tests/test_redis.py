import asyncio

import pytest

from virtool_core.redis import Redis, RedisError


class TestConnect:
    async def test_ok_and_ping(self, redis: Redis):
        assert redis.server_version.startswith("6.")
        await asyncio.sleep(0.3)
        assert redis.last_pong is not None

    async def test_address_fail(self):
        with pytest.raises(RedisError) as e:
            async with Redis("redis://localhost:6374") as _:
                ...

        assert "Could not connect" in str(e.value)

    async def test_auth_fail(self, redis_connection_string: str):
        with pytest.raises(RedisError) as e:
            async with Redis(redis_connection_string.replace("virtool", "wrong")) as _:
                ...

        assert str(e.value) == "Could not authenticate: invalid username or password"

    async def test_connect_close(self, redis_connection_string: str):
        """Test that we can connect to a Redis server and close the connection without
        using the context manager.
        """
        redis = Redis(redis_connection_string)
        await redis.connect()

        assert redis.server_version.startswith("6.")

        # Sleep so that ping gets into the try-except block and CancelledError can be
        # handled.
        await asyncio.sleep(0.3)
        await redis.close()


class TestGet:
    async def test_str(self, redis: Redis):
        """Test that we can set and get a string value from Redis."""
        await redis.set("key", "value")
        value = await redis.get("key")
        assert value == "value"

    async def test_int(self, redis: Redis):
        """Test that we can set and get an integer value from Redis."""
        await redis.set("key", 1)
        value = await redis.get("key")
        assert value == 1

    async def test_json(self, redis: Redis):
        """Test that we can set and get JSON from Redis with automatic serialization and
        deserialization.
        """
        await redis.set("key", {"a": 1})
        assert await redis.get("key") == {"a": 1}

    async def test_does_not_exist(self, redis: Redis):
        assert await redis.get("key") is None


class TestDelete:
    async def test_ok(self, redis: Redis):
        """Test that we can delete a key from Redis."""
        await redis.set("key", "value")
        assert await redis.delete("key") is None
        assert await redis.get("key") is None

    async def test_does_not_exist(self, redis: Redis):
        """Test that deleting a key that does not exist does not raise an error."""
        assert await redis.delete("key") is None


class TestExpireAndTTL:
    async def test_no_expire(self, redis: Redis):
        """Test that a key with no expiration time set has a TTL of -1."""
        await redis.set("key", "value")
        assert await redis.ttl("key") == -1

    async def test_expire(self, redis: Redis):
        """Test that a key with an expiration time set has a reasonable TTL."""
        await redis.set("key", "value", expire=60)
        await asyncio.sleep(1)
        assert 60 > await redis.ttl("key") > 57


@pytest.mark.parametrize("value", ["value", 1, {"a": 1}], ids=["str", "int", "json"])
async def test_pubsub(value, redis: Redis):
    """Test that we can publish and subscribe to a channel."""

    async def listen():
        async for message in redis.subscribe("channel"):
            assert message == value
            return

    task = asyncio.create_task(listen())
    await asyncio.sleep(0.3)

    await redis.publish("channel", value)
    await asyncio.sleep(0.3)

    await task


async def test_rpush_and_blpop(redis: Redis):
    """Test that we can push and pop a value from a list."""
    await redis.rpush("key", "buffer")
    await redis.rpush("key", 1)
    await redis.rpush("key", "value")
    await redis.rpush("key", {"a": 1})

    assert await redis.blpop("key") == "buffer"
    assert await redis.blpop("key") == 1
    assert await redis.blpop("key") == "value"
    assert await redis.blpop("key") == {"a": 1}


class TestLpop:
    async def test_ok(self, redis: Redis):
        """Test that we can pop a value from a list."""
        await redis.rpush("key", "buffer")
        await redis.rpush("key", 1)

        assert await redis.lpop("key") == "buffer"
        assert await redis.lpop("key") == 1

    async def test_empty(self, redis: Redis):
        """Test that popping from an empty list returns None."""
        assert await redis.lpop("key") is None


async def test_llen(redis: Redis):
    """Test that get the correct value for a list's length."""
    assert await redis.llen("key") == 0
    await redis.rpush("key", "item1", "item2", "item3")
    assert await redis.llen("key") == 3


async def test_lrange(redis: Redis):
    """Test that we can get a range of values from a list."""
    await redis.rpush("key", "item1", "item2", "item3")

    assert await redis.lrange("key", 0, -1) == ["item1", "item2", "item3"]
    assert await redis.lrange("key", 0, 1) == ["item1", "item2"]


async def test_lrem(redis: Redis):
    """Test that we can remove values from a list."""
    await redis.rpush("key", "item1", "item2", "item3")
    await redis.lrem("key", 1, "item2")

    assert await redis.lrange("key", 0, -1) == ["item1", "item3"]


async def test_flushdb(redis: Redis):
    """Test that we can flush the Redis database."""
    await redis.set("key", "value   ")
    await redis.rpush("list", "item1", "item2")
    await redis.flushdb()

    assert await redis.get("key") is None
    assert await redis.lrange("list", 0, -1) == []
