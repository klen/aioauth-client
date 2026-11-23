"""The LinkedinClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class LinkedinClient(OAuth2Client):
    """Support linkedin.com.

    * Dashboard: https://www.linkedin.com/developer/apps
    * Docs: https://developer.linkedin.com/docs/oauth2
    * API reference: https://developer.linkedin.com/docs/rest-api
    """

    name = "linkedin"
    access_token_key = "oauth2_access_token"
    access_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    authorize_url = "https://www.linkedin.com/oauth/v2/authorization"
    user_info_url = (
        "https://api.linkedin.com/v1/people/~:("
        "id,email-address,first-name,last-name,formatted-name,picture-url,"
        "public-profile-url,location)?format=json"
    )

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse user data."""
        assert isinstance(data, dict)
        yield "id", data.get("id")
        yield "email", data.get("emailAddress")
        yield "first_name", data.get("firstName")
        yield "last_name", data.get("lastName")
        yield "username", data.get("formattedName")
        yield "picture", data.get("pictureUrl")
        yield "link", data.get("publicProfileUrl")
        yield "country", data.get("location", {}).get("name")
