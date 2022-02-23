from http import HTTPStatus


def test_ログアウト後は401であること(authApi, api_version):
    response = authApi.login(api_version=api_version)
    assert response.status_code == HTTPStatus.OK

    response = authApi.logout(api_version=api_version)
    assert response.status_code == HTTPStatus.OK

    response = authApi.is_logged_in(api_version=api_version)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_ログイン中は200であること(authApi, api_version):
    response = authApi.login(api_version=api_version)
    assert response.status_code == HTTPStatus.OK

    response = authApi.is_logged_in(api_version=api_version)
    assert response.status_code == HTTPStatus.OK


def test_ログインしていない場合は401であること(authApi, api_version):
    response = authApi.is_logged_in(api_version=api_version)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
