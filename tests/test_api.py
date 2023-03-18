import json
from app import app

def test_get_all_bookmarks(client):
    response = client.get('/api/bookmarks')
    assert response.status_code == 200

def test_get_all_bookmarks_sorted_by_title(client):
    response = client.get('/api/bookmarks/by-title')
    assert response.status_code == 200
    assert len(response.json) == 4
    assert response.json[0]['title'] == 'Flask'
    assert response.json[1]['title'] == 'GitHub'
    assert response.json[2]['title'] == 'Google'
    assert response.json[3]['title'] == 'Microsoft'

def test_get_all_bookmarks_sorted_by_created_date(client):
    response = client.get('/api/bookmarks/by-created-date')
    assert response.status_code == 200
    assert len(response.json) == 4
    assert response.json[0]['title'] == 'GitHub'
    assert response.json[1]['title'] == 'Flask'
    assert response.json[2]['title'] == 'Google'
    assert response.json[3]['title'] == 'Microsoft'

def test_create_bookmark(client):
    data = {
        'title': 'Google',
        'url': 'https://www.google.com',
        'notes': 'Search engine'
    }
    response = client.post('/api/bookmarks', json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Google'
    assert data['url'] == 'https://www.google.com'
    assert data['notes'] == 'Search engine'

def test_update_bookmark(client):
    data = {
        'title': 'Google',
        'url': 'https://www.google.com',
        'notes': 'Search engine'
    }
    response = client.put('/api/bookmarks/1', json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Google'
    assert data['url'] == 'https://www.google.com'
    assert data['notes'] == 'Search engine'

def test_delete_bookmark(client):
    response = client.delete('/api/bookmarks/1')
    assert response.status_code == 200