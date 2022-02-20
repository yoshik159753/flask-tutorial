import os
from http import cookies

import jwt
import pytest


@pytest.mark.parametrize(('username', 'password', 'error_code'), (
    ('a', 'test', 1),
    ('test', 'a', 1),
))
def test_ログインできないこと(authApi, api_version, username, password, error_code):
    response = authApi.login(username=username,
                             password=password,
                             api_version=api_version)
    assert response.status_code == 400

    res = response.get_json()
    assert res['error_code'] == error_code


def test_ログインできること(authApi, api_version):
    response = authApi.login(api_version=api_version)
    assert response.status_code == 200

    # cookie に token があること
    # ref. https://stackoverflow.com/questions/55517607/accessing-all-cookies-in-the-flask-test-response
    cookies_str = response.headers.get('Set-Cookie')
    assert cookies_str is not None
    cookie = cookies.SimpleCookie()
    cookie.load(cookies_str)
    assert cookie["session-token"]["httponly"] is True
    payload = jwt.decode(cookie["session-token"].value,
                         key=os.getenv('SECRET_KEY'),
                         algorithms=['HS256'])
    assert payload is not None
