from movie_app.core.config import get_settings, Settings
from movie_app.infrastructure.database.session import DatabaseClient
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db(settings: Settings =Depends(get_settings)) -> Session:

    db_client = DatabaseClient(str(settings.DATABASE_URL))
    db = db_client.get_session()
    try:
        yield db
    finally:
        db_client.close_session(db)
