from typing import Annotated

from pydantic import Field, BeforeValidator


def empty_validator(value):
    if len(value) == 0:
        raise ValueError('String must be not empty.')
    return value

NotEmptyStr = Annotated[str, BeforeValidator(empty_validator)]

StrFrom1To30 = Annotated[NotEmptyStr, Field(max_length=30)]
StrFrom1To255 = Annotated[NotEmptyStr, Field(max_length=255)]
StrFrom1To500 = Annotated[NotEmptyStr, Field(max_length=500)]
