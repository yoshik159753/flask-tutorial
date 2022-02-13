import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db
from freezegun import freeze_time

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE_URL': os.getenv('TEST_DATABASE_URL'),
    })

    with app.app_context():
        init_db()

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(_data_sql)
        db.commit()

        yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def frozen_datetime():
    test_datetime_str = "2020-01-23T12:34:56.123456+00:00"
    with freeze_time(test_datetime_str) as frozen_datetime_:
        yield frozen_datetime_
