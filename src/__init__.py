from flask_restx import Api

from src.db import db
from flask import g, jsonify, session, Blueprint
import config
from src.extensions import app
from .custom_exceptions import NotFoundError, NotAuthorizedError, BusinessRuleConflictError
from .apis.books import api as book_api
from .apis.libraries import api as library_api
from .apis.library_books_records import api as library_book_api
from .apis.users import api as user_api

blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint, title='Libraries API', version='1.0', description='')
api.add_namespace(book_api, '/books')
api.add_namespace(library_api, '/libraries')
api.add_namespace(library_book_api, '/library_book_records')
api.add_namespace(user_api, '/users')


def register_extensions(app):
    with app.app_context():
        db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blueprint)
    pass


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all(app=app)

    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        db.session.remove()


def handle_error(error):
    error_payload = error.to_dict()
    return jsonify(error_payload), getattr(error, "code")


def load_error_handler(app):
    app.register_error_handler(NotFoundError, handle_error)
    app.register_error_handler(NotAuthorizedError, handle_error)
    app.register_error_handler(BusinessRuleConflictError, handle_error)


def init_app():
    config.load(app)
    configure_database(app)
    register_extensions(app)
    register_blueprints(app)
    load_error_handler(app)
    return app
