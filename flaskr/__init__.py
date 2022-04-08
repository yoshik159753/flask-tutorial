import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if os.getenv('SECRET_KEY') is not None:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if os.getenv('DATABASE_URL') is not None:
        app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if os.getenv('CORS_ORIGINS') is not None:
        app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS').split(',')
    if os.getenv('CORS_METHODS') is not None:
        app.config['CORS_METHODS'] = os.getenv('CORS_METHODS').split(',')
    if os.getenv('CORS_ALLOW_HEADERS') is not None:
        app.config['CORS_ALLOW_HEADERS'] = os.getenv('CORS_ALLOW_HEADERS').split(',')
    if os.getenv('CORS_SUPPORTS_CREDENTIALS') is not None:
        app.config['CORS_SUPPORTS_CREDENTIALS'] = os.getenv('CORS_SUPPORTS_CREDENTIALS')
    CORS(app)

    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from .routes.routes import initialize_routes
    api = Api(app)
    initialize_routes(api)

    if os.getenv('JWT_TOKEN_LOCATION') is not None:
        app.config['JWT_TOKEN_LOCATION'] = os.getenv('JWT_TOKEN_LOCATION').split(',')
    if os.getenv('JWT_COOKIE_SECURE') is not None:
        app.config['JWT_COOKIE_SECURE'] = os.getenv('JWT_COOKIE_SECURE')
    if os.getenv('JWT_COOKIE_SAMESITE') is not None:
        app.config['JWT_COOKIE_SAMESITE'] = os.getenv('JWT_COOKIE_SAMESITE')
    JWTManager(app)

    return app
