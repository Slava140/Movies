from pathlib import Path
from typing import Sequence, Mapping

from numpy import nan
import pandas as pd

from schemas.movies import InMovieS
from services.movies import MovieService


def rows_to_schemas(rows: Sequence[Mapping[str, str | int | None]]) -> tuple[InMovieS, ...]:
    return tuple(InMovieS(**movie_dict) for movie_dict in rows)

def save_movies_to_table(path_to_csv: str | Path, movie_service: MovieService, movies_in_part: int = 1000) -> None:
    movies_df = pd.read_csv(path_to_csv)
    movies_df = movies_df.replace(nan, None)

    for part_start_index in range(0, len(movies_df), movies_in_part):
        part_end_index = part_start_index + movies_in_part
        part_df = movies_df[part_start_index:part_end_index]
        movie_schemas = rows_to_schemas(part_df.to_dict('records'))
        movie_service.add_many(movie_schemas)
