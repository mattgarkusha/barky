from adapters.BookmarkRepository import BookmarkRepository
from .AbstractUnitOfWork import AbstractUnitOfWork

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        isolation_level="REPEATABLE READ",
    )
)

class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.bookmarks_repo = BookmarkRepository()
        return super().__enter__()

    def __exit__(self, *args):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()