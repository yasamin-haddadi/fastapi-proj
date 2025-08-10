from fastapi import FastAPI
from movie_app.core.config import get_settings
from contextlib import asynccontextmanager
from movie_app.infrastructure.database.session import DatabaseClient
from movie_app.infrastructure.redis.redis_client import RedisClient
from movie_app.core.logging_config import get_logger
from movie_app.auth.v1.routers.auth import router as auth_router
from movie_app.users.v1.routers.user import router as user_router
from sqlalchemy import text
from movie_app.initial_data.role_seeder import seed_roles
import asyncio

logger = get_logger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup
    logger.info("Starting app, connecting to services")

    # Initialize Database client (singleton)
    db_client = DatabaseClient(str(settings.DATABASE_URL))

    # Initialize Redis client (singleton)
    redis_client = RedisClient()

    # Optionally check connections:
    try:
        pong = await asyncio.to_thread(redis_client.client.ping)
        logger.info(f"Redis ping response: {pong}")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise e

    try:
        def db_check_and_seed():
            with db_client.get_session() as session:
                session.execute(text("SELECT 1"))
                seed_roles(session)

        await asyncio.to_thread(db_check_and_seed)  # ✅ تغییر مشابه بالا
        logger.info("Database connection successful and roles seeded")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e

    yield

    # shutdown
    logger.info("Closing connections, cleaning up")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
