import util.config
import redis.asyncio as redis

r = redis.Redis(
    host=util.config.REDIS_HOST,
    port=util.config.REDIS_PORT,
    db=util.config.REDIS_DB,
    decode_responses=True,
)


async def initialize_redis():
    await r.ping()
    print("Connected to Redis!")
