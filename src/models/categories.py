from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, pk_int, str_255_unique


class CategoryM(Base):
    __tablename__ = 'categories'

    id:         Mapped[pk_int]
    name:       Mapped[str_255_unique]


class MovieCategoryM(Base):
    __tablename__ = 'movies_categories'

    id:             Mapped[pk_int]
    movie_id:       Mapped[int] = mapped_column(ForeignKey(column='movies.id'))
    category_id:    Mapped[int] = mapped_column(ForeignKey(column='categories.id'))