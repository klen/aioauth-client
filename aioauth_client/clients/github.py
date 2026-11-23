"""The GithubClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class GithubClient(OAuth2Client):
    """Support Github.

    * Dashboard: https://github.com/settings/applications/
    * Docs: http://developer.github.com/v3/#authentication
    * API reference: http://developer.github.com/v3/
    """

    access_token_url = "https://github.com/login/oauth/access_token"
    authorize_url = "https://github.com/login/oauth/authorize"
    base_url = "https://api.github.com"
    name = "github"
    user_info_url = "https://api.github.com/user"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "email", data.get("email")
        first_name, _, last_name = (data.get("name") or "").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
        yield "username", data.get("login")
        yield "picture", data.get("avatar_url")
        yield "link", data.get("html_url")
        location = data.get("location", "")
        if location:
            split_location = location.split(",")
            yield "country", split_location[0].strip()
            if len(split_location) > 1:
                yield "city", split_location[1].strip()
