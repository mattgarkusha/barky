from domain.Bookmark import Bookmark
from repo.BookmarkRepository import BookmarkRepository
from datetime import datetime
import requests

class BookmarkService:
    def __init__(self):
        self.repo = BookmarkRepository()

    def get_all_bookmarks(self):
        return self.repo.get_all()
    
    def get_all_bookmarks_by_title(self):
        return self.repo.get_all(sort_field='title')
    
    def get_all_bookmarks_by_created_date(self):
        return self.repo.get_all(sort_field='created_at')

    def get_bookmark_by_id(self, id):
        return self.repo.get_by_id(id)

    def create_bookmark(self, data):
        now = datetime.now()
        bookmark = Bookmark(title=data['title'], url=data['url'], notes=data['notes'], created_at=now, updated_at=now)
        return self.repo.create(bookmark)

    def update_bookmark(self, id, data):
        now = datetime.now()
        bookmark = self.repo.get_by_id(id)
        if bookmark is None:
            return None
        bookmark.title = data.get('title', bookmark.title)
        bookmark.url = data.get('url', bookmark.url)
        bookmark.notes = data.get('notes', bookmark.notes)
        bookmark.updated_at = now
        return self.repo.update(bookmark)
    
    def delete_bookmark(self, bookmark_id):
        bookmark = self.repo.get_by_id(bookmark_id)
        if bookmark:
            self.repo.delete(bookmark)
            return bookmark
        else:
            return None
    
    def import_github_stars(self, github_username):
        bookmarks_imported = 0

        github_username = github_username
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
                json = self._extract_bookmark_info(repo)
                
                self.create_bookmark(json)
    
    def _extract_bookmark_info(self, repo):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }