from unittest import mock

import pytest
from httpx import Response


@pytest.fixture(params=[
    pytest.param('asyncio'),
    pytest.param('trio'),
], autouse=True)
def aiolib(request):
    return request.param


@pytest.fixture(autouse=True)
def response():
    def generate(status_code=200, **params):
        return Response(status_code, **params)

    return generate


@pytest.fixture(autouse=True)
def http(response):
    with mock.patch('httpx.AsyncClient.request') as mocked:
        mocked.return_value = response(text='response=ok')
        yield mocked
