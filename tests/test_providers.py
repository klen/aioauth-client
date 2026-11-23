import pytest

from aioauth_client import (
    ClientRegistry,
    DiscordClient,
    FoursquareClient,
    GithubClient,
    MTSClient,
    OAuthError,
    Plurk,
    SlackClient,
    TumblrClient,
    User,
)


def test_location_without_country():
    data = {"response": {"user": {"id": "1", "homeCity": "Moscow"}}}
    user = dict(FoursquareClient.user_parse(data))
    assert user["city"] == "Moscow"
    assert user["country"] == ""


def test_plurk_location_without_comma():
    user = dict(Plurk.user_parse({"user_info": {"id": "1", "location": "Moscow"}}))
    assert user["city"] == "Moscow"
    assert user["country"] == ""


def test_tumblr_without_blogs():
    data = {"response": {"user": {"name": "user", "blogs": []}}}
    assert dict(TumblrClient.user_parse(data))["link"] is None


def test_slack_error():
    with pytest.raises(OAuthError):
        dict(SlackClient.user_parse({"ok": False, "error": "invalid_auth"}))


def test_slack_profile():
    data = {"ok": True, "profile": {"display_name": "user", "email": "u@example.com"}}
    user = dict(SlackClient.user_parse(data))
    assert user["username"] == "user"
    assert user["email"] == "u@example.com"


def test_extra_user_fields():
    mts = User(**dict(MTSClient.user_parse({"phone": "+7900", "birthday": "1990-01-01"})))
    assert mts.phone == "+7900"
    assert mts.birthday == "1990-01-01"

    discord_data = {"id": "1", "avatar": "a", "discriminator": "1234"}
    assert User(**dict(DiscordClient.user_parse(discord_data))).discriminator == "1234"


def test_registry_skips_unnamed_subclasses():
    class Unnamed(GithubClient):
        pass

    assert ClientRegistry.clients["github"] is GithubClient
    assert "" not in ClientRegistry.clients


def test_provider_urls_use_https():
    attrs = ("base_url", "authorize_url", "access_token_url", "request_token_url", "user_info_url")
    insecure = [
        (client.name, attr, getattr(client, attr))
        for client in ClientRegistry.clients.values()
        for attr in attrs
        if getattr(client, attr, "").startswith("http://")
    ]
    assert insecure == []


def test_every_client_has_its_own_module():
    for name, cls in ClientRegistry.clients.items():
        if name in ("oauth1", "oauth2"):
            continue
        assert cls.__module__ == f"aioauth_client.clients.{name}"


def test_public_api_reexports_everything():
    import aioauth_client

    for name in aioauth_client.__all__:
        assert getattr(aioauth_client, name) is not None
