"""The Plurk provider client."""

from collections.abc import Iterator
from typing import Any, cast

from aioauth_client.base import OAuthError
from aioauth_client.oauth1 import OAuth1Client
from aioauth_client.utils import split_location


class Plurk(OAuth1Client):
    """Support Plurk.

    * Dashboard: http://www.plurk.com/PlurkApp/
    * API: http://www.plurk.com/API
    * API explorer: http://www.plurk.com/OAuth/test/
    """

    access_token_url = "https://www.plurk.com/OAuth/access_token"
    authorize_url = "https://www.plurk.com/OAuth/authorize"
    base_url = "https://www.plurk.com/APP/"
    name = "plurk"
    request_token_url = "https://www.plurk.com/OAuth/request_token"
    user_info_url = "https://www.plurk.com/APP/Profile/getOwnProfile"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        if not isinstance(data, dict):
            raise OAuthError("Invalid response: %r", data)

        user_info = cast(dict[str, str], data.get("user_info", {}))
        user_id = user_info.get("id") or user_info.get("uid")
        yield "id", user_id
        yield "locale", user_info.get("default_lang")
        yield "username", user_info.get("display_name")
        first_name, _, last_name = user_info.get("full_name", "").partition(" ")
        yield "first_name", first_name
        yield "last_name", last_name
        yield "picture", "http://avatars.plurk.com/{0}-big2.jpg".format(user_id)
        city, country = split_location(user_info.get("location"))
        yield "city", city
        yield "country", country
