import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

# Use REDIS_URL with fallback to localhost for development
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)