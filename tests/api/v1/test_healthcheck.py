import datetime

import pytest


@pytest.fixture()
def server_url(api_version):
    return f"/api/{api_version}"


@pytest.fixture()
def url(server_url):
    return f"{server_url}/healthcheck"


def test_正常終了(client, url, frozen_datetime):

    def assert_response(response, expected_read, expected_write):
        assert response.status_code == 200
        res = response.get_json()
        assert res['read_datetime'] == expected_read
        assert res['write_datetime'] == expected_write

    response1 = client.get(url)

    # 初回の read は None となる
    assert_response(response1,
                    None,
                    frozen_datetime().strftime('%Y-%m-%dT%H:%M:%S.%f'))

    frozen_datetime.tick(delta=datetime.timedelta(days=3))
    response2 = client.get(url)

    assert_response(response2,
                    response1.get_json()['write_datetime'],
                    frozen_datetime().strftime('%Y-%m-%dT%H:%M:%S.%f'))
