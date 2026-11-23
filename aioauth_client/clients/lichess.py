"""The LichessClient provider client."""

from collections.abc import Iterator
from typing import Any, cast

from aioauth_client.base import OAuthError
from aioauth_client.oauth2 import OAuth2Client


class LichessClient(OAuth2Client):
    """Support Lichess.

    * Dashboard: https://lichess.org/account/oauth/app
    * Docs: https://lichess.org/api#section/Authentication
    * API reference: https://lichess.org/api
    """

    access_token_url = "https://oauth.lichess.org/oauth"
    authorize_url = "https://oauth.lichess.org/oauth/authorize"
    base_url = "https://lichess.org/"
    name = "lichess"
    user_info_url = "https://lichess.org/api/account"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        if not isinstance(data, dict):
            raise OAuthError("Invalid response: %r", data)

        yield "id", data.get("id")
        yield "username", data.get("username")
        yield "gender", data.get("title")
        profile = cast(dict[str, str] | None, data.get("profile"))
        if profile is not None:
            yield "first_name", profile.get("firstName")
            yield "last_name", profile.get("lastName")
            yield "country", profile.get("country")
