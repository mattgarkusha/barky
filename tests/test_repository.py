# the database module is much more testable as its actions are largely atomic
# that said, the database module could certain be refactored to achieve decoupling
# in fact, either the implementation of the Unit of Work or just changing to sqlalchemy would be good.

from datetime import datetime

import pytest
from repository.sqla_repository import SQLARespository
from repository.models import BookmarkModel

@pytest.fixture
def repo() -> SQLARespository:
    repo = SQLARespository()
    yield repo


def test_add_one():
    bookmark = BookmarkModel
    bookmark.title = 'title'
    bookmark.url = 'http://fake.com'
    bookmark.notes = 'my fav bookmark'
    repo.add_one(bookmark)