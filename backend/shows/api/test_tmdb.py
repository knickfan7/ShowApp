import unittest
from tmdb import TMDB

""" 
    Run Tests
    
    python test_tmdb.py
    python test_tmdb.py TMDBTestCase.test_search
    python test_tmdb.py TMDBTestCase.test_info
    python test_tmdb.py TMDBTestCase.test_recommendations
"""

tmdb = TMDB()

ANIME_ID_1 = 12971 # DBZ
ANIME_ID_2 = 295830 # AOT

MOVIE_ID_1 = 120 # LOTR Fellowship
MOVIE_ID_2 = 447404 # Detective Pikachu

SHOW_ID_1 = 95834 # Legend of Fei
SHOW_ID_2 = 1399 # GoT

class TMDBTestCase(unittest.TestCase):
    
    def display_list(self, lst):
        """
            Prints the results in user friendly view
            
            Args: list of movies and shows
        """
        for i in range(len(lst)):
            print(str(i) + ": " + lst[i]['title'] + ' ' + str(lst[i]['id'])) 
        print()
        
    def display_friendly(self, lst):
        for x in lst:
            print("\033[1m Title: \033[0m" + x['title'])
            print("\033[1m Description: \033[0m" + x['description'])
            
            try:
                print("\033[1m Release Date: \033[0m" + x['release_date'])
            except:
                pass
            print("\033[1m Main Language: \033[0m" + x['language'])
            
            try:
                print("\033[1m Genre List: \033[0m")
                for genre in x['genres']:
                    print("\t\u2022 " + genre)
            except:
                print("\u2022 None")
                
            print("\033[1m Image: \033[0m" + x['img'])
            try:
                print("\033[1m Video List: \033[0m")
                
                for video in x['trailer']:
                    print("\t\u2022 " + video)
            except:
                print("\u2022 None")
            print()
     
    def test_search(self):
        # Test Search for Anime
        result = tmdb.get_search_results("Dragon Ball Z")
        self.display_list(result)
        
        result = tmdb.get_search_results("Attack on Titan")
        self.display_list(result)
        
        # Test Search for Movie
        result = tmdb.get_search_results("Lord of the Rings: The Fellowship of the Ring")
        self.display_list(result)
        
        result = tmdb.get_search_results("Detective Pikachu")
        self.display_list(result)
        
        # Test Search for Shows
        result = tmdb.get_search_results("Legend of Fei")
        self.display_list(result)
        
        result = tmdb.get_search_results("Game of Thrones")
        self.display_list(result)

    def test_get_info(self):
        result = tmdb.get_info(MOVIE_ID_1, "movie")  
        print(result)
        #result = tmdb.get_info(SHOW_ID_2, "tv")  
        #print(result)
        
    def test_tv_page(self):
        result = tmdb.get_tv_page()
        print(result)
        
if __name__ == "__main__":
    unittest.main()