async def test_oauth2(http, response):
    from aioauth_client import GithubClient, ClientRegistry

    github = GithubClient(client_id="cid", client_secret="csecret")
    assert github
    assert "github" in ClientRegistry.clients
    assert (
        github.get_authorize_url()
        == "https://github.com/login/oauth/authorize?client_id=cid&response_type=code"
    )  # noqa

    http.return_value = response(json={"access_token": "TEST-TOKEN"})
    token, meta = await github.get_access_token("000")
    assert token == "TEST-TOKEN"
    assert meta
    assert http.called

    http.reset_mock()
    http.return_value = response(json={"access_token": "TEST-TOKEN"})

    res = await github.request("GET", "user", access_token="NEW-TEST-TOKEN")
    assert res
    http.assert_called_with(
        "GET",
        "https://api.github.com/user",
        params=None,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": "Bearer NEW-TEST-TOKEN",
        },
    )


async def test_oauth2_request(http):
    from aioauth_client import GithubClient

    github = GithubClient(client_id="cid", client_secret="csecret", access_token="token")
    res = await github.request("GET", "/user", params={"test": "ok"})
    assert res
    http.assert_called_with(
        "GET",
        "https://api.github.com/user",
        params={"test": "ok"},
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": "Bearer token",
        },
    )


async def test_headers_not_mutated(http):
    from aioauth_client import GithubClient

    headers = {"X-Test": "1"}
    github = GithubClient(client_id="cid", client_secret="csecret", access_token="TOKEN-1")
    await github.request("GET", "user", headers=headers)
    github.access_token = "TOKEN-2"
    await github.request("GET", "user", headers=headers)
    assert headers == {"X-Test": "1"}
    assert http.call_args.kwargs["headers"]["Authorization"] == "Bearer TOKEN-2"


async def test_access_token_kept_on_error(http, response):
    from aioauth_client import GithubClient

    github = GithubClient(client_id="cid", client_secret="csecret", access_token="OLD")
    http.return_value = response(json={"error": "bad_verification_code"})
    token, data = await github.get_access_token("bad-code")
    assert token == ""
    assert data == {"error": "bad_verification_code"}
    assert github.access_token == "OLD"
