from fastapi import Depends
from sqlalchemy.orm import Session
from movie_app.infrastructure.database.deps import get_db
from movie_app.users.v1.services.user_service import UserService


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)



# ================================
from redis import Redis
from movie_app.infrastructure.redis.deps import get_redis
from movie_app.users.v1.services.redis_cache_service import UserCacheService


def get_redis_cache_service(redis_client: Redis = Depends(get_redis)) -> UserCacheService:
    return UserCacheService(redis_client)

