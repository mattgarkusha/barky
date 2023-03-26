from domain.model import Bookmark
from typing import List, Set
from abc import ABC, abstractmethod
from datetime import datetime
from domain import model

class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set() # type: Set[model.Bookmark]
    
    @abstractmethod
    def get_all(self, sort_field=None, sort_descending=False):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def create(self, bookmark: Bookmark):
        raise NotImplementedError

    @abstractmethod
    def update(self, bookmark: Bookmark):
        raise NotImplementedError

    @abstractmethod
    def delete(self, bookmark: Bookmark):
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
    
    def get_all(self, sort_field=None, sort_descending=False) -> List[Bookmark]:
        query = self.session.query(Bookmark)
        if sort_field is not None:
            sort_attr = getattr(Bookmark, sort_field)
            if sort_descending:
                query = query.order_by(sort_attr.desc())
            else:
                query = query.order_by(sort_attr)
        bookmarks = query.all()
        # for bookmark in bookmarks:
        #     self.seen.add(bookmark)
        print(bookmarks)
        return bookmarks

    def get_by_id(self, id) -> Bookmark:
        bookmark = self.session.get(Bookmark, id)
        # if bookmark:
        #     self.seen.add(bookmark)
        return bookmark

    def create(self, bookmark: Bookmark) -> Bookmark:
        now = datetime.now()
        bookmark.created_at = now
        bookmark.updated_at = now
        self.session.add(bookmark)
        self.session.commit()
        # if bookmark:
        #     self.seen.add(bookmark)
        return bookmark

    def update(self, bookmark: Bookmark) -> Bookmark:
        now = datetime.now()
        bookmark.updated_at = now
        self.session.commit()
        # if bookmark:
        #     self.seen.add(bookmark)
        return bookmark

    def delete(self, id) -> Bookmark:
        bookmark = self.get_by_id(id)
        self.session.delete(bookmark)
        self.session.commit()
        # if bookmark:
        #     self.seen.add(bookmark)
        return bookmark