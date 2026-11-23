"""The FoursquareClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client
from aioauth_client.utils import split_location


class FoursquareClient(OAuth2Client):
    """Support Foursquare.

    * Dashboard: https://foursquare.com/developers/apps
    * Docs: https://developer.foursquare.com/overview/auth.html
    * API reference: https://developer.foursquare.com/docs/
    """

    access_token_url = "https://foursquare.com/oauth2/access_token"
    authorize_url = "https://foursquare.com/oauth2/authenticate"
    base_url = "https://api.foursquare.com/v2/"
    name = "foursquare"
    user_info_url = "https://api.foursquare.com/v2/users/self"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        user = data.get("response", {}).get("user", {})
        yield "id", user.get("id")
        yield "email", user.get("contact", {}).get("email")
        yield "first_name", user.get("firstName")
        yield "last_name", user.get("lastName")
        city, country = split_location(user.get("homeCity"), ", ")
        yield "city", city
        yield "country", country
