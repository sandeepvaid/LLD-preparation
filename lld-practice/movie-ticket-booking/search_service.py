class SearchService:
    def __init__(self,theaters):
        self.theaters = theaters
        
    def search_movie_by_location(self,location):
        movies = []
        for theater in self.theaters:
            if theater.location == location:
                movies.extend(theater.movies)
        return movies