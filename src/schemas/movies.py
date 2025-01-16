import dataclasses
import datetime
from typing import Any, Annotated

from pydantic import BaseModel, PositiveInt, field_validator, Field, BeforeValidator

from base_pydantic_types import StrFrom1To255, StrFrom1To30, StrFrom1To500, NotEmptyStr
from models.movies import MovieM


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
    show_id:        StrFrom1To30
    type:           StrFrom1To255
    title:          StrFrom1To255
    director:       StrFrom1To500 | None
    cast:           NotEmptyStr | None
    country:        StrFrom1To500 | None
    date_added:     datetime.date | None
    release_year:   PositiveInt
    rating:         StrFrom1To30 | None
    duration:       PositiveInt
    listed_in:      StrFrom1To255
    description:    NotEmptyStr


class InMovieS(BaseMovieS):
    show_id:    Annotated[StrFrom1To30,         BeforeValidator(show_id_validator)]
    date_added: Annotated[datetime.date | None, BeforeValidator(date_added_validator)]
    duration:   Annotated[PositiveInt,          BeforeValidator(duration_validator)]


class OutMovieS(BaseMovieS):
    id: PositiveInt


#################

@dataclasses.dataclass()
class Default:
    limit = 50
    desc  = True
    sort_by = 'release_year'


def sorted_by_validator(value: str) -> str:
    if value in MovieM.get_fields_names():
        return value
    return Default.sort_by


class MoviesQS(BaseModel):
    find:  str
    limit: int  = Default.limit
    desc:  bool = Default.desc
    sort_by: Annotated[str, BeforeValidator(sorted_by_validator)] = Default.sort_by


