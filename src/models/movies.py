from datetime import date

from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_500, str_255, str_30, str_30_unique


class MovieM(Base):
    __tablename__ = 'movies'

    id:             Mapped[pk_int]
    show_id:        Mapped[str_30_unique]
    type:           Mapped[str_255]
    title:          Mapped[str_255]
    director:       Mapped[str_500 | None]
    cast:           Mapped[str | None]
    country:        Mapped[str_500 | None]
    date_added:     Mapped[date | None]
    release_year:   Mapped[int]
    rating:         Mapped[str_30 | None]
    duration:       Mapped[int]
    listed_in:      Mapped[str_255]
    description:    Mapped[str]

