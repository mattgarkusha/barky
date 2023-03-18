import pytest
from app import app, db
from domain.Bookmark import Bookmark

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.add(Bookmark(title='GitHub', url='https://github.com', notes='Git repository hosting service'))
            db.session.add(Bookmark(title='Flask', url='https://palletsprojects.com/p/flask/', notes='Web application framework'))
            db.session.add(Bookmark(title='Google', url='https://google.com', notes='You know, for search.'))
            db.session.add(Bookmark(title='Microsoft', url='https://microsoft.com', notes='For computers'))
            db.session.commit()
        yield client
        db.session.remove()
        db.drop_all()