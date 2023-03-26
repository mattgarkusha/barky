import pytest
from api.flaskapi import app
from adapters import orm
from domain.model import Bookmark
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from config import TestingConfig

@pytest.fixture(scope="session")
def create_test_data():
    app.config.from_object(TestingConfig)

    # Create tables
    with app.app_context():
        orm.create_tables()

    Session = sessionmaker(bind=orm.engine)
    session = Session()

    now = datetime.now()
    session.add(Bookmark(id=1000, title='GitHub', url='https://github.com', notes='Git repository hosting service', created_at=now, updated_at=now))
    session.add(Bookmark(id=2000, title='Flask', url='https://palletsprojects.com/p/flask/', notes='Web application framework', created_at=now, updated_at=now))
    session.add(Bookmark(id=3000, title='Google', url='https://google.com', notes='You know, for search.', created_at=now, updated_at=now))
    session.add(Bookmark(id=4000, title='Microsoft', url='https://microsoft.com', notes='For computers', created_at=now, updated_at=now))
    session.commit()

    yield
      
      # Drop tables
    with app.app_context():
        orm.drop_tables()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client