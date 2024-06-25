from redis.asyncio import Redis

from todoapp.common.settings import Config


async def build_redis_client(
    config: Config
) -> Redis:
    client = Redis.from_url(str(config.redis_url))
    await client.ping()

    return client
