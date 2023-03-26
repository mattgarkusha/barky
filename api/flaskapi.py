from flask import Flask, jsonify, request
from adapters import orm
from services import message_bus, unit_of_work
from domain.commands import *
from domain.model import Bookmark

# bookmark_service = BookmarkService(uow)

app = Flask(__name__)
orm.start_mappers()

@app.before_first_request
def create_tables():
    orm.create_tables()

@app.route('/api/bookmarks', methods=['GET'])
def list_bookmarks():
    cmd = ListBookmarksCommand()
    bookmarks = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]

    return jsonify(bookmarks)

@app.route('/api/bookmarks/by-title', methods=['GET'])
def list_bookmarks_by_title():
    cmd = ListBookmarksCommand()
    cmd.sort_order = 'title'
    bookmarks = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]
    return jsonify([bookmark for bookmark in bookmarks])

@app.route('/api/bookmarks/by-created-date', methods=['GET'])
def list_bookmarks_by_created_date():
    cmd = ListBookmarksCommand()
    cmd.sort_order = 'created_at'
    bookmarks = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]
    return jsonify([bookmark for bookmark in bookmarks])

@app.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.json
    cmd = AddBookmarkCommand(None, data['title'], data['url'], data['notes'])
    bookmark = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]
    return jsonify(bookmark)

@app.route('/api/bookmarks/<int:id>', methods=['GET'])
def get_bookmark(id):
    cmd = GetBookmarkByIdCommand(id=id)
    bookmark = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark)

@app.route('/api/bookmarks/<int:id>', methods=['PUT'])
def update_bookmark(id):
    data = request.json
    cmd = EditBookmarkCommand(
        id=id,
        title=data.get('title'),
        url=data.get('url'),
        notes=data.get('notes'),
    )
    bookmark = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark)

@app.route('/api/bookmarks/<int:id>', methods=['DELETE'])
def delete_bookmark(id):
    cmd = DeleteBookmarkCommand(id=id)
    bookmark = message_bus.handle(message=cmd, uow= unit_of_work.SqlAlchemyUnitOfWork())[0]
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark)


# @app.route('/api/bookmarks/import-github/<string:username>', methods=['GET'])
# def import_github_bookmarks(username):
#     bookmark_service.import_github_stars(username)
#     return jsonify({'success': 'true'})
