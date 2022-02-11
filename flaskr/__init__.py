import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE_URL=os.getenv('DATABASE_URL'),
    )

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
    app.config.from_mapping(
        CORS_ORIGINS=cors_origins,
        CORS_METHODS=cors_methods,
        CORS_ALLOW_HEADERS=cors_allow_headers
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
