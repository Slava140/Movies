from typing import Iterable

from sqlalchemy import insert, select, text, desc
from sqlalchemy.exc import IntegrityError

from models.movies import MovieM
from schemas.movies import InMovieS, OutMovieS
from database import db


class MovieDAO:
    model = MovieM

    @classmethod
    def add(cls, movie: InMovieS) -> OutMovieS:
        print('Я выполняюсь')
        stmt = insert(
            cls.model
        ).values(
            **movie.model_dump()
        ).returning('*')

        result = db.session.execute(stmt).mappings().one()
        db.session.commit()
        print(result)
        return OutMovieS(**result)

    @classmethod
    def add_many(cls, movies: Iterable[InMovieS]) -> list[OutMovieS]:
        stmt = insert(
            cls.model
        ).values(
            [movie.model_dump() for movie in movies]
        ).returning('*')

        try:
            result = db.session.execute(stmt).mappings().fetchall()
            db.session.commit()
            return [OutMovieS(**movie_dict) for movie_dict in result]
        except IntegrityError as error:
            raise ValueError(f'Cannot insert entities. {error.orig}') from None

    @classmethod
    def find_by_title(cls, title: str, size: int, more_first: bool, sort_by: str) -> list[OutMovieS]:
        query = select(
            cls.model
        ).where(
            cls.model.title.ilike(f'%{title}%')
        ).order_by(
            desc(text(sort_by)) if more_first else text(sort_by)
        ).limit(
            size
        )


        result = db.session.execute(query).scalars().fetchall()
        return [OutMovieS(**movie_model.to_dict()) for movie_model in result]