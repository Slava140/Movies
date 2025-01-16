from copy import deepcopy
from typing import Annotated

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, registry, mapped_column


str_30 = Annotated[str, 30]
str_255 = Annotated[str, 255]
str_500 = Annotated[str, 500]

str_30_unique = Annotated[str, mapped_column(String(30), unique=True)]
str_255_unique = Annotated[str, mapped_column(String(255), unique=True)]

pk_int = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_30: String(30),
            str_255: String(255),
            str_500: String(500),
        }
    )

    def to_dict(self) -> dict:
        d = deepcopy(self.__dict__)
        d.pop('_sa_instance_state')
        return d

    @classmethod
    def get_fields_names(cls):
        return cls.__table__.c

db = SQLAlchemy(model_class=Base, engine_options={"connect_args": {"options": "-c timezone=utc"}})
