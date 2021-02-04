from django.test import TestCase
from rest_framework.test import APIClient
import json

client = APIClient()

class WatchlistsTestCase(TestCase):
    """
        Test fails when running all tests
        
        Passes when running individually
        python manage.py test watchlists.tests.WatchlistsTestCase.test_create_watchlists
    """
    def setUp(self):
        self.url = 'http://localhost:8000/api/user/watchlists/'
        self.user = client.post('http://localhost:8000/api/auth/register/', {"username": "AnonymousPanda", "email": "Panda123@gmail.com", "password": "password"})

    def test_get_watchlists(self):
        print("\nTesting User Watch Lists")
        
        user = json.loads(self.user.content)
        token = user['token']
        response = client.get(self.url, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 200
        assert len(watchlists) == 0
    
    def test_create_watchlists(self):
        print("\nTesting User Create Watch Lists")
        
        user = json.loads(self.user.content)
        token = user['token']
        
        response = client.get(self.url, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 200
        assert len(watchlists) == 0
        
        response = client.post(self.url, {"name": "Completed"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 201
        assert watchlists['name'] == "Completed"
    
    def test_update_watchlist(self):
        print("\nTesting User Update Watch Lists")
        
        user = json.loads(self.user.content)
        token = user['token']
        
        response = client.get(self.url, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 200
        assert len(watchlists) == 0
        
        response = client.post(self.url, {"name": "Currently Watching"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 201
        assert watchlists['name'] == "Currently Watching"
        
        response = client.patch(self.url + str(watchlists['id']) + "/", {"name": "Completed"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        
        assert response.status_code == 200
        assert json.loads(response.content)['name'] == 'Completed'
                
    def test_delete_watchlists(self):
        print("\nTesting User Update Watch Lists")
        
        user = json.loads(self.user.content)
        token = user['token']
        
        response = client.get(self.url, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 200
        assert len(watchlists) == 0
        
        response = client.post(self.url, {"name": "Currently Watching"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 201
        
        response = client.delete(self.url + str(watchlists['id']) + "/", client.credentials(HTTP_AUTHORIZATION="Token " + token))
        
        assert response.status_code == 204
        
        response = client.get(self.url, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists = (json.loads(response.content))
        
        assert response.status_code == 200
        assert len(watchlists) == 0
        
        
        