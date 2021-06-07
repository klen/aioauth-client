from unittest import mock
from httpx import Response

import pytest

from aioauth_client import * # noqa


@pytest.fixture(params=[
    pytest.param('asyncio'),
    pytest.param('trio'),
], autouse=True)
def aiolib(request):
    return request.param


@pytest.fixture(autouse=True)
def http():
    with mock.patch('httpx.AsyncClient.request') as mocked:
        mocked.return_value = Response(200, text='response=ok')
        yield mocked


def test_userinfo_container():
    user = User(email='email')
    assert user.email == 'email'
    assert user.id == None


def test_signatures():
    sig = HmacSha1Signature()
    assert sig.name
    assert sig.sign('secret', 'GET', '/test', oauth_token_secret='secret')


@pytest.mark.skip
def test_oauth1(loop):  # noqa
    twitter = TwitterClient(
        consumer_key='oUXo1M7q1rlsPXm4ER3dWnMt8',
        consumer_secret='YWzEvXZJO9PI6f9w2FtwUJenMvy9SPLrHOvnNkVkc5LdYjKKup',
    )
    assert twitter

    assert 'twitter' in ClientRegistry.clients

    coro = twitter.get_request_token(oauth_callback='http://fuf.me:5000/twitter')
    rtoken, rsecret, _ = loop.run_until_complete(coro)
    assert rtoken
    assert rsecret
    assert twitter.oauth_token == rtoken
    assert twitter.oauth_token_secret == rsecret

    url = twitter.get_authorize_url()
    assert url == 'https://api.twitter.com/oauth/authorize?oauth_token=%s' % rtoken

    coro = twitter.get_access_token('wrong', rtoken)
    with pytest.raises(web.HTTPBadRequest):
        loop.run_until_complete(coro)


async def test_client(http):
    google = GoogleClient(client_id='123', client_secret='456', access_token='789')
    data = await google.request('GET', '/')
    assert data == {'response': 'ok'}
    http.assert_called_with(
        'GET', 'https://www.googleapis.com/', params=None,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer 789'
        }
    )


async def test_oauth2(http):
    github = GithubClient(client_id='cid', client_secret='csecret')
    assert github
    assert 'github' in ClientRegistry.clients
    assert github.get_authorize_url() == 'https://github.com/login/oauth/authorize?client_id=cid&response_type=code'  # noqa

    http.return_value = Response(200, json={'access_token': 'TEST-TOKEN'})
    token, meta = await github.get_access_token('000')
    assert token == 'TEST-TOKEN'
    assert meta
    assert http.called

    http.reset_mock()
    http.return_value = Response(200, json={'access_token': 'TEST-TOKEN'})

    res = await github.request('GET', 'user', access_token='NEW-TEST-TOKEN')
    assert res
    http.assert_called_with(
        'GET', 'https://api.github.com/user', params=None,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer NEW-TEST-TOKEN'
        }
    )


async def test_oauth2_request(http):
    github = GithubClient(client_id='cid', client_secret='csecret', access_token='token')
    res = await github.request('GET', '/user', params={'test': 'ok'})
    assert res
    http.assert_called_with(
        'GET', 'https://api.github.com/user', params={'test': 'ok'},
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer token'
        }
    )


async def test_custom_client(http):
    transport = httpx.AsyncClient()
    github = GithubClient(client_id='cid', client_secret='csecret', transport=transport)
    assert github.transport

    http.return_value = Response(200, json={'access_token': 'TOKEN'})

    token, meta = await github.get_access_token('000')
    assert token
    assert meta
    assert http.called


# pylama:ignore=W0401,E711
