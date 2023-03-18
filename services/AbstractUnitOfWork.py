from adapters.AbstractRepository import AbstractRepository

from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    bookmarks_repo: AbstractRepository
    
    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, *args):
        pass