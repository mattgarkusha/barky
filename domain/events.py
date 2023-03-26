from abc import ABC
from dataclasses import dataclass
from typing import Optional, List

from domain.model import Bookmark


class Event(ABC):
    pass

@dataclass
class BookmarkAdded(Event):
    id: int
    title: str
    url: str
    created_at: str
    updated_at: str
    bookmark_notes: Optional[str] = None


@dataclass
class BookmarkEdited(Event):
    id: int
    title: str
    url: str
    updated_at: str
    bookmark_notes: Optional[str] = None


@dataclass
class BookmarksListed(Event):
    bookmarks: List[Bookmark]

@dataclass
class BookmarksListedByTitle(Event):
    bookmarks: List[Bookmark]

@dataclass
class BookmarksListedByCreatedDate(Event):
    bookmarks: List[Bookmark]


@dataclass
class BookmarkDeleted(Event):
    bookmark: Bookmark

@dataclass
class BookmarkGottenByID(Event):
    bookmark: Bookmark