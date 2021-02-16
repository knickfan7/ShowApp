"""
~~~~~~~~~~~~~~~~~~~~~~~
Module handles calling TMDB API and cleaning the data for use.

"""
import tmdbsimple as tmdb
import os
import dotenv
from .imdbapi import IMDBAPI
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
    
class TMDB():
    def __init__(self):
        tmdb.API_KEY = os.environ['TMDB_API_KEY']
        self.imdb = IMDBAPI()
        self.genre_obj = {
                28 : "Action",
                12 :"Adventure",
                16 : "Animation",
                35 : "Comedy",
                80 : "Crime",
                99 : "Documentary",
                18 : "Drama",
                10751 : "Family",
                14 : "Fantasy",
                36 : "History",
                27 : "Horror",
                10402 : "Music",
                9648 : "Mystery",
                10749 : "Romance",
                878 : "Science Fiction",
                10770 : "TV Movie",
                53 : "Thriller",
                10752 : "War",
                37 : "Western"
            }
        self.image_url = 'https://image.tmdb.org/t/p/w500/'
        self.youtube_url = 'https://www.youtube.com/watch?v='
                   
    def get_search_results(self, title):
        """
            Search for movie or show based on user query string. Get the results for the first 4 pages.
            
            Args: title string.
            
            Returns: List representation of related results.
        """
        search = tmdb.Search()
        results = []
        
        for x in range(1,4):
            search.multi(query=title, page=x)
            
            for show in search.results:
                result_obj = {}
                
                if show['media_type'] == 'tv' or show['media_type'] == 'movie':
                    try:
                        result_obj['title'] = show['title']
                    except:
                        result_obj['title'] = show['name']
                    self.handle_exceptions(result_obj, 'id', show, 'id')
                    self.handle_exceptions(result_obj, 'type', show, 'media_type')
                    self.handle_exceptions(result_obj, 'overview', show, 'overview')
                    self.handle_exceptions(result_obj, 'img', show, 'poster_path')
                    self.handle_exceptions(result_obj, 'rank', show, 'popularity')
                    results.append(result_obj)
                    
        results = (sorted(results, key=lambda show: show['rank'], reverse=True))
        return results
    
    def get_info(self, id, media_type):
        """
            Get information regarding movie or show. 
            
            Args: ID of the (Movie/Show), Media_type (Movie/Show)
            
            Returns: List representation of result
        """
        result = {}
        result['id'] = id
        result['type'] = media_type
        
        if media_type == "movie":
            movie = tmdb.Movies(id)
            response = movie.info()
            result['title'] = response['title'] 
            
            self.handle_exceptions(result, 'overview', response, 'overview')
            self.handle_exceptions(result, 'release_date', response, 'release_date')
            self.handle_exceptions(result, 'runtime', response, 'runtime')            
            self.handle_exceptions(result, 'img', response, 'poster_path')
            self.handle_exceptions(result, 'status', response, 'status')
            self.handle_exceptions(result, 'rating', response, 'vote_average')
            self.handle_exceptions(result, 'vote', response, 'vote_count')
            self.handle_exceptions(result, 'popularity', response, 'popularity')
            # Response Obj List
            self.handle_lst_exceptions(result, 'collection', response['belongs_to_collection'], 'name')
            self.handle_lst_exceptions(result, 'genres', response['genres'], 'name')
            self.handle_lst_exceptions(result, 'languages', response['spoken_languages'], 'name')
            self.handle_lst_exceptions(result, 'countries', response['production_countries'], 'name')
            
            result['trailer'] = self.get_videos(id)
            result['cast'] = self.get_min_cast_info(id, media_type)
            result['recommendations'] = self.get_recommendations(id, media_type)
            try:
                result['imdb'] = self.imdb.retrieve(int(response['imdb_id'][2:]))
            except: 
                result['imdb'] = []    
        else:
            tv = tmdb.TV(id)
            response = tv.info()
            result['title'] = response['name']
            self.handle_exceptions(result, 'country', response, 'origin_country')
            self.handle_exceptions(result, 'overview', response, 'overview')        
            self.handle_exceptions(result, 'status', response, 'status')
            self.handle_exceptions(result, 'first_air', response, 'first_air_date')
            self.handle_exceptions(result, 'last_air', response, 'last_air_date')
            self.handle_exceptions(result, 'next_air', response, 'next_episode_to_air')
            self.handle_exceptions(result, 'seasons', response, 'number_of_seasons')
            self.handle_exceptions(result, 'num_eps', response, 'number_of_episodes')
            self.handle_exceptions(result, 'ep_runtime', response, 'episode_run_time')
            self.handle_exceptions(result, 'rating', response, 'vote_average')
            self.handle_exceptions(result, 'img', response, 'poster_path')
            self.handle_exceptions(result, 'vote', response, 'vote_count')
            self.handle_exceptions(result, 'popularity', response, 'popularity')
            
            self.handle_lst_exceptions(result, 'languages', response['spoken_languages'], 'name')
            self.handle_lst_exceptions(result, 'countries', response['production_countries'], 'name')
            self.handle_lst_exceptions(result, 'genres', response['genres'], 'name')

            result['trailer'] = self.get_videos(id)
            result['cast'] = self.get_min_cast_info(id, media_type)
            result['recommendations'] = self.get_recommendations(id, media_type)
            result['imdb'] = self.imdb.retrieve_tv(int(tv.external_ids()['imdb_id'][2:]))
        lst = []
        lst.append(result)
        return lst
    
    def insert_info(self, id, media_type):
        """
            Get information regarding movie or show. 
            
            Args: ID of the (Movie/Show), Media_type (Movie/Show)
            
            Returns: List representation of result
        """
        result = {}
        result['id'] = id
        result['type'] = media_type
        
        if media_type == "movie":
            movie = tmdb.Movies(id)
            response = movie.info()
            result['title'] = response['title']
            self.handle_exceptions(result, 'image', response, 'poster_path')
        else:
            tv = tmdb.TV(id)
            response = tv.info()
            result['title'] = response['name']
            self.handle_exceptions(result, 'image', response, 'poster_path')

                
        lst = []
        lst.append(result)
        return lst
    
    def get_min_cast_info(self, id, media_type):
        """
            Get cast info regarding movie or show. 
            
            Args: ID of the (Movie/Show), Media_type (Movie/Show)
            
            Returns: List representation of Cast members and their roles
        """
        cast_info = []
        
        if media_type == "movie":
            movie = tmdb.Movies(id)
            response = movie.credits()
        else:
            tv = tmdb.TV(id)
            response = tv.credits()
        for cast_member in response['cast'][:6]:
            temp= {}
            self.handle_exceptions(temp, 'name', cast_member, 'name')
            self.handle_exceptions(temp, 'character', cast_member, 'character')
            self.handle_exceptions(temp, 'img', cast_member, 'profile_path')
            cast_info.append(temp)
        return cast_info
    
    def get_full_cast_info(self, id, media_type):
        cast_info = []
        
        if media_type == "movie":
            movie = tmdb.Movies(id)
            response = movie.credits()
        else:
            tv = tmdb.TV(id)
            response = tv.credits()
            
        for cast_member in response['cast'][:30]:
            temp= {}
            self.handle_exceptions(temp, 'name', cast_member, 'name')
            self.handle_exceptions(temp, 'character', cast_member, 'character')
            self.handle_exceptions(temp, 'img', cast_member, 'profile_path')
            cast_info.append(temp)
            
        return cast_info
    
    def get_recommendations(self, id, media_type):
        """
            Get recommendations about movie or show
            
            Args: ID of the (Movie/Show), Media_type (Movie/Show)
            
            Return: List represntation of results with title/name and image
        """
        recommendation_list = []
        
        if media_type == "movie":
            movie = tmdb.Movies(id)
            response = movie.recommendations()
        else:
            show = tmdb.TV(id)
            response = show.recommendations()
            
        for recommendation in response['results']:
            temp = {}
            temp['id'] = recommendation['id']
            try:
                temp['title'] = recommendation['title']
            except:
                temp['title'] = recommendation['name']            
            self.handle_exceptions(temp, 'img', recommendation, 'poster_path')
            self.handle_exceptions(temp, 'overview', recommendation, 'overview')

            recommendation_list.append(temp)
        return recommendation_list
    
    def get_videos(self, id):
        """
            Get trailers and other videos about movie or show
            
            Args: ID of the (Movie/Show)
            
            Return: List represntation of urls
        """
        video_list = []
        try: 
            movie = tmdb.Movies(id)
            response = movie.videos()
            for link in response['results']:
                video_list.append(self.youtube_url + link['key'])
        except:
            tv = tmdb.TV(id)
            response = tv.videos()
            for link in response['results']:
                video_list.append(self.youtube_url + link['key'])

        return video_list

    def get_tv_page(self):
        tv = tmdb.TV()
        results = []
        on_air = []
        popular = []
        top_rated = []
        
        for x in range(1,3):
            response = tv.on_the_air(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['name']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'tv'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                on_air.append(temp)
                
        for x in range(1,3):
            response = tv.popular(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['name']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'tv'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                popular.append(temp)
    
        for x in range(1,3):
            response = tv.top_rated(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['name']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'tv'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                top_rated.append(temp)
    
        results.append({"type": "on-air", "list": on_air})
        results.append({"type": "popular", "list": popular})
        results.append({"type": "top-rated", "list": top_rated})
        return results

    def get_movie_page(self):
        movie = tmdb.Movies()
        results = []
        now_playing = []
        popular = []
        top_rated = []
        upcoming = []
        
        for x in range(1,3):
            response = movie.now_playing(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['title']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'movie'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                now_playing.append(temp)
        
        for x in range(1,3):
            response = movie.popular(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['title']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'movie'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                popular.append(temp)
                
        for x in range(1,3):
            response = movie.top_rated(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['title']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'movie'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                top_rated.append(temp)
                
        for x in range(1,3):
            response = movie.upcoming(page=x)
            for show in response['results']:
                temp = {}
                temp['title'] = show['title']  
                self.handle_exceptions(temp, 'id', show, 'id')
                temp['type'] = 'movie'
                self.handle_exceptions(temp, 'overview', show, 'overview')
                self.handle_exceptions(temp, 'img', show, 'poster_path')
                upcoming.append(temp)
                
        results.append({"type": "now_playing", "list": now_playing})
        results.append({"type": "popular", "list": popular})
        results.append({"type": "top-rated", "list": top_rated})
        results.append({"type": "upcoming", "list": upcoming})
        return results        
        
    def handle_exceptions(self, result, result_key, response, response_key):
        try:
            if response_key == "poster_path" or response_key == "profile_path":
                result[result_key] = self.image_url + response[response_key]
            else:
                result[result_key] = response[response_key]
        except:
            result[result_key] = None
            
    def handle_lst_exceptions(self, result, result_key, response, response_key):
        try:
            temp_list = []
            for item in response:
                temp_list.append(item[response_key])
            result_str = ', '.join(temp_list)
            result[result_key] = result_str
        except:
            result[result_key] = None
        