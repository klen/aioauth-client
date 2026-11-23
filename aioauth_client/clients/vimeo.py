"""The VimeoClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth1 import OAuth1Client


class VimeoClient(OAuth1Client):
    """Support Vimeo."""

    access_token_url = "https://vimeo.com/oauth/access_token"
    authorize_url = "https://vimeo.com/oauth/authorize"
    base_url = "https://vimeo.com/api/rest/v2/"
    name = "vimeo"
    request_token_url = "https://vimeo.com/oauth/request_token"
    user_info_url = "https://vimeo.com/api/rest/v2?format=json&method=vimeo.oauth.checkAccessToken"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        _user = data.get("oauth", {}).get("user", {})
        yield "id", _user.get("id")
        yield "username", _user.get("username")
        first_name, _, last_name = _user.get("display_name").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
