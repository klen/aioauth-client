"""The FacebookClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.base import User
from aioauth_client.oauth2 import OAuth2Client
from aioauth_client.types import TParams, TRes


class FacebookClient(OAuth2Client):
    """Support Facebook.

    * Dashboard: https://developers.facebook.com/apps
    * Docs: http://developers.facebook.com/docs/howtos/login/server-side-login/
    * API reference: http://developers.facebook.com/docs/reference/api/
    * API explorer: http://developers.facebook.com/tools/explorer
    """

    access_token_url = "https://graph.facebook.com/oauth/access_token"
    authorize_url = "https://www.facebook.com/dialog/oauth"
    base_url = "https://graph.facebook.com/v2.4"
    name = "facebook"
    user_info_url = "https://graph.facebook.com/me"

    async def user_info(self, params: TParams | None = None, **kwargs: Any) -> tuple[User, TRes]:
        """Facebook required fields-param."""
        params = params or {}
        params["fields"] = "id,email,first_name,last_name,name,link,locale,gender,location"
        return await super(FacebookClient, self).user_info(params=params, **kwargs)

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from provider."""
        assert isinstance(data, dict)
        id_ = data.get("id")
        yield "id", id_
        yield "email", data.get("email")
        yield "first_name", data.get("first_name")
        yield "last_name", data.get("last_name")
        yield "username", data.get("name")
        yield (
            "picture",
            "http://graph.facebook.com/{0}/picture?type=large".format(
                id_,
            ),
        )
        yield "link", data.get("link")
        yield "locale", data.get("locale")
        yield "gender", data.get("gender")

        location = data.get("location", {}).get("name")
        if location:
            split_location = location.split(", ")
            yield "city", split_location[0].strip()
            if len(split_location) > 1:
                yield "country", split_location[1].strip()
