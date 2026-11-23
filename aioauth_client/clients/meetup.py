"""The Meetup provider client."""

from collections.abc import Iterator
from typing import Any, cast

from aioauth_client.base import OAuthError
from aioauth_client.oauth1 import OAuth1Client


class Meetup(OAuth1Client):
    """Support Meetup.

    * Dashboard: http://www.meetup.com/meetup_api/oauth_consumers/
    * Docs: http://www.meetup.com/meetup_api/auth/#oauth
    * API: http://www.meetup.com/meetup_api/docs/
    """

    access_token_url = "https://api.meetup.com/oauth/access/"
    authorize_url = "https://www.meetup.com/authorize/"
    base_url = "https://api.meetup.com/2/"
    name = "meetup"
    request_token_url = "https://api.meetup.com/oauth/request/"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        if not isinstance(data, dict):
            raise OAuthError("Invalid response: %r", data)

        yield "id", data.get("id") or data.get("member_id")
        yield "locale", data.get("lang")
        yield "picture", cast(dict[str, str], data.get("photo", {})).get("photo_link")
