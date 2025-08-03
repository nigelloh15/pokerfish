from typing import Optional
from redis.asyncio import Redis

redis_client: Redis

async def connect_to_redis() -> Redis:
    global redis_client
    redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

    try:
        await redis_client.ping()
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Redis: {e}")

    return redis_client

async def close_redis_connection():
    global redis_client
    if redis_client:
        await redis_client.close()

