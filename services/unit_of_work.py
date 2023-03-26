from adapters.repository import SqlAlchemyRepository
from abc import ABC, abstractmethod
from adapters.repository import AbstractRepository

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config


class AbstractUnitOfWork(ABC):
    bookmarks_repo: AbstractRepository
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for bookmark in self.bookmarks_repo.seen:
            while bookmark.events:
                yield bookmark.events.pop(0)

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    

    def collect_new_events(self):
        for bookmark in self.bookmarks_repo.seen:
            while bookmark.events:
                yield bookmark.events.pop(0)



DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        isolation_level="READ UNCOMMITTED",
    )
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.bookmarks_repo = SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()