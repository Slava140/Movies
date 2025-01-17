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
    def get_movies(cls,
                   *,
                   limit: int,
                   offset: int,
                   more_first: bool,
                   sort_by: str,
                   title: str | None = None) -> list[OutMovieS]:
        return cls.dao.get_movies(
            title=title,
            limit=limit,
            offset=offset,
            more_first=more_first,
            sort_by=sort_by
        )

    @classmethod
    def get_movies_count(cls, title: str | None = None) -> int:
        return cls.dao.get_movies_count(title)


