import pytest


@pytest.fixture()
def url(server_url):
    return f"{server_url}/blog"


def test_一覧を取得できること(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert response.headers.get('X-Total-Count') == '1'
    blogs = response.get_json()
    assert len(blogs) == 1
    blog = blogs[0]
    assert blog['title'] == 'test title'
    assert blog['created'] == '2018-01-01T00:00:00'
    assert blog['body'] == 'test\nbody'
    assert blog['author_id'] == 1
