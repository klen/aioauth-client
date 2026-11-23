"""The InstagramClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.base import OAuthError
from aioauth_client.oauth2 import OAuth2Client


class InstagramClient(OAuth2Client):
    """Support Instagram.

    * Dashboard: https://www.instagram.com/developer/clients/manage/
    * Docs: https://www.instagram.com/developer/
    """

    access_token_url = "https://api.instagram.com/oauth/access_token"
    authorize_url = "https://api.instagram.com/oauth/authorize"
    base_url = "https://api.instagram.com/v1"
    name = "instagram"
    user_info_url = "https://api.instagram.com/v1/users/self"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        user = data.get("data")
        if not isinstance(user, dict):
            raise OAuthError(f"Invalid user info response: {data!r}")
        yield "id", user.get("id")
        yield "username", user.get("username")
        yield "picture", user.get("profile_picture")
        first_name, _, last_name = user.get("full_name", "").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
