from redis import asyncio as redis
from dotenv import load_dotenv
import os

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")


async def get_redis():
    r = redis.Redis(
        host=redis_host,  # type: ignore
        port=int(redis_port),  # type: ignore
        db=int(redis_db),  # type: ignore
        decode_responses=True
    )
    r.config_set("save", "900 1 300 10 60 10000")
    try:
        yield r
    finally:
        await r.close()
