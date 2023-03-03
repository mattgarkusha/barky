"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
import sys
from abc import ABC, abstractmethod
from datetime import datetime

import requests

from services.database import DatabaseManager
from repository.sqla_repository import SQLARespository
from repository.models import BookmarkModel

# module scope
db = DatabaseManager("bookmarks.db")
repo = SQLARespository("sqlite:///bookmarks.db")


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError("A command must implement the execute method")


class CreateBookmarksTableCommand(Command):
    """
    uses the DatabaseManager to create the bookmarks table
    """

    def execute(self, data=None):
        db.create_table(
            "bookmarks",
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data["date_added"] = datetime.utcnow().isoformat()
        repo.add_one(data)
        return "Bookmark added!"


class ListBookmarksCommand(Command):
    
    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        return repo.find_all(query=None)


class DeleteBookmarkCommand(Command):


    def execute(self, data):
        repo.delete_one(data)
        return "Bookmark deleted!"


class ImportGitHubStarsCommand(Command):

    def _extract_bookmark_info(self, repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data):
        bookmarks_imported = 0

        github_username = data["github_username"]
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"
        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            next_page_of_results = stars_response.links.get("next", {}).get("url")

            for repo_info in stars_response.json():
                repo = repo_info["repo"]

                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        repo_info["starred_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1
                bookmark = BookmarkModel(self._extract_bookmark_info(repo))
                bookmark.created_date = timestamp
                
                repo.add_one(bookmark)

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class EditBookmarkCommand(Command):
    def execute(self, data):
        repo.update(data)
        return "Bookmark updated!"


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()