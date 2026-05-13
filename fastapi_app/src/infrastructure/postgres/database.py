from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.core.config import settings


class Database:
    def __init__(self):
        self._db_url = settings.database_url
        self._engine = create_engine(self._db_url)

    @contextmanager
    def session(self):
        Session = sessionmaker(bind=self._engine, expire_on_commit=False)
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


database = Database()
Base = declarative_base()