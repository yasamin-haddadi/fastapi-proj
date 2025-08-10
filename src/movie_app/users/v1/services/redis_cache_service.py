from redis import Redis
import json
from typing import Optional

class UserCacheService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    @staticmethod
    def _get_key(user_id: str) -> str:
        return f"user:{user_id}"

    def set_user_cache(self, user_id: str, data: dict, expire_seconds: int = 3600):
        key = self._get_key(user_id)
        self.redis.set(key, json.dumps(data), ex=expire_seconds)

    def get_user_cache(self, user_id: str) -> Optional[dict]:
        key = self._get_key(user_id)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def delete_user_cache(self, user_id: str):
        key = self._get_key(user_id)
        self.redis.delete(key)