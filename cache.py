from redis import asyncio as aioredis

import config

class RedisClient:
    def __init__(self) -> None:
        self.client = None
        self.key = "gpt_cache_"

    async def init_redis(self, addr, secret):
        l = addr.split(":")
        client = await aioredis.Redis(host=l[0], port=l[1], db=config.db, password=secret)
        self.client = client
        # client

    def get_key(self, user_id):
        return self.key+user_id

    def get_group_key(self, user_id, group_id):
        return self.key+group_id+"_"+user_id    

redis_client = RedisClient()
