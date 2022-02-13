import pytest


@pytest.fixture()
def api_version():
    return 'v1'


@pytest.fixture()
def server_url(api_version):
    return f"/api/{api_version}"
