"""The Flickr provider client."""

from collections.abc import Iterator
from typing import Any, cast

from aioauth_client.base import OAuthError
from aioauth_client.oauth1 import OAuth1Client


class Flickr(OAuth1Client):
    """Support Flickr.

    * Dashboard: https://www.flickr.com/services/apps/
    * Docs: https://www.flickr.com/services/api/auth.oauth.html
    * API reference: https://www.flickr.com/services/api/
    """

    access_token_url = "https://www.flickr.com/services/oauth/access_token"
    authorize_url = "https://www.flickr.com/services/oauth/authorize"
    base_url = "https://api.flickr.com/"
    name = "flickr"
    request_token_url = "https://www.flickr.com/services/oauth/request_token"
    user_info_url = (
        "https://api.flickr.com/services/rest?method=flickr.test.login&format=json&nojsoncallback=1"
    )

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        if not isinstance(data, dict):
            raise OAuthError("Invalid response: %r", data)

        user_ = cast(dict, data.get("user", {}))
        yield "id", data.get("user_nsid") or user_.get("id")
        yield "username", cast(dict, user_.get("username", {})).get("_content")
        first_name, _, last_name = (
            cast(dict, data.get("fullname", {})).get("_content", "").partition(" ")
        )
        yield "first_name", first_name
        yield "last_name", last_name
