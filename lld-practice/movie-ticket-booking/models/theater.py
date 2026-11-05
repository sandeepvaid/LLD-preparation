from rpds import List
from .movie import Movie

class Theater:
    def __init__(self, id: int, name: str, location: str,movies: List[Movie]):
        self.id = id
        self.name = name
        self.location = location
        self.movies = movies