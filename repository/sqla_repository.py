# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base_repository import BaseRepository
from .models import Base, BookmarkModel

class SQLARespository(BaseRepository):
    """
    Uses guidance from the basic SQLAlchemy 1.3 tutorial: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
    """

    def __init__(self, url=None) -> None:
        #this is where you either connect directly to the DB, or set up the ORM
        super().__init__()

        self.engine = None

        # create db connection
        if url != None:
            self.engine = create_engine(url)
        else:
            self.engine = create_engine('sqlite:///:memory:', echo=True)

        # ensure tables are there
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_one(self, bookmark: BookmarkModel) -> int:
        self.session.add(bookmark)
        self.session.commit()

    def add_many(self, bookmarks: list[BookmarkModel]) -> int:
        for bookmark in bookmarks:
            self.add_one(bookmark)

    def delete_one(self, bookmark) -> int:
        self.session.delete(bookmark)
        self.session.commit()

    def delete_many(self, bookmarks) -> int:
        for bookmark in bookmarks:
            self.delete_one(bookmark)

    def update(self, bookmark) -> int:
        self.session.merge(bookmark)
        self.session.commit()

    def update_many(self, bookmarks) -> int:
        for bookmark in bookmarks:
            self.update(bookmark)

    def find_first(self, query) -> BookmarkModel:
        self.session.query(query).first()

    def find_all(self, query) -> list[BookmarkModel]:
        self.session.query(query).all()