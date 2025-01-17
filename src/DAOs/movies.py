from typing import Iterable

from sqlalchemy import insert, select, text, desc, func
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
    def get_movies(cls,
                   *,
                   title: str | None,
                   limit: int,
                   offset: int,
                   more_first: bool,
                   sort_by: str) -> list[OutMovieS]:
        if title is None:
            query = select(cls.model)
        else:
            query = select(
                cls.model
            ).where(
                cls.model.title.ilike(f'%{title}%')
            )

        query = query.order_by(
            desc(text(sort_by)) if more_first else text(sort_by)
        ).limit(
            limit
        ).offset(
            offset
        )

        result = db.session.execute(query).scalars().fetchall()
        return [OutMovieS(**movie_model.to_dict()) for movie_model in result]

    @classmethod
    def get_movies_count(cls, title: str | None) -> int:
        query = select(
            func.count()
        ).select_from(
            cls.model
        )

        if title is not None:
            query = query.where(cls.model.title.ilike(f'%{title}%'))

        result = db.session.execute(query).scalar_one()
        return result

