# how would I test Barky?
# First, I wouldn't test barky, I would test the reusable modules barky relies on:
# commands.py and database.py

import pytest
from database import DatabaseManager
import commands

@pytest.fixture
def database_manager() -> DatabaseManager:
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()
    os.remove(filename)

def test_add_bookmark_command():
    #arrange
    expected_result = 'Bookmark added!'
    
    #act
    result = commands.AddBookmarkCommand.execute(database_manager, {'title': 'Bookmark 1', 'url': 'https://google.com'})

    #assert
    assert result == expected_result

def test_list_bookmarks_by_date_command():
    #arrange
    database_manager.order_by = "date_added"
    
    #act
    result = commands.ListBookmarksCommand.execute(database_manager)

    #pass if no exception
    pass

def test_list_bookmarks_by_title_command():
    #arrange
    database_manager.order_by = "title"
    
    #act
    result = commands.ListBookmarksCommand.execute(database_manager)

    #pass if no exception
    pass

def test_delete_bookmark_command():
    #arrange
    expected_result = 'Bookmark deleted!'
    #just make sure it's not an empty list
    commands.AddBookmarkCommand.execute(database_manager, {'title': 'Bookmark I\'m totally going to delete if it happens to be the first one in the list', 'url': 'https://deleted.com'})
    
    #act
    result = commands.DeleteBookmarkCommand.execute(database_manager, 1)
    
    #assert
    assert result == expected_result


    
# okay, should I test the other commands?
# not really, they are tighly coupled with sqlite3 and its use in the database.py module
