from abc import ABC
from dataclasses import dataclass
from typing import Optional

class Command(ABC):
    pass

@dataclass
class AddBookmarkCommand(Command):
    id: int
    title: str
    url: str
    notes: Optional[str] = None

@dataclass
class DeleteBookmarkCommand(Command):
    id: int

@dataclass
class EditBookmarkCommand(Command):
    id: int
    title: str
    url: str
    notes: Optional[str] = None

@dataclass
class ImportGithubBookmarksCommand(Command):
    username: str