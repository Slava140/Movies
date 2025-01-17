from flask import Blueprint, render_template, request, make_response, redirect, url_for
from flask_jwt_extended import jwt_required

from config import settings
from decorators.validator import validate
from schemas.movies import MoviesQS
from schemas.users import InUserS, OutUserS, LoginUserS
from services.movies import MovieService
from services.users import UserService
from utils import converter

router = Blueprint(name='movies', import_name=__name__, url_prefix='/movies')
login_router = Blueprint(name='login', import_name=__name__, url_prefix='/login')
profile_router = Blueprint(name='profile', import_name=__name__, url_prefix='/profile')


@router.get('/from_csv/')
def add_movies_from_csv() -> str:
    converter.save_movies_to_table(settings.SRC_PATH.parent / 'files' / 'movies.csv', MovieService())
    return 'ok'


@router.get('/data/')
@validate()
def get_movies(query: MoviesQS):
    print(request.args.get('order[3][dir]'))
    movies_schemas = MovieService.get_movies(
        title=query.search_value,
        limit=query.length,
        offset=query.start,
        more_first=query.order_direction == 'desc',
        sort_by=query.order_by
    )
    total_movies_count = MovieService.get_movies_count()
    filtered_movies_count = MovieService.get_movies_count(query.search_value)
    return {
        'data': [movie.model_dump() for movie in movies_schemas],
        'draw': query.draw,
        'recordsFiltered': filtered_movies_count,
        'recordsTotal': total_movies_count
    }


@router.get('/')
def movies_table_view():
    return render_template('index.html', title='Movies')


@login_router.post('/register/')
@validate()
def register(body: InUserS) -> OutUserS:
    return UserService.register(body)

@login_router.post('/')
@validate()
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return UserService.login(LoginUserS(email=email, password=password))


@login_router.get('/')
def login_view():
    return render_template('login.html')


@profile_router.get('/')
@jwt_required()
def profile_view():
    return render_template('profile.html')