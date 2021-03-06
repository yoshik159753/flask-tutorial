from http import cookies

from flask import current_app


def test_ログアウトできること(authApi, api_version):
    response = authApi.login(api_version=api_version)
    assert response.status_code == 200

    response = authApi.logout(api_version=api_version)
    assert response.status_code == 200

    # cookie の token の値がないこと
    cookies_str = response.headers.get('Set-Cookie')
    assert cookies_str is not None
    cookie = cookies.SimpleCookie()
    cookie.load(cookies_str)
    session_name = current_app.config.get('JWT_ACCESS_COOKIE_NAME')
    assert cookie[session_name]["httponly"] is True
    assert cookie[session_name].value == ''


def test_ログアウト中にログアウトできること(authApi, api_version):
    response = authApi.logout(api_version=api_version)
    assert response.status_code == 200

    # cookie の token の値がないこと
    cookies_str = response.headers.get('Set-Cookie')
    assert cookies_str is not None
    cookie = cookies.SimpleCookie()
    cookie.load(cookies_str)
    session_name = current_app.config.get('JWT_ACCESS_COOKIE_NAME')
    assert cookie[session_name]["httponly"] is True
    assert cookie[session_name].value == ''
