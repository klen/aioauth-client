"""
enable Google+ API by visiting
https://console.developers.google.com/apis/api/plus.googleapis.com/overview

Requirements:
    aioauth-client
    asgi-tools
    asgi-sessions
    uvicorn

Run the example with uvicorn:

    $ uvicorn --port 5000 example.google_example:app

"""

from asgi_sessions import SessionMiddleware
from asgi_tools import App, ResponseRedirect

from aioauth_client import GoogleClient

from .config import CREDENTIALS

app = App()
app.middleware(SessionMiddleware.setup(secret_key="aioauth-client"))  # noqa:


class CFG:
    redirect_uri = "http://localhost:5000/oauth/google"  # define it in google api console

    # client id and secret from google api console
    client_id = CREDENTIALS["google"]["client_id"]
    client_secret = CREDENTIALS["google"]["client_secret"]

    # secret_key for session encryption
    # key must be 32 url-safe base64-encoded bytes
    secret_key = b"abcdefghijklmnopqrstuvwxyz123456"


@app.route("/oauth/google")
async def oauth(request):
    client = GoogleClient(
        client_id=CFG.client_id,
        client_secret=CFG.client_secret,
    )

    if "code" not in request.url.query:
        return ResponseRedirect(
            client.get_authorize_url(
                scope="email profile",
                redirect_uri=CFG.redirect_uri,
            ),
        )

    token, data = await client.get_access_token(
        request.url.query["code"],
        redirect_uri=CFG.redirect_uri,
    )
    request.session["token"] = token
    return ResponseRedirect("/")


def login_required(fn):
    """auth decorator

    call function(request, user: <aioauth_client User object>)
    """

    async def wrapped(request, **kwargs):
        if "token" not in request.session:
            return ResponseRedirect("/oauth/google")

        client = GoogleClient(
            client_id=CFG.client_id,
            client_secret=CFG.client_secret,
            access_token=request.session["token"],
        )

        try:
            user, info = await client.user_info()
        except Exception:  # noqa:
            return ResponseRedirect(CFG.oauth_redirect_path)

        return await fn(request, user, **kwargs)

    return wrapped


@app.route("/")
@login_required
async def index(_, user):
    text = f"""
        <link rel="stylesheet"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" />
        <div class="container">
            <header class="navbar navbar-dark" style="background-color: #7952b3">
                <h2 class="navbar-brand">AIOAuth Google Client Example</h2>
            </header>
            <table class="table mt-4">
                <tr><td> ID </td><td> { user.id } </td></tr>
                <tr><td>First, last name</td><td>{ user.first_name }, { user.last_name }</td></tr>
                <tr><td>Email</td><td> { user.email } </td></tr>
                <tr><td>Picture</td><td> { user.picture } </td></tr>
            </table>
        <div>
        """
    return text
