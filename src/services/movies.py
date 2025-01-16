from typing import Sequence

from DAOs.movies import MovieDAO
from schemas.movies import InMovieS, OutMovieS


class MovieService:
    dao = MovieDAO

    @classmethod
    def add(cls, movie: InMovieS) -> OutMovieS:
        return cls.dao.add(movie)

    @classmethod
    def add_many(cls, movies: Sequence[InMovieS]) -> list[OutMovieS]:
        if len(movies) > 1000:
            raise ValueError('Too many entities. Max count 1000.')

        return cls.dao.add_many(movies)

    @classmethod
    def find_by_title(cls, title: str, size: int, desc: bool, sort_by: str):
        return cls.dao.find_by_title(title, size, desc, sort_by)


