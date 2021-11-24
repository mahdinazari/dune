import redis

from .config import Config


r = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT, 
    db=Config.REDIS_DB
    #password=Config.REDIS_PASSWORD,
)
