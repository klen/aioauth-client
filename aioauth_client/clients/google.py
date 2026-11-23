"""The GoogleClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class GoogleClient(OAuth2Client):
    """Support Google.

    * Dashboard: https://console.developers.google.com/project
    * Docs: https://developers.google.com/accounts/docs/OAuth2
    * API reference: https://developers.google.com/gdata/docs/directory
    * API explorer: https://developers.google.com/oauthplayground/
    """

    authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
    access_token_url = "https://oauth2.googleapis.com/token"
    base_url = "https://www.googleapis.com/userinfo/v2/"
    name = "google"
    user_info_url = "https://www.googleapis.com/userinfo/v2/me"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "email", data.get("email")
        yield "first_name", data.get("given_name")
        yield "last_name", data.get("family_name")
        yield "link", data.get("link")
        yield "locale", data.get("locale")
        yield "picture", data.get("picture")
        yield "gender", data.get("gender")
