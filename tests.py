from unittest import mock

import httpx
import pytest

from aioauth_client import * # noqa


@pytest.fixture(params=[
    pytest.param('asyncio'),
    pytest.param('trio'),
], autouse=True)
def aiolib(request):
    return request.param


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


async def test_client():
    with mock.patch('httpx.AsyncClient.request') as mocked:
        mocked.return_value = httpx.Response(200, text="test=passed")
        google = GoogleClient(client_id='123', client_secret='456', access_token='789')
        data = await google.request('GET', '/')
        assert data == {'test': 'passed'}


async def test_oauth2():  # noqa
    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )
    assert github

    assert 'github' in ClientRegistry.clients

    assert github.get_authorize_url()

    with mock.patch('aioauth_client.OAuth2Client._request') as mocked:
        mocked.return_value = {'access_token': 'TEST-TOKEN'}
        token, meta = await github.get_access_token('000')
        assert mocked.called
        assert token == 'TEST-TOKEN'
        assert meta

        mocked.reset_mock()
        mocked.return_value = {'access_token': 'TEST-TOKEN'}

        res = await github.request('GET', 'user', access_token='NEW-TEST-TOKEN')
        assert res
        mocked.assert_called_with(
            'GET', 'https://api.github.com/user',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Authorization': 'Bearer NEW-TEST-TOKEN'
            }
        )


async def test_custom_client():
    transport = httpx.AsyncClient()
    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        transport=transport,
    )
    assert github.transport

    with mock.patch.object(transport, 'send') as mocked:
        res = httpx.Response(200, headers={'Content-Type':  'json'})
        res._text = '{"access_token": "TOKEN"}'
        mocked.return_value = res

        token, meta = await github.get_access_token('000')
        assert token
        assert meta
        assert mocked.called

# pylama:ignore=W0401,E711
