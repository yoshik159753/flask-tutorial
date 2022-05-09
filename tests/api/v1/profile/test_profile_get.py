import pytest


@pytest.fixture()
def url(server_url):
    return f"{server_url}/profile"


def test_githubからプロフィールを取得できること(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_githubから英語のプロフィールを取得できること(client, url):
    response = client.get(f"{url}?lang=en")
    assert response.status_code == 200
