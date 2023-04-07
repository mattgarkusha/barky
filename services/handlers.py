from __future__ import annotations
from typing import TYPE_CHECKING
import requests

from domain import commands, model

if TYPE_CHECKING:
    from . import unit_of_work

def add_bookmark(
    cmd: commands.AddBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmark = model.Bookmark(id=None, title=cmd.title, url=cmd.url, notes=cmd.notes, created_at=None, updated_at=None)
        result = uow.bookmarks_repo.create(bookmark)         
        uow.commit()
        return result.to_dict()


# DeleteBookmarkCommand: id: int
def delete_bookmark(
    cmd: commands.DeleteBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        result = uow.bookmarks_repo.delete(cmd.id) 
        return result.to_dict()


# EditBookmarkCommand(Command):
def edit_bookmark(
    cmd: commands.EditBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmark = uow.bookmarks_repo.get_by_id(cmd.id)
        if bookmark is None:
            return None
        bookmark.title = cmd.title
        bookmark.url = cmd.url
        bookmark.notes = cmd.notes
        result = uow.bookmarks_repo.update(bookmark)
        return result.to_dict()
    
def import_github_stars(
    cmd: commands.ImportGithubBookmarksCommand,
    uow: unit_of_work.AbstractUnitOfWork,):
        bookmarks_imported = 0

        github_username = cmd.username
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"
        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            next_page_of_results = stars_response.links.get("next", {}).get("url")

            for repo_info in stars_response.json():
                repo = repo_info["repo"]

                bookmarks_imported += 1
                json = _extract_bookmark_info(repo)
                print(json)
                
                add_bookmark_command = commands.AddBookmarkCommand(None, json['title'], json['url'], json['notes'])
                add_bookmark(cmd=add_bookmark_command, uow=uow)

def _extract_bookmark_info(repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }