from flask import jsonify, request
from app import app
from services.BookmarkService import BookmarkService

bookmark_service = BookmarkService()

@app.route('/api/bookmarks', methods=['GET'])
def list_bookmarks():
    bookmarks = bookmark_service.get_all_bookmarks()
    return jsonify([bookmark.to_dict() for bookmark in bookmarks])

@app.route('/api/bookmarks/by-title', methods=['GET'])
def list_bookmarks_by_title():
    bookmarks = bookmark_service.get_all_bookmarks_by_title()
    return jsonify([bookmark.to_dict() for bookmark in bookmarks])

@app.route('/api/bookmarks/by-created-date', methods=['GET'])
def list_bookmarks_by_created_date():
    bookmarks = bookmark_service.get_all_bookmarks_by_created_date()
    return jsonify([bookmark.to_dict() for bookmark in bookmarks])

@app.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.json
    bookmark = bookmark_service.create_bookmark(data)
    return jsonify(bookmark.to_dict())

@app.route('/api/bookmarks/<int:id>', methods=['GET'])
def get_bookmark(id):
    bookmark = bookmark_service.get_bookmark_by_id(id)
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark.to_dict())

@app.route('/api/bookmarks/<int:id>', methods=['PUT'])
def update_bookmark(id):
    data = request.json
    bookmark = bookmark_service.update_bookmark(id, data)
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark.to_dict())

@app.route('/api/bookmarks/<int:id>', methods=['DELETE'])
def delete_bookmark(id):
    bookmark = bookmark_service.delete_bookmark(id)
    if bookmark is None:
        return jsonify({'error': 'Bookmark not found'}), 404
    return jsonify(bookmark.to_dict())

@app.route('/api/bookmarks/import-github/<string:username>', methods=['GET'])
def import_github_bookmarks(username):
    bookmark_service.import_github_stars(username)
    return jsonify({'success': 'true'})