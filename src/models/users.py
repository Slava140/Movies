from sqlalchemy.orm import Mapped

from database import Base, pk_int, str_255_unique


class UserM(Base):
    __tablename__ = 'users'

    id:                 Mapped[pk_int]
    username:           Mapped[str_255_unique]
    email:              Mapped[str_255_unique]
    hashed_password:    Mapped[str]