import pytest

from virtool_core.redis import Redis, connect
import logging


async def test_redis_success(caplog, redis_connection_string):
    caplog.set_level(logging.WARNING)
    await connect(redis_connection_string)
    for record in caplog.records:
        if record.levelname == "INFO":
            assert "Found Redis 6" in record.message


@pytest.mark.asyncio
async def test_redis_set_get(redis_connection_string):
    redis = Redis(redis_connection_string)
    await redis.set("key", "value")
    value = await redis.get("key")
    assert value == "value"
    await redis.close()


@pytest.mark.asyncio
async def test_redis_delete(redis_connection_string):
    redis = Redis(redis_connection_string)
    await redis.set("key", "value")
    await redis.delete("key")
    value = await redis.get("key")
    assert value is None
    await redis.close()


@pytest.mark.asyncio
async def test_redis_ttl(redis_connection_string):
    redis = Redis(redis_connection_string)
    await redis.set("key", "value", ex=10)
    ttl = await redis.ttl("key")
    assert ttl > 0
    await redis.close()


@pytest.mark.asyncio
async def test_redis_subscribe_publish(redis_connection_string):
    redis = Redis(redis_connection_string)
    channel = await redis.subscribe("test_channel")
    await redis.publish("test_channel", "test_message")
    message = await channel.get_message()
    assert message["data"].decode() == "test_message"
    await redis.close()

@pytest.mark.asyncio
async def test_redis_blpop(redis_connection_string):
    redis = Redis(redis_connection_string)
    await redis.rpush("test_list", "item1", "item2")
    item = await redis.blpop("test_list")
    assert item[1].decode() == "item1"
    await redis.close()


@pytest.mark.asyncio
async def test_redis_lrange(redis_connection_string):
    redis = Redis(redis_connection_string)
    await redis.rpush("test_list", "item1", "item2", "item3")
    items = await redis.lrange("test_list", 0, -1)
    assert [item.decode() for item in items] == ["item1", "item2", "item3"]
    await redis.close()


@pytest.mark.asyncio
async def test_redis_flushdb(redis_connection_string):
    redis = Redis(redis_connection_string)
    await redis.set("key", "value")
    await redis.flushdb()
    value = await redis.get("key")
    assert value is None
    await redis.close()


@pytest.mark.asyncio
async def test_connect_invalid_url():
    with pytest.raises(SystemExit):
        await connect("invalid_url")
