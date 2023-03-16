"""Aioauth-client example.

Requirements:
    aioauth-client
    asgi-tools
    uvicorn

Run the example with uvicorn:

    $ uvicorn --port 5000 example.app:app

"""


import html
from pprint import pformat

from asgi_tools import App, ResponseRedirect

from aioauth_client import ClientRegistry, GithubClient, OAuth1Client

from .config import CREDENTIALS

app = App(debug=True)


@app.route("/")
async def index(_):
    return """
        <link rel="stylesheet"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" />
        <div class="container">
            <header class="navbar navbar-dark" style="background-color: #7952b3">
                <h2 class="navbar-brand">AIOAuth Client Example</h2>
            </header>
            <ul class="nav flex-column mt-5">
                <li class="nav-item">
                    <a class="nav-link" href="/oauth/bitbucket">Login with Bitbucket</a></li>
                <li class="nav-item">
                    <a class="nav-link" href="/oauth/facebook">Login with Facebook</a></li>
                <li class="nav-item">
                    <a class="nav-link" href="/oauth/github">Login with Github</a></li>
                <li class="nav-item">
                    <a class="nav-link" href="/oauth/google">Login with Google</a></li>
                <li class="nav-item">
                    <a class="nav-link" href="/oauth/twitter">Login with Twitter</a></li>
            </ul>
        </div>
    """


@app.route("/oauth/{provider}")
async def oauth(request):
    provider = request.path_params.get("provider")
    if provider not in CREDENTIALS:
        return 404, "Unknown provider %s" % provider

    # Create OAuth1/2 client
    client_cls = ClientRegistry.clients[provider]
    params = CREDENTIALS[provider]
    client = client_cls(**params)
    client.params[
        "oauth_callback" if issubclass(client_cls, OAuth1Client) else "redirect_uri"
    ] = str(
        request.url.with_query(""),
    )

    # Check if is not redirect from provider
    if client.shared_key not in request.url.query:
        # For oauth1 we need more work
        if isinstance(client, OAuth1Client):
            token, secret, _ = await client.get_request_token()

            # Dirty save a token_secret
            # Dont do it in production
            request.app.secret = secret
            request.app.token = token

        # Redirect client to provider
        return ResponseRedirect(client.get_authorize_url(access_type="offline"))

    # For oauth1 we need more work
    if isinstance(client, OAuth1Client):
        client.oauth_token_secret = request.app.secret
        client.oauth_token = request.app.token

    _, meta = await client.get_access_token(request.url.query)
    user, info = await client.user_info()
    text = f"""
        <link rel="stylesheet"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" />
        <div class="container">
            <header class="navbar navbar-dark" style="background-color: #7952b3">
                <h2 class="navbar-brand">AIOAuth Client Example ({ client.name })</h2>
            </header>
            <a class="btn btn-primary mt-4" href='/'>Return back</a>
            <table class="table mt-4">
                <tr><td> ID </td><td> { user.id } </td></tr>
                <tr><td> Username </td><td> { user.username } </td></tr>
                <tr><td>First, last name</td><td>{ user.first_name }, { user.last_name }</td></tr>
                <tr><td>Gender</td><td> { user.gender } </td></tr>
                <tr><td>Email</td><td> { user.email } </td></tr>
                <tr><td>Link</td><td> { user.link } </td></tr>
                <tr><td>Picture</td><td> { user.picture } </td></tr>
                <tr><td>Country, City</td><td> { user.country }, { user.city } </td></tr>
            </table>
            <h3 class="mt-4">Raw data</h3>
            <pre>{ html.escape(pformat(info)) }</pre>
            <pre>{ html.escape(pformat(meta)) }</pre>
        <div>
        """
    return text


# Simple Github (OAuth2) example (not connected to app)
async def github(request):
    github = GithubClient(
        client_id="b6281b6fe88fa4c313e6",
        client_secret="21ff23d9f1cad775daee6a38d230e1ee05b04f7c",  # noqa:
    )
    if "code" not in request.url.query:
        return ResponseRedirect(github.get_authorize_url(scope="user:email"))

    # Get access token
    code = request.url.query["code"]
    token, _ = await github.get_access_token(code)
    assert token

    # Get a resource `https://api.github.com/user`
    response = await github.request("GET", "user")
    return await response.read()
