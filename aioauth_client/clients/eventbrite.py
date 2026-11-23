"""The EventbriteClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth2 import OAuth2Client


class EventbriteClient(OAuth2Client):
    """Support Eventbrite.

    * Dashboard: http://www.eventbrite.com/myaccount/apps/
    * Docs: https://developer.eventbrite.com/docs/auth/
    * API: http://developer.eventbrite.com/docs/
    """

    access_token_url = "https://www.eventbrite.com/oauth/token"
    authorize_url = "https://www.eventbrite.com/oauth/authorize"
    base_url = "https://www.eventbriteapi.com/v3/"
    name = "eventbrite"
    user_info_url = "https://www.eventbriteapi.com/v3/users/me"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        for email in data.get("emails", []):
            if email.get("primary"):
                yield "id", email.get("email")
                yield "email", email.get("email")
                break
