from redis import Redis

redis_client: Redis | None = None

def connect_to_redis():
    global redis_client
    redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def close_redis_connection():
    global redis_client
    if redis_client:
        redis_client.close()
