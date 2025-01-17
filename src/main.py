from flask import Flask, Blueprint, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError
from pydantic import ValidationError

from database import db
from routes import router as movies_router, login_router, profile_router
from config import settings


main_router = Blueprint(name='main', import_name=__name__, url_prefix='/')
main_router.register_blueprint(movies_router)
main_router.register_blueprint(login_router)
main_router.register_blueprint(profile_router)


@main_router.get('/')
def is_ok():
    return 'ok'


def create_app() -> Flask:
    app_ = Flask(__name__)
    app_.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
    app_.config['SQLALCHEMY_ECHO'] = False
    app_.config["JWT_SECRET_KEY"] = settings.JWT_SECRET
    app_.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.access_token_ttl_timedelta
    app_.config['JWT_TOKEN_LOCATION'] = ['headers']

    app_.register_blueprint(main_router)

    with app_.app_context():
        db.init_app(app_)

    JWTManager(app_)

    return app_


@main_router.errorhandler(JWTExtendedException)
def handle_flask_jwt_error(error: JWTExtendedException):
    return jsonify({'message': str(error)}), 401


@main_router.errorhandler(PyJWTError)
def handle_jwt_error(error: PyJWTError):
    return jsonify({'message': str(error)}), 401


@main_router.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    errors = [
        {
            'loc': err['loc'],
            'input': err['input'],
            'msg': err['msg']
        } for err in error.errors()
    ]
    return jsonify(errors), 422


@main_router.errorhandler(ValueError)
def handle_value_error(error: ValueError):
    return jsonify({'message': str(error)}), 400


if __name__ == "__main__":
    app = create_app()
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)
