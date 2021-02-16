import imdb

class IMDBAPI():
    
    def __init__(self):
        self.imdb = imdb.IMDb()
        
    def retrieve(self, tmdb_id):
        response = self.imdb.get_movie(tmdb_id, info=['synopsis', 'plot'])
        self.imdb.update(response)
        result_obj = {}
        try:
            self.handle_errors(result_obj, 'synopsis', response['synopsis'][0])
        except:
            result_obj['synopsis'] = ""
        self.handle_errors(result_obj, 'imdb_rating', response['rating'])
        self.handle_errors(result_obj, 'votes', response['votes'])
        return result_obj
    
    def retrieve_tv(self, tmdb_id):
        response = self.imdb.get_movie(tmdb_id, info=['synopsis', 'plot'])
        self.imdb.update(response)
        
        result_obj = {}
        try:
            self.handle_errors(result_obj, 'synopsis', max(response['plot'], key=len).split('::',1)[0])
        except:
            result_obj['synopsis'] = ""
        self.handle_errors(result_obj, 'imdb_rating', response['rating'])
        self.handle_errors(result_obj, 'votes', response['votes'])
        return result_obj
        
        
    def handle_errors(self, result, result_col, response):
        try:
            result[result_col] = response
        except:
            pass