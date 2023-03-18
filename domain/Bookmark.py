from app import db

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, title, url, notes='', created_at=None, updated_at=None):
        self.title = title
        self.url = url
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }