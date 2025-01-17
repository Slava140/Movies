import re
from typing import Annotated

from pydantic import Field, BeforeValidator, AfterValidator


def password_validator(value: str) -> str:
    if len(value) < 8:
        raise ValueError('Password length must be greater or equal than 8')

    if len(value) > 20:
        raise ValueError('Password length must be less or equal than 20')

    if not re.search(r'\d', value):
        raise ValueError('Password must contain at least one digit')

    if not re.search(r'[A-Z]', value):
        raise ValueError('Password must contain at least one uppercase letter')

    if not re.search(r'[a-z]', value):
        raise ValueError('Password must contain at least one lowercase letter')

    return value


def empty_validator(value):
    if len(value) == 0:
        raise ValueError('String must be not empty.')
    return value

NotEmptyStr = Annotated[str, BeforeValidator(empty_validator)]

NotEmptyStr30 = Annotated[NotEmptyStr, Field(max_length=30)]
NotEmptyStr255 = Annotated[NotEmptyStr, Field(max_length=255)]
NotEmptyStr500 = Annotated[NotEmptyStr, Field(max_length=500)]

PasswordStr = Annotated[str, AfterValidator(password_validator)]

