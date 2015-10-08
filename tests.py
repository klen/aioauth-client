from aioauth_client import * # noqa
import pytest
import asyncio


@pytest.fixture(scope='session')
def loop():
    return asyncio.get_event_loop()


def test_oauth1(loop):
    twitter = TwitterClient(
        consumer_key='oUXo1M7q1rlsPXm4ER3dWnMt8',
        consumer_secret='YWzEvXZJO9PI6f9w2FtwUJenMvy9SPLrHOvnNkVkc5LdYjKKup',
    )
    assert twitter

    assert 'twitter' in ClientRegistry.clients

    coro = twitter.get_request_token(oauth_callback='http://fuf.me:5000/twitter')
    rtoken, rsecret = loop.run_until_complete(coro)
    assert rtoken
    assert rsecret
    assert twitter.oauth_token == rtoken
    assert twitter.oauth_token_secret == rsecret

    url = twitter.get_authorize_url()
    assert url == 'https://api.twitter.com/oauth/authorize?oauth_token=%s' % rtoken

    coro = twitter.get_access_token('wrong', rtoken)
    with pytest.raises(web.HTTPBadRequest):
        loop.run_until_complete(coro)


def test_oauth2(loop):
    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )
    assert github

    assert 'github' in ClientRegistry.clients

    assert github.get_authorize_url()

    coro = github.get_access_token('000')

    with pytest.raises(web.HTTPBadRequest):
        loop.run_until_complete(coro)
