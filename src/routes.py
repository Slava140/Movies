from flask import Blueprint

from config import settings
from decorators.validator import validate
from schemas.movies import InMovieS, OutMovieS, MoviesQS
from services.movies import MovieService
from utils import converter

router = Blueprint(name='movies', import_name=__name__, url_prefix='/movies')


@router.get('/from_csv/')
def add_movies_from_csv() -> str:
    converter.save_movies_to_table(settings.SRC_PATH.parent / 'files' / 'movies.csv', MovieService())
    return 'ok'


@router.get('/')
@validate()
def get_movies(query: MoviesQS):
    return MovieService.find_by_title(query.find, query.limit, query.desc, query.sort_by)
