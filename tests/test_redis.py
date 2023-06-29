from virtool_core.redis import connect_redis
import logging


async def test_redis_success(caplog, redis_connection_string):
    caplog.set_level(logging.WARNING)
    await connect_redis(redis_connection_string)
    for record in caplog.records:
        if record.levelname == "INFO":
            assert "Found Redis 6" in record.message
