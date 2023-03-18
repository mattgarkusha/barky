from app import db
from .AbstractRepository import AbstractRepository
from domain.Bookmark import Bookmark

class BookmarkRepository(AbstractRepository):
    def get_all(self, sort_field=None, sort_descending=False):
        query = Bookmark.query
        if sort_field is not None:
            sort_attr = getattr(Bookmark, sort_field)
            if sort_descending:
                query = query.order_by(sort_attr.desc())
            else:
                query = query.order_by(sort_attr)
        return query.all()

    def get_by_id(self, id):
        return Bookmark.query.filter_by(id=id).first()

    def create(self, bookmark):
        db.session.add(bookmark)
        db.session.commit()
        return bookmark

    def update(self, bookmark):
        db.session.commit()
        return bookmark

    def delete(self, bookmark):
        db.session.delete(bookmark)
        db.session.commit()
        return bookmark