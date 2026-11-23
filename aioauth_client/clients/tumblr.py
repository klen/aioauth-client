"""The TumblrClient provider client."""

from collections.abc import Iterator
from typing import Any

from aioauth_client.oauth1 import OAuth1Client


class TumblrClient(OAuth1Client):
    """Support Tumblr.

    * Dashboard: http://www.tumblr.com/oauth/apps
    * Docs: http://www.tumblr.com/docs/en/api/v2#auth
    * API reference: http://www.tumblr.com/docs/en/api/v2
    """

    access_token_url = "https://www.tumblr.com/oauth/access_token"
    authorize_url = "https://www.tumblr.com/oauth/authorize"
    base_url = "https://api.tumblr.com/v2/"
    name = "tumblr"
    request_token_url = "https://www.tumblr.com/oauth/request_token"
    user_info_url = "https://api.tumblr.com/v2/user/info"

    @staticmethod
    def user_parse(data: dict[str, Any]) -> Iterator[tuple[str, Any]]:
        """Parse information from the provider."""
        assert isinstance(data, dict)
        _user = data.get("response", {}).get("user", {})
        yield "id", _user.get("name")
        yield "username", _user.get("name")
        yield "link", (_user.get("blogs") or [{}])[0].get("url")
