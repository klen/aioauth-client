from httpx import AsyncClient


def test_userinfo():
    from aioauth_client import User

    user = User(email="email")
    assert user.email == "email"
    assert user.id is None


def test_signatures():
    from aioauth_client import HmacSha1Signature

    sig = HmacSha1Signature()
    assert sig.name
    assert sig.sign("secret", "GET", "/test", oauth_token_secret="secret")


async def test_client(http):
    from aioauth_client import GoogleClient

    google = GoogleClient(client_id="123", client_secret="456", access_token="789")
    data = await google.request("GET", "/")
    assert data == {"response": "ok"}
    http.assert_called_with(
        "GET",
        "https://www.googleapis.com/",
        params=None,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": "Bearer 789",
        },
    )


async def test_client_url(http):
    from aioauth_client import GoogleClient

    client = GoogleClient("test", "test")
    assert client.urljoin("https://example.com") == "https://example.com"
    assert client.urljoin("/a/b") == "https://www.googleapis.com/a/b"
    assert client.urljoin("a/b") == f"{client.base_url}a/b"


async def test_custom_client(http, response):
    from aioauth_client import GithubClient

    transport = AsyncClient()
    github = GithubClient(client_id="cid", client_secret="csecret", transport=transport)
    assert github.transport

    http.return_value = response(json={"access_token": "TOKEN"})

    token, meta = await github.get_access_token("000")
    assert http.called
    assert meta
    assert token
