import json

API_URL = 'http://127.0.0.1:5000'
def test_create_bookmark(client):
    data = {
        'title': 'Google',
        'url': 'https://www.google.com',
        'notes': 'Search engine'
    }
    print(API_URL + '/api/bookmarks')
    response = client.post(API_URL + '/api/bookmarks', json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Google'
    assert data['url'] == 'https://www.google.com'
    assert data['notes'] == 'Search engine'

def test_get_all_bookmarks(client):
    response = client.get(API_URL + '/api/bookmarks')
    assert response.status_code == 200
    assert len(response.json) == 8
    assert response.json[0]['title'] == 'Google'

def test_get_all_bookmarks_sorted_by_title(client):
    response = client.get(API_URL + '/api/bookmarks/by-title')
    assert response.status_code == 200
    assert len(response.json) == 8
    assert response.json[0]['title'] == 'Google'

def test_get_all_bookmarks_sorted_by_created_date(client):
    response = client.get(API_URL + '/api/bookmarks/by-created-date')
    assert response.status_code == 200
    assert len(response.json) == 8
    assert response.json[0]['title'] == 'Google'

def test_update_bookmark(client):
    data = {
        'title': 'Google Search',
        'url': 'https://www.google.com',
        'notes': 'Search engine'
    }
    response = client.put(API_URL + '/api/bookmarks/1', json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Google Search'
    assert data['url'] == 'https://www.google.com'
    assert data['notes'] == 'Search engine'

def test_delete_bookmark(client):
    response = client.delete(API_URL + '/api/bookmarks/1')
    assert response.status_code == 200
