from flask import Flask, jsonify, request
from adapters import orm
from api import views
from domain.commands import *
import bootstrap

app = Flask(__name__)
message_bus = bootstrap.bootstrap()

@app.before_first_request
def create_tables():
    orm.create_tables()

@app.route('/api/bookmarks', methods=['GET'])
def list_bookmarks():
    result = views.get_bookmarks(message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/bookmarks/by-title', methods=['GET'])
def list_bookmarks_by_title():
    result = views.get_bookmarks_sorted("title", message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/bookmarks/by-created-date', methods=['GET'])
def list_bookmarks_by_created_date():
    result = views.get_bookmarks_sorted("created_at", message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.json
    cmd = AddBookmarkCommand(None, data['title'], data['url'], data['notes'])
    bookmark = message_bus.handle(message=cmd)
    return jsonify(bookmark)

@app.route('/api/bookmarks/<int:id>', methods=['GET'])
def get_bookmark(id):
    result = views.get_bookmark_by_id(id, message_bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

@app.route('/api/bookmarks/<int:id>', methods=['PUT'])
def update_bookmark(id):
    data = request.json
    cmd = EditBookmarkCommand(
        id=id,
        title=data.get('title'),
        url=data.get('url'),
        notes=data.get('notes'),
    )
    bookmark = message_bus.handle(message=cmd)
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark)

@app.route('/api/bookmarks/<int:id>', methods=['DELETE'])
def delete_bookmark(id):
    cmd = DeleteBookmarkCommand(id=id)
    bookmark = message_bus.handle(message=cmd)
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark)


@app.route('/api/bookmarks/import-github/<string:username>', methods=['GET'])
def import_github_bookmarks(username):
    cmd = ImportGithubBookmarksCommand(username=username)
    message_bus.handle(message=cmd)
    return jsonify({'success': 'true'})
