import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api


def set_env_value_to_app(app, key):
    env_value = os.getenv(key)
    if env_value is not None:
        app.config[key] = env_value


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE_URL=os.getenv('DATABASE_URL'),
    )

    set_env_value_to_app(app, 'SESSION_COOKIE_NAME')
    set_env_value_to_app(app, 'SESSION_COOKIE_HTTPONLY')
    set_env_value_to_app(app, 'SESSION_COOKIE_SECURE')
    set_env_value_to_app(app, 'SESSION_COOKIE_SAMESITE')

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

    cors_origins = os.getenv('CORS_ORIGINS')
    cors_origins = cors_origins.split(',') if cors_origins is not None else None
    cors_methods = os.getenv('CORS_METHODS')
    cors_methods = cors_methods.split(',') if cors_methods is not None else None
    cors_allow_headers = os.getenv('CORS_ALLOW_HEADERS')
    cors_allow_headers = cors_allow_headers.split(',') if cors_allow_headers is not None else None
    cors_supports_credentials = os.getenv('CORS_SUPPORTS_CREDENTIALS')
    cors_supports_credentials = cors_supports_credentials if cors_supports_credentials is not None else False
    app.config.from_mapping(
        CORS_ORIGINS=cors_origins,
        CORS_METHODS=cors_methods,
        CORS_ALLOW_HEADERS=cors_allow_headers,
        CORS_SUPPORTS_CREDENTIALS=cors_supports_credentials,
    )
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

    return app
