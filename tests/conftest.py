import pytest
from httpx import Response

# python 3.7
try:
    import mock  # type: ignore
except ImportError:
    from unittest import mock  # type: ignore


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
