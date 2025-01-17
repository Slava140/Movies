import datetime
from typing import Any, Annotated

from pydantic import BaseModel, PositiveInt, Field, BeforeValidator

from base_pydantic_types import NotEmptyStr255, NotEmptyStr30, NotEmptyStr500, NotEmptyStr


def show_id_validator(value: Any) -> str:
    return str(value)


def date_added_validator(value: str | None) -> datetime.date | None:
    if value is None:
        return None
    value_datetime = datetime.datetime.strptime(value.strip(), '%B %d, %Y')
    return value_datetime.date()


def duration_validator(value: str) -> int:
    number, minutes_or_season = value.strip().split()
    return int(number)


class BaseMovieS(BaseModel):
    show_id:        NotEmptyStr30
    type:           NotEmptyStr255
    title:          NotEmptyStr255
    director:       NotEmptyStr500 | None
    cast:           NotEmptyStr | None
    country:        NotEmptyStr500 | None
    date_added:     datetime.date | None
    release_year:   PositiveInt
    rating: NotEmptyStr30 | None
    duration:       PositiveInt
    listed_in:      NotEmptyStr255
    description:    NotEmptyStr


class InMovieS(BaseMovieS):
    show_id:    Annotated[NotEmptyStr30,         BeforeValidator(show_id_validator)]
    date_added: Annotated[datetime.date | None, BeforeValidator(date_added_validator)]
    duration:   Annotated[PositiveInt,          BeforeValidator(duration_validator)]


class OutMovieS(BaseMovieS):
    id: PositiveInt


#################


class MoviesQS(BaseModel):
    draw:   int
    start:  int
    length: int
    start:  int
    search_value: Annotated[str, Field(alias='search[value]')]
    order_by: Annotated[str, Field(alias='order[0][name]')] = 'release_year'
    order_direction: Annotated[str, Field(alias='order[0][dir]')] = 'desc'
