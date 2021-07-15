async def test_oauth2(http, response):
    from aioauth_client import GithubClient, ClientRegistry

    github = GithubClient(client_id='cid', client_secret='csecret')
    assert github
    assert 'github' in ClientRegistry.clients
    assert github.get_authorize_url() == 'https://github.com/login/oauth/authorize?client_id=cid&response_type=code'  # noqa

    http.return_value = response(json={'access_token': 'TEST-TOKEN'})
    token, meta = await github.get_access_token('000')
    assert token == 'TEST-TOKEN'
    assert meta
    assert http.called

    http.reset_mock()
    http.return_value = response(json={'access_token': 'TEST-TOKEN'})

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
    from aioauth_client import GithubClient

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
