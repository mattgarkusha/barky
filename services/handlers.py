from __future__ import annotations
from typing import TYPE_CHECKING

from domain import commands, events, model

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

# ListBookmarksCommand
def list_bookmarks(
    cmd: commands.ListBookmarksCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmarks = uow.bookmarks_repo.get_all(sort_field=cmd.sort_order)
        results = []
        for bookmark in bookmarks:
            results.append(bookmark.to_dict())
        return results

# GetBookmarkByID: id: int
def get_bookmark_by_id(
    cmd: commands.DeleteBookmarkCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        bookmark = uow.bookmarks_repo.get_by_id(cmd.id)
        return bookmark.to_dict()


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