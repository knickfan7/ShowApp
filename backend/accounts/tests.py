from django.test import TestCase
from rest_framework.test import APIClient
import json


class AccountsTestCase(TestCase):
    
    def setUp(self):
        self.url = 'http://localhost:8000/api/auth/'
    
    def test_register_user(self):
        print("Testing User Registration")
        client = APIClient()
        response = client.post(self.url + 'register/', {"username": "AnonymousPanda", "email": "Panda123@gmail.com", "password": "password"})
        try:
            json.loads(response.content)
        except: 
            pass
        assert response.status_code == 200
        
        
    def test_user(self):
        print("\nTesting User Info")
        client = APIClient()
        response = client.post(self.url + 'register/', {"username": "AnonymousPanda", "email": "Panda123@gmail.com", "password": "password"})
        user = json.loads(response.content)
        
        token_str = ('Token ' + user['token'])
        response = client.get(self.url + 'user/', client.credentials(HTTP_AUTHORIZATION=token_str))

        assert response.status_code == 200        
        
    def test_user_login_out(self):
        print("\nTesting User Logout and Login")
        client = APIClient()
        response = client.post(self.url + 'register/', {"username": "AnonymousPanda", "email": "Panda123@gmail.com", "password": "password"})
        user = json.loads(response.content)
        
        assert response.status_code == 200  
        token_str = ('Token ' + user['token'])
        
        client.get(self.url + "logout/", client.credentials(HTTP_AUTHORIZATION=token_str))

        # Test login with wrong credentials
        response = client.post(self.url + 'logins/', {"username": "AnonymousKoala", "password": "password"})
        content = (json.loads(response.content))
        assert response.status_code == 400
        assert content['non_field_errors'][0] == "Incorrect Credentials. Try Again."
        
        # Test Login with correct credentials
        response = client.post(self.url + 'logins/', {"username": "AnonymousPanda", "password": "password"})
        assert response.status_code == 200
