from redis import asyncio as aioredis

import config


class RedisClient:
    def __init__(self) -> None:
        self.client = None

    async def init_redis(self, addr, secret):
        l = addr.split(":")
        client = await aioredis.Redis(host=l[0], port=l[1], db=config.db, password=secret)
        self.client = client
        # client

    def get_key(self, user_id):
        return "gpt_cache_"+user_id

redis_client = RedisClient()
