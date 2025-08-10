from movie_app.core.config import get_settings
from redis import Redis
from redis.exceptions import ConnectionError, TimeoutError
import logging
import time


logger = logging.getLogger(__name__)
settings = get_settings()

class RedisClient:
    _instance = None
    _client: Redis = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        attempts = 2  # مثلا 2 بار تلاش
        for attempt in range(attempts):
            try:
                self._client = Redis.from_url(
                    str(settings.REDIS_URL),
                    decode_responses=True,
                    socket_timeout=5,
                    health_check_interval=30
                )
                self._client.ping()
                logger.info("Connected to Redis successfully.")
                return
            except (ConnectionError, TimeoutError) as e:
                logger.error(f"Failed to connect to Redis (attempt {attempt + 1}): {e}")
                if attempt < attempts - 1:
                    time.sleep(2)
            except Exception as e:
                logger.exception(f"Failed to connect to Redis: {e}")
                raise
        raise ConnectionError("Could not connect to Redis after retries.")


    @property
    def client(self) -> Redis:
        try:
            self._client.ping()
        except (ConnectionError, TimeoutError):
            logger.warning("Redis connection lost. Reconnecting...")
            self._connect()
        return self._client

    def close(self):
        if self._client:
            try:
                self._client.close()
                logger.info("Redis connection closed.")

            except (ConnectionError, TimeoutError) as e:
                logger.error(f"Error closing Redis connection: {e}")

            except Exception as e:
                logger.exception(f"Error closing Redis connection: {e}")