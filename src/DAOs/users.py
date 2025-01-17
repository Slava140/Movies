from sqlalchemy import insert, select

from database import db
from models.users import UserM
from schemas.users import InUserS, OutUserS, OutUserWithPassS
from services.utils import get_hashed_password


class UserDAO:
    model = UserM

    @classmethod
    def add(cls, user: InUserS) -> OutUserS:
        stmt = insert(
            UserM
        ).values(
            email=user.email,
            username=user.username,
            hashed_password=get_hashed_password(user.password)
        ).returning('*')

        with db.session.begin() as transaction:
            if cls.get_by_email(str(user.email)) is not None:
                raise ValueError(f'User with email {user.email} already exists')

            if cls.get_by_username(user.username) is not None:
                raise ValueError(f'User with username {user.username} already exists')

            result = db.session.execute(stmt).mappings().one()
            transaction.commit()

        return OutUserS(**result)

    @classmethod
    def get_by_email(cls, email: str, with_password: bool = False) -> OutUserS | OutUserWithPassS | None:
        query = select(
            cls.model
        ).where(
            cls.model.email == email
        )

        result = db.session.execute(query).scalar_one_or_none()

        if result is None:
            return None

        return OutUserWithPassS(**result.to_dict()) if with_password else OutUserS(**result.to_dict())

    @classmethod
    def get_by_username(cls, username: str) -> OutUserS | None:
        query = select(
            cls.model
        ).where(
            cls.model.username == username
        )

        result = db.session.execute(query).scalar_one_or_none()
        return OutUserS(**result.to_dict()) if result is not None else None