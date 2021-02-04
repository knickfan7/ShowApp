from django.test import TestCase
from rest_framework.test import APIClient
import json

client = APIClient()
ANIME_ID_1 = 12971 # DBZ
ANIME_ID_2 = 295830 # AOT

MOVIE_ID_1 = 120 # LOTR Fellowship
MOVIE_ID_2 = 447404 # Detective Pikachu

SHOW_ID_1 = 95834 # Legend of Fei
SHOW_ID_2 = 1399 # GoT

class ShowListTestCase(TestCase):
    def setUp(self):
        self.get_url = 'http://localhost:8000/api/shows/'
        self.post_url = 'http://127.0.0.1:8000/api/add/show/'
        self.watchlist_url = 'http://localhost:8000/api/user/watchlists/'
        self.user = client.post('http://localhost:8000/api/auth/register/', {"username": "AnonymousPanda", "email": "Panda123@gmail.com", "password": "password"})
        self.user_1 = client.post('http://localhost:8000/api/auth/register/', {"username": "AnonymousKoala", "email": "Koala123@gmail.com", "password": "password"})

    def test_search_show(self):
        print("\nTesting Search Shows")
        response = client.get(self.get_url + "?title=Lord%of%the%rings")
        
        assert json.loads(response.content)[0]['title'] == 'The Lord of the Rings: The Two Towers'
        assert response.status_code == 200
        
        response = client.get(self.get_url + "?title=Detective%Pikachu")

        assert json.loads(response.content)[0]['title'] == "Pokémon Detective Pikachu"
        assert response.status_code == 200
        
        response = client.get(self.get_url + "?title=Attack%on%titan")
        json.loads(response.content)[0]['title'] == 'Attack on Titan'
        
    def test_get_show_info(self):
        response = client.get(self.get_url + "?title=Lord%of%the%rings")
        response_obj = json.loads(response.content)[0]
        
        assert response_obj['title'] == 'The Lord of the Rings: The Two Towers'
        assert response.status_code == 200
        
        info_response = client.get(self.get_url + 'info/?id=' + str(response_obj['id']) + '&type=' + response_obj['type'])
        info_response_obj = json.loads(info_response.content)[0]        
        
        assert info_response_obj['title'] == response_obj['title']
        assert info_response.status_code == 200
        
        
        response_1 = client.get(self.get_url + "?title=Detective%Pikachu")
        response_obj_1 = json.loads(response_1.content)[0]
        
        assert response_obj_1['title'] == "Pokémon Detective Pikachu"
        assert response_1.status_code == 200
        
        info_response_1 = client.get(self.get_url + 'info/?id=' + str(response_obj_1['id']) + '&type=' + response_obj_1['type'])
        info_response_obj_1 = json.loads(info_response_1.content)[0]        
        
        assert info_response_obj_1['title'] == response_obj_1['title']
        assert info_response_1.status_code == 200
        
        response_2 = client.get(self.get_url + "?title=Attack%on%titan")
        response_obj_2 = json.loads(response_2.content)[0]
        
        assert response_obj_2['title'] == "Attack on Titan"
        assert response_2.status_code == 200
        
        info_response_2 = client.get(self.get_url + 'info/?id=' + str(response_obj_2['id']) + '&type=' + response_obj_2['type'])
        info_response_obj_2 = json.loads(info_response_2.content)[0]        
        
        assert info_response_obj_2['title'] == response_obj_2['title']
        assert info_response_2.status_code == 200
        
    def test_add_show(self):
        print("\n Testing User Create Watch Lists")
        
        user = json.loads(self.user.content)
        token = user['token']
        
        # User 1 Show 1
        response = client.get(self.get_url + "?title=Lord%of%the%rings")
        response_obj = json.loads(response.content)[0]
        
        info_response = client.get(self.get_url + 'info/?id=' + str(response_obj['id']) + '&type=' + response_obj['type'])
        info_response_obj = json.loads(info_response.content)[0]        

        post_response = client.post(self.post_url, {"id": info_response_obj['id'], "type": info_response_obj['type'], "show": "Completed"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        post_response_obj = json.loads(post_response.content)
        
        assert post_response.status_code == 201
        assert post_response_obj['owner'] == 1     
        
        # User 1 Show 2
        response_1 = client.get(self.get_url + "?title=Detective%Pikachu")
        response_obj_1 = json.loads(response_1.content)[0]
        
        info_response_1 = client.get(self.get_url + 'info/?id=' + str(response_obj_1['id']) + '&type=' + response_obj_1['type'])
        info_response_obj_1 = json.loads(info_response_1.content)[0]        
        
        post_response_1 = client.post(self.post_url, {"id": info_response_obj_1['id'], "type": info_response_obj_1['type'], "show": "Completed"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        post_response_obj_1 = json.loads(post_response_1.content)
        
        assert post_response_1.status_code == 201
        assert post_response_obj_1['owner'] == 1   
        
        # User 1 Show 3
        response_2 = client.get(self.get_url + "?title=Attack%on%titan")
        response_obj_2 = json.loads(response_2.content)[0]
        
        info_response_2 = client.get(self.get_url + 'info/?id=' + str(response_obj_2['id']) + '&type=' + response_obj_2['type'])
        info_response_obj_2 = json.loads(info_response_2.content)[0]        

        post_response_2 = client.post(self.post_url, {"id": info_response_obj_2['id'], "type": info_response_obj_2['type'], "show": "To Watch"}, client.credentials(HTTP_AUTHORIZATION="Token " + token))
        post_response_obj_2 = json.loads(post_response_2.content)
        
        assert post_response_2.status_code == 201
        assert post_response_obj_2['owner'] == 1   
        
        # User 2 Show 1
        user_1 = json.loads(self.user_1.content)
        token_1 = user_1['token']
        
        response_3 = client.get(self.get_url + "?title=Attack%on%titan")
        response_obj_3 = json.loads(response_3.content)[0]
        
        info_response_3 = client.get(self.get_url + 'info/?id=' + str(response_obj_3['id']) + '&type=' + response_obj_3['type'])
        info_response_obj_3 = json.loads(info_response_3.content)[0]        

        post_response_3 = client.post(self.post_url, {"id": info_response_obj_3['id'], "type": info_response_obj_3['type'], "show": "On Hold"}, client.credentials(HTTP_AUTHORIZATION="Token " + token_1))
        post_response_obj_3 = json.loads(post_response_3.content)
        
        assert post_response_3.status_code == 201
        assert post_response_obj_3['owner'] == 2   
        
        print("\n Testing User Get Watch Lists")
        watchlist_response = client.get(self.watchlist_url + '?name=Completed', client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists_response_obj = json.loads(watchlist_response.content)
        
        assert watchlist_response.status_code == 200
        assert len(watchlists_response_obj) == 2

        watchlist_response_1 = client.get(self.watchlist_url + '?name=To%20Watch', client.credentials(HTTP_AUTHORIZATION="Token " + token))
        watchlists_response_obj_1 = json.loads(watchlist_response_1.content)
        
        assert watchlist_response_1.status_code == 200
        assert len(watchlists_response_obj_1) == 1
        
        watchlist_response_2 = client.get(self.watchlist_url + '?name=On%20Hold', client.credentials(HTTP_AUTHORIZATION="Token " + token_1))
        watchlists_response_obj_2 = json.loads(watchlist_response_2.content)
        
        assert watchlist_response_2.status_code == 200
        assert len(watchlists_response_obj_2) == 1
        