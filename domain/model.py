from datetime import datetime
from dataclasses import dataclass
from typing import List

@dataclass(unsafe_hash=True)
class Bookmark:

    id: int
    title: str
    url: str
    notes: str
    created_at: datetime
    updated_at: datetime
    
    def __init__(
        self,
        id: int,
        title: str,
        url: str,
        notes: str,
        created_at: datetime,
        updated_at: datetime
    ) -> None:
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        self.events = []  # type: List[events.Event]

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
