from redis.asyncio import Redis

from todoapp.common.settings import Config


async def build_redis_client(
    config: Config
) -> Redis:
    client = Redis.from_url(str(config.redis_url))

    yield client

    await client.aclose()


async def ping_redis_client(client: Redis):
    await client.ping()
