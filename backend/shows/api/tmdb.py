"""
ShowList
~~~~~~~~~~~~~~~~~~~~~~~
Module handles calling TMDB API and cleaning the data for use.

"""

import tmdbsimple as tmdb

class TMDB():
    
    def __init__(self):
        tmdb.API_KEY = '604a4d6912d3b03e660175fa2ed6b693'
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
        
    def handle_errors(self, col_name, result_col, lst):
        try:
            lst[col_name] = result_col
        except:
            lst[col_name] = None
        
    def handle_errors_list(self, col_name, result_col, result_key, lst):
        try:
            temp = []
            for element in result_col:
                temp.append(element[result_key])
            result_str = ",".join(temp)
            lst[col_name] = result_str
        except:
            lst[col_name] = None
            
    def get_search_results(self, title):
        """
            Search for movie or show based on user query string.
            
            Args: title string.
            
            Returns: List representation of related results.
        """
        search = tmdb.Search()
        search.multi(query=title)
        results = []
        
        for result in search.results:
            result_obj = {}
            
            self.handle_errors('id', result['id'], result_obj)
            self.handle_errors('type', result['media_type'], result_obj)
            self.handle_errors('overview', result['overview'], result_obj)
            self.handle_errors('img', result['poster_path'], result_obj)
            
            try:
                self.handle_errors('title', result['title'], result_obj)
            except:
                self.handle_errors('title', result['name'], result_obj)
                
            results.append(result_obj)
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
            self.handle_errors("title", response['title'], result)
            self.handle_errors("overview", response['overview'], result)
            self.handle_errors("release_date", response['release_date'][0:4], result)
            self.handle_errors("runtime", response['runtime'], result)
            self.handle_errors("series", response['belongs_to_collection']['name'], result)
            self.handle_errors("img", self.image_url + response['poster_path'], result)
            self.handle_errors("status", response["status"], result)
            self.handle_errors("rating", response['vote_average'], result)
            self.handle_errors("vote", response['vote_count'], result)
            self.handle_errors("popularity", response['popularity'], result)
            self.handle_errors("recommendations", self.get_recommendations(id, media_type), result)
            self.handle_errors("cast", self.get_cast_info(id, media_type), result)
            self.handle_errors_list("genres", response['genres'], 'name', result)
            self.handle_errors("trailer", self.get_videos(id), result)
            self.handle_errors_list("languages", response['spoken_languages'], 'name', result)
        
        else:
            tv = tmdb.TV(id)
            response = tv.info()
            self.handle_errors("title", response['name'], result)
            self.handle_errors("country",  response['origin_country'], result)
            self.handle_errors("overview",  response['overview'], result)
            self.handle_errors("first_air",  response['first_air_date'], result)
            self.handle_errors("last_air", response['last_air_date'], result)
            self.handle_errors("next_air", response['next_episode_to_air'], result)
            self.handle_errors("seasons", response['number_of_seasons'], result)
            self.handle_errors("num_eps", response['number_of_episodes'], result)
            self.handle_errors("episode_run_time", response['episode_run_time'], result)
            self.handle_errors("img", self.image_url + response['poster_path'], result)
            self.handle_errors("trailer", self.get_videos(id), result)
            self.handle_errors("rating", response["vote_average"], result)
            self.handle_errors("recommendations", self.get_recommendations(id, media_type), result)
            self.handle_errors("cast", self.get_cast_info(id, media_type), result)
            self.handle_errors_list("genres", response['genres'], 'name', result)
            self.handle_errors_list("languages", response['spoken_languages'], 'name', result)
                
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
            self.handle_errors("title", response['title'], result)
            self.handle_errors("image", self.image_url + response['poster_path'], result)
        else:
            tv = tmdb.TV(id)
            response = tv.info()
            self.handle_errors("title", response['name'], result)
            self.handle_errors("image", self.image_url + response['poster_path'], result)

                
        lst = []
        lst.append(result)
        return lst
    
    def get_cast_info(self, id, media_type):
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
            
        for cast_member in response['cast'][:15]:
            temp= {}
            self.handle_errors("name", cast_member['name'], temp)
            self.handle_errors("character", cast_member['character'], temp)
            try:
                self.handle_errors("img", self.image_url + cast_member['profile_path'], temp)
            except:
                pass
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
            self.handle_errors("id", recommendation['id'], temp)
            self.handle_errors("title", recommendation['title'], temp) if media_type == "movie" else self.handle_errors("title", recommendation['name'], temp)
            self.handle_errors("overview", recommendation['overview'], temp)
            self.handle_errors("img", self.image_url + recommendation['poster_path'] if recommendation['poster_path'] is not None else "None", temp)
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
