# AIOAuth Client

[![tests](https://github.com/klen/aioauth-client/actions/workflows/tests.yml/badge.svg)](https://github.com/klen/aioauth-client/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/aioauth-client)](https://pypi.org/project/aioauth-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/aioauth-client)](https://pypi.org/project/aioauth-client/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

OAuth 1.0a and OAuth 2.0 client helpers for [asyncio](https://docs.python.org/3/library/asyncio.html)
and [trio](https://trio.readthedocs.io/en/stable/), built on [httpx](https://www.python-httpx.org/).

- OAuth 1.0a and OAuth 2.0 authorization flows
- 28 ready-made provider clients (see [the table](#provider-clients))
- works with asyncio and trio, no callbacks: plain `async`/`await`
- typed, ships `py.typed`
- Python 3.11+

## Requirements

Python 3.11 or newer. The only runtime dependency is `httpx`.

## Installation

```bash
pip install aioauth-client
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add aioauth-client
```

## Usage

The snippets below are meant to run inside `async` code.

### OAuth 2.0

```python
from aioauth_client import GithubClient

github = GithubClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

# 1. Send the user's browser to this URL
authorize_url = github.get_authorize_url(scope="user:email")

# 2. The provider redirects back to your app with ?code=...
token, data = await github.get_access_token(code)

# 3. The client keeps the token, so later calls are authenticated
profile = await github.request("GET", "user")
user, raw = await github.user_info()

print(user.username, user.email)
```

`get_access_token()` returns `(token, provider_data)`. If the provider refuses
the exchange, it returns `("", data)` and logs a warning; a token the client
already held is left untouched.

Each client instance stores the token it received. Create one client per
user/request and do not share an instance between concurrent logins. When
tokens live elsewhere, pass them explicitly:
`await github.request("GET", "user", access_token=token)`.

### OAuth 1.0a

```python
from aioauth_client import TwitterClient

twitter = TwitterClient(
    consumer_key="YOUR_CONSUMER_KEY",
    consumer_secret="YOUR_CONSUMER_SECRET",
)

request_token, _ = await twitter.get_request_token()
print("Open in a browser:", twitter.get_authorize_url(request_token))

# After the user returns with an oauth_verifier / PIN code
token, data = await twitter.get_access_token(oauth_verifier)
token_secret = data["oauth_token_secret"]

twitter = TwitterClient(
    consumer_key="YOUR_CONSUMER_KEY",
    consumer_secret="YOUR_CONSUMER_SECRET",
    oauth_token=token,
    oauth_token_secret=token_secret,
)
timeline = await twitter.request("GET", "statuses/home_timeline.json")
```

`get_access_token()` stores the new `oauth_token`/`oauth_token_secret` on the
instance as well, and checks the request token when one is passed.

For web apps, pass `oauth_callback` when requesting the token and read
`oauth_verifier` from the callback query instead of asking for a PIN:

```python
request_token, _ = await twitter.get_request_token(
    oauth_callback="https://app.example/oauth/twitter",
)
# The provider redirects to oauth_callback?oauth_token=...&oauth_verifier=...
token, data = await twitter.get_access_token(verifier_from_callback)
```

### Responses and errors

`request()` returns parsed data, not an `httpx.Response`:

- a `dict` for JSON responses,
- a `dict` for form-encoded responses,
- a `str` for anything else.

HTTP errors are not raised by default, so a `401` body comes back as data. Pass
`raise_for_status=True` to get an `OAuthError` on any status `>= 300`; the
library does this for token exchange and `user_info()`. Some providers report
errors inside a `200` response (Slack's `ok: false`), and their parsers raise
`OAuthError` themselves.

```python
from aioauth_client import OAuthError

try:
    user, raw = await github.user_info()
except OAuthError:
    ...
```

### Timeouts, retries and connection pooling

Without a transport, every call opens a new HTTP connection. To reuse
connections and configure timeouts or retries, pass your own
`httpx.AsyncClient`; the library never closes a client it did not create:

```python
import httpx

transport = httpx.AsyncClient(
    timeout=10,
    transport=httpx.AsyncHTTPTransport(retries=3),
)
github = GithubClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    transport=transport,
)

try:
    await github.request("GET", "user")
finally:
    await transport.aclose()
```

A per-request timeout works too:
`await github.request("GET", "user", timeout=30)`.

### Provider clients

Every client below is registered in `ClientRegistry.clients` under the name in
the first column:

```python
from aioauth_client import ClientRegistry

client_cls = ClientRegistry.clients["github"]
```

| Provider | Client class | Protocol | `user_info()` profile |
| --- | --- | --- | --- |
| `amazon` | `AmazonClient` | OAuth 2.0 | yes |
| `bitbucket` | `Bitbucket2Client` | OAuth 2.0 | yes |
| `discord` | `DiscordClient` | OAuth 2.0 | yes |
| `eventbrite` | `EventbriteClient` | OAuth 2.0 | yes |
| `facebook` | `FacebookClient` | OAuth 2.0 | yes |
| `flickr` | `Flickr` | OAuth 1.0a | yes |
| `foursquare` | `FoursquareClient` | OAuth 2.0 | yes |
| `github` | `GithubClient` | OAuth 2.0 | yes |
| `gitlab` | `GitlabClient` | OAuth 2.0 | yes |
| `google` | `GoogleClient` | OAuth 2.0 | yes |
| `instagram` | `InstagramClient` | OAuth 2.0 | yes |
| `lichess` | `LichessClient` | OAuth 2.0 | yes |
| `linkedin` | `LinkedinClient` | OAuth 2.0 | yes |
| `meetup` | `Meetup` | OAuth 1.0a | — |
| `microsoft` | `MicrosoftClient` | OAuth 2.0 | yes |
| `mts` | `MTSClient` | OAuth 2.0 | yes |
| `odnoklassniki` | `OdnoklassnikiClient` | OAuth 2.0 | yes |
| `pinterest` | `PinterestClient` | OAuth 2.0 | yes |
| `plurk` | `Plurk` | OAuth 1.0a | yes |
| `slack` | `SlackClient` | OAuth 2.0 | yes |
| `strava` | `StravaClient` | OAuth 2.0 | — |
| `todoist` | `TodoistClient` | OAuth 2.0 | yes |
| `trello` | `TrelloClient` | OAuth 1.0a | raw |
| `tumblr` | `TumblrClient` | OAuth 1.0a | yes |
| `twitter` | `TwitterClient` | OAuth 1.0a | yes |
| `vimeo` | `VimeoClient` | OAuth 1.0a | yes |
| `vk` | `VKClient` | OAuth 2.0 | yes |
| `yandex` | `YandexClient` | OAuth 2.0 | yes |

`—` in the last column means the client has no `user_info_url` and
`user_info()` raises `NotImplementedError`. `raw` means the method returns the
provider response but the base parser only fills `User.id`.

### Custom provider

Subclass `OAuth2Client` (or `OAuth1Client`), set the endpoints and a
`user_parse` generator, and the class registers itself under its `name`:

```python
from aioauth_client import OAuth2Client


class MyProviderClient(OAuth2Client):
    name = "myprovider"
    base_url = "https://api.example.com"
    authorize_url = "https://example.com/oauth/authorize"
    access_token_url = "https://example.com/oauth/token"
    user_info_url = "https://api.example.com/me"

    @staticmethod
    def user_parse(data):
        yield "id", data.get("id")
        yield "email", data.get("email")
        yield "first_name", data.get("given_name")
```

`user_parse` yields `(field, value)` pairs consumed by `User`. Only fields
declared in `User.__slots__` are stored: `id`, `email`, `first_name`,
`last_name`, `username`, `picture`, `link`, `locale`, `city`, `country`,
`gender`, `discriminator`, `phone`, `birthday`. Anything else is still
available in the raw provider data returned by `user_info()`.

## Development

```bash
uv sync --all-groups          # install dev and example dependencies
uv run pytest tests           # tests; also runs mypy via pytest addopts
uv run ruff check aioauth_client
uv run ruff format --check    # formatting (ruff format, not black)
uv run mypy
uv run pre-commit install     # ruff format, ruff, uv lock check, mypy, pytest
```

CI runs the tests on Python 3.11 through 3.15. Pushing a version tag (what
`make release` does) re-runs the tests and publishes the build to PyPI.

To try the bundled demo app:

```bash
make example   # serves http://localhost:8080
```

The demo lives in [`example/`](example) and needs provider credentials in
`example/config.py`; it is not part of the library.

## Contributing

Bug reports and pull requests are welcome at
[github.com/klen/aioauth-client](https://github.com/klen/aioauth-client).
Run the checks from [Development](#development) before opening a PR.

## License

[MIT](LICENSE). Copyright (c) Kirill Klenov.
