from flask import Flask, Blueprint

from database import db
from routes import router as movies_router
from config import settings


main_router = Blueprint(name='main', import_name=__name__, url_prefix='/')
main_router.register_blueprint(movies_router)


@main_router.get('/')
def is_ok():
    return 'ok'


def create_app() -> Flask:
    app_ = Flask(__name__)
    app_.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
    app_.config['SQLALCHEMY_ECHO'] = False

    app_.register_blueprint(main_router)

    with app_.app_context():
        db.init_app(app_)

    return app_


if __name__ == "__main__":
    app = create_app()
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)
