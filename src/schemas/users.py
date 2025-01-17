from pydantic import BaseModel, EmailStr, NonNegativeInt

from base_pydantic_types import PasswordStr, NotEmptyStr255


class BaseUserS(BaseModel):
    username:   NotEmptyStr255
    email:      EmailStr


class InUserS(BaseUserS):
    password: PasswordStr


class OutUserS(BaseUserS):
    id: NonNegativeInt


class OutUserWithPassS(OutUserS):
    hashed_password: str


class LoggedInUserS(OutUserS):
    access_token: str


class LoginUserS(BaseModel):
    email:      EmailStr
    password:   str