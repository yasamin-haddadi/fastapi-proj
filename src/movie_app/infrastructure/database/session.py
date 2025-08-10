from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
#from movie_app.infrastructure.database.base import Base
from movie_app.core.logging_config import get_logger

logger = get_logger(__name__)


class DatabaseClient:
    _instance = None

    def __new__(cls, database_url: str):
        if cls._instance is None:
            cls._instance = super(DatabaseClient, cls).__new__(cls)
            cls._instance._initialize(database_url)
        return cls._instance

    def _initialize(self, database_url: str) -> None:
        self.engine = create_engine(database_url, pool_recycle=3600)
        self.session_factory = sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self.engine,
        )
        self.scoped_session =scoped_session(self.session_factory)

    # Create all tables in the database based on SQLAlchemy models metadata
    # def create_tables(self) -> None:
    #     Base.metadata.create_all(bind=self.engine)

    # Drop all tables in the database based on SQLAlchemy models metadata
    # def drop_tables(self) -> None:
    #     Base.metadata.drop_all(bind=self.engine)


    def get_session(self) -> Session:
        return self.scoped_session()

    def close_session(self, session: Session = None) -> None:
        if session:
            session.close()
            self.scoped_session.remove()


    # Optional context manager methods (__enter__, __exit__)
    # Uncomment if you want to use 'with DatabaseClient() as session' syntax
    def __enter__(self) -> Session:
        self._session_instance = self.get_session()
        return self._session_instance

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_session(self._session_instance)
        if exc_type:
            logger.error("Exception in DB session", exc_info=(exc_type, exc_val, exc_tb))
