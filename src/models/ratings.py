from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_16_unique


class RatingM(Base):
    __tablename__ = 'ratings'

    id:     Mapped[pk_int]
    name:   Mapped[str_16_unique]
