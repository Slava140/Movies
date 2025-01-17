from flask_jwt_extended import create_access_token

from DAOs.users import UserDAO
from schemas.users import InUserS, OutUserS, LoggedInUserS, LoginUserS
from services.utils import is_correct_password


class UserService:
    dao = UserDAO

    @classmethod
    def register(cls, user: InUserS) -> LoggedInUserS:
        created_user = cls.dao.add(user)
        access_token = create_access_token(identity=str(created_user.id))
        return LoggedInUserS(**user.model_dump(), access_token=access_token)

    @classmethod
    def login(cls, user_credential: LoginUserS) -> LoggedInUserS:
        user = UserDAO.get_by_email(email=str(user_credential.email), with_password=True)

        if user is not None and is_correct_password(user_credential.password, user.hashed_password):
            access_token = create_access_token(identity=str(user.id))
            return LoggedInUserS(**user.model_dump(), access_token=access_token)
        else:
            raise ValueError('Invalid email or password.')
