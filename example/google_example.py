"""
enable Google+ API by visiting
https://console.developers.google.com/apis/api/plus.googleapis.com/overview

requirements:
    aiodns
    aiohttp
    aiohttp_session
    aiohttp_session[secure]
    cchardet
    cryptography

    aioauth-client
"""

import aiohttp_session
from aioauth_client import GoogleClient
from aiohttp import web
from aiohttp_session import get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage


class cfg:
    oauth_redirect_path = '/oauth'  # path of oauth callback in your app
    redirect_uri = 'http://127.0.0.1:8000/oauth'  # define it in google api console

    # client id and secret from google api console
    client_id = "123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com"
    client_secret = "abcdEFGHijklMNOPqrstUVWX"

    # secret_key for session encryption
    # key must be 32 url-safe base64-encoded bytes
    secret_key = b'abcdefghijklmnopqrstuvwxyz123456'


async def oauth(request):
    client = GoogleClient(
        client_id=cfg.client_id,
        client_secret=cfg.client_secret
    )

    if 'code' not in request.GET:
        return web.HTTPFound(client.get_authorize_url(
            scope='email profile',
            redirect_uri=cfg.redirect_uri
        ))
    token, data = await client.get_access_token(
        request.GET['code'],
        redirect_uri=cfg.redirect_uri
    )
    session = await get_session(request)
    session['token'] = token
    return web.HTTPFound('/')


def login_required(fn):
    """auth decorator

    call function(request, user: <aioauth_client User object>)
    """

    async def wrapped(request, **kwargs):
        session = await get_session(request)

        if 'token' not in session:
            return web.HTTPFound(cfg.oauth_redirect_path)

        client = GoogleClient(
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
            access_token=session['token']
        )

        try:
            user, info = await client.user_info()
        except Exception:
            return web.HTTPFound(cfg.oauth_redirect_path)

        return await fn(request, user, **kwargs)

    return wrapped


@login_required
async def index(request, user):
    text = ("<ul>"
            "<li>ID: %(id)s</li>"
            "<li>Username: %(username)s</li>"
            "<li>First, last name: %(first_name)s, %(last_name)s</li>"
            "<li>Gender: %(gender)s</li>"
            "<li>Email: %(email)s</li>"
            "<li>Link: %(link)s</li>"
            "<li>Picture: %(picture)s</li>"
            "<li>Country, city: %(country)s, %(city)s</li>"
            "</ul>") % user.__dict__
    return web.Response(text=text, content_type='text/html')


app = web.Application()
app.router.add_get(cfg.oauth_redirect_path, oauth)
app.router.add_get('/', index)

if __name__ == '__main__':
    aiohttp_session.setup(app,
                          EncryptedCookieStorage(cfg.secret_key))
    web.run_app(app, port=8000)
