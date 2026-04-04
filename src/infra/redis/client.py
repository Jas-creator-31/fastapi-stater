import redis
from dotenv import load_dotenv
import os

load_dotenv()

redis_host: str = os.getenv("REDIS_HOST")
redis_port: str = os.getenv("REDIS_PORT")
redis_db: str = os.getenv("REDIS_DB")

r = redis.Redis(host=redis_host, port=int(redis_port), db=int(redis_db))

