""" Aioauth-client example. """

import asyncio

from aiohttp import web
from aioauth_client import GithubClient, TwitterClient, GoogleClient


app = web.Application()


@asyncio.coroutine
def index(request):
    return web.Response(text="""
        <ul>
            <li><a href="/oauth/google">Login with Google</a></li>
            <li><a href="/oauth/github">Login with Github</a></li>
            <li><a href="/oauth/twitter">Login with Twitter</a></li>
        </ul>
    """, content_type="text/html")


@asyncio.coroutine
def twitter(request):
    twitter = TwitterClient(
        consumer_key='oUXo1M7q1rlsPXm4ER3dWnMt8',
        consumer_secret='YWzEvXZJO9PI6f9w2FtwUJenMvy9SPLrHOvnNkVkc5LdYjKKup',
    )
    if 'oauth_verifier' not in request.GET:
        token, secret = yield from twitter.get_request_token()

        # Dirty save a token_secret
        # Dont do it in production
        request.app.secret = secret
        request.app.token = token

        return web.HTTPFound(twitter.get_authorize_url())

    oauth_verifier = request.GET['oauth_verifier']
    twitter.oauth_token_secret = request.app.secret
    twitter.oauth_token = request.app.token

    # Get access token
    token, secret = yield from twitter.get_access_token(oauth_verifier)

    # Get a resource
    response = yield from twitter.request('GET', 'account/verify_credentials.json')
    body = yield from response.read()
    return web.Response(body=body, content_type='application/json')


@asyncio.coroutine
def github(request):
    github = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )
    if 'code' not in request.GET:
        return web.HTTPFound(github.get_authorize_url(scope='user:email'))

    # Get access token
    code = request.GET['code']
    token = yield from github.get_access_token(code)

    # Get a resource
    response = yield from github.request('GET', 'user')
    body = yield from response.read()
    return web.Response(body=body, content_type='application/json')


@asyncio.coroutine
def google(request):
    google = GoogleClient(
        client_id='150775235058-9fmas709maee5nn053knv1heov12sh4n.apps.googleusercontent.com',
        client_secret='df3JwpfRf8RIBz-9avNW8Gx7',

        redirect_uri='http://%s%s' % (request.host, request.path),
        scope='email profile',
    )
    if 'code' not in request.GET:
        return web.HTTPFound(google.get_authorize_url())

    # Get access token
    code = request.GET['code']
    token = yield from google.get_access_token(code)

    # Get a resource
    response = yield from google.request('GET', 'people/me')
    body = yield from response.read()
    return web.Response(body=body, content_type='application/json')


app.router.add_route('GET', '/', index)
app.router.add_route('GET', '/oauth/twitter', twitter)
app.router.add_route('GET', '/oauth/github', github)
app.router.add_route('GET', '/oauth/google', google)

loop = asyncio.get_event_loop()
f = loop.create_server(app.make_handler(), '127.0.0.1', 5000)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# pylama:ignore=D
