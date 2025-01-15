from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, pk_int, str_500, str_16, str_255


class MovieM(Base):
    __tablename__ = 'movies'

    id:             Mapped[pk_int]
    show_id:        Mapped[str_16]
    type:           Mapped[str_255]
    title:          Mapped[str_255]
    director:       Mapped[str_500]
    cast:           Mapped[str_500]
    country:        Mapped[str_500]
    date_added:     Mapped[date]
    duration:       Mapped[int]
    description:    Mapped[str]

    category_id:    Mapped[int] = mapped_column(ForeignKey(column='categories.id'))
    rating_id:      Mapped[int] = mapped_column(ForeignKey(column='ratings.id'))
