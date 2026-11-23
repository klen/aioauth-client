"""The PinterestClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class PinterestClient(OAuth2Client):
    """Support pinterest.com.

    * Dashboard: https://developers.pinterest.com/apps/
    * Docs: https://developers.pinterest.com/docs/api/overview/
    """

    name = "pinterest"
    access_token_url = "https://api.pinterest.com/v1/oauth/token"
    authorize_url = "https://api.pinterest.com/oauth/"
    user_info_url = "https://api.pinterest.com/v1/me/"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse user data."""
        assert isinstance(data, dict)
        data = data.get("data", {})
        yield "id", data.get("id")
        yield "first_name", data.get("first_name")
        yield "last_name", data.get("last_name")
        yield "link", data.get("url")
