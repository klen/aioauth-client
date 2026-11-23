"""The TwitterClient provider client."""

from collections.abc import Iterator
from typing import Any, cast

from aioauth_client.oauth1 import OAuth1Client


class TwitterClient(OAuth1Client):
    """Support Twitter.

    * Dashboard: https://dev.twitter.com/apps
    * Docs: https://dev.twitter.com/docs
    * API reference: https://dev.twitter.com/docs/api
    """

    access_token_url = "https://api.twitter.com/oauth/access_token"
    authorize_url = "https://api.twitter.com/oauth/authorize"
    base_url = "https://api.twitter.com/1.1/"
    name = "twitter"
    request_token_url = "https://api.twitter.com/oauth/request_token"
    user_info_url = "https://api.twitter.com/1.1/account/verify_credentials.json"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        yield "id", data.get("id") or data.get("user_id")
        first_name, _, last_name = cast(str, data["name"]).partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
        yield "email", data.get("email")
        yield "picture", data.get("profile_image_url")
        yield "locale", data.get("lang")
        yield "link", data.get("url")
        yield "username", data.get("screen_name")
        city, _, country = (s.strip() for s in cast(str, data.get("location", "")).partition(","))
        yield "city", city
        yield "country", country
