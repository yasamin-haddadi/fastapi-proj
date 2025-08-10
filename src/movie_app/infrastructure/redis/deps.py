from fastapi import Depends
from movie_app.infrastructure.redis.redis_client import RedisClient
from redis import Redis


def get_redis() -> Redis:
    return RedisClient().client