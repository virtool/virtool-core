import aioredis


class CoreRedis(aioredis.Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
