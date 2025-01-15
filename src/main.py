from flask import Flask
from flask.sansio.blueprints import Blueprint

from config import settings

main_router = Blueprint(name='main', import_name=__name__, url_prefix='/')


@main_router.get('/')
def is_ok():
    return 'ok'

def create_app() -> Flask:
    app_ = Flask(__name__)
    app_.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
    return app_


if __name__ == "__main__":
    app = create_app()
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)
